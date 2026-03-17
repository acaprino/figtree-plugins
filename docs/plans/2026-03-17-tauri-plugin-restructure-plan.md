# Tauri Plugin Restructure Implementation Plan

> **For agentic workers:** Use subagent-driven execution (if subagents available) or ai-tooling:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Restructure tauri-development plugin from 1 skill to 3 (core/desktop/mobile), upgrade both agents with modern patterns, and create new desktop-specific reference content.

**Architecture:** Extract universal content from tauri2-mobile into tauri-core, create new tauri-desktop skill with researched content, slim down tauri2-mobile to mobile-only, and enhance agents with tracing/rkyv/Canvas/backpressure patterns.

**Tech Stack:** Tauri v2, Rust, TypeScript/React, markdown reference files

**Spec:** `docs/plans/2026-03-17-tauri-plugin-restructure-design.md`

---

## Chunk 1: Create tauri-core Skill (Extract Universal Content)

### Task 1: Create tauri-core directory and SKILL.md

**Files:**
- Create: `plugins/tauri-development/skills/tauri-core/SKILL.md`
- Create: `plugins/tauri-development/skills/tauri-core/references/` (directory)

- [ ] **Step 1: Create tauri-core SKILL.md**

```markdown
---
name: tauri-core
description: >
  Core Tauri 2 development patterns for both desktop and mobile. Use when working
  with Tauri commands, IPC communication, plugin integration, project setup, OAuth/PKCE
  authentication, or CI/CD pipelines. Covers Rust backend patterns, frontend TypeScript
  integration, and universal plugin configuration.
---

# Tauri 2 Core Development

Cross-platform patterns for Tauri 2 applications -- desktop and mobile.

## Quick Reference

| Task | Command |
|------|---------|
| New project | `npm create tauri-app@latest` |
| Add plugin | `npm run tauri add <plugin-name>` |
| Dev mode | `cargo tauri dev` |
| Build | `cargo tauri build` |
| Info | `cargo tauri info` |

## Workflow Decision Tree

### New Project Setup
1. Read [references/setup.md](references/setup.md) for environment prerequisites
2. Run `npm create tauri-app@latest`
3. Configure `tauri.conf.json` with app identifier

### Adding Features
- **Rust commands/state/channels**: Read [references/rust-patterns.md](references/rust-patterns.md)
- **Frontend integration (invoke/events)**: Read [references/frontend-patterns.md](references/frontend-patterns.md)
- **Plugin integration**: Read [references/plugins-core.md](references/plugins-core.md)
- **Authentication (OAuth/PKCE)**: Read [references/authentication.md](references/authentication.md)

### CI/CD
- **Pipeline setup**: Read [references/ci-cd.md](references/ci-cd.md)

## Project Structure

` ` `
my-app/
+-- src/                          # Frontend (React/Vue/Svelte/etc.)
+-- src-tauri/
|   +-- Cargo.toml
|   +-- tauri.conf.json           # Main config
|   +-- src/
|   |   +-- main.rs               # Desktop entry (don't modify)
|   |   +-- lib.rs                # Main code + mobile entry
|   +-- capabilities/
|   |   +-- default.json          # Permissions
|   +-- gen/
|       +-- android/              # Android project (if mobile)
|       +-- apple/                # Xcode project (if mobile)
` ` `

## Essential Configuration

### tauri.conf.json
` ` `json
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "MyApp",
  "identifier": "com.company.myapp",
  "build": {
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist"
  }
}
` ` `

### capabilities/default.json
` ` `json
{
  "identifier": "default",
  "windows": ["main"],
  "permissions": ["core:default"]
}
` ` `

## Common Issues

| Problem | Solution |
|---------|----------|
| White screen | Check JS console, verify `devUrl`, check capabilities |
| Command not found | Verify handler registered in `invoke_handler` |
| Permission denied | Add permission to capabilities/default.json |
| Plugin not loaded | Check `.plugin()` call in lib.rs |

## Resources

- Docs: https://v2.tauri.app
- Plugins: https://v2.tauri.app/plugin/
- GitHub: https://github.com/tauri-apps/tauri
```

Note: Replace ` ` ` with actual triple backticks in the file. The plan uses spaced backticks to avoid markdown nesting issues.

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri-core/SKILL.md
git commit -m "Add tauri-core skill with universal SKILL.md"
```

### Task 2: Extract setup.md (universal parts)

**Files:**
- Create: `plugins/tauri-development/skills/tauri-core/references/setup.md`
- Source: `plugins/tauri-development/skills/tauri2-mobile/references/setup.md`

- [ ] **Step 1: Create core setup.md**

Copy from current `setup.md` but keep ONLY:
- "Prerequisites > All Platforms" section (Rust, Node.js, Tauri CLI)
- "Project Initialization" section (npm create, cargo tauri info)
- Remove: "Android Development" section entirely
- Remove: "iOS Development" section entirely
- Remove: "Vite Configuration for Mobile" section (HMR/TAURI_DEV_HOST is mobile-specific)
- Remove: "Platform-Specific Configuration" section (AndroidManifest, Info.plist)

