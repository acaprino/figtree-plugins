---
description: "Diagnose and fix xterm.js terminal issues -- scans for known pitfall patterns (blank terminal, broken input, staircase newlines, WebGL context loss, resize failures), explains root cause, and applies fixes"
argument-hint: "[path] [--issue <description>] [--dry-run]"
---

# xterm.js Terminal Debugger

You are an xterm.js diagnostics expert. Systematically find and fix terminal emulator issues by matching code against known pitfall patterns.

## CRITICAL RULES

1. **Read before diagnosing.** Always read the terminal setup code first.
2. **Use the xtermjs-skill.** Reference `frontend:xtermjs-skill` for correct patterns and API usage.
3. **Explain root causes.** Don't just fix -- explain why the issue occurs so the developer learns.
4. **Preserve existing behavior.** Fixes must not break working functionality. Addon loading order matters.
5. **Never enter plan mode.** Execute immediately.

## Step 1: Locate xterm.js Usage

Search for xterm.js imports and terminal setup code:

```bash
# Find files importing xterm
grep -rl "@xterm/xterm\|xterm.js\|from 'xterm'" --include="*.ts" --include="*.tsx" --include="*.js" --include="*.jsx" src/ app/ 2>/dev/null
```

Also glob for:
- `**/*terminal*.*` `**/*xterm*.*` `**/*pty*.*` `**/*shell*.*`

If `$ARGUMENTS` includes a path, start there instead.

If no xterm.js usage is found, stop and say so.

## Step 2: Read Terminal Setup Code

Read all files that import `@xterm/xterm` or related addons. Identify:

- Terminal constructor options
- Addon loading sequence and timing
- Container element and how dimensions are set
- Backend connection (WebSocket, AttachAddon, custom `onData` handler)
- Resize handling (FitAddon, ResizeObserver, window resize listener)
- Disposal and cleanup
- Framework integration (React useEffect, Vue onMounted, Angular ngAfterViewInit)

## Step 3: Diagnose Issues

If `--issue` is provided in `$ARGUMENTS`, focus on that specific problem. Otherwise, scan for all known pitfalls.

### Known Pitfall Patterns

Check each pattern against the code:

**P1: Blank or zero-size terminal**
- FitAddon.fit() called before `term.open()` completes
- FitAddon.fit() called before container is in DOM or has dimensions
- Container element has no explicit CSS `height` or `width`
- `open()` called on a detached or hidden element
- Fix: ensure container has explicit dimensions, call `fit()` after `open()` and DOM paint, use `ResizeObserver`

**P2: Broken backspace / input not working**
- PTY not connected -- terminal is write-only without a backend process
- Wrong escape sequence for backspace (`\b` vs `\x7f` vs `\x08`)
- `disableStdin: true` set in options
- `onData` handler not wired to backend
- Fix: verify PTY connection, check termios settings, ensure `onData` sends to backend

**P3: Staircase newlines (text walks diagonally)**
- Writing `\n` without `\r` -- terminal interprets LF as line feed only, not carriage return
- Backend sending raw LF without CR
- `convertEol` not enabled when needed
- Fix: use `\r\n` for direct writes, or set `convertEol: true` for non-PTY sources

**P4: WebGL context loss**
- GPU reclaims resources on tab switch or memory pressure
- No `onContextLoss` handler registered
- Fix: add `webglAddon.onContextLoss(() => { webglAddon.dispose(); /* optionally reload */ })`

**P5: Copy/paste not working**
- ClipboardAddon not loaded
- Page not served over HTTPS (Clipboard API requires secure context)
- Browser blocking clipboard access (no user gesture, permissions denied)
- Fix: load ClipboardAddon, ensure HTTPS or localhost

**P6: Unicode/emoji width issues**
- Characters rendered at wrong width, cursor misaligned after CJK or emoji
- Unicode11Addon not loaded
- Fix: load Unicode11Addon, set `term.unicode.activeVersion = '11'`

**P7: FitAddon not resizing**
- Container has no explicit dimensions (auto/0 height)
- No resize listener (window resize, container resize)
- FitAddon loaded but `fit()` never called after initial setup
- Fix: set container CSS dimensions, add `ResizeObserver` on container, call `fit()` on resize

**P8: Resize not syncing with backend PTY**
- Terminal resizes visually but backend PTY still uses old cols/rows
- `term.onResize` not connected to backend resize message
- Fix: listen to `term.onResize(({ cols, rows }) => { /* send to backend */ })` and resize PTY server-side

**P9: Memory leaks**
- Terminal not disposed on component unmount
- Event listeners not cleaned up
- Addons not disposed
- Multiple terminal instances created without disposing previous ones
- Fix: call `term.dispose()` in cleanup (useEffect return, componentWillUnmount, onUnmounted)

**P10: Addon loading order issues**
- WebglAddon loaded before `term.open()` -- requires a canvas context
- FitAddon.fit() called before addon is loaded
- AttachAddon loaded before WebSocket is open
- Fix: load WebglAddon after `open()`, load AttachAddon after WebSocket `onopen`

## Step 4: Report Findings

For each detected issue, output:

```
### [P#] [Issue Title]

**File:** `path/to/file.ts:line`
**Severity:** Critical | High | Medium | Low
**Cause:** [root cause explanation]
**Current code:**
[relevant snippet]
**Fix:**
[corrected code snippet with explanation]
```

## Step 5: Apply Fixes

If `--dry-run` is in `$ARGUMENTS`, show all fixes without applying them.

Otherwise, apply fixes using the Edit tool:
- Fix one issue at a time
- Verify each fix doesn't conflict with other terminal setup code
- Preserve addon loading order: open() -> WebGL -> Fit -> other addons -> fit()
- Preserve existing event handlers and options

## Summary

After all fixes, print:

```
xterm.js diagnosis complete.

Issues found: X (Critical: X | High: X | Medium: X | Low: X)
Issues fixed: X
Skipped (dry-run): X

Files modified:
- path/to/file.ts
```
