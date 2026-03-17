# Tauri Development Plugin

> Build fast, secure cross-platform apps. Expert Rust engineering plus Tauri 2 optimization for desktop and mobile -- with concrete performance targets for startup time, memory, and IPC latency.

## Agents

### `tauri-optimizer`

Expert in Tauri v2 + React optimization for trading and high-frequency data scenarios.

| | |
|---|---|
| **Model** | `opus` |
| **Use for** | IPC optimization, state management, memory leaks, WebView tuning, Raw Payloads with rkyv, Canvas/OffscreenCanvas HFT rendering, backpressure |

**Invocation:**
```
Use the tauri-optimizer agent to analyze [project/file]
```

**Performance targets:**
| Metric | Target | Critical |
|--------|--------|----------|
| Startup time | < 1s | < 2s |
| Memory baseline | < 100MB | < 150MB |
| IPC latency | < 0.5ms | < 1ms |
| Frame rate | 60 FPS | > 30 FPS |

---

### `rust-engineer`

Expert Rust developer specializing in systems programming and memory safety.

| | |
|---|---|
| **Model** | `opus` |
| **Use for** | Ownership patterns, async tokio, FFI, performance optimization, tracing/observability, rkyv serialization, loom concurrency testing |

**Invocation:**
```
Use the rust-engineer agent to implement [feature]
```

**Checklist enforced:**
- Zero unsafe code outside core abstractions
- clippy::pedantic compliance
- Complete documentation with examples
- MIRI verification for unsafe blocks

---

## Skills

### `tauri-core`

Universal Tauri 2 development patterns for both desktop and mobile.

| | |
|---|---|
| **Use for** | Rust commands, IPC (invoke/channels/events), core plugins (fs, store, sql, http), OAuth/PKCE, CI/CD pipelines |

**References:**
| File | Content |
|------|---------|
| setup.md | Rust, Node, Tauri CLI prerequisites, project init |
| rust-patterns.md | Commands, state, channels, events, error handling |
| frontend-patterns.md | invoke, channels, events, TypeScript typing, React hooks |
| plugins-core.md | Universal plugins: fs, store, sql, http, log, dialog, opener |
| authentication.md | OAuth/PKCE via system browser, CSRF/nonce protection |
| ci-cd.md | Provider-agnostic CI/CD: caching, matrix builds, signing |

---

### `tauri-desktop`

Desktop-specific Tauri 2 development patterns.

| | |
|---|---|
| **Use for** | Window management, system tray, shell plugin, desktop bundling, WebView platform differences |

**References:**
| File | Content |
|------|---------|
| window-management.md | Multi-window, frameless, system tray, native menus |
| shell-plugin.md | Child processes, sidecar binaries, scoped commands |
| build-deploy.md | .msi, .dmg, .AppImage bundling, code signing, auto-updater |
| platform-webviews.md | WebView2, WKWebView, WebKitGTK differences |

---

### `tauri2-mobile`

Mobile-specific Tauri 2 development for Android and iOS.

| | |
|---|---|
| **Use for** | Mobile setup, emulator/ADB, mobile plugins (biometric, haptics, NFC), IAP, store deployment |

**Quick commands:**
| Task | Command |
|------|---------|
| Init Android | `npm run tauri android init` |
| Dev Android | `npm run tauri android dev` |
| Build APK | `npm run tauri android build --apk` |
| Build iOS | `npm run tauri ios build` |

**References:**
| File | Content |
|------|---------|
| setup-mobile.md | Android SDK, Xcode, NDK, mobile HMR |
| plugins-mobile.md | Biometric, haptics, barcode, NFC, safe areas |
| testing.md | Emulator, ADB, logcat, WebView debugging |
| iap.md | Google Play / App Store in-app purchases |
| authentication-mobile.md | Deep link OAuth, Apple Sign-In, Firebase callback |
| build-deploy-mobile.md | APK/IPA builds, keystore, store submission |
| ci-cd-mobile.md | Mobile CI/CD: signing, store upload, Fastlane |

---

**Related:** [workflows](workflows.md) (`/tauri-pipeline` and `/mobile-tauri-pipeline` orchestrate these agents) | [frontend](frontend.md) (UI polish and layout for Tauri webviews) | [react-development](react-development.md) (React performance in Tauri)