Add a generic Vite config section (without mobile HMR):

```markdown
## Vite Configuration

` ` `typescript
// vite.config.ts
import { defineConfig } from 'vite';

export default defineConfig({
  clearScreen: false,
  envPrefix: ['VITE_', 'TAURI_'],
  build: {
    target: 'esnext',
    minify: !process.env.TAURI_ENV_DEBUG ? 'esbuild' : false,
    sourcemap: !!process.env.TAURI_ENV_DEBUG,
  },
});
` ` `
```

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri-core/references/setup.md
git commit -m "Extract universal setup.md to tauri-core"
```

### Task 3: Move rust-patterns.md to core

**Files:**
- Create: `plugins/tauri-development/skills/tauri-core/references/rust-patterns.md`
- Source: `plugins/tauri-development/skills/tauri2-mobile/references/rust-patterns.md`

- [ ] **Step 1: Copy rust-patterns.md to core**

Copy as-is -- content is already universal. Only change the title from "Rust Patterns for Tauri Mobile" to "Rust Patterns for Tauri".

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri-core/references/rust-patterns.md
git commit -m "Move rust-patterns.md to tauri-core (universal)"
```

### Task 4: Extract frontend-patterns.md (remove mobile-specific)

**Files:**
- Create: `plugins/tauri-development/skills/tauri-core/references/frontend-patterns.md`
- Source: `plugins/tauri-development/skills/tauri2-mobile/references/frontend-patterns.md`

- [ ] **Step 1: Create core frontend-patterns.md**

Copy from current `frontend-patterns.md` but:
- Change title from "Frontend Patterns for Tauri Mobile" to "Frontend Patterns for Tauri"
- Keep: "Invoking Rust Commands", "Channels (Streaming)", "Event Listeners", "Platform Detection"
- Keep: "File System", "HTTP Client" plugin examples (universal)
- Keep: "React Hooks Examples" (useInvoke, useEvent)
- Keep: "Capabilities Configuration" -- but simplify to core-only permissions
- Remove: "Biometric Authentication" section (mobile-only)
- Remove: "Geolocation" section (mobile-only)
- Remove: "Haptics" section (mobile-only)
- Remove: "Deep Links" section (moved to mobile)
- Remove: "Notifications" section -- keep as universal but note mobile requires extra setup
- Remove: "Safe Areas on Android WebView" entire section (mobile-only)
- Remove: mobile capabilities JSON block (`mobile.json`)

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri-core/references/frontend-patterns.md
git commit -m "Extract universal frontend-patterns.md to tauri-core"
```

### Task 5: Extract plugins-core.md (universal plugins only)

**Files:**
- Create: `plugins/tauri-development/skills/tauri-core/references/plugins-core.md`
- Source: `plugins/tauri-development/skills/tauri2-mobile/references/plugins.md`

- [ ] **Step 1: Create plugins-core.md**

From current `plugins.md`, keep only universal plugins and patterns:
- Keep: "Adding Plugins" section (npm run tauri add)
- Keep from table: fs, http, notification, clipboard-manager, dialog, opener, store, sql, log, os, deep-link (mark mobile/desktop support)
- Remove from table: biometric, barcode-scanner, haptics, nfc (mobile-only -- move to plugins-mobile.md)
- Keep: "Plugin Configuration > lib.rs Setup" -- but remove `#[cfg(mobile)]` conditional plugins
- Keep: "Permissions (capabilities/default.json)" -- core permissions only
- Keep: "Deep Linking Configuration" -- keep desktop scheme, note mobile config is in tauri2-mobile
- Keep: "Opener Plugin" -- universal, but note the shell plugin alternative on desktop
- Keep: "Logging Plugin", "Store Plugin", "SQL Plugin" sections
- Remove: "Barcode Scanner", "NFC", community mobile plugins
- Remove: Android Intent Filter, iOS Associated Domains (move to plugins-mobile)

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri-core/references/plugins-core.md
git commit -m "Extract plugins-core.md with universal plugins to tauri-core"
```

### Task 6: Extract authentication.md (universal OAuth/PKCE)

**Files:**
- Create: `plugins/tauri-development/skills/tauri-core/references/authentication.md`
- Source: `plugins/tauri-development/skills/tauri2-mobile/references/authentication.md`

- [ ] **Step 1: Create core authentication.md**

From current `authentication.md`, keep universal OAuth/PKCE architecture:
- Keep: "The WebView Problem" (applies to desktop too -- Google blocks embedded WebViews)
- Keep: "Solution: System Browser + Deep Links" -- generalize flow description for desktop and mobile
- Keep: "Security Warning" about token exposure
- Keep: "TypeScript Interfaces"
- Keep: "Configuration with Validation"
- Keep: "Secure State Management" (oauth-state.ts)
- Keep: "Initiate OAuth Flow (with CSRF Protection)" -- but generalize, don't reference `opener` plugin specifically (desktop can use `shell:open`)
- Keep: "Handle Callback with State Validation"
- Keep: "PKCE Utilities" and "PKCE OAuth Flow" (the recommended approach)
- Keep: "Token Refresh"
- Keep: "Google Cloud Console Setup"
- Keep: "Security Checklist"
- Remove: "Create Hosted Callback Page" (mobile-specific Firebase hosting -- move to authentication-mobile)
- Remove: "Apple Sign-In" entire section (move to authentication-mobile)
- Remove: "Complete Example: Secure Auth Context" with deep link listener (mobile-specific integration -- move to authentication-mobile)
- Generalize: OAuth flow diagram to show "System Browser" without specifying Chrome Custom Tabs

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri-core/references/authentication.md
git commit -m "Extract universal OAuth/PKCE authentication.md to tauri-core"
```

