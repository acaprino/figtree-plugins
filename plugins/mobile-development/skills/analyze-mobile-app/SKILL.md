---
name: analyze-mobile-app
description: "Mobile app competitive analyzer via ADB. Use PROACTIVELY when analyzing competitor Android apps, exploring app UX patterns, documenting mobile user flows, or conducting competitive research. Captures screenshots, navigates UI, extracts design systems, and generates structured analysis reports."
---

# Mobile App Competitive Analyzer

Automated competitive analysis of Android mobile apps via ADB. Navigate the app, capture screenshots, document UX/UI, generate complete reports.

## Config

Output: `docs/{APP}_ANALYSIS.md`, `docs/{APP}_REPORT.html`, `docs/{APP}_USER_FLOWS.md`, `img/*.png`

## Workflow

### 1. Setup
```bash
adb devices                                        # Verify connection
adb shell wm size                                  # Device info
adb shell dumpsys window | grep mCurrentFocus      # Current app package
```

### 2. Main Loop (repeat for each screen)
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

### 3. Navigation Commands
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

See `references/report-templates.md` for ANALYSIS.md, USER_FLOWS.md, and REPORT.html templates.

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

# Tap not working - recalculate coordinates from fresh UI dump,
# verify clickable="true", add sleep 1 before tap
```
