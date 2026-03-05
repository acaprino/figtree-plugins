---
name: css-master
description: Comprehensive CSS skill covering modern CSS features, architecture methodologies (BEM, CSS Modules, Cascade Layers), SASS/preprocessors, accessibility patterns, responsive images, cross-browser compatibility, and web fonts. Trigger when writing CSS, refactoring styles, handling modern CSS features (Container Queries, View Transitions, Scroll-driven animations, Masonry), or architecting a style system.
---

<!-- Upstream source (modern CSS content): https://github.com/paulirish/dotfiles/tree/main/agents/paulirish-skills/skills/modern-css -->

# CSS Master

Comprehensive reference for writing modern, robust, maintainable, and accessible CSS — from cutting-edge native features to production architecture patterns.

---

## Layout & Responsive Design

### Container Queries
```css
.card {
  container: --my-card / inline-size;
}

@container --my-card (width < 40ch) {
  /* Component-based responsive design */
}

@container (20ch < width < 50ch) {
  /* Range syntax */
}
```

**Container units:** `cqi`, `cqb`, `cqw`, `cqh` - size relative to container dimensions

**Anchored container queries:** Style positioned elements based on anchor fallback state
```css
.tooltip {
  container-type: anchored;
}

@container anchored(top) {
  /* Styles when positioned at top */
}
```

### Media Query Range Syntax
```css
@media (width <= 1024px) { }
@media (360px < width < 1024px) { }
```


### Grid Enhancements
- **Subgrid:** Inherit parent grid lines for nested layouts
- **Masonry:** `display: grid-lanes` for Pinterest-style layouts with logical tab order. (Previously proposed as `grid-template-rows: masonry`).

---

## Color & Theming

### Color Scheme & Light-Dark Function
```css
:root {
  color-scheme: light dark;
  --surface-1: light-dark(white, #222);
  --text-1: light-dark(#222, #fff);
}
```

### Modern Color Spaces
```css
/* OKLCH: uniform brightness, P3+ colors */
.vibrant {
  background: oklch(72% 75% 330);
}

/* Display-P3 for HDR displays */
@media (dynamic-range: high) {
  .neon {
    --neon-red: color(display-p3 1 0 0);
  }
}

/* Better gradients with in oklch */
.gradient {
  background: linear-gradient(
    to right in oklch,
    color(display-p3 1 0 .5),
    color(display-p3 0 1 1)
  );
}
```

### Color Manipulation
```css
/* color-mix() */
.lighten {
  background: color-mix(in oklab, var(--brand), white);
}

/* Relative color syntax */
.lighter {
  background: oklch(from blue calc(l + .25) c h);
  background: oklch(from blue 75% c h); /* Set to specific lightness */
}

.semi-transparent {
  background: oklch(from var(--color) l c h / 50%);
}

.complementary {
  background: hsl(from blue calc(h + 180) s l);
}
```

### Accent Color
```css
:root {
  accent-color: hotpink; /* Tints checkboxes, radios, range inputs */
}
```

---

## Typography

### Text Wrapping
```css
h1 {
  text-wrap: balance; /* Balanced multi-line headings */
  max-inline-size: 25ch;
}

p {
  text-wrap: pretty; /* No orphans */
  max-inline-size: 50ch;
}
```

### Text Box Trim
```css
h1, p, button {
  text-box: trim-both cap alphabetic; /* Optical vertical centering */
}
```

### Fluid Typography
```css
.heading {
  font-size: clamp(1rem, 1rem + 0.5vw, 2rem); /* Respects user preferences */
}
```

### Dynamic Viewport Units
- `dvh` / `dvw` - Dynamic (accounts for mobile browser UI)
- `svh` / `svw` - Small (smallest possible viewport)
- `lvh` / `lvw` - Large (largest possible viewport)

