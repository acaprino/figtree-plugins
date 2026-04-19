# Browser Extensions Plugin

> Build, debug, publish, and maintain Firefox WebExtensions. Covers Manifest V2 and V3, all 51 browser.* APIs, content scripts, background scripts, native messaging, cross-browser compatibility, AMO publishing, and web-ext CLI -- plus three commands for the full scaffold / lint / publish lifecycle.

## Skills

### `firefox-extension-dev`

Firefox WebExtension development guidance covering the full extension lifecycle.

| | |
|---|---|
| **Invoke** | Skill reference |
| **Trigger** | Firefox extension, WebExtension, browser add-on, manifest.json, content scripts, background scripts, AMO publishing, web-ext CLI, Manifest V3 migration |

**Coverage:**
- Extension anatomy (manifest.json, background scripts, content scripts, popup, sidebar)
- Manifest V2 and V3 with migration guidance
- All 51 browser.* APIs
- Native messaging between extensions and native apps
- Cross-browser compatibility with `webextension-polyfill`
- AMO (addons.mozilla.org) publishing and review process
- web-ext CLI for development, linting, and building

**Key references:**
- MDN WebExtensions docs: [mdn/content](https://github.com/mdn/content/tree/main/files/en-us/mozilla/add-ons/webextensions)
- Official examples: [mdn/webextensions-examples](https://github.com/mdn/webextensions-examples)
- Browser polyfill: [mozilla/webextension-polyfill](https://github.com/mozilla/webextension-polyfill)
- Extension Workshop: [extensionworkshop.com](https://extensionworkshop.com)

---

## Commands

### `/firefox-scaffold`

Scaffold a new Firefox WebExtension with Manifest V3 defaults, web-ext config, AMO-compliant structure, and a working "Hello World" popup.

```
/firefox-scaffold my-extension --mv V3 --content-script
/firefox-scaffold url-shortener --with-agent --options-page
```

| Flag | Effect |
|------|--------|
| `--mv V2\|V3` | Manifest version (default V3) |
| `--sidebar` | Include `sidebar_action` and sidebar template |
| `--content-script` | Include content script template (default: on) |
| `--options-page` | Include options UI template |

Generates: `manifest.json` with MV3 defaults + `browser_specific_settings.gecko.id`, `src/{background,content,popup,options,sidebar}/`, `web-ext-config.js`, `package.json` with web-ext scripts, icons directory, `.gitignore`, README with first-run instructions.

**Safety:** Starts with empty `permissions` / `host_permissions` arrays (AMO reviewers reject over-request). Prompts for extension ID rather than using placeholders.

---

### `/firefox-lint`

Comprehensive pre-publish lint. Runs `web-ext lint` plus static checks for forbidden APIs (eval, remote scripts), permission bloat (all_urls, unused `tabs`), auth anti-patterns (tokens in `localStorage`), and MV3 migration issues.

```
/firefox-lint ./my-extension
/firefox-lint ./my-extension --strict    # treat warnings as blockers (CI)
/firefox-lint ./my-extension --json      # machine-readable output
```

Catches AMO blockers (`eval`, `new Function`, remote script loading, wildcard host_permissions) plus quality issues (over-requested permissions, tokens in localStorage, stale MV2 patterns).

---

### `/firefox-publish`

Publish a signed XPI to AMO (addons.mozilla.org). Runs lint first, bumps version, builds artifact, signs via `web-ext sign`, and walks through the review workflow.

```
/firefox-publish ./my-extension --channel listed --version 1.0.0
/firefox-publish ./my-extension --channel unlisted   # self-distribution, auto-signed
/firefox-publish ./my-extension --dry-run            # skip the sign step
```

| Flag | Effect |
|------|--------|
| `--channel listed` | Public AMO listing, goes through Mozilla review (1-14 days) |
| `--channel unlisted` | Self-distribution, auto-signed immediately |
| `--version <semver>` | Bump to this version (omit to prompt patch/minor/major) |
| `--dry-run` | Build + lint but skip the upload |

**Credentials:** Requires `WEB_EXT_API_KEY` and `WEB_EXT_API_SECRET` from the [AMO API key page](https://addons.mozilla.org/en-US/developers/addon/api/key/). Refuses to proceed if `.env` is not gitignored.

**Post-submission:** For listed channel, links to the developer dashboard and reminds to upload source if the project uses a bundler (webpack / Vite / Rollup / esbuild).

---

**Related:** [typescript-development](typescript-development.md) (TypeScript coding standards for extension code)
