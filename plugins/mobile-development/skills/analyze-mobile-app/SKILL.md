---
name: analyze-mobile-app
description: "Mobile App Competitive Analyzer. Automated competitive analysis of Android mobile apps via ADB. Navigate the app, capture screenshots, document UX/UI, generate complete reports. Use when: analyzing competitor apps, exploring app UX, mobile app analysis, competitive research."
---

# Mobile App Competitive Analyzer

Automated competitive analysis of Android mobile apps via ADB. Navigate the app, capture screenshots, document UX/UI, generate complete reports.

## Trigger

- "analizza app [nome]"
- "competitor analysis [app]"
- "esplora UX di [app]"
- "analisi competitiva [app]"
- /analyze-mobile-app

## Config

```yaml
adb_path: adb
screenshot_format: "{app}_{seq:02d}.png"
output_structure:
  - docs/{APP}_ANALYSIS.md
  - docs/{APP}_REPORT.html
  - docs/{APP}_USER_FLOWS.md
  - img/*.png
```

## Workflow

### 1. SETUP
```bash
# Verify connection
adb devices
# Output: emulator-5554  device

# Device info
adb shell wm size

# Current app package
adb shell dumpsys window | grep mCurrentFocus
```

### 2. MAIN LOOP (repeat for each screen)
```bash
# A) Screenshot
adb exec-out screencap -p > {app}_{seq:02d}.png

# B) Analyze screenshot visually (Read tool)

# C) UI dump for coordinates
adb shell uiautomator dump /sdcard/ui.xml
adb shell cat /sdcard/ui.xml

# D) Find bounds: [left,top][right,bottom]
# E) Calculate center: x=(left+right)/2, y=(top+bottom)/2

# F) Tap
adb shell input tap X Y

# G) Repeat from A)
```

### 3. NAVIGATION COMMANDS
```bash
adb shell input tap X Y                      # Tap
adb shell input swipe 540 1500 540 500 300   # Scroll down
adb shell input swipe 540 500 540 1500 300   # Scroll up
adb shell input swipe 900 1000 100 1000 300  # Swipe left
adb shell input swipe 100 1000 900 1000 300  # Swipe right
adb shell input swipe X Y X Y 1000           # Long press
adb shell input keyevent 4                   # Back
adb shell input keyevent 3                   # Home
adb shell input keyevent 66                  # Enter
adb shell input text "text"                  # Type
```

## Analysis

### Visual Design
- Colors (hex), typography, spacing, icons, illustrations, brand

### UX Patterns
- Navigation, info hierarchy, CTA, forms, onboarding, empty/error states

### Psychology
- Social proof, scarcity, commitment, gamification, loss aversion

### Business Model
- Paywall type, pricing, free vs premium, upsell timing

## Report Templates

### ANALYSIS.md
```markdown
# {APP} - Competitive Analysis

> Date: {DATE} | Version: {VERSION} | Method: ADB + UI inspection

## Executive Summary
| Metric | Value |
|--------|-------|
| Onboarding screens | {N} |
| Input methods | {N} |
| Price (annual) | {PRICE} |

## Company Profile
| Attribute | Value |
|-----------|-------|
| Company | {NAME} |
| HQ | {LOCATION} |
| Founded | {YEAR} |

## Target Market
### Segment A ({PCT}%)
- Profile: {PROFILE}
- Motivation: {MOTIVATION}

## Onboarding Flow
| Stage | Screens | Purpose |
|-------|---------|---------|

## Psychology
- Social Proof: {DESC}
- Gamification: {DESC}

## Pricing
| Plan | Price |
|------|-------|
| Monthly | {PRICE} |
| Annual | {PRICE} |

## Design System
```css
--primary: {HEX};
--accent: {HEX};
--radius: {PX};
```

## Navigation
| Tab | Function |
|-----|----------|

## Features
| Feature | Free | Premium |
|---------|------|---------|

## Recommendations
1. {REC}

## Screenshot Index
| File | Content |
|------|---------|
| {app}_01.png | {DESC} |
```

### USER_FLOWS.md
```markdown
# {APP} - User Flows

## Navigation
\`\`\`mermaid
flowchart TD
    TAB1[Tab 1] --> CONTENT1
    TAB2[Tab 2] --> CONTENT2
\`\`\`

## Onboarding
\`\`\`mermaid
flowchart TD
    START([Launch]) --> WELCOME
    WELCOME --> QUESTIONS
    QUESTIONS --> PAYWALL
    PAYWALL --> HOME([Home])
\`\`\`

## Core Feature
\`\`\`mermaid
flowchart TD
    HOME --> ADD[+]
    ADD --> METHOD1
    ADD --> METHOD2
    METHOD1 --> RESULT
    RESULT --> SAVE --> HOME
\`\`\`
```

### REPORT.html
```html
<!DOCTYPE html>
<html>
<head>
<style>
:root{--primary:#1E3A5F;--accent:#4ECDC4;--bg:#F5F7FA}
body{font-family:system-ui;background:var(--bg);margin:0;padding:20px}
.container{max-width:1200px;margin:0 auto}
.card{background:#fff;border-radius:12px;padding:24px;margin:20px 0;box-shadow:0 2px 8px rgba(0,0,0,0.1)}
.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}
.gallery img{width:100%;border-radius:8px;border:1px solid #eee}
h1,h2{color:var(--primary)}
h2{border-bottom:2px solid var(--accent);padding-bottom:8px}
table{width:100%;border-collapse:collapse}
th,td{padding:12px;text-align:left;border-bottom:1px solid #eee}
th{background:var(--bg)}
</style>
</head>
<body>
<div class="container">
<h1>{APP} - Competitive Analysis</h1>
<div class="card"><h2>Screenshots</h2>
<div class="gallery">
<img src="../img/{app}_01.png">
<img src="../img/{app}_02.png">
</div></div>
</div>
</body>
</html>
```

## Checklist

- [ ] Onboarding complete
- [ ] All tabs explored
- [ ] Settings captured
- [ ] Paywall documented
- [ ] Input methods tested
- [ ] User flows created
- [ ] Design tokens extracted
- [ ] Psychology analyzed
- [ ] Business model mapped
- [ ] Recommendations written
- [ ] ZIP created

## Troubleshooting

```bash
# No device
adb kill-server && adb start-server && adb devices

# UI dump fail
adb shell uiautomator dump /data/local/tmp/ui.xml
adb shell cat /data/local/tmp/ui.xml

# Black screenshot
adb shell screencap -p /sdcard/s.png && adb pull /sdcard/s.png

# Tap not working
# -> Recalculate coordinates from fresh UI dump
# -> Verify clickable="true"
# -> Add sleep 1 before
```

## PowerShell Helpers

```powershell
function ss($p){adb exec-out screencap -p|Set-Content $p -Enc Byte}
function ui{adb shell uiautomator dump /sdcard/ui.xml;adb shell cat /sdcard/ui.xml}
function tap($x,$y){adb shell input tap $x $y}
function sd{adb shell input swipe 540 1500 540 500 300}
function su{adb shell input swipe 540 500 540 1500 300}
function bk{adb shell input keyevent 4}
```

## Example

```
User: Analyze Yazio

Agent:
1. adb devices → emulator-5554 ✓
2. ss "yazio_01.png" → splash
3. ui → "Get Started" [100,1800][980,1900]
4. tap 540 1850
5. ss "yazio_02.png" → goal selection
... [50+ screens] ...
6. Generate YAZIO_ANALYSIS.md
7. Generate YAZIO_REPORT.html
8. Generate YAZIO_USER_FLOWS.md
9. ZIP → Desktop
```