### Web Fonts
```css
/* Variable fonts — one file, infinite variations */
@font-face {
  font-family: 'Inter';
  src: url('inter.woff2') format('woff2');
  font-weight: 100 900;       /* Weight axis range */
  font-style: normal oblique; /* Style axis range */
  font-display: swap;         /* Prevent invisible text while loading */
}

/* Size-specific subsets reduce file size */
@font-face {
  font-family: 'Inter';
  src: url('inter-latin.woff2') format('woff2');
  unicode-range: U+0000-00FF;
}

/* Use variable axes */
.display {
  font-variation-settings: 'wght' 800, 'wdth' 75;
}
```

**Performance tips:**
- Always use `woff2` — best compression, universal browser support
- Preload critical fonts: `<link rel="preload" as="font" href="font.woff2" crossorigin>`
- Use `font-display: swap` or `optional` (zero layout shift but may show fallback briefly)
- Subsetting: use only the characters you need via tools like `glyphhanger` or Google Fonts `text=` param

---

## Animations & Motion

### Scroll-Driven Animation
```css
/* Animate on scroll position */
.parallax {
  animation: slide-up linear both;
  animation-timeline: scroll();
}

/* Animate on viewport intersection */
.fade-in {
  animation: fade linear both;
  animation-timeline: view();
  animation-range: cover -75cqi contain 20cqi;
}
```

### View Transitions
**Status:** Baseline Newly Available (Same-document).
Cross-document transitions are in Limited Availability (Chrome/Safari 18.2+).

```css
@view-transition {
  navigation: auto; /* Automatically animate page transitions (MPAs) */
}

nav {
  view-transition-name: --persist-nav; /* Persist specific elements */
  view-transition-class: --site-header; /* Group transitions with classes */
}

/* Style the active transition */
html:active-view-transition {
  overflow: hidden;
}
```

**Nested View Transition Groups:** Preserve 3D transforms and clipping during transitions.

### Advanced Easing with linear()
```css
.springy {
  --spring: linear(
    0, 0.14 4%, 0.94 17%, 1.15 24% 30%, 1.02 43%, 0.98 51%, 1 77%, 1
  );
  transition: transform 1s var(--spring);
}
```

### @starting-style
```css
.dialog {
  transition: opacity .5s, scale .5s;

  @starting-style {
    opacity: 0;
    scale: 1.1;
  }
}
```

---

## Custom Properties & Advanced Features

### @property
Type-safe, animatable custom properties:
```css
@property --gradient-angle {
  syntax: "<angle>";
  inherits: false;
  initial-value: 0deg;
}

.animate {
  transition: --gradient-angle 1s ease;

  &:hover {
    --gradient-angle: 360deg;
  }
}
```

### Math Functions & calc-size()
**Newly Available:** `calc-size()` allows calculations and transitions on intrinsic sizes (auto, min-content).

```css
/* Finally: Animate to auto height! */
.accordion-content {
  height: 0;
  overflow: hidden;
  transition: height 0.3s ease;
}

.accordion-item.open .accordion-content {
  height: calc-size(auto);
}

.radial-layout {
  --_angle: calc(var(--sibling-index) * var(--_offset));
  translate:
    calc(cos(var(--_angle)) * var(--_circle-size))
    calc(sin(var(--_angle)) * var(--_circle-size));
}
```

### Tree Counting Functions (Coming Soon)
```css
.staggered {
  animation-delay: calc(sibling-index() * .1s);
  background-color: hsl(sibling-count() 50% 50%);
}
```

### Conditional CSS with if() (Coming Soon)
```css
.dynamic {
  color: if(
    style(--theme: dark),
    white,
    black
  );
}
```

---

## Architecture & Organization

### Cascade Layers
```css
@layer reset, design-system, components, utilities;

@import "open-props/colors" layer(design-system);
@import "components/nav/base.css" layer(components.nav);

@layer components.nav.primary {
  nav {
    position: sticky;
    inset-block-start: 0;
  }
}
```

Benefits:
- Import third-party CSS with lower specificity
- Organize styles by concern, not selector weight
- Nested layers create clear hierarchies

### BEM Naming Convention
Block-Element-Modifier: predictable, collision-free class names for component-scoped CSS without tooling.