### Task 7: Create ci-cd.md (provider-agnostic base)

**Files:**
- Create: `plugins/tauri-development/skills/tauri-core/references/ci-cd.md`
- Source: `plugins/tauri-development/skills/tauri2-mobile/references/ci-cd.md` (extract patterns, rewrite as generic)

- [ ] **Step 1: Create core ci-cd.md**

Write a NEW provider-agnostic CI/CD reference covering:

```markdown
# CI/CD for Tauri Applications

## Pipeline Stages

A typical Tauri CI/CD pipeline has these stages:

1. **Setup** -- install toolchain (Rust, Node.js, platform SDK)
2. **Cache** -- restore Rust target/, node_modules/
3. **Build frontend** -- bundle the web assets
4. **Build Tauri** -- compile Rust + bundle into platform installer
5. **Sign** -- code signing for distribution
6. **Artifact** -- upload build output
7. **Release** (optional) -- create release, publish

## Caching Strategy

### Rust Compilation Cache
Cache `src-tauri/target/` keyed by:
- OS + architecture
- `Cargo.lock` hash
- Rust toolchain version

Typical cache sizes: 500MB-2GB. Use incremental compilation cache where supported.

### Node Dependencies
Cache `node_modules/` keyed by lockfile hash.

### Platform-Specific Caches
- **Gradle** (Android): `~/.gradle/caches/`
- **CocoaPods** (iOS): `~/Library/Caches/CocoaPods/`, `Pods/`

## OS Matrix

| Target Platform | CI Runner OS | Notes |
|----------------|-------------|-------|
| Windows (.msi, .nsis) | Windows | WebView2 bundled or bootstrapped |
| macOS (.dmg, .app) | macOS | WKWebView (system) |
| Linux (.AppImage, .deb) | Ubuntu | libwebkit2gtk-4.1 required |
| Android (.apk, .aab) | Ubuntu | Android SDK + NDK required |
| iOS (.ipa) | macOS | Xcode required |

## Release Profiles in CI

Ensure `Cargo.toml` has optimized release profile:

` ` `toml
[profile.release]
lto = true
opt-level = "s"       # Optimize for size (or "3" for speed)
codegen-units = 1     # Better optimization
strip = true          # Remove debug symbols
panic = "abort"       # Smaller binary
` ` `

## Code Signing Concepts

### Signing Secrets Management
- Store signing keys/certificates as CI secrets (base64-encoded for binary files)
- Decode at build time into temporary paths
- Never commit signing credentials to the repository

### Platform Signing Overview
| Platform | Signing Method | Required Credentials |
|----------|---------------|---------------------|
| Windows | Authenticode (optional) | Code signing certificate (.pfx) |
| macOS | codesign + notarization | Apple Developer ID, API key |
| Linux | None required | -- |
| Android | Keystore | .jks file + password + alias |
| iOS | Apple provisioning | Certificate + provisioning profile or API key |

## Artifact Management

Build outputs by platform:
| Platform | Output | Typical Location |
|----------|--------|-----------------|
| Windows | `.msi`, `.nsis` | `src-tauri/target/release/bundle/` |
| macOS | `.dmg`, `.app` | `src-tauri/target/release/bundle/` |
| Linux | `.AppImage`, `.deb` | `src-tauri/target/release/bundle/` |
| Android | `.apk`, `.aab` | `src-tauri/gen/android/app/build/outputs/` |
| iOS | `.ipa` | `src-tauri/gen/apple/build/` |

## Tauri Official CI Action

The `tauri-apps/tauri-action` simplifies desktop builds with automatic artifact upload and release creation. Works with GitHub Actions; for other CI providers, use direct CLI commands.

## Environment Variables

Common variables needed in CI:
` ` `
TAURI_SIGNING_PRIVATE_KEY    # For auto-updater signing
TAURI_SIGNING_PRIVATE_KEY_PASSWORD
` ` `

## Pipeline Anti-Patterns

- **No caching** -- Rust builds are slow; always cache target/
- **Building all targets sequentially** -- use parallel jobs per platform
- **Hardcoded paths** -- use CI variables for temp dirs and artifact paths
- **Skipping release profile** -- debug builds are 10-50x larger
```

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri-core/references/ci-cd.md
git commit -m "Add provider-agnostic CI/CD base reference to tauri-core"
```

---

## Chunk 2: Slim Down tauri2-mobile (Mobile-Only Content)

### Task 8: Create setup-mobile.md

**Files:**
- Create: `plugins/tauri-development/skills/tauri2-mobile/references/setup-mobile.md`
- Source: `plugins/tauri-development/skills/tauri2-mobile/references/setup.md`

- [ ] **Step 1: Create setup-mobile.md**

From current `setup.md`, extract ONLY mobile-specific sections:
- "Android Development" (Android Studio, SDK, NDK, environment variables, Strawberry Perl, Rust targets)
- "iOS Development (macOS only)" (Xcode, CocoaPods, Apple Developer, Rust targets)
- "Vite Configuration for Mobile" (TAURI_DEV_HOST, HMR for mobile)
- "Platform-Specific Configuration" (AndroidManifest.xml, Info.plist)
- Add at top: "For base prerequisites (Rust, Node, Tauri CLI), see `tauri-core/references/setup.md`."

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri2-mobile/references/setup-mobile.md
git commit -m "Create setup-mobile.md with Android/iOS specific setup"
```

