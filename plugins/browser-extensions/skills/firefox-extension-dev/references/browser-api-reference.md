# WebExtension JavaScript APIs (Complete Reference)

All APIs accessed via `browser.*` namespace. Firefox returns Promises for all async methods.

## API Reference Table

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

## Key API Details

### browser.tabs

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

### browser.storage

**Four storage areas:**
- `storage.local` - 10 MB limit, persists on disk
- `storage.sync` - 100 KB limit, synced across devices
- `storage.managed` - read-only, set by domain admin
- `storage.session` - 10 MB limit, in-memory only, lost on restart

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

// IMPORTANT: Never use window.localStorage - Firefox clears it during privacy cleanup
```

### browser.runtime

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

### browser.declarativeNetRequest

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

## Common Permission List

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