```css
/* Block: standalone component */
.card { }

/* Element: part of the block, never standalone */
.card__title { }
.card__image { }
.card__body { }

/* Modifier: variant or state of a block or element */
.card--featured { }
.card--dark { }
.card__title--truncated { }
```

Rules:
- Elements never depend on other elements: `.card__title`, not `.card__header__title`
- Modifiers never appear alone — always with their block/element class
- Avoid deep nesting in selectors; BEM trades class verbosity for zero specificity wars
- One block = one file in a component-driven project

### CSS Modules (React/Vite)
Scoped styles via build-time hash — zero runtime overhead, zero global leakage.

```css
/* Button.module.css */
.button {
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-md);
}

.button--primary {
  background: var(--brand);
  color: white;
}

.button--ghost {
  background: transparent;
  border: 1px solid currentColor;
}
```

```tsx
// Button.tsx
import styles from './Button.module.css';

export function Button({ variant = 'primary', children }) {
  return (
    <button className={`${styles.button} ${styles[`button--${variant}`]}`}>
      {children}
    </button>
  );
}
```

**Composing classes:**
```css
.error-button {
  composes: button from './Button.module.css';
  background: var(--danger);
}
```

**When to use BEM vs CSS Modules:**
- **BEM**: Plain HTML projects, design systems shipped as CSS, teams preferring no build step
- **CSS Modules**: React/Vue/Svelte component projects — scoping is automatic and co-location is clean
- **Tailwind**: Utility-first, good for rapid iteration; pair with `@apply` sparingly for repeated patterns

### SASS/Preprocessors
Native CSS now covers most SASS use cases (custom properties, nesting, `@layer`). Use SASS when you need:

```scss
// Maps: iterate design tokens
$spacing: (
  'sm': 0.5rem,
  'md': 1rem,
  'lg': 1.5rem,
);

@each $name, $value in $spacing {
  .p-#{$name} { padding: $value; }
  .m-#{$name} { margin: $value; }
}

// Mixins: reusable style blocks with arguments
@mixin visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.sr-only { @include visually-hidden; }

// @use and @forward (modern SASS module system — NOT @import)
// _tokens.scss
$brand: oklch(60% 0.2 230);

// main.scss
@use 'tokens' as t;
.button { background: t.$brand; }
```

**When to skip SASS:** If the project uses native CSS custom properties, `@layer`, and native nesting, SASS adds complexity without benefit. Prefer native CSS for new projects.

---

## Interactive Components

### Dialog
```html
<dialog id="modal">
  <form method="dialog">
    <button value="cancel">Cancel</button>
    <button value="confirm">Confirm</button>
  </form>
</dialog>

<button commandfor="modal" command="showModal">Open</button>
<button commandfor="modal" command="close">Close</button>
```

**New:** `closedby` attribute enables light-dismiss behavior

### Popover
```html
<button popovertarget="menu">Show Menu</button>
<div popover id="menu">...</div>
```

**popover=hint:** Ephemeral tooltips that don't dismiss other popovers

```css
[popover] {
  transition:
    display .5s allow-discrete,
    overlay .5s allow-discrete,
    opacity .5s;

  @starting-style {
    &:popover-open {
      opacity: 0;
    }
  }
}
```

### Anchor Positioning
```css
.tooltip-anchor {
  anchor-name: --tooltip;
}

.tooltip[popover] {
  position-anchor: --tooltip;
  position-area: block-start;
  position-try-fallbacks: flip-block;
  position-try-order: most-height;
}
```

**Pseudo-elements:** `anchor()`, `::scroll-button()`, `::scroll-marker()`

### Exclusive Accordion
```html
<details name="accordion">...</details>
<details name="accordion">...</details>
<!-- Only one can be open at a time -->
```

### Customizable Select
```css
select {
  appearance: base-select; /* Full CSS control */
}

/* Style options with rich HTML */
select option::before {
  content: ""; /* Can include images, icons */
}
```

### Search Element
```html
<search>
  <form>
    <input type="search" name="q">
    <button type="submit">Search</button>
  </form>
</search>
```