### Task 9: Rename build-deploy.md to build-deploy-mobile.md

**Files:**
- Create: `plugins/tauri-development/skills/tauri2-mobile/references/build-deploy-mobile.md`
- Source: `plugins/tauri-development/skills/tauri2-mobile/references/build-deploy.md`

- [ ] **Step 1: Copy and rename**

Copy existing `build-deploy.md` as `build-deploy-mobile.md`. Content is already entirely mobile-specific (APK/AAB/IPA, keystore, store submission). Only changes:
- Update title to "Mobile Build and Deploy"
- Add note at top: "For release optimization profiles (Cargo.toml), see `tauri-core/references/ci-cd.md`."

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri2-mobile/references/build-deploy-mobile.md
git commit -m "Create build-deploy-mobile.md from existing build-deploy.md"
```

### Task 10: Create plugins-mobile.md

**Files:**
- Create: `plugins/tauri-development/skills/tauri2-mobile/references/plugins-mobile.md`
- Source: `plugins/tauri-development/skills/tauri2-mobile/references/plugins.md` + `frontend-patterns.md`

- [ ] **Step 1: Create plugins-mobile.md**

Combine mobile-only plugin content:

From `plugins.md`:
- Barcode Scanner section
- NFC Plugin section
- Community Plugins (tauri-plugin-iap reference, keep-screen-on, camera, share)
- Android Intent Filter for deep links
- iOS Associated Domains for deep links
- The `#[cfg(mobile)]` plugin patterns from lib.rs
- Mobile-specific capabilities JSON

From `frontend-patterns.md`:
- Biometric Authentication example
- Geolocation example
- Haptics example
- Safe Areas on Android WebView entire section
- Mobile capabilities configuration (`mobile.json`)
- Deep Links example

Add at top: "For universal plugins (fs, store, sql, http, etc.), see `tauri-core/references/plugins-core.md`."

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri2-mobile/references/plugins-mobile.md
git commit -m "Create plugins-mobile.md with mobile-only plugins and patterns"
```

### Task 11: Create authentication-mobile.md

**Files:**
- Create: `plugins/tauri-development/skills/tauri2-mobile/references/authentication-mobile.md`
- Source: `plugins/tauri-development/skills/tauri2-mobile/references/authentication.md`

- [ ] **Step 1: Create authentication-mobile.md**

From current `authentication.md`, extract mobile-specific content:
- Deep link callback setup (tauri.conf.json mobile config)
- Opener plugin for system browser on mobile (Chrome Custom Tabs, Safari)
- Hosted callback page (Firebase Hosting) with full HTML
- Firebase Hosting configuration
- Apple Sign-In section (App Store Connect setup, implementation, Firebase integration, Apple-specific callback handling)
- Complete Auth Context example with deep link listener (onOpenUrl)
- Login screen usage example
- Mobile-specific troubleshooting entries

Add at top: "For OAuth/PKCE architecture and security patterns, see `tauri-core/references/authentication.md`."

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri2-mobile/references/authentication-mobile.md
git commit -m "Create authentication-mobile.md with deep links and Apple Sign-In"
```

### Task 12: Create ci-cd-mobile.md

**Files:**
- Create: `plugins/tauri-development/skills/tauri2-mobile/references/ci-cd-mobile.md`
- Source: `plugins/tauri-development/skills/tauri2-mobile/references/ci-cd.md`

- [ ] **Step 1: Create ci-cd-mobile.md**

Extract mobile-specific CI/CD from current `ci-cd.md`, rewritten as provider-agnostic:

