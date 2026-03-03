---
name: firefox-extension-dev
description: "Expert Firefox extension (WebExtension) developer. Use when building, debugging, publishing, or porting browser extensions for Firefox. Triggers on: Firefox extension, WebExtension, browser add-on, manifest.json for extensions, content scripts, background scripts, browser.tabs, browser.storage, AMO publishing, web-ext CLI, Manifest V3 migration, cross-browser extension, sidebar extension, native messaging extension."
---

# Firefox Extension Development Expert

Build, debug, publish, and maintain Firefox WebExtensions. Covers Manifest V2 and V3, all 51 browser.* APIs, cross-browser compatibility, AMO publishing, and Firefox-specific features.

## Documentation Source

All knowledge sourced from MDN WebExtensions documentation.

**Keep updated from:** `https://github.com/mdn/content/tree/main/files/en-us/mozilla/add-ons/webextensions`

**Key GitHub repos:**
- MDN docs source: [mdn/content](https://github.com/mdn/content/tree/main/files/en-us/mozilla/add-ons/webextensions)
- Official examples: [mdn/webextensions-examples](https://github.com/mdn/webextensions-examples)
- Browser API polyfill: [mozilla/webextension-polyfill](https://github.com/mozilla/webextension-polyfill)
- web-ext CLI: [mozilla/web-ext](https://github.com/mozilla/web-ext)
- Extension Workshop: [extensionworkshop.com](https://extensionworkshop.com)

---

## Extension Anatomy

Every extension is a collection of files packaged as a `.zip`. The only mandatory file is `manifest.json`.

### File Structure

```
my-extension/
  manifest.json              # REQUIRED — metadata + pointers
  background.js              # event handling, extension lifecycle
  content-scripts/
    content.js               # injected into web pages
    styles.css               # injected styles
  popup/
    popup.html               # toolbar button popup
    popup.js
    popup.css
  sidebar/
    sidebar.html             # sidebar panel (Firefox-only)
    sidebar.js
  options/
    options.html             # settings page
    options.js
  icons/
    icon-48.png
    icon-96.png
  _locales/                  # i18n strings
    en/messages.json
  web-accessible-resources/  # files accessible to page scripts
```

### Component Types

| Component | Purpose | API Access |
|---|---|---|
| Background scripts | Browser event handling, extension lifecycle | Full (all permitted APIs) |
| Content scripts | DOM manipulation in web pages | Limited subset + messaging |
| Popup | Toolbar button UI (HTML) | Full (same as background) |
| Sidebar | Side panel UI (Firefox-only) | Full (same as background) |
| Options page | User preferences UI | Full (same as background) |
| Extension pages | Custom HTML loaded via `tabs.create`/`windows.create` | Full (same as background) |
| DevTools page | Developer tools panel | Full + devtools APIs |

---

## manifest.json Reference

### Required Keys

Only 3 keys are mandatory:

```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0"
}
```

### Complete Key Reference

| Key | MV2 | MV3 | Notes |
|---|---|---|---|
| `manifest_version` | 2 | 3 | Required |
| `name` | Y | Y | Required |
| `version` | Y | Y | Required. Format: numbers separated by up to 3 dots, max 9 digits each |
| `action` | — | Y | Toolbar button (replaces `browser_action`) |
| `author` | Y | Y | |
| `background` | Y | Y | MV2: `scripts`+`persistent`. MV3: `scripts` (event page in Firefox, service_worker in Chrome) |
| `browser_action` | Y | — | MV2 only, use `action` in MV3 |
| `browser_specific_settings` | Y | Y | Firefox-only. Set gecko ID and min version |
| `chrome_settings_overrides` | Y | Y | Override default search, homepage |
| `chrome_url_overrides` | Y | Y | Override new tab, bookmarks, history pages |
| `commands` | Y | Y | Keyboard shortcuts |
| `content_scripts` | Y | Y | Declarative content script injection |
| `content_security_policy` | Y | Y | MV2: string. MV3: `{ "extension_pages": "..." }` |
| `declarative_net_request` | Y | Y | Declarative network request rules |
| `default_locale` | Y | Y | Required if `_locales/` exists |
| `description` | Y | Y | |
| `developer` | Y | Y | |
| `devtools_page` | Y | Y | |
| `dictionaries` | Y | Y | |
| `homepage_url` | Y | Y | |
| `host_permissions` | — | Y | MV3 only. Separated from `permissions` |
| `icons` | Y | Y | Sizes: 16, 32, 48, 96, 128 |
| `incognito` | Y | Y | |
| `omnibox` | Y | Y | |
| `optional_host_permissions` | — | Y | MV3 only |
| `optional_permissions` | Y | Y | |
| `options_page` | Y | Y | |
| `options_ui` | Y | Y | |
| `page_action` | Y | — | Retained in Firefox MV3 but MV2-only in Chrome |
| `permissions` | Y | Y | |
| `protocol_handlers` | Y | Y | Firefox-only |
| `short_name` | Y | Y | |
| `sidebar_action` | Y | Y | Firefox-only |
| `storage` | Y | Y | Managed storage schema (Firefox unsupported) |
| `theme` | Y | Y | |
| `theme_experiment` | Y | Y | Firefox-only, experimental |
| `user_scripts` | Y | — | MV2 only |
| `version_name` | Y | Y | |
| `web_accessible_resources` | Y | Y | MV2: string array. MV3: object array with `resources`+`matches`+`extension_ids` |

### Manifest V3 Example (Firefox)

```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0",
  "description": "A Firefox extension",
  "browser_specific_settings": {
    "gecko": {
      "id": "my-extension@example.org",
      "strict_min_version": "109.0"
    }
  },
  "permissions": [
    "storage",
    "alarms"
  ],
  "host_permissions": [
    "*://*.example.com/*"
  ],
  "optional_permissions": [
    "tabs",
    "history"
  ],
  "optional_host_permissions": [
    "https://*.other-site.com/*"
  ],
  "background": {
    "scripts": ["background.js"]
  },
  "action": {
    "default_icon": {
      "16": "icons/icon-16.png",
      "32": "icons/icon-32.png"
    },
    "default_title": "My Extension",
    "default_popup": "popup/popup.html"
  },
  "content_scripts": [{
    "matches": ["*://*.example.com/*"],
    "js": ["content-scripts/content.js"],
    "css": ["content-scripts/styles.css"],
    "run_at": "document_idle"
  }],
  "icons": {
    "48": "icons/icon-48.png",
    "96": "icons/icon-96.png"
  },
  "options_ui": {
    "page": "options/options.html"
  },
  "web_accessible_resources": [{
    "resources": ["images/*"],
    "matches": ["*://*.example.com/*"]
  }],
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'"
  }
}
```

### Manifest V2 Example (Firefox)

```json
{
  "manifest_version": 2,
  "name": "My Extension",
  "version": "1.0",
  "description": "A Firefox extension",
  "browser_specific_settings": {
    "gecko": {
      "id": "my-extension@example.org",
      "strict_min_version": "57.0"
    }
  },
  "permissions": [
    "storage",
    "tabs",
    "*://*.example.com/*"
  ],
  "background": {
    "scripts": ["background.js"],
    "persistent": false
  },
  "browser_action": {
    "default_icon": {
      "19": "icons/icon-19.png",
      "38": "icons/icon-38.png"
    },
    "default_title": "My Extension",
    "default_popup": "popup/popup.html"
  },
  "content_scripts": [{
    "matches": ["*://*.example.com/*"],
    "js": ["content-scripts/content.js"],
    "run_at": "document_idle"
  }],
  "icons": {
    "48": "icons/icon-48.png",
    "96": "icons/icon-96.png"
  },
  "web_accessible_resources": ["images/*"]
}
```

### Access Manifest at Runtime

```javascript
const manifest = browser.runtime.getManifest();
console.log(manifest.version);
```

---

## WebExtension JavaScript APIs (Complete List)

All APIs accessed via `browser.*` namespace. Firefox returns Promises for all async methods.

### API Reference Table

| API | Description | Permission |
|---|---|---|
| `action` | Toolbar button (MV3) | manifest `action` key |
| `alarms` | Scheduled events | `alarms` |
| `bookmarks` | Bookmark management | `bookmarks` |
| `browserAction` | Toolbar button (MV2) | manifest `browser_action` key |
| `browserSettings` | Global browser settings (Firefox-only) | `browserSettings` |
| `browsingData` | Clear browsing data | `browsingData` |
| `captivePortal` | Detect captive portal (Firefox-only) | `captivePortal` |
| `clipboard` | System clipboard | `clipboardWrite` |
| `commands` | Keyboard shortcuts | manifest `commands` key |
| `contentScripts` | Register content scripts (MV2) | host permissions |
| `contextualIdentities` | Container tabs (Firefox-only) | `contextualIdentities` + `cookies` |
| `cookies` | Cookie management | `cookies` + host permissions |
| `declarativeNetRequest` | Declarative network filtering | `declarativeNetRequest` |
| `devtools` | DevTools integration | manifest `devtools_page` key |
| `dns` | DNS resolution (Firefox-only) | `dns` |
| `dom` | Extension-only DOM features | none |
| `downloads` | Download management | `downloads` |
| `events` | Common event types | none (utility) |
| `extension` | Extension utilities | none |
| `extensionTypes` | Shared type definitions | none (utility) |
| `find` | Find text in pages (Firefox-only) | `find` |
| `history` | Browser history | `history` |
| `i18n` | Internationalization | none |
| `identity` | OAuth2 authentication | `identity` |
| `idle` | System idle detection | `idle` |
| `management` | Add-on management | `management` |
| `menus` | Context menu (Firefox name) | `menus` |
| `notifications` | OS notifications | `notifications` |
| `omnibox` | Address bar suggestions | manifest `omnibox` key |
| `pageAction` | Address bar button | manifest `page_action` key |
| `permissions` | Runtime permissions | none |
| `pkcs11` | Security modules (Firefox-only) | `pkcs11` |
| `privacy` | Privacy settings | `privacy` |
| `proxy` | Proxy management | `proxy` + host permissions |
| `runtime` | Extension lifecycle + messaging | none |
| `scripting` | Inject JS/CSS (MV3) | `scripting` + host permissions |
| `search` | Search engine management | `search` |
| `sessions` | Restore closed tabs/windows | `sessions` |
| `sidebarAction` | Sidebar panel (Firefox-only) | manifest `sidebar_action` key |
| `storage` | Key-value storage | `storage` |
| `tabGroups` | Tab group management | `tabGroups` |
| `tabs` | Tab management | `tabs` (for URL/title) |
| `theme` | Theme management | `theme` |
| `topSites` | Frequently visited sites | `topSites` |
| `types` | BrowserSetting type | none (utility) |
| `userScripts` | Register user scripts | `userScripts` |
| `webNavigation` | Navigation events | `webNavigation` |
| `webRequest` | HTTP request interception | `webRequest` (+ `webRequestBlocking` for blocking) |
| `windows` | Window management | none |

### Key API Details

#### browser.tabs

**Methods:** `query()`, `create()`, `update()`, `remove()`, `get()`, `duplicate()`, `move()`, `reload()`, `sendMessage()`, `connect()`, `captureVisibleTab()`, `goBack()`, `goForward()`, `print()`, `saveAsPDF()`, `toggleReaderMode()`, `discard()`, `group()`, `ungroup()`, `warmup()`, `highlight()`

**Events:** `onActivated`, `onCreated`, `onRemoved`, `onUpdated`, `onMoved`, `onAttached`, `onDetached`, `onHighlighted`, `onZoomChange`, `onReplaced`

**MV2-only methods (use `browser.scripting` in MV3):** `executeScript()`, `insertCSS()`, `removeCSS()`

```javascript
// Query active tab
const [tab] = await browser.tabs.query({ active: true, currentWindow: true });

// Create tab
await browser.tabs.create({ url: "https://example.com" });

// Send message to content script
await browser.tabs.sendMessage(tabId, { type: "doSomething" });

// Capture visible tab screenshot
const dataUrl = await browser.tabs.captureVisibleTab(null, { format: "png" });
```

#### browser.storage

**Four storage areas:**
- `storage.local` — 10 MB limit, persists on disk
- `storage.sync` — 100 KB limit, synced across devices
- `storage.managed` — read-only, set by domain admin
- `storage.session` — 10 MB limit, in-memory only, lost on restart

**Methods (all areas):** `get()`, `set()`, `remove()`, `clear()`, `getBytesInUse()`

**Event:** `storage.onChanged`

```javascript
// Set data
await browser.storage.local.set({ settings: { theme: "dark", fontSize: 14 } });

// Get data with defaults
const { settings } = await browser.storage.local.get({ settings: { theme: "light" } });

// Listen for changes
browser.storage.onChanged.addListener((changes, areaName) => {
  for (const [key, { oldValue, newValue }] of Object.entries(changes)) {
    console.log(`${areaName}.${key}: ${oldValue} -> ${newValue}`);
  }
});

// IMPORTANT: Never use window.localStorage — Firefox clears it during privacy cleanup
```

#### browser.runtime

**Properties:** `id`, `lastError`

**Methods:** `sendMessage()`, `connect()`, `sendNativeMessage()`, `connectNative()`, `getManifest()`, `getURL()`, `getPlatformInfo()`, `getBrowserInfo()`, `getBackgroundPage()`, `openOptionsPage()`, `reload()`, `setUninstallURL()`, `getContexts()`, `getFrameId()`

**Lifecycle events:** `onInstalled`, `onStartup`, `onSuspend`, `onSuspendCanceled`, `onUpdateAvailable`

**Messaging events:** `onMessage`, `onMessageExternal`, `onConnect`, `onConnectExternal`, `onUserScriptMessage`, `onUserScriptConnect`

```javascript
// Check install/update reason
browser.runtime.onInstalled.addListener(({ reason }) => {
  if (reason === "install") initializeDefaults();
  if (reason === "update") migrateData();
});

// Get extension URL
const url = browser.runtime.getURL("popup/popup.html");

// Set uninstall URL (feedback page)
browser.runtime.setUninstallURL("https://example.com/uninstall-survey");
```

#### browser.declarativeNetRequest

**Rule structure:**

```javascript
{
  id: 1,
  priority: 1,
  condition: {
    urlFilter: "*://ads.example.com/*",
    resourceTypes: ["script", "image"]
  },
  action: { type: "block" }
}
```

**Action types:** `block`, `redirect`, `allow`, `allowAllRequests`, `upgradeScheme`, `modifyHeaders`

**Rule sources:** static (manifest-defined), dynamic (persists across sessions), session (memory-only)

**Firefox advantage:** Supports both `declarativeNetRequest` AND blocking `webRequest` simultaneously.

---

## Content Scripts

### Loading Methods

**1. Declarative (manifest.json):**

```json
{
  "content_scripts": [{
    "matches": ["*://*.example.com/*"],
    "exclude_matches": ["*://admin.example.com/*"],
    "js": ["jquery.js", "content.js"],
    "css": ["styles.css"],
    "run_at": "document_idle",
    "all_frames": false,
    "match_about_blank": false
  }]
}
```

`run_at` values:
- `document_start` — before DOM construction
- `document_end` — DOM ready, before subresources
- `document_idle` — default, after page load

**2. Programmatic (MV3 scripting API):**

```javascript
// One-time injection
await browser.scripting.executeScript({
  target: { tabId },
  files: ["content.js"]
});

// CSS injection
await browser.scripting.insertCSS({
  target: { tabId },
  files: ["styles.css"]
});

// Persistent registration
await browser.scripting.registerContentScripts([{
  id: "my-script",
  matches: ["*://*.example.com/*"],
  js: ["content.js"],
  persistAcrossSessions: true
}]);
```

**3. MV2 programmatic:**

```javascript
await browser.tabs.executeScript(tabId, { file: "content.js" });
await browser.tabs.insertCSS(tabId, { file: "styles.css" });
```

### Content Script Environment

- **DOM access:** Full access to page DOM via standard Web APIs
- **JS isolation:** Cannot see page-defined JS variables (Xray vision in Firefox, isolated world in Chrome)
- **API access:** Limited subset only

**Available APIs in content scripts:**
- `extension.getURL()`, `extension.inIncognitoContext`
- `runtime.connect()`, `runtime.getManifest()`, `runtime.getURL()`, `runtime.onConnect`, `runtime.onMessage`, `runtime.sendMessage()`
- `i18n.getMessage()`, `i18n.getAcceptLanguages()`, `i18n.getUILanguage()`, `i18n.detectLanguage()`
- `menus.getTargetElement`
- `storage.*` (all methods)

### Content Script Isolation Example

```javascript
// content-script.js
// CAN access page DOM
const heading = document.querySelector("h1");
heading.style.color = "red";

// CANNOT access page JS variables
console.log(window.pageVariable); // undefined

// window.confirm() calls ORIGINAL, not page-redefined version
window.confirm("Are you sure?"); // original browser dialog
```

### Using Libraries in Content Scripts

Bundle and inject alongside your content script:

```json
"content_scripts": [{
  "matches": ["*://*.example.com/*"],
  "js": ["lib/jquery.min.js", "content.js"]
}]
```

### Restricted Domains (Firefox)

Content scripts cannot run on these Mozilla domains:
- `accounts-static.cdn.mozilla.net`, `accounts.firefox.com`
- `addons.cdn.mozilla.net`, `addons.mozilla.org`
- `api.accounts.firefox.com`, `content.cdn.mozilla.net`
- `discovery.addons.mozilla.org`, `install.mozilla.org`
- `oauth.accounts.firefox.com`, `profile.accounts.firefox.com`
- `support.mozilla.org`, `sync.services.mozilla.com`

---

## Background Scripts

### MV3 Event Page (Firefox)

Firefox MV3 uses **event pages** (non-persistent background pages with DOM access), NOT service workers like Chrome.

```json
{
  "background": {
    "scripts": ["background.js"]
  }
}
```

**Critical rules for event pages:**

1. **Register listeners at top level synchronously** — deferred registration breaks wake-up

```javascript
// CORRECT
browser.runtime.onMessage.addListener((msg) => { /* handle */ });
browser.menus.create({ id: "myMenu", title: "Menu", contexts: ["selection"] });

// WRONG — will not wake the event page
window.onload = () => {
  browser.runtime.onMessage.addListener(() => { /* broken */ });
};
```

2. **Persist state via storage, not globals**

```javascript
// Use storage.session for ephemeral state
browser.runtime.onMessage.addListener(async (msg) => {
  if (msg === "increment") {
    let { count } = await browser.storage.session.get({ count: 0 });
    count++;
    await browser.storage.session.set({ count });
    return count;
  }
});
```

3. **Use alarms instead of setTimeout/setInterval**

```javascript
browser.alarms.create("periodicCheck", { periodInMinutes: 5 });
browser.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === "periodicCheck") {
    doPeriodicWork();
  }
});
```

4. **`runtime.onSuspend` fires before unload** — use for cleanup

### MV2 Background Script

```json
{
  "background": {
    "scripts": ["background.js"],
    "persistent": false
  }
}
```

Set `"persistent": true` only if needed (e.g., `webRequest` blocking in MV2). Non-persistent is recommended.

---

## Message Passing

### One-Off Messages

**Content script → Background:**

```javascript
// content-script.js
browser.runtime.sendMessage({ type: "getData", key: "user" })
  .then(response => console.log(response));

// background.js
browser.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type === "getData") {
    return browser.storage.local.get(message.key); // return Promise
  }
});
```

**Background → Content script:**

```javascript
// background.js
await browser.tabs.sendMessage(tabId, { type: "update", data: newData });

// content-script.js
browser.runtime.onMessage.addListener((message) => {
  if (message.type === "update") {
    updateUI(message.data);
  }
});
```

### Port Connections (Long-Lived)

```javascript
// content-script.js
const port = browser.runtime.connect({ name: "data-stream" });
port.postMessage({ greeting: "hello" });
port.onMessage.addListener((msg) => { /* handle */ });
port.onDisconnect.addListener(() => { /* cleanup */ });

// background.js
browser.runtime.onConnect.addListener((port) => {
  if (port.name === "data-stream") {
    port.onMessage.addListener((msg) => {
      port.postMessage({ reply: "received" });
    });
  }
});
```

### Cross-Extension Messaging

```javascript
// Send to another extension
browser.runtime.sendMessage("other-extension@example", { data: "shared" });

// Receive from another extension
browser.runtime.onMessageExternal.addListener((message, sender) => {
  if (sender.id === "trusted-extension@example") { /* handle */ }
});
```

### Content Script ↔ Page Script (window.postMessage)

```javascript
// page-script.js
window.postMessage({ direction: "from-page", message: "hello" }, "*");

// content-script.js
window.addEventListener("message", (event) => {
  if (event.source === window && event?.data?.direction === "from-page") {
    // SECURITY: validate all data from page scripts
    // NEVER use eval() with untrusted data
    console.log(event.data.message);
  }
});
```

**Security warning:** Never `eval()` data received from page scripts. Extensions are privileged code — hostile pages can exploit this.

---

## Match Patterns

**Syntax:** `<scheme>://<host><path>`

**Special value:** `<all_urls>` — matches all supported scheme URLs

### Scheme

- `*` — matches `http`, `https`, `ws`, `wss`
- Explicit: `http`, `https`, `ws`, `wss`, `ftp`, `data`, `file`

### Host

- `*` — any host
- `*.example.com` — example.com and all subdomains
- `example.com` — exact host only

### Path

- Must start with `/`
- `*` wildcard anywhere in path
- Matches URL path + query string (ignores fragments)

### Examples

| Pattern | Matches |
|---|---|
| `<all_urls>` | All URLs with supported schemes |
| `*://*/*` | All HTTP/HTTPS/WS URLs |
| `*://*.mozilla.org/*` | mozilla.org + subdomains |
| `https://mozilla.org/` | Exact host, HTTPS only |
| `https://*/path` | Any HTTPS host with /path |
| `file:///home/*` | Local files under /home/ |

### Invalid Patterns

- `resource://path/` — unsupported scheme
- `https://mozilla.org` — missing path (need trailing `/`)
- `https://mozilla.*.org/` — wildcard not at start
- `https://*zilla.org/` — wildcard not standalone or before dot

---

## Permissions

### Install-Time Permissions

Declared in `permissions` (MV2/MV3) and `host_permissions` (MV3 only):

```json
{
  "permissions": ["storage", "alarms", "tabs"],
  "host_permissions": ["*://*.example.com/*"]
}
```

### Optional Permissions

Must be requested at runtime from a user action handler:

```json
{
  "optional_permissions": ["tabs", "history"],
  "optional_host_permissions": ["https://*.other-site.com/*"]
}
```

```javascript
document.getElementById("enableFeature").addEventListener("click", async () => {
  const granted = await browser.permissions.request({
    permissions: ["tabs"],
    origins: ["https://*.other-site.com/*"]
  });
  if (granted) enableAdvancedFeature();
});

// Listen for changes (users can revoke in Add-ons Manager since Firefox 84)
browser.permissions.onAdded.addListener((perms) => enableFeatures(perms));
browser.permissions.onRemoved.addListener((perms) => disableFeatures(perms));
```

### Common Permission List

| Permission | Grants |
|---|---|
| `activeTab` | Temporary access to active tab on user action |
| `alarms` | `browser.alarms` API |
| `bookmarks` | `browser.bookmarks` API |
| `browserSettings` | `browser.browserSettings` API (Firefox-only) |
| `browsingData` | `browser.browsingData` API |
| `clipboardRead` | Read clipboard |
| `clipboardWrite` | Write clipboard |
| `contextualIdentities` | `browser.contextualIdentities` API (Firefox-only) |
| `cookies` | `browser.cookies` API |
| `declarativeNetRequest` | `browser.declarativeNetRequest` API |
| `dns` | `browser.dns` API (Firefox-only) |
| `downloads` | `browser.downloads` API |
| `find` | `browser.find` API (Firefox-only) |
| `geolocation` | Geolocation API |
| `history` | `browser.history` API |
| `identity` | `browser.identity` API |
| `idle` | `browser.idle` API |
| `management` | `browser.management` API |
| `menus` | `browser.menus` API |
| `nativeMessaging` | `browser.runtime.connectNative()`/`sendNativeMessage()` |
| `notifications` | `browser.notifications` API |
| `pkcs11` | `browser.pkcs11` API (Firefox-only) |
| `privacy` | `browser.privacy` API |
| `proxy` | `browser.proxy` API |
| `scripting` | `browser.scripting` API |
| `search` | `browser.search` API |
| `sessions` | `browser.sessions` API |
| `storage` | `browser.storage` API |
| `tabGroups` | `browser.tabGroups` API |
| `tabHide` | `browser.tabs.hide()`/`show()` (Firefox-only, experimental) |
| `tabs` | Access `url`, `title`, `favIconUrl` on Tab objects |
| `theme` | `browser.theme` API |
| `topSites` | `browser.topSites` API |
| `unlimitedStorage` | Unlimited `storage.local` |
| `userScripts` | `browser.userScripts` API (MV3: optional-only) |
| `webNavigation` | `browser.webNavigation` API |
| `webRequest` | `browser.webRequest` API |
| `webRequestBlocking` | Blocking `webRequest` (Firefox keeps this in MV3) |
| `webRequestFilterResponse` | Filter response bodies (Firefox-only) |

---

## Native Messaging

Enables communication between extension and native applications.

### Extension Setup

```json
{
  "permissions": ["nativeMessaging"],
  "browser_specific_settings": {
    "gecko": {
      "id": "my-extension@example.org"
    }
  }
}
```

### Native App Manifest

Create a JSON manifest for the native app:

```json
{
  "name": "my_native_app",
  "description": "My native messaging app",
  "path": "/path/to/native-app",
  "type": "stdio",
  "allowed_extensions": ["my-extension@example.org"]
}
```

**Chrome difference:** Uses `"allowed_origins"` instead of `"allowed_extensions"`.

### Windows Registry Setup

Registry key at:
- `HKEY_CURRENT_USER\Software\Mozilla\NativeMessagingHosts\my_native_app`
- Default value: path to the JSON manifest

### Message Wire Protocol

Messages are JSON, UTF-8 encoded, preceded by a 32-bit unsigned native-byte-order length prefix.

**Limits:** Max 1 MB from app, max 4 GB to app.

### Connection-Based Messaging

```javascript
const port = browser.runtime.connectNative("my_native_app");

port.onMessage.addListener((response) => {
  console.log(`Received: ${JSON.stringify(response)}`);
});

port.postMessage({ action: "getData" });
```

### Connectionless Messaging

```javascript
const response = await browser.runtime.sendNativeMessage("my_native_app", "ping");
console.log(response); // "pong"
```

### Python Native App (Python 3)

```python
#!/usr/bin/env -S python3 -u
import sys, json, struct

def get_message():
    raw_length = sys.stdin.buffer.read(4)
    if len(raw_length) == 0:
        sys.exit(0)
    message_length = struct.unpack('@I', raw_length)[0]
    message = sys.stdin.buffer.read(message_length).decode('utf-8')
    return json.loads(message)

def send_message(content):
    encoded = json.dumps(content, separators=(',', ':')).encode('utf-8')
    sys.stdout.buffer.write(struct.pack('@I', len(encoded)))
    sys.stdout.buffer.write(encoded)
    sys.stdout.buffer.flush()

while True:
    msg = get_message()
    if msg == "ping":
        send_message("pong")
```

---

## Firefox-Specific Features

### Container Tabs (contextualIdentities)

Firefox-exclusive. Manage isolated container tabs with separate cookie stores.

**Permission:** `contextualIdentities` + `cookies`

```javascript
// Create container
const container = await browser.contextualIdentities.create({
  name: "Work",
  color: "blue",
  icon: "briefcase"
});

// Open tab in container
await browser.tabs.create({
  url: "https://example.com",
  cookieStoreId: container.cookieStoreId
});

// List containers
const containers = await browser.contextualIdentities.query({});
```

### Sidebar (sidebarAction)

Firefox-exclusive sidebar panel API.

```json
{
  "sidebar_action": {
    "default_title": "My Sidebar",
    "default_panel": "sidebar/panel.html",
    "default_icon": "icons/sidebar.png"
  }
}
```

```javascript
await browser.sidebarAction.open();
await browser.sidebarAction.close();
const isOpen = await browser.sidebarAction.isOpen({});
await browser.sidebarAction.setPanel({ panel: "sidebar/alt-panel.html" });
```

**Chrome equivalent:** `side_panel` manifest key + `sidePanel` API (not directly compatible).

### Protocol Handlers

Firefox-exclusive. Register extension as handler for URI protocols.

```json
{
  "protocol_handlers": [{
    "protocol": "mailto",
    "name": "My Mail Handler",
    "uriTemplate": "https://mail.example.com/compose?to=%s"
  }]
}
```

**Custom protocols:** Use `ext+customname` or `web+customname` format.

### userScripts API (MV3)

Register third-party user scripts with isolated execution worlds.

```javascript
// Configure world
await browser.userScripts.configureWorld({ messaging: true });

// Register
await browser.userScripts.register([{
  id: "my-userscript",
  matches: ["https://example.com/*"],
  js: [{ code: 'browser.runtime.sendMessage({ data: document.title });' }],
  world: "USER_SCRIPT"
}]);

// Listen
browser.runtime.onUserScriptMessage.addListener((msg, sender) => {
  console.log(msg.data);
});
```

**Firefox MV3:** `userScripts` must be in `optional_permissions` and requested at runtime.

### Other Firefox-Exclusive APIs

| API | Description |
|---|---|
| `browser.dns` | Resolve domain names |
| `browser.pkcs11` | PKCS#11 security module access |
| `browser.find` | Find and highlight text in pages |
| `browser.captivePortal` | Detect captive portal state |
| `browser.tabs.hide()`/`show()` | Hide/show tabs (experimental) |
| `browser.tabs.saveAsPDF()` | Save page as PDF |
| `browser.tabs.print()` | Print tab contents |
| `browser.tabs.toggleReaderMode()` | Toggle Reader View |
| `browser.browserSettings` | Modify global browser settings |

### Firefox Keeps webRequest Blocking in MV3

The most significant policy difference from Chrome: Firefox MV3 retains `webRequest.onBeforeRequest` with blocking capability alongside `declarativeNetRequest`. Content blockers like uBlock Origin continue to work at full power.

---

## Manifest V3 Migration

### Firefox MV3 vs Chrome MV3

| Feature | Firefox MV3 | Chrome MV3 |
|---|---|---|
| Background | Event pages (DOM access) | Service workers (no DOM) |
| webRequest blocking | Fully supported + DNR | Removed; DNR only |
| host_permissions | Treated as optional (user-grantable) | Granted at install |
| Page Action | Retained | Merged into Action |
| MV2 support | Indefinite | Disabled (July 2025) |
| Data cloning | Structured clone algorithm | JSON serialization |

### Migration Checklist (MV2 → MV3)

1. Set `"manifest_version": 3`
2. Move host permissions from `permissions` to `host_permissions` / `optional_host_permissions`
3. Rename `browser_action` → `action`, `_execute_browser_action` → `_execute_action`
4. Remove `browser_style` from all manifest keys
5. Replace `tabs.executeScript`/`insertCSS`/`removeCSS` → `browser.scripting` API
6. Convert background to non-persistent: set `"persistent": false` or omit
7. Move all event listeners to top-level synchronous registration
8. Replace global state variables → `storage.session`/`storage.local`
9. Replace `setTimeout`/`setInterval` → `browser.alarms`
10. Update CSP format: `"content_security_policy": { "extension_pages": "..." }`
11. Update `web_accessible_resources` → object array format with `resources`+`matches`+`extension_ids`
12. Remove all `eval()` usage (forbidden in MV3)
13. Move inline scripts to separate files
14. Ensure version string format: numbers separated by up to 3 dots, max 9 digits each

---

## Cross-Browser Compatibility

### Namespace

- Firefox: `browser.*` (Promises) + `chrome.*` (callbacks)
- Chrome: `chrome.*` (MV2: callbacks, MV3: Promises from Chrome 121+)
- Safari: `browser.*` (Promises)

### WebExtension Browser API Polyfill

**Repo:** [mozilla/webextension-polyfill](https://github.com/mozilla/webextension-polyfill)

```bash
npm install webextension-polyfill
```

```json
{
  "background": { "scripts": ["browser-polyfill.js", "background.js"] },
  "content_scripts": [{
    "matches": ["*://*/*"],
    "js": ["browser-polyfill.js", "content.js"]
  }]
}
```

### Key Incompatibilities

| Area | Firefox | Chrome |
|---|---|---|
| `web_accessible_resources` URLs | Random UUID per install (`moz-extension://«UUID»/`) | Fixed extension ID (`chrome-extension://«ID»/`) |
| `eval()` in content scripts | `window.eval()` runs in page context | `window.eval()` runs in content script context |
| Background `alert()`/`confirm()` | Not supported | Supported |
| Injected CSS relative URLs | Resolved relative to CSS file | Resolved relative to page |
| Content script XHR URLs (MV2) | Must be absolute | Can be relative (resolved to page) |
| Message data cloning | Structured clone (supports more types) | JSON serialization |
| `tabs.remove()` | Waits for `beforeunload` | Does not wait |
| Proxy API | `proxy.onRequest` | `proxy.ProxyConfig` |
| Sidebar | `sidebar_action` + `sidebarAction` | `side_panel` + `sidePanel` |

### Cross-Browser Development Strategy

1. Code for Firefox first using `browser.*` + Promises
2. Apply webextension-polyfill for Chrome/Edge/Opera
3. Use runtime feature detection for platform-specific APIs
4. Create separate `manifest.json` per browser
5. Test on all target browsers before submission

```javascript
// Feature detection
if (typeof browser.sidebarAction !== "undefined") {
  // Firefox sidebar
}
if (typeof browser.contextualIdentities !== "undefined") {
  // Firefox containers
}
```

---

## Development Workflow

### web-ext CLI

**Install:**

```bash
npm install --global web-ext
```

**Key Commands:**

```bash
# Run with auto-reload
web-ext run --firefox nightly --browser-console --start-url https://example.com

# Run targeting specific Firefox
web-ext run --firefox /path/to/firefox

# Run on Android
web-ext run --target firefox-android --adb-device <device-id>

# Lint
web-ext lint

# Build
web-ext build --overwrite-dest

# Sign for self-distribution
web-ext sign --channel unlisted --api-key $WEB_EXT_API_KEY --api-secret $WEB_EXT_API_SECRET

# Sign for AMO listing
web-ext sign --channel listed --amo-metadata amo-metadata.json
```

**Configuration file (`.web-extrc` or `web-ext-config.js`):**

```json
{
  "sourceDir": "./src",
  "artifactsDir": "./dist",
  "run": {
    "firefox": "nightly",
    "startUrl": ["https://example.com"],
    "browserConsole": true
  },
  "build": {
    "overwriteDest": true
  }
}
```

**Environment variables:** All options support `$WEB_EXT_` prefix (e.g., `$WEB_EXT_API_KEY`).

### Loading Temporarily (Without web-ext)

1. Open Firefox → `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on..."
3. Select `manifest.json` from extension directory
4. Extension loads until Firefox closes

### Debugging

- **Browser Console:** `Ctrl+Shift+J` — see background script logs
- **Extension Debugger:** `about:debugging` → Inspect on extension
- **Content Script Console:** Regular page DevTools console (select extension context)
- **Extension Storage:** `about:debugging` → Inspect → Storage tab

---

## Publishing to AMO

### Distribution Channels

| Channel | Review | Signing | Auto-Updates |
|---|---|---|---|
| AMO Listed | Auto + manual post-pub | AMO signs | AMO handles |
| Self-distributed (unlisted) | Auto only | AMO signs | Extension manages via `update_url` |

### Publishing Process

1. Package: `web-ext build`
2. Submit to [addons.mozilla.org](https://addons.mozilla.org)
3. Automated review runs in seconds
4. Manual review follows post-publication
5. Each version must have a unique version number (no reverting)

### Review Policies

**Requirements:**
- No remote code execution — bundle all code locally
- No `eval()` — forbidden in MV3, dangerous in MV2
- Minimal permissions — request only what's needed
- Transparent functionality — no surprises
- Data disclosure — all collection/transmission must be disclosed
- Third-party libraries — must be unmodified and documented
- Submit source code for minified/transpiled builds (`--upload-source-code`)

**Rejection triggers:**
- Modified third-party libraries
- Remote script loading
- Overly broad permissions without justification
- Missing source code for obfuscated builds

### Security Best Practices

- **Never load remote scripts** — bundle everything locally
- **Use safe DOM methods** — `createElement()`, `setAttribute()`, `textContent`
- **Sanitize HTML** — use DOMPurify 2.0.7+ for any HTML insertion
- **Use CSP defaults** — don't relax Content Security Policy
- **Lint with `eslint-plugin-no-unsanitized`**
- **Keep libraries updated** — outdated CVEs may trigger AMO blocking
- **Prevent fingerprinting** — don't expose `moz-extension://{UUID}` to pages
- **Use REST APIs for analytics** — don't embed tracking JS

---

## Common Patterns

### Toolbar Button with Popup

```json
{
  "action": {
    "default_icon": { "16": "icons/16.png", "32": "icons/32.png" },
    "default_title": "Click me",
    "default_popup": "popup/popup.html"
  }
}
```

```html
<!-- popup/popup.html -->
<!DOCTYPE html>
<html>
<head><link rel="stylesheet" href="popup.css"></head>
<body>
  <button id="action">Do Something</button>
  <script src="popup.js"></script>
</body>
</html>
```

```javascript
// popup/popup.js
document.getElementById("action").addEventListener("click", async () => {
  const [tab] = await browser.tabs.query({ active: true, currentWindow: true });
  await browser.tabs.sendMessage(tab.id, { type: "doAction" });
  window.close();
});
```

### Context Menu

```javascript
// background.js
browser.runtime.onInstalled.addListener(() => {
  browser.menus.create({
    id: "search-selection",
    title: "Search for '%s'",
    contexts: ["selection"]
  });
});

browser.menus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "search-selection") {
    browser.tabs.create({
      url: `https://example.com/search?q=${encodeURIComponent(info.selectionText)}`
    });
  }
});
```

### Page Modification (Content Script)

```javascript
// content.js
function modifyPage() {
  document.querySelectorAll("img").forEach(img => {
    img.style.border = "3px solid red";
  });
}

// Run when DOM is ready
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", modifyPage);
} else {
  modifyPage();
}
```

### Options Page with Storage

```json
{
  "options_ui": {
    "page": "options/options.html",
    "open_in_tab": false
  }
}
```

```javascript
// options/options.js
async function saveOptions() {
  const theme = document.getElementById("theme").value;
  await browser.storage.sync.set({ theme });
}