---

## Form Enhancements

### Field Sizing
```css
textarea, select, input {
  field-sizing: content; /* Auto-grow to content */
}

textarea {
  min-block-size: 3lh; /* Line-height units */
  max-block-size: 80dvh;
}
```

### Better Validation Pseudo-Classes
```css
/* Wait for user interaction before showing errors */
:user-invalid {
  outline-color: red;
}

:user-valid {
  outline-color: green;
}

label:has(+ input:user-invalid) {
  text-decoration: underline wavy red;
}
```

### HR in Select
```html
<select>
  <option>Option 1</option>
  <hr>
  <option>Option 2</option>
</select>
```

---

## Visual Effects

### Scrollbar Styling
```css
.custom-scrollbar {
  scrollbar-color: hotpink transparent;
  scrollbar-width: thin;
}
```

### Shape Function
```css
.complex-clip {
  clip-path: shape(
    from 0% 0%,
    curve by 50% 25% via 25% 50%,
    line to 100% 100%
  );
}
```

### Corner Shapes
```css
.fancy-corners {
  corner-shape: squircle;
  corner-shape: notch;
  corner-shape: scoop;
  corner-shape: superellipse(0.7);
}
```

---

## Accessible Styles

### Focus Management
```css
/* :focus-visible — only show ring for keyboard, not mouse */
:focus-visible {
  outline: 2px solid var(--brand);
  outline-offset: 2px;
}

/* Remove default focus ring only if providing a custom one */
:focus:not(:focus-visible) {
  outline: none;
}
```

### Visually Hidden (Screen Reader Only)
```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Unhide on focus (e.g. skip links) */
.sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  overflow: visible;
  clip: auto;
  white-space: normal;
}
```

### Skip Link Pattern
```html
<a class="skip-link" href="#main-content">Skip to main content</a>
<main id="main-content">...</main>
```
```css
.skip-link {
  position: absolute;
  top: -100%;
  left: 1rem;
  padding: 0.5rem 1rem;
  background: var(--brand);
  color: white;
  border-radius: var(--radius-sm);
  z-index: 9999;
}
.skip-link:focus { top: 1rem; }
```

### Forced Colors / High Contrast Mode
```css
/* Respect Windows High Contrast / Forced Colors mode */
@media (forced-colors: active) {
  .button {
    border: 2px solid ButtonText;
    forced-color-adjust: none; /* Only when you need to preserve specific colors */
  }
}

/* Never convey information by color alone */
.error {
  color: var(--danger);
  border-left: 3px solid var(--danger); /* Also a shape cue */
}
.error::before {
  content: "⚠ "; /* Also a text cue */
}
```

**WCAG contrast minimums:**
- Normal text: 4.5:1 (AA), 7:1 (AAA)
- Large text (18px+/14px+ bold): 3:1 (AA), 4.5:1 (AAA)
- UI components and focus rings: 3:1 (AA)
- Use `oklch()` — its uniform lightness makes contrast estimation intuitive

---

## Responsive Images

```html
<!-- srcset + sizes: browser picks the right resolution -->
<img
  src="hero-800.jpg"
  srcset="hero-400.jpg 400w, hero-800.jpg 800w, hero-1600.jpg 1600w"
  sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 800px"
  alt="Description"
  loading="lazy"
  decoding="async"
>

<!-- picture: art direction (different crops at different sizes) -->
<picture>
  <source
    media="(min-width: 800px)"
    srcset="hero-wide.webp"
    type="image/webp"
  >
  <source
    media="(max-width: 799px)"
    srcset="hero-square.webp"
    type="image/webp"
  >
  <img src="hero-wide.jpg" alt="Description">
</picture>
```

**CSS aspect ratio (prevents layout shift):**
```css
img {
  aspect-ratio: 16 / 9;
  width: 100%;
  height: auto;
  object-fit: cover;
}

/* Reserve space before image loads */
.image-container {
  aspect-ratio: 16 / 9;
  overflow: hidden;
}
```