```markdown
# Mobile CI/CD

> For base CI/CD patterns (caching, OS matrix, release profiles), see `tauri-core/references/ci-cd.md`.

## Mobile Build Requirements

### Android
- Java 17+ (JDK)
- Android SDK with Platform Tools, Build Tools, NDK
- Rust targets: `aarch64-linux-android`, `armv7-linux-androideabi`

### iOS
- macOS runner (required -- iOS builds cannot run on Linux/Windows)
- Xcode (full install)
- Rust targets: `aarch64-apple-ios`, `aarch64-apple-ios-sim`

## Android Signing in CI

1. Store keystore as base64-encoded secret
2. Decode at build time:
` ` `bash
echo "$ANDROID_KEYSTORE_BASE64" | base64 -d > /tmp/keystore.jks
` ` `
3. Write `keystore.properties` with alias, password, path

### Required Secrets
` ` `
ANDROID_KEY_ALIAS
ANDROID_KEY_PASSWORD
ANDROID_KEYSTORE_BASE64    # base64 -i upload-keystore.jks | tr -d '\n'
` ` `

## iOS Signing in CI

Use App Store Connect API key for headless signing:

### Required Secrets
` ` `
APPLE_API_ISSUER
APPLE_API_KEY
APPLE_API_KEY_CONTENT      # Content of .p8 file
APPLE_TEAM_ID
` ` `

## Mobile Caching

In addition to Rust and Node caches:

| Cache | Path | Key |
|-------|------|-----|
| Gradle | `~/.gradle/caches/` | OS + `gradle-wrapper.properties` hash |
| CocoaPods | `Pods/`, `~/Library/Caches/CocoaPods/` | OS + `Podfile.lock` hash |

## Store Upload Automation

### Google Play
Use Fastlane or the Google Play Developer API to upload AABs:
- Track options: internal, alpha, beta, production
- Requires service account JSON with appropriate permissions

### App Store
Use Fastlane or `xcrun altool` to upload IPAs:
- Requires App Store Connect API key
- Can skip screenshots/metadata for automated uploads

## Mobile Build Tips

- Build Android on Ubuntu runners (fastest, cheapest)
- Build iOS on macOS runners (required by Apple)
- Run Android and iOS builds in parallel
- Use `--target aarch64` to skip x86 builds if not needed
- 16KB page size alignment may be required for Google Play (NDK < 28)
```

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri2-mobile/references/ci-cd-mobile.md
git commit -m "Create ci-cd-mobile.md with provider-agnostic mobile CI/CD patterns"
```

### Task 13: Update tauri2-mobile SKILL.md

**Files:**
- Modify: `plugins/tauri-development/skills/tauri2-mobile/SKILL.md`

- [ ] **Step 1: Rewrite SKILL.md for mobile-only scope**

Update the SKILL.md to:
- Change description to mobile-only scope
- Update all reference links to new filenames
- Add cross-references to tauri-core for shared content
- Update quick reference table to mobile-only commands
- Update common issues to mobile-only issues

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri2-mobile/SKILL.md
git commit -m "Update tauri2-mobile SKILL.md to mobile-only scope with new reference links"
```

### Task 14: Delete old reference files from tauri2-mobile

**Files:**
- Delete: `plugins/tauri-development/skills/tauri2-mobile/references/setup.md`
- Delete: `plugins/tauri-development/skills/tauri2-mobile/references/rust-patterns.md`
- Delete: `plugins/tauri-development/skills/tauri2-mobile/references/frontend-patterns.md`
- Delete: `plugins/tauri-development/skills/tauri2-mobile/references/plugins.md`
- Delete: `plugins/tauri-development/skills/tauri2-mobile/references/authentication.md`
- Delete: `plugins/tauri-development/skills/tauri2-mobile/references/build-deploy.md`
- Delete: `plugins/tauri-development/skills/tauri2-mobile/references/ci-cd.md`

- [ ] **Step 1: Remove old files**

```bash
git rm plugins/tauri-development/skills/tauri2-mobile/references/setup.md
git rm plugins/tauri-development/skills/tauri2-mobile/references/rust-patterns.md
git rm plugins/tauri-development/skills/tauri2-mobile/references/frontend-patterns.md
git rm plugins/tauri-development/skills/tauri2-mobile/references/plugins.md
git rm plugins/tauri-development/skills/tauri2-mobile/references/authentication.md
git rm plugins/tauri-development/skills/tauri2-mobile/references/build-deploy.md
git rm plugins/tauri-development/skills/tauri2-mobile/references/ci-cd.md
```

- [ ] **Step 2: Verify remaining files in tauri2-mobile**

Expected remaining files:
```
skills/tauri2-mobile/
  SKILL.md
  references/
    setup-mobile.md
    testing.md              (unchanged)
    iap.md                  (unchanged)
    build-deploy-mobile.md
    plugins-mobile.md
    ci-cd-mobile.md
    authentication-mobile.md
```

- [ ] **Step 3: Commit**

```bash
git commit -m "Remove old reference files replaced by tauri-core and renamed mobile files"
```

---

## Chunk 3: Create tauri-desktop Skill (New Research Content)

### Task 15: Create tauri-desktop SKILL.md

**Files:**
- Create: `plugins/tauri-development/skills/tauri-desktop/SKILL.md`
- Create: `plugins/tauri-development/skills/tauri-desktop/references/` (directory)

- [ ] **Step 1: Create SKILL.md**