async function loadOptions() {
  const { theme } = await browser.storage.sync.get({ theme: "light" });
  document.getElementById("theme").value = theme;
}

document.addEventListener("DOMContentLoaded", loadOptions);
document.getElementById("save").addEventListener("click", saveOptions);
```

### Intercepting Web Requests

```javascript
// background.js — block specific URLs
browser.webRequest.onBeforeRequest.addListener(
  (details) => {
    return { cancel: true };
  },
  { urls: ["*://ads.example.com/*"] },
  ["blocking"]
);
```

### Badge Text on Action Button

```javascript
// background.js
async function updateBadge(tabId) {
  const count = await getCount(tabId);
  await browser.action.setBadgeText({ text: String(count), tabId });
  await browser.action.setBadgeBackgroundColor({ color: "#4688F1", tabId });
}
```

### Alarm-Based Periodic Tasks (MV3)

```javascript
// background.js
browser.runtime.onInstalled.addListener(() => {
  browser.alarms.create("checkUpdates", { periodInMinutes: 30 });
});

browser.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name === "checkUpdates") {
    const data = await fetch("https://api.example.com/updates").then(r => r.json());
    if (data.hasUpdate) {
      browser.notifications.create({
        type: "basic",
        iconUrl: browser.runtime.getURL("icons/icon-48.png"),
        title: "Update Available",
        message: data.message
      });
    }
  }
});
```

---

## Internationalization (i18n)

### Directory Structure

```
_locales/
  en/messages.json
  fr/messages.json
  de/messages.json
