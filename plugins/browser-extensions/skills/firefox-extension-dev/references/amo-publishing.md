# AMO Publishing and Security Reference

## Distribution Channels

| Channel | Review | Signing | Auto-Updates |
|---|---|---|---|
| AMO Listed | Auto + manual post-pub | AMO signs | AMO handles |
| Self-distributed (unlisted) | Auto only | AMO signs | Extension manages via `update_url` |

## Publishing Process

1. Package: `web-ext build`
2. Submit to [addons.mozilla.org](https://addons.mozilla.org)
3. Automated review runs in seconds
4. Manual review follows post-publication
5. Each version must have a unique version number (no reverting)

## Review Policies

**Requirements:**
- No remote code execution - bundle all code locally
- No `eval()` - forbidden in MV3, dangerous in MV2
- Minimal permissions - request only what's needed
- Transparent functionality - no surprises
- Data disclosure - all collection/transmission must be disclosed
- Third-party libraries - must be unmodified and documented
- Submit source code for minified/transpiled builds (`--upload-source-code`)

**Rejection triggers:**
- Modified third-party libraries
- Remote script loading
- Overly broad permissions without justification
- Missing source code for obfuscated builds

## Security Best Practices

- **Never load remote scripts** - bundle everything locally
- **Use safe DOM methods** - `createElement()`, `setAttribute()`, `textContent`
- **Sanitize HTML** - use DOMPurify 2.0.7+ for any HTML insertion
- **Use CSP defaults** - don't relax Content Security Policy
- **Lint with `eslint-plugin-no-unsanitized`**
- **Keep libraries updated** - outdated CVEs may trigger AMO blocking
- **Prevent fingerprinting** - don't expose `moz-extension://{UUID}` to pages
- **Use REST APIs for analytics** - don't embed tracking JS

## Content Security Policy

### MV3 CSP Format

```json
{
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'self'"
  }
}
```

### MV2 CSP Format

```json
{
  "content_security_policy": "script-src 'self'; object-src 'self'"
}
```

### CSP Rules for Extensions

- Default policy restricts `eval()` and inline scripts
- MV3 forbids `eval()` entirely
- Remote script loading blocked by default
- `wasm-unsafe-eval` allowed for WebAssembly in MV3
- Extension pages and sandbox pages can have different policies

## web-ext Signing Commands

```bash
# Sign for self-distribution
web-ext sign --channel unlisted --api-key $WEB_EXT_API_KEY --api-secret $WEB_EXT_API_SECRET

# Sign for AMO listing
web-ext sign --channel listed --amo-metadata amo-metadata.json
```

## Internationalization for AMO Listing

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

### Usage in manifest.json

```json
{
  "name": "__MSG_extensionName__",
  "default_locale": "en"
}
```

### Usage in JavaScript

```javascript
const greeting = browser.i18n.getMessage("greeting", ["World"]);
```

### Usage in HTML/CSS

```html
<span data-l10n-id="greeting">__MSG_greeting__</span>
```