```markdown
---
name: tauri-desktop
description: >
  Desktop-specific Tauri 2 development. Use when working with window management
  (multi-window, frameless, system tray, native menus), shell plugin for child processes,
  desktop bundling (.msi, .dmg, .AppImage), code signing, auto-updater, or
  platform-specific WebView differences (WebView2, WKWebView, WebKitGTK).
---

# Tauri 2 Desktop Development

Desktop-specific patterns and capabilities for Tauri 2 applications.

## Quick Reference

| Task | Command |
|------|---------|
| Dev mode | `cargo tauri dev` |
| Build | `cargo tauri build` |
| Build debug | `cargo tauri build --debug` |
| Generate icons | `cargo tauri icon ./app-icon.png` |

## Workflow Decision Tree

### Window Management
- **Multi-window / frameless / transparency**: Read [references/window-management.md](references/window-management.md)

### Native Desktop Features
- **Child processes / sidecar binaries**: Read [references/shell-plugin.md](references/shell-plugin.md)

### Building & Distribution
- **Bundling, signing, auto-updater**: Read [references/build-deploy.md](references/build-deploy.md)

### Platform Differences
- **WebView quirks per OS**: Read [references/platform-webviews.md](references/platform-webviews.md)

## Desktop Capabilities

Desktop Tauri apps can do things mobile apps cannot:
- Execute child processes and system commands (shell plugin)
- Create multiple windows with independent content
- System tray icons with context menus
- Native application menus
- Global keyboard shortcuts
- Frameless/transparent windows with custom title bars
- Auto-updater for self-updating apps

## Resources

- Desktop bundler docs: https://v2.tauri.app/distribute/
- Window API: https://v2.tauri.app/reference/javascript/api/namespacewindow/
- Shell plugin: https://v2.tauri.app/plugin/shell/
```

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri-desktop/SKILL.md
git commit -m "Add tauri-desktop skill with SKILL.md"
```

### Task 16: Research and create window-management.md

**Files:**
- Create: `plugins/tauri-development/skills/tauri-desktop/references/window-management.md`

- [ ] **Step 1: Research Tauri v2 window management API**

Research via Tauri v2 docs and source the following topics:
- `WebviewWindowBuilder` / `WindowBuilder` API
- Creating additional windows at runtime
- Frameless windows (`decorations: false`)
- Transparent windows
- System tray with `tauri-plugin-tray-icon` (context menu, click events, dynamic icon)
- Native application menus
- Window events (close requested, focus, resize, move)
- Window state (maximize, minimize, fullscreen)
- Custom title bar patterns

- [ ] **Step 2: Write window-management.md with researched content**

Include code examples for Rust and TypeScript sides.

- [ ] **Step 3: Commit**

```bash
git add plugins/tauri-development/skills/tauri-desktop/references/window-management.md
git commit -m "Add window-management.md reference for tauri-desktop"
```

### Task 17: Research and create shell-plugin.md

**Files:**
- Create: `plugins/tauri-development/skills/tauri-desktop/references/shell-plugin.md`

- [ ] **Step 1: Research Tauri v2 shell plugin**

Research:
- `tauri-plugin-shell` Command API (spawn, execute, output)
- Stdout/stderr streaming
- Sidecar binaries configuration
- Scoped shell commands (security model)
- Opening URLs with shell:open vs opener plugin
- Examples: running scripts, Git commands, system utilities

- [ ] **Step 2: Write shell-plugin.md with researched content**

- [ ] **Step 3: Commit**

```bash
git add plugins/tauri-development/skills/tauri-desktop/references/shell-plugin.md
git commit -m "Add shell-plugin.md reference for tauri-desktop"
```

### Task 18: Research and create build-deploy.md (desktop)

**Files:**
- Create: `plugins/tauri-development/skills/tauri-desktop/references/build-deploy.md`

- [ ] **Step 1: Research desktop bundling in Tauri v2**

Research:
- Windows: .msi (WiX), .nsis, code signing with Authenticode
- macOS: .dmg, .app, code signing + notarization, universal binaries (x86_64 + aarch64)
- Linux: .AppImage, .deb, .rpm, .pacman
- Auto-updater: `tauri-plugin-updater`, update server endpoints, signing keys
- `tauri.conf.json` bundle configuration

- [ ] **Step 2: Write build-deploy.md with researched content**

- [ ] **Step 3: Commit**

```bash
git add plugins/tauri-development/skills/tauri-desktop/references/build-deploy.md
git commit -m "Add desktop build-deploy.md reference for tauri-desktop"
```

### Task 19: Create platform-webviews.md

**Files:**
- Create: `plugins/tauri-development/skills/tauri-desktop/references/platform-webviews.md`

- [ ] **Step 1: Research and write platform-webviews.md**

Content from tauri-optimizer agent (expand):
- WebView2 (Windows) -- Chromium-based, most consistent
- WKWebView (macOS) -- Safari engine, CSS differences, DevTools via Safari
- WebKitGTK (Linux) -- version varies by distro, test thoroughly
- CSS feature support differences
- JavaScript API compatibility
- DevTools access per platform
- Performance characteristics per WebView

- [ ] **Step 2: Commit**

```bash
git add plugins/tauri-development/skills/tauri-desktop/references/platform-webviews.md
git commit -m "Add platform-webviews.md reference for tauri-desktop"
```

---

## Chunk 4: Upgrade Agents

### Task 20: Upgrade rust-engineer.md

**Files:**
- Modify: `plugins/tauri-development/agents/rust-engineer.md`

- [ ] **Step 1: Add new capabilities**

Add to CAPABILITIES section after existing bullets:

```markdown
- Observability -- `tracing`, `tracing-subscriber`, structured spans with `#[instrument]`, log filtering layers
- Advanced testing -- `loom` for lock-free/concurrency model verification, `insta` for snapshot testing, `tarpaulin` for code coverage
- Serialization -- zero-copy deserialization with `rkyv` for high-throughput scenarios; `serde` for standard JSON/YAML/TOML
- Rich diagnostics -- `miette` for CLI-quality error reports with source snippets, labels, and help text
```

- [ ] **Step 2: Add observability code pattern**

Add new pattern to CODE PATTERNS section:

```markdown
## Observability with tracing

