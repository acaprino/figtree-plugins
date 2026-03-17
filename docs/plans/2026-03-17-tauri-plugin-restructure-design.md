# Tauri Plugin Restructure - Design Spec

**Date:** 2026-03-17
**Plugin:** tauri-development
**Current version:** 1.8.0

## Problem

The tauri-development plugin has a single skill (`tauri2-mobile`) containing 9 reference files, 8 of which have content applicable to desktop Tauri development. Desktop-specific topics (window management, shell plugin, desktop bundling) are missing entirely. The two agents (`rust-engineer`, `tauri-optimizer`) are solid but lack coverage of modern Rust patterns (tracing, rkyv, loom) and advanced HFT rendering (Canvas/OffscreenCanvas, backpressure).

## Design

### Skill Restructure: 3 Skills

#### 1. `tauri-core/` -- Universal patterns (desktop + mobile)

**SKILL.md trigger:** Any Tauri 2 development work (commands, IPC, plugins, project setup).

**references/**
| File | Content | Source |
|------|---------|--------|
| `setup.md` | Rust, Node, Tauri CLI prerequisites, project init, tauri.conf.json basics | Extracted from current setup.md (remove Android/iOS sections) |
| `rust-patterns.md` | lib.rs entry, `#[tauri::command]`, State with Mutex, Channel streaming, error handling with thiserror, conditional compilation (`cfg(mobile)`/`cfg(desktop)`) | Extracted from current rust-patterns.md (universal parts) |
| `frontend-patterns.md` | invoke wrappers, Channel callbacks, event listeners, TypeScript typing, React hooks (useInvoke, useEvent), capability config | Extracted from current frontend-patterns.md (remove safe-areas hack) |
| `plugins-core.md` | Universal plugins: fs, store, sql, http, log, dialog, opener. Plugin setup in lib.rs, capability permissions, Channel API for streaming | Extracted from current plugins.md (remove mobile-only plugins) |
| `authentication.md` | OAuth/PKCE via system browser -- pattern universale. State/nonce/CSRF protection, token refresh. Desktop and mobile both need system browser for Google/Microsoft WebView blocks | Extracted from current authentication.md (universal architecture) |
| `ci-cd.md` | Base CI/CD patterns: Rust/node_modules caching, OS matrix builds, release profiles in CI, signing concepts, artifact upload. Provider-agnostic (not GitHub Actions specific) | New, extracted common patterns from current ci-cd.md |

#### 2. `tauri-desktop/` -- Desktop-specific (NEW)

**SKILL.md trigger:** Desktop Tauri development, window management, system tray, desktop bundling, platform-specific WebView issues.

**references/**
| File | Content | Source |
|------|---------|--------|
| `window-management.md` | Multi-window (WindowBuilder), frameless/transparent windows, system tray (tauri-plugin-tray-icon), native menus, window events, decorations | NEW - research required |
| `shell-plugin.md` | Execute child processes, read stdout/stderr, run scripts, sidecar binaries. Desktop-only capability (forbidden on mobile OS) | NEW - research required |
| `build-deploy.md` | Desktop bundling: .msi/.nsis (Windows), .dmg/.app (macOS), .AppImage/.deb (Linux). Code signing per platform, auto-updater | NEW - research required |
| `platform-webviews.md` | WebView2 (Windows/Chromium), WKWebView (macOS/Safari), WebKitGTK (Linux). CSS differences, feature detection, platform quirks | NEW - partially from tauri-optimizer agent, expanded with research |

#### 3. `tauri2-mobile/` -- Mobile-specific (slimmed down)

**SKILL.md trigger:** Mobile Tauri development for Android/iOS, emulator testing, store deployment, IAP.

**references/**
| File | Content | Source |
|------|---------|--------|
| `setup-mobile.md` | Android SDK, NDK, Strawberry Perl, iOS Xcode, CocoaPods, Apple Developer account, mobile HMR config | Extracted from current setup.md (mobile-only sections) |
| `testing.md` | Emulator setup, ADB commands, logcat, Chrome DevTools for WebView, permission testing, deep link testing, troubleshooting | Current testing.md (unchanged) |
| `iap.md` | Google Play / Apple App Store IAP, server-side verification, RTDN, subscription lifecycle, sandbox testing | Current iap.md (unchanged) |
| `build-deploy-mobile.md` | APK/AAB/IPA building, Android keystore, iOS signing, Play Store/App Store submission, Windows cross-compile issues (symlinks, path length, stale .so) | Extracted from current build-deploy.md (mobile parts) |
| `plugins-mobile.md` | Mobile-only plugins: biometric, haptics, barcode-scanner, nfc. Safe-areas CSS workaround. Deep link configuration for OAuth callback | NEW - extracted from current plugins.md + frontend-patterns.md |
| `ci-cd-mobile.md` | Extends core CI/CD: mobile build matrix (Android targets, iOS), store upload automation, IAP testing in CI, Fastlane integration. References tauri-core/ci-cd.md for base patterns | Extracted from current ci-cd.md (mobile-specific parts) |
| `authentication-mobile.md` | Mobile-specific OAuth details: deep link callback setup, opener plugin for system browser, hosted callback page (Firebase), Apple Sign-In configuration | Extracted from current authentication.md (mobile-specific parts) |

### Agent Upgrades

#### `rust-engineer.md` additions:

1. **CAPABILITIES section:**
   - Observability -- `tracing`, `tracing-subscriber`, `#[instrument]` for async spans
   - Advanced Testing -- `loom` for concurrency testing, `insta` for snapshot testing, `tarpaulin` for code coverage
   - Serialization -- zero-copy with `rkyv` for extreme performance; `serde` for standard JSON/YAML
   - Diagnostics -- `miette` for rich error diagnostics (CLI/tools)

2. **CODE PATTERNS section -- new pattern:**
   - Observability with tracing (instrument, info, error with structured fields)

#### `tauri-optimizer.md` additions:

1. **IPC Communication Patterns -- expand Raw Payloads:**
   - `rkyv` zero-copy serialization on Rust side
   - `DataView`/`Float64Array` consumption on frontend (bypass JSON entirely)

2. **New section: Extreme High-Frequency Rendering:**
   - Anti-pattern: React DOM updates for < 16ms ticks
   - Correct: HTML5 Canvas + OffscreenCanvas + Web Workers for dense data (orderbook, charts)
   - React manages UI shell only; critical data path bypasses Virtual DOM

3. **New section: Backpressure & Memory Protection:**
   - Frame dropping strategy before saturating UI thread
   - Web Worker message queue limits
   - OOM prevention patterns

### File Operations Summary

All paths relative to `plugins/tauri-development/`.

**Files to CREATE (entirely new content, requires research):**
- `skills/tauri-desktop/SKILL.md`
- `skills/tauri-desktop/references/window-management.md`
- `skills/tauri-desktop/references/shell-plugin.md`
- `skills/tauri-desktop/references/build-deploy.md` -- desktop bundling (.msi, .dmg, .AppImage); NOT from existing build-deploy.md which is entirely mobile
- `skills/tauri-desktop/references/platform-webviews.md`

**Files to EXTRACT+EDIT (copy content from existing, then edit to keep only relevant parts):**
- Current `setup.md` -> `skills/tauri-core/references/setup.md` (remove Android/iOS sections) + `skills/tauri2-mobile/references/setup-mobile.md` (keep only Android/iOS sections)
- Current `rust-patterns.md` -> `skills/tauri-core/references/rust-patterns.md` (content is already universal, copy as-is)
- Current `frontend-patterns.md` -> `skills/tauri-core/references/frontend-patterns.md` (remove safe-areas CSS hack, remove biometric/haptics/geolocation examples)
- Current `plugins.md` -> `skills/tauri-core/references/plugins-core.md` (keep universal plugins: fs, store, sql, http, log, dialog, opener) + `skills/tauri2-mobile/references/plugins-mobile.md` (keep mobile-only: biometric, haptics, barcode, nfc, safe-areas workaround, deep links)
- Current `authentication.md` -> `skills/tauri-core/references/authentication.md` (keep OAuth/PKCE architecture, state/nonce/CSRF, token refresh) + `skills/tauri2-mobile/references/authentication-mobile.md` (keep deep link callback, opener plugin flow, Firebase hosted page, Apple Sign-In)
- Current `build-deploy.md` -> `skills/tauri2-mobile/references/build-deploy-mobile.md` (existing file is entirely mobile: APK/AAB/IPA, keystore, store submission, Windows cross-compile issues)
- Current `ci-cd.md` -> `skills/tauri-core/references/ci-cd.md` (extract provider-agnostic base: caching, matrix builds, release profiles, signing concepts) + `skills/tauri2-mobile/references/ci-cd-mobile.md` (mobile delta: Android/iOS targets, store upload, Fastlane as build tool)

**Files to CREATE (new SKILL.md files):**
- `skills/tauri-core/SKILL.md`

**Files to KEEP (unchanged):**
- `skills/tauri2-mobile/references/testing.md`
- `skills/tauri2-mobile/references/iap.md`

**Files to DELETE (after all extractions complete):**
- `skills/tauri2-mobile/references/setup.md`
- `skills/tauri2-mobile/references/plugins.md`
- `skills/tauri2-mobile/references/authentication.md`
- `skills/tauri2-mobile/references/build-deploy.md`
- `skills/tauri2-mobile/references/ci-cd.md`
- `skills/tauri2-mobile/references/rust-patterns.md`
- `skills/tauri2-mobile/references/frontend-patterns.md`

**Files to EDIT (in-place modifications):**
- `agents/rust-engineer.md` -- add capabilities + code patterns
- `agents/tauri-optimizer.md` -- add Raw Payloads, HFT rendering, backpressure sections
- `skills/tauri2-mobile/SKILL.md` -- update to mobile-only scope, update reference links

### Marketplace Changes

- Update skills array to: `["./skills/tauri-core", "./skills/tauri-desktop", "./skills/tauri2-mobile"]`
- Bump plugin version from 1.8.0 to 2.0.0 (breaking restructure)
- Bump `metadata.version`

### Notes

- **CLAUDE.md**: No update needed -- plugin count stays at 33, plugin name unchanged
- **docs/plugins/**: Check if `docs/plugins/tauri-development.md` exists; if so, update after restructure
- **CI/CD provider-agnostic**: Both `ci-cd.md` (core) and `ci-cd-mobile.md` must be provider-agnostic. Fastlane is referenced as a build/deploy tool, not a CI provider
- **No desktop CI/CD file**: Desktop builds are standard Cargo/Tauri CLI invocations covered by the core CI/CD base patterns
