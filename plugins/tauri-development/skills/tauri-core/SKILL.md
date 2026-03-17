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

```
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
```

## Essential Configuration

### tauri.conf.json
```json
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "MyApp",
  "identifier": "com.company.myapp",
  "build": {
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist"
  }
}
```

### capabilities/default.json
```json
{
  "identifier": "default",
  "windows": ["main"],
  "permissions": ["core:default"]
}
```

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