` ` `rust
use tracing::{instrument, info, error};

#[instrument(skip(data), fields(bytes = data.len()))]
pub async fn process_payload(id: uuid::Uuid, data: &[u8]) -> Result<(), AppError> {
    info!("Starting payload processing");
    match decode_and_store(data).await {
        Ok(_) => {
            info!("Successfully processed");
            Ok(())
        }
        Err(e) => {
            error!(error = %e, "Failed to process payload");
            Err(e.into())
        }
    }
}

// Subscriber setup in main/lib
fn init_tracing() {
    use tracing_subscriber::{fmt, EnvFilter, prelude::*};

    tracing_subscriber::registry()
        .with(fmt::layer())
        .with(EnvFilter::from_default_env())
        .init();
}
` ` `
```

- [ ] **Step 3: Commit**

```bash
git add plugins/tauri-development/agents/rust-engineer.md
git commit -m "Upgrade rust-engineer agent with tracing, rkyv, loom, miette capabilities"
```

### Task 21: Upgrade tauri-optimizer.md

**Files:**
- Modify: `plugins/tauri-development/agents/tauri-optimizer.md`

- [ ] **Step 1: Expand Raw Payloads in IPC section**

After the existing "Binary Payloads" subsection, add:

```markdown
**Zero-Copy Serialization with rkyv:**
` ` `rust
use rkyv::{Archive, Deserialize, Serialize};
use tauri::ipc::Response;

#[derive(Archive, Deserialize, Serialize)]
struct OrderBookSnapshot {
    bids: Vec<(f64, f64)>,  // (price, quantity)
    asks: Vec<(f64, f64)>,
    timestamp: u64,
}

#[tauri::command]
async fn get_orderbook_binary() -> Response {
    let snapshot = generate_orderbook_snapshot();
    let bytes = rkyv::to_bytes::<_, 4096>(&snapshot)
        .expect("serialization failed");
    Response::new(bytes.to_vec()) // ArrayBuffer in JS
}
` ` `

**Frontend: TypedArray consumption (bypass JSON):**
` ` `typescript
const buffer = await invoke<ArrayBuffer>('get_orderbook_binary');
const view = new Float64Array(buffer);
// Direct memory access -- zero parsing overhead
// Layout: [bid_price, bid_qty, ..., ask_price, ask_qty, ..., timestamp]
` ` `
```

- [ ] **Step 2: Add Extreme High-Frequency Rendering section**

Add new section after "React State Management for Trading":

```markdown
### Extreme High-Frequency Rendering

**Anti-pattern: React DOM updates at > 60 FPS**
Virtual DOM diffing cannot sustain sub-16ms ticks for thousands of orderbook rows. No amount of memoization or virtualization fixes this -- the DOM is the bottleneck.

**Correct: Canvas + OffscreenCanvas + Web Workers**
Use React for the UI shell (controls, navigation, settings). Delegate data-intensive rendering (charts, dense orderbooks, heatmaps) to Canvas driven by a Web Worker.

` ` `typescript
// React component: holds canvas ref, delegates rendering to Worker
const canvasRef = useRef<HTMLCanvasElement>(null);

useEffect(() => {
  const canvas = canvasRef.current!;
  const offscreen = canvas.transferControlToOffscreen();
  const worker = new Worker(new URL('./renderWorker.ts', import.meta.url));

  // Transfer canvas ownership to worker -- React no longer touches these pixels
  worker.postMessage({ type: 'init', canvas: offscreen }, [offscreen]);

  // Connect Tauri IPC binary channel directly to worker
  const channel = new Channel<ArrayBuffer>();
  channel.onmessage = (data) => {
    worker.postMessage({ type: 'data', buffer: data }, [data]);
  };
  invoke('subscribe_orderbook_binary', { channel });

  return () => worker.terminate();
}, []);
` ` `

` ` `typescript
// renderWorker.ts -- runs off main thread
let ctx: OffscreenCanvasRenderingContext2D;

self.onmessage = (e) => {
  if (e.data.type === 'init') {
    ctx = e.data.canvas.getContext('2d')!;
  } else if (e.data.type === 'data') {
    const view = new Float64Array(e.data.buffer);
    renderOrderbook(ctx, view); // Pure canvas drawing, no DOM
  }
};
` ` `