**Performance rules:**
- Always set `width` and `height` attributes on `<img>` — browser reserves space before load
- Use `loading="lazy"` for below-fold images; never on LCP image
- Prefer `webp` with jpg/png fallback via `<picture>`
- Use `fetchpriority="high"` on the LCP image

---

## Progressive Enhancement & Cross-Browser Compatibility

### Feature Detection with @supports
```css
@supports (animation-timeline: view()) {
  .fade-in {
    animation: fade linear both;
    animation-timeline: view();
  }
}

@supports (container-type: inline-size) {
  .responsive-card {
    container-type: inline-size;
  }
}

/* Negative — apply styles only when NOT supported */
@supports not (display: grid) {
  .layout { display: flex; flex-wrap: wrap; }
}
```

### Vendor Prefixes
Modern browsers require very few vendor prefixes (Autoprefixer handles the rest). The few remaining cases:

```css
/* -webkit- still needed for some properties */
.gradient {
  background: -webkit-linear-gradient(top, #000, #fff);
  background: linear-gradient(to bottom, #000, #fff);
}

/* Always write the unprefixed version last */
```

**Use Autoprefixer in your build tool** (PostCSS plugin) — don't write vendor prefixes manually. Configure `browserslist` in `package.json` to target the browsers you support:

```json
{
  "browserslist": "> 0.5%, last 2 versions, not dead"
}
```

### Respect User Preferences
```css
@media (prefers-reduced-motion: no-preference) {
  .animated {
    animation: slide 1s ease;
  }
}

@media (prefers-color-scheme: dark) {
  :root {
    --surface: #222;
  }
}

@media (prefers-contrast: more) {
  .text {
    font-weight: 600;
  }
}
```

---

## Checking Browser Support: Baseline

**What is Baseline?** A unified way to understand cross-browser feature availability. Features are marked as:

- **Widely Available:** Supported in the last 2.5 years of all major browsers
- **Newly Available:** Available in all major browsers
- **Limited Availability:** Not yet in all browsers

### How to Check Baseline Status