```

### messages.json Format

```json
{
  "extensionName": {
    "message": "My Extension",
    "description": "Name of the extension"
  },
  "greeting": {
    "message": "Hello, $USER$!",
    "description": "Greeting message",
    "placeholders": {
      "user": {
        "content": "$1",
        "example": "John"
      }
    }
  }
}
```

### Usage

**In manifest.json:**

```json
{
  "name": "__MSG_extensionName__",
  "default_locale": "en"
}
```

**In JavaScript:**

```javascript
const greeting = browser.i18n.getMessage("greeting", ["World"]);
```

**In HTML/CSS:**

```html
<span data-l10n-id="greeting">__MSG_greeting__</span>
```

---

## Debugging Checklist

When an extension doesn't work:

1. **Check `about:debugging`** — is the extension loaded? Any errors?
2. **Browser Console (`Ctrl+Shift+J`)** — background script errors
3. **Page DevTools Console** — content script errors (select extension context)
4. **Permissions** — are all needed permissions declared?
5. **Match patterns** — do content script patterns match the target URLs?
6. **CSP violations** — check for Content Security Policy blocks
7. **MV3 event page** — are listeners registered synchronously at top level?
8. **Storage** — using `browser.storage` instead of `window.localStorage`?
9. **web-ext lint** — run `web-ext lint` to catch common issues
10. **Cross-browser** — testing with the right browser? Using polyfill?
