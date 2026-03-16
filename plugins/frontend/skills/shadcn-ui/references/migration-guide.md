# Tailwind v3 to v4 Migration Guide

Step-by-step migration for shadcn/ui projects upgrading to Tailwind v4.

Source: https://ui.shadcn.com/docs/tailwind-v4

## Prerequisites

- Existing shadcn/ui project on Tailwind v3
- Migration is non-breaking -- existing v3/React 18 apps continue to function

## Migration Steps

### Step 1: Run the Tailwind Codemod

```bash
npx @tailwindcss/upgrade@next
```

This removes deprecated utilities and migrates CSS variables to the `@theme` directive.

### Step 2: Swap Animation Library

Remove `tailwindcss-animate` and its `@plugin` import. Install `tw-animate-css`:

```bash
pnpm remove tailwindcss-animate
pnpm add -D tw-animate-css
```

In `globals.css`, replace the plugin import with:

```css
@import "tw-animate-css";
```

### Step 3: Restructure CSS Variables

Move CSS variable declarations out of `@layer base`. Use `@theme inline` to reference them:

```css
/* Before (v3) */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
  }
}

/* After (v4) */
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.141 0.005 285.823);
}

@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  --color-secondary: var(--secondary);
  --color-secondary-foreground: var(--secondary-foreground);
  --color-muted: var(--muted);
  --color-muted-foreground: var(--muted-foreground);
  --color-accent: var(--accent);
  --color-accent-foreground: var(--accent-foreground);
  --color-destructive: var(--destructive);
  --color-border: var(--border);
  --color-input: var(--input);
  --color-ring: var(--ring);
  --color-sidebar-background: var(--sidebar-background);
  --color-sidebar-foreground: var(--sidebar-foreground);
}
```

No more `hsl()` wrappers in utility classes -- theme colors include the function natively.

### Step 4: Update Chart Config

Remove `hsl()` wrappers from chart color values if present.

### Step 5: Use size-* Utilities

Replace paired `w-*` / `h-*` with `size-*` (available since Tailwind v3.4):

```tsx
// Before
<div className="w-4 h-4" />

// After
<div className="size-4" />
```

### Step 6: Update Dependencies

```bash
pnpm up "@radix-ui/*" cmdk lucide-react recharts
```

### Step 7: Remove forwardRef (React 19)

All shadcn components updated for React 19 drop `React.forwardRef`. Convert custom wrappers:

```tsx
// Before (React 18)
const MyButton = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, ...props }, ref) => (
    <button ref={ref} className={cn("...", className)} {...props} />
  )
)
MyButton.displayName = "MyButton"

// After (React 19)
function MyButton({ className, ref, ...props }: ButtonProps & { ref?: React.Ref<HTMLButtonElement> }) {
  return <button ref={ref} className={cn("...", className)} data-slot="button" {...props} />
}
```

### Step 8: Add data-slot Attributes

All shadcn primitives now have `data-slot` attributes for targeted CSS overrides:

```css
/* Target specific component slots without class specificity fights */
[data-slot="sidebar-header"] {
  padding: var(--space-md);
}
```

## Color System: HSL to OKLCH

New projects default to OKLCH for perceptual uniformity. Existing HSL values continue to work but new components ship with OKLCH.

Key difference: OKLCH produces more uniform perceived brightness across hues, making palette generation more predictable.

## New Defaults

- **Style**: `new-york` is the default; `default` style is deprecated
- **Framework**: Tailwind v4 + React 19
- **Primitives**: `data-slot` on every component for CSS targeting
