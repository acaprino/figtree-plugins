---
name: tauri2-mobile
description: >
  Mobile-specific Tauri 2 development for Android and iOS. Use when working with
  mobile environment setup (Android SDK, Xcode), emulator/ADB testing, mobile plugins
  (biometric, haptics, barcode, NFC), in-app purchases, mobile OAuth deep links,
  code signing for Play Store/App Store, and mobile CI/CD pipelines.
  For universal Tauri patterns (commands, IPC, core plugins), see tauri-core.
---

# Tauri 2 Mobile Development

Mobile-specific patterns for Tauri 2 Android and iOS applications.

> For universal Tauri patterns (Rust commands, IPC, core plugins, project setup), see the `tauri-core` skill.

## Quick Reference

| Task | Command |
|------|---------|
| Init Android | `npm run tauri android init` |
| Init iOS | `npm run tauri ios init` |
| Dev Android | `npm run tauri android dev` |
| Dev iOS | `npm run tauri ios dev` |
| Build APK | `npm run tauri android build --apk` |
| Build AAB | `npm run tauri android build --aab` |
| Build iOS | `npm run tauri ios build` |

## Workflow Decision Tree

### Mobile Environment Setup
1. Read [references/setup-mobile.md](references/setup-mobile.md) for Android SDK / iOS Xcode setup
2. Run `npm run tauri android init` / `npm run tauri ios init`
3. Configure mobile-specific permissions

### Adding Mobile Features
- **Mobile plugins (biometric, haptics, NFC)**: Read [references/plugins-mobile.md](references/plugins-mobile.md)
- **In-app purchases**: Read [references/iap.md](references/iap.md)
- **Mobile OAuth (deep links, Apple Sign-In)**: Read [references/authentication-mobile.md](references/authentication-mobile.md)

### Testing
- **Emulator/ADB debug**: Read [references/testing.md](references/testing.md)
- Use `adb logcat | grep -iE "(tauri|RustStdout)"` for logs

### Building & Deployment
- **APK/IPA builds, store submission**: Read [references/build-deploy-mobile.md](references/build-deploy-mobile.md)
- **Mobile CI/CD pipelines**: Read [references/ci-cd-mobile.md](references/ci-cd-mobile.md)

## Mobile Configuration

### tauri.conf.json (mobile-specific)
```json
{
  "bundle": {
    "iOS": { "minimumSystemVersion": "14.0" },
    "android": { "minSdkVersion": 24 }
  },
  "plugins": {
    "deep-link": {
      "mobile": [
        { "scheme": ["myapp"], "appLink": false }
      ]
    }
  }
}
```

### lib.rs (Mobile Entry)
```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .plugin(tauri_plugin_deep_link::init())
        #[cfg(mobile)]
        .plugin(tauri_plugin_biometric::init())
        #[cfg(mobile)]
        .plugin(tauri_plugin_haptics::init())
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error");
}

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}
```

## Common Issues

| Problem | Solution |
|---------|----------|
| iOS won't connect | Use `--force-ip-prompt`, select IPv6 |
| INSTALL_FAILED_ALREADY_EXISTS | `adb uninstall com.your.app` |
| Emulator not detected | Verify `adb devices`, restart ADB |
| HMR not working | Configure `vite.config.ts` with `TAURI_DEV_HOST` |
| Shell plugin URL error | Use `opener` plugin instead (`openUrl()`) |
| Google OAuth fails | Google blocks WebView; use system browser flow |
| Deep link not received | Check scheme in tauri.conf.json, init plugin |
| Safe area CSS fails on Android | `env()` not supported in WebView; use JS fallback |
| Windows APK build symlink error | Enable Developer Mode or copy .so files manually |
| Stale content after rebuild | .so in dev mode embeds old assets; see build-deploy-mobile.md |
| OpenSSL cross-compile fails | Install Strawberry Perl; see build-deploy-mobile.md |

See [references/testing.md](references/testing.md) for detailed troubleshooting.

## Resources

- Docs: https://v2.tauri.app
- Plugins: https://v2.tauri.app/plugin/
- GitHub: https://github.com/tauri-apps/tauri
