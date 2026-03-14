# manifest.json Complete Schema Reference

## Required Keys

Only 3 keys are mandatory:

```json
{
  "manifest_version": 3,
  "name": "My Extension",
  "version": "1.0"
}
```

## Complete Key Reference

| Key | MV2 | MV3 | Notes |
|---|---|---|---|
| `manifest_version` | 2 | 3 | Required |
| `name` | Y | Y | Required |
| `version` | Y | Y | Required. Format: numbers separated by up to 3 dots, max 9 digits each |
| `action` | - | Y | Toolbar button (replaces `browser_action`) |
| `author` | Y | Y | |
| `background` | Y | Y | MV2: `scripts`+`persistent`. MV3: `scripts` (event page in Firefox, service_worker in Chrome) |
| `browser_action` | Y | - | MV2 only, use `action` in MV3 |
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
| `host_permissions` | - | Y | MV3 only. Separated from `permissions` |
| `icons` | Y | Y | Sizes: 16, 32, 48, 96, 128 |
| `incognito` | Y | Y | |
| `omnibox` | Y | Y | |
| `optional_host_permissions` | - | Y | MV3 only |
| `optional_permissions` | Y | Y | |
| `options_page` | Y | Y | |
| `options_ui` | Y | Y | |
| `page_action` | Y | - | Retained in Firefox MV3 but MV2-only in Chrome |
| `permissions` | Y | Y | |
| `protocol_handlers` | Y | Y | Firefox-only |
| `short_name` | Y | Y | |
| `sidebar_action` | Y | Y | Firefox-only |
| `storage` | Y | Y | Managed storage schema (Firefox unsupported) |
| `theme` | Y | Y | |
| `theme_experiment` | Y | Y | Firefox-only, experimental |
| `user_scripts` | Y | - | MV2 only |
| `version_name` | Y | Y | |
| `web_accessible_resources` | Y | Y | MV2: string array. MV3: object array with `resources`+`matches`+`extension_ids` |

## Manifest V3 Example (Firefox)

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

## Manifest V2 Example (Firefox)

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

## Access Manifest at Runtime

```javascript
const manifest = browser.runtime.getManifest();
console.log(manifest.version);
```