0. BEST: Fetch https://web-platform-dx.github.io/web-features-explorer/groups/ and find the feature in there, then fetch it's detail page.
1. **Can I Use:** [caniuse.com](https://caniuse.com) shows Baseline badges at the top of each feature
2. **MDN:** Look for the Baseline badge in the browser compatibility table
3. **web.dev:** Feature articles include Baseline status


**Remember:** Always check Baseline status, use `@supports` for cutting-edge features, and respect user preferences with media queries. Modern CSS is about progressive enhancement and building resilient interfaces that work for everyone.


---

## Real-World Example: Modern Component

Here's a card component using many modern CSS features:

```css
/* Cascade layer for organization */
@layer components.card {

  /* Custom properties with @property */
  @property --card-hue {
    syntax: "<number>";
    inherits: false;
    initial-value: 200;
  }

  .card {
    /* Container for responsive design */
    container: card / inline-size;

    /* Logical properties */
    inline-size: 100%;
    padding-inline: var(--space-md);
    padding-block: var(--space-lg);

    /* Modern color system */
    background: light-dark(
      oklch(98% 0.02 var(--card-hue)),
      oklch(20% 0.02 var(--card-hue))
    );

    /* Border with relative color */
    border: 1px solid oklch(from var(--surface) calc(l * 0.9) c h);

    /* Smooth corners */
    border-radius: var(--radius-md);

    /* View transition */
    view-transition-name: --card;

    /* Scroll-driven animation */
    animation: fade-in linear both;
    animation-timeline: view();
    animation-range: entry 0% cover 30%;

    /* Anchor for tooltips */
    anchor-name: --card-anchor;

    /* Transition custom property */
    transition: --card-hue 0.5s var(--ease-spring-3);

    &:hover {
      --card-hue: 280;
    }

    /* Responsive typography in container */
    @container card (width > 30ch) {
      .card__title {
        font-size: clamp(1.5rem, 3cqi, 2.5rem);
        text-wrap: balance;
      }
    }

    @container card (width < 30ch) {
      .card__image {
        aspect-ratio: 16 / 9;
        object-fit: cover;
      }
    }
  }

  .card__title {
    /* Text box trim for optical alignment */
    text-box: trim-both cap alphabetic;
    text-wrap: balance;

    /* Logical margin */
    margin-block-end: var(--space-sm);
  }

  .card__body {
    text-wrap: pretty;
    max-inline-size: 65ch;
  }

  .card__cta {
    /* Inherit font */
    font: inherit;

    /* Accent color */
    accent-color: var(--brand);

    /* Field sizing */
    field-sizing: content;

    /* Logical properties */
    padding-inline: var(--space-md);
    padding-block: var(--space-sm);

    /* Modern color with relative syntax */
    background: oklch(from var(--brand) l c h);
    color: oklch(from var(--brand) 95% 0.05 h);

    &:hover {
      background: oklch(from var(--brand) calc(l * 1.1) c h);
    }

    &:user-invalid {
      outline: 2px solid light-dark(red, #ff6b6b);
    }
  }

  /* Popover tooltip anchored to card */
  .card__tooltip[popover] {
    position-anchor: --card-anchor;
    position-area: block-start;
    position-try-fallbacks: flip-block;

    /* Entry animation */
    @starting-style {
      opacity: 0;
      scale: 0.9;
    }

    transition:
      opacity 0.2s,
      scale 0.2s,
      display 0.2s allow-discrete,
      overlay 0.2s allow-discrete;
  }

  /* Scroll state container queries */
  @supports (container-type: scroll-state) {
    .card__sticky-header {
      container-type: scroll-state;
      position: sticky;
      inset-block-start: 0;

      @container scroll-state(stuck: top) {
        box-shadow: 0 2px 8px oklch(0% 0 0 / 0.1);
      }
    }
  }

  /* Respect user preferences */
  @media (prefers-reduced-motion: reduce) {
    .card {
      animation: none;
      transition: none;
    }
  }

  @media (prefers-contrast: more) {
    .card {
      border-width: 2px;
    }
  }
}

/* Keyframes for scroll animation */
@keyframes fade-in {
  from {
    opacity: 0;
    scale: 0.95;
  }
  to {
    opacity: 1;
    scale: 1;
  }
}
```

### HTML for the Example

```html
<article class="card">
  <img
    class="card__image"
    src="image.jpg"
    alt="Description"
    loading="lazy"
  >

  <h2 class="card__title">Card Title</h2>

  <p class="card__body">
    Card description with pretty text wrapping that avoids orphans.
  </p>

  <button
    class="card__cta"
    popovertarget="card-tooltip"
  >
    Learn More
  </button>

  <div
    class="card__tooltip"
    popover="hint"
    id="card-tooltip"
  >
    Additional information appears here
  </div>
</article>
```


## Canonical Resources

- [CSS Wrapped 2025](https://chrome.dev/css-wrapped-2025/) - The year's CSS features
- [The Coyier CSS Starter](https://frontendmasters.com/blog/the-coyier-css-starter/) - Opinionated modern baseline
- [Adam Argyle's CascadiaJS 2025 Deck](https://cascadiajs-2025.netlify.app/) - (markdownified locally in ./argyle-cacadia-2025-deck.md)
- [Modern CSS in Real Life](https://chriscoyier.net/2023/06/06/modern-css-in-real-life/) - Practical applications


## Usage Guidelines

1.  **Prioritize Stability:**
    *   Recommend **Newly Available** or **Widely Available** features for production code.
    *   Use **Limited Availability** features with progressive enhancement, graceful degredation, or `@supports`. Or ask the user how they want to handle it.

2.  **Use the web platform:**
    *   Always prefer standard CSS solutions over JavaScript libraries for layout, animation, and interaction (e.g., use CSS Masonry instead of Masonry.js, Popover API instead of custom tooltip scripts).

3.  **Code Style:**
    *   Use modern color spaces (`oklch`) for new palettes.