**When to use Canvas vs DOM:**
| Scenario | Approach |
|----------|----------|
| < 100 rows, < 10 updates/sec | React + virtualization |
| 100-1000 rows, 10-60 updates/sec | React + Jotai atomic + virtualization |
| > 1000 rows or > 60 updates/sec | Canvas + Web Worker |
| Charts with streaming data | Canvas (lightweight-charts or custom) |
```

- [ ] **Step 3: Add Backpressure & Memory Protection section**

Add new section after the rendering section:

```markdown
### Backpressure & Memory Protection

**Problem:** If the Rust backend produces data faster than the frontend consumes it, the message queue grows unbounded and causes OOM.

**Rust-side throttling (preferred):**
` ` `rust
use tokio::time::{interval, Duration};

async fn throttled_stream(channel: Channel<Vec<u8>>) {
    let mut tick = interval(Duration::from_millis(16)); // ~60 FPS cap
    let mut latest: Option<Vec<u8>> = None;

    loop {
        tokio::select! {
            data = data_rx.recv() => {
                // Always keep only the latest frame -- drop stale data
                latest = Some(data?);
            }
            _ = tick.tick() => {
                if let Some(frame) = latest.take() {
                    let _ = channel.send(frame); // Drop if frontend disconnected
                }
            }
        }
    }
}
` ` `

**Frontend Worker queue limit:**
` ` `typescript
// In main thread: drop frames if worker is backlogged
let pendingFrames = 0;
const MAX_PENDING = 3;

channel.onmessage = (data) => {
  if (pendingFrames < MAX_PENDING) {
    pendingFrames++;
    worker.postMessage({ type: 'data', buffer: data }, [data]);
  }
  // else: drop frame silently
};

// Worker acknowledges processing
worker.onmessage = () => { pendingFrames--; };
` ` `

**Memory monitoring:**
` ` `typescript
if (import.meta.env.DEV) {
  setInterval(() => {
    const mem = (performance as any).memory;
    if (mem && mem.usedJSHeapSize > 500 * 1024 * 1024) {
      console.warn('Heap exceeding 500MB -- check for leaks');
    }
  }, 5000);
}
` ` `
```

- [ ] **Step 4: Commit**

```bash
git add plugins/tauri-development/agents/tauri-optimizer.md
git commit -m "Upgrade tauri-optimizer with rkyv Raw Payloads, Canvas HFT rendering, backpressure"
```

---

## Chunk 5: Marketplace Update and Documentation

### Task 22: Update marketplace.json

**Files:**
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Update tauri-development plugin entry**

Change the skills array from:
```json
"skills": ["./skills/tauri2-mobile"]
```
to:
```json
"skills": ["./skills/tauri-core", "./skills/tauri-desktop", "./skills/tauri2-mobile"]
```

- [ ] **Step 2: Bump plugin version to 2.0.0**

Change:
```json
"version": "1.8.0"
```
to:
```json
"version": "2.0.0"
```

- [ ] **Step 3: Bump metadata version**

Change:
```json
"version": "2.68.0"
```
to:
```json
"version": "2.69.0"
```

- [ ] **Step 4: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "Register tauri-core and tauri-desktop skills, bump to v2.0.0"
```

### Task 23: Update docs/plugins/tauri-development.md

**Files:**
- Modify: `docs/plugins/tauri-development.md`

- [ ] **Step 1: Update documentation page**

Add `tauri-core` and `tauri-desktop` skill entries. Update existing `tauri2-mobile` entry to reflect slimmed-down scope.

- [ ] **Step 2: Commit**

```bash
git add docs/plugins/tauri-development.md
git commit -m "Update tauri-development docs to reflect 3-skill structure"
```

### Task 24: Final verification

- [ ] **Step 1: Verify all files exist**

```bash
ls plugins/tauri-development/skills/tauri-core/references/
# Expected: setup.md, rust-patterns.md, frontend-patterns.md, plugins-core.md, authentication.md, ci-cd.md

ls plugins/tauri-development/skills/tauri-desktop/references/
# Expected: window-management.md, shell-plugin.md, build-deploy.md, platform-webviews.md

ls plugins/tauri-development/skills/tauri2-mobile/references/
# Expected: setup-mobile.md, testing.md, iap.md, build-deploy-mobile.md, plugins-mobile.md, ci-cd-mobile.md, authentication-mobile.md
```

- [ ] **Step 2: Verify no orphan references in SKILL.md files**

Check that all links in each SKILL.md point to existing files.

- [ ] **Step 3: Verify marketplace.json is valid**

```bash
python -c "import json; json.load(open('.claude-plugin/marketplace.json'))"
```

- [ ] **Step 4: Final commit if any fixes needed**

---

## Execution Order Summary

| Chunk | Tasks | Description |
|-------|-------|-------------|
| 1 | 1-7 | Create tauri-core skill, extract universal content |
| 2 | 8-14 | Create mobile-specific files, update tauri2-mobile, delete old files |
| 3 | 15-19 | Create tauri-desktop skill with new researched content |
| 4 | 20-21 | Upgrade both agents with modern patterns |
| 5 | 22-24 | Update marketplace, docs, verify |

**Critical ordering:** Chunk 2 Task 14 (delete old files) MUST happen after Chunks 1 and 2 Tasks 8-13 are complete.
