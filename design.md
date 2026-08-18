# CampusArchive Design System

UI/UX Design and Visual Identity Documentation

---

## Design Philosophy

CampusArchive's visual design embodies the values of academic institutions: trust, professionalism, permanence, and accessibility. The interface balances modern web design principles with traditional academic aesthetics, creating a platform that feels both contemporary and enduring.

### Core Principles

**1. Academic Professionalism**
The design uses an institutional color palette (forest green, warm ivory, antique gold) that evokes trust, tradition, and scholarly excellence rather than consumer-focused bright colors.

**2. Content-First Layout**
Information hierarchy prioritizes project content, metadata, and discovery over decorative elements. Clean layouts with generous whitespace ensure readability.

**3. Accessibility**
High contrast ratios, semantic HTML, clear typography, and keyboard-navigable interfaces ensure the platform is usable by all students, faculty, and staff.

**4. Responsive Design**
Mobile-first CSS ensures the platform works seamlessly on smartphones, tablets, and desktop computers, accommodating diverse access scenarios (library computers, personal laptops, mobile devices).

**5. Visual Consistency**
Unified component library, predictable interaction patterns, and consistent spacing/typography create a cohesive experience across all pages.

---

## Visual Identity

### Color System

CampusArchive uses a sophisticated academic color palette with distinct light and dark modes.

#### Light Mode Colors

**Primary (Forest Green)**
- `--color-primary: #073B2B` — Primary brand color, buttons, accents
- `--color-primary-hover: #0A4634` — Hover state for interactive elements
- `--color-primary-light: #E7EEE7` — Light tint for backgrounds

**Accent (Antique Gold)**
- `--color-accent: #B8892F` — Highlight color for important elements, active states
- `--color-accent-hover: #C99A43` — Hover state for gold elements
- `--color-accent-light: #F1E4C8` — Light gold tint

**Background (Warm Ivory)**
- `--color-bg: #F7F3EA` — Page background (warm parchment-like ivory)
- `--color-bg-alt: #FBF9F3` — Alternative background shade
- `--color-surface: #FBF9F3` — Card and component surfaces
- `--color-surface-alt: #F3EEE3` — Alternate surface (hover states, table rows)

**Text**
- `--color-text: #073B2B` — Primary text (dark forest green, high contrast)
- `--color-text-muted: #5E675F` — Secondary text (muted gray-green)
- `--color-text-light: #8A877B` — Tertiary text (light gray)

**Borders**
- `--color-border: #DED2B9` — Standard borders (warm neutral tan)
- `--color-border-focus: #073B2B` — Focus state borders (forest green)

**Status Colors**
- Success: `#2D7A4E` (forest green for approved)
- Warning: `#B8892F` (gold for pending/needs revision)
- Danger: `#A23B32` (muted red for rejected)
- Info: `#276B64` (teal for informational)

#### Dark Mode Colors

**Primary (Deep Forest Green)**
- `--color-primary: #0B4A36` — Muted forest green for dark backgrounds
- `--color-primary-hover: #105D44` — Lighter hover state
- `--color-primary-light: rgba(184,137,47,.12)` — Translucent tint

**Accent (Bright Gold)**
- `--color-accent: #B8892F` — Gold accent (same as light mode)
- `--color-accent-hover: #D3A553` — Brighter gold hover
- `--color-accent-light: rgba(184,137,47,.18)` — Translucent gold tint

**Background (Dark Forest Green)**
- `--color-bg: #031C15` — Very dark forest green page background (almost black)
- `--color-bg-alt: #052219` — Alternative dark background
- `--color-surface: #06271D` — Card surfaces (dark green)
- `--color-surface-alt: #073B2B` — Alternate surfaces

**Text (Warm Ivory)**
- `--color-text: #F7F3EA` — Primary text (warm ivory, high contrast on dark)
- `--color-text-muted: #CFC4AA` — Secondary text (muted cream)
- `--color-text-light: #978F7C` — Tertiary text (light brown)

**Borders**
- `--color-border: #1C4A39` — Dark green borders
- `--color-border-focus: #B8892F` — Focus state uses gold accent

**Status Colors (Dark Mode Adjusted)**
- Success: `#79B58E` (lighter forest green)
- Warning: `#D3A553` (brighter gold)
- Danger: `#E58478` (coral red)
- Info: `#87BEB5` (seafoam teal)

### Color Usage Guidelines

**Backgrounds:**
- Page backgrounds: `--color-bg`
- Cards and panels: `--color-surface`
- Alternating table rows: `--color-surface-alt`
- Sidebar: `--sidebar-bg` (solid forest green in light, near-black in dark)

**Interactive Elements:**
- Primary buttons: `--color-primary` background, white text
- Secondary buttons: transparent background, `--color-primary` border and text
- Hover states: `--color-primary-hover` or `--color-accent-hover`
- Active/selected states: `--color-accent` (gold)

**Text Hierarchy:**
- Headings: `--color-text` (maximum contrast)
- Body text: `--color-text` (maximum contrast)
- Secondary text (meta info, captions): `--color-text-muted`
- Disabled text: `--color-text-light`

**Status Indicators:**
- Approved: Green badge with success color
- Pending: Gold/yellow badge with warning color
- Rejected: Red badge with danger color
- Needs Revision: Blue badge with info color

---

## Typography

### Font Stack

**Headings (Serif)**
- Font: `'Playfair Display', serif`
- Weights: 400 (regular), 600 (semi-bold), 700 (bold), 900 (black)
- Usage: Page titles, section headings, card titles, hero text
- Character: Editorial, traditional, academic

**Body Text (Sans-Serif)**
- Font: `'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif`
- Weights: 400 (regular), 500 (medium), 600 (semi-bold), 700 (bold), 800 (extra-bold)
- Usage: Paragraphs, UI labels, buttons, form inputs, navigation
- Character: Modern, clean, highly readable

### Type Scale

**Display (Hero Titles)**
- Size: `clamp(2.5rem, 5vw, 4rem)` (40px–64px)
- Weight: 900
- Font: Playfair Display
- Line height: 1.1
- Letter spacing: -0.02em

**H1 (Page Titles)**
- Size: `clamp(2rem, 4vw, 3rem)` (32px–48px)
- Weight: 900
- Font: Playfair Display
- Line height: 1.15
- Letter spacing: -0.02em

**H2 (Section Headings)**
- Size: `clamp(1.5rem, 3vw, 2rem)` (24px–32px)
- Weight: 800
- Font: Playfair Display
- Line height: 1.3

**H3 (Subsection Headings)**
- Size: `1.25rem` (20px)
- Weight: 700
- Font: Playfair Display
- Line height: 1.4

**Body Text**
- Size: `1rem` (16px)
- Weight: 400
- Font: Inter
- Line height: 1.6

**Small Text (Captions, Meta Info)**
- Size: `0.875rem` (14px)
- Weight: 500
- Font: Inter
- Line height: 1.5

**Tiny Text (Labels, Badges)**
- Size: `0.75rem` (12px)
- Weight: 600
- Font: Inter
- Line height: 1.4
- Transform: uppercase
- Letter spacing: 0.05em

---

## Layout System

### Navigation Layouts

#### Public Navigation (Navbar)
**Location:** Top of page  
**Height:** `80px`  
**Background:** `--color-surface` with subtle shadow  
**Effect:** Sticky positioning, backdrop blur (glass-morphism)

**Structure:**
```
[Logo] [Navigation Links]                    [Theme Toggle] [Sign In]
```

**Components:**
- Logo: SVG book icon + "CampusArchive" text (Playfair Display 800)
- Links: Home, Browse Projects, About (Inter 600)
- Theme toggle: Sun/moon icon button
- Auth button: "Sign In" or "Register" (Inter 600)

#### Authenticated Navigation (Sidebar)
**Location:** Left side of screen  
**Width:** `268px`  
**Background:** `--sidebar-bg` (solid forest green / near-black)  
**Behavior:** Fixed positioning on desktop, slide-out drawer on mobile

**Structure:**
```
[Logo]
─────
[Dashboard]
[My Projects]
[Submit Project]
─────
[Browse Archive]
[About]
─────
[Settings]
[Logout]
```

**Components:**
- Logo section: SVG icon + "CampusArchive" (Playfair Display 700, white text)
- Nav sections: Grouped by function with dividers
- Active state: Gold background (`--sidebar-active`)
- Hover state: Subtle gold tint (`--sidebar-hover`)
- Icons: Emoji icons for each menu item

### Grid System

**Max Container Width:** `1280px`–`1440px` (varies by page)  
**Horizontal Padding:** `48px` desktop, `24px` tablet, `20px` mobile  
**Vertical Padding:** `48px`–`96px` sections

**Grid Patterns:**

**Two-Column (Hero, Browse)**
```
Desktop:  [60% Content] [40% Image/Filters]
Tablet:   [100% Content] → [100% Image/Filters]
Mobile:   [100% Stack]
```

**Three-Column (Dashboard Stats)**
```
Desktop:  [33%] [33%] [33%]
Tablet:   [50%] [50%] → [100%]
Mobile:   [100%] stacked
```

**Four-Column (Stats Bar)**
```
Desktop:  [25%] [25%] [25%] [25%]
Tablet:   [50%] [50%] → [50%] [50%]
Mobile:   [100%] stacked
```

### Spacing Scale

**Base unit:** `4px`

**Scale:**
- `xs`: `4px` — Tight spacing (icon-to-text gaps)
- `sm`: `8px` — Small gaps (button padding)
- `md`: `16px` — Default gaps (between elements)
- `lg`: `24px` — Section spacing (between cards)
- `xl`: `32px` — Large spacing (between major sections)
- `2xl`: `48px` — Extra-large (section padding)
- `3xl`: `64px`+ — Hero section padding

---

## Component Library

### Buttons

**Primary Button**
- Background: `--color-primary`
- Text: white
- Padding: `12px 28px`
- Border radius: `10px`
- Font: Inter 600, 0.9rem
- Hover: Darker background + 1px lift (`translateY(-1px)`)
- Active: Pressed appearance

**Secondary Button**
- Background: transparent
- Border: `1.5px solid --color-primary`
- Text: `--color-primary`
- Padding: `11px 28px` (1px less to account for border)
- Hover: Light tint background

**Danger Button (Destructive Actions)**
- Background: `--color-danger`
- Text: white
- Same dimensions as primary

**Ghost Button (Subtle Actions)**
- Background: transparent
- Text: `--color-text-muted`
- No border
- Hover: Light background tint

### Cards

**Standard Card**
- Background: `--color-surface`
- Border: `1.5px solid --color-border`
- Border radius: `16px`
- Padding: `28px`
- Shadow: `0 2px 8px rgba(0,0,0,.04)`
- Hover: Enhanced shadow + 2px lift

**Project Card (Browse)**
- Same as standard card
- Header: Category badge + title (Playfair Display 800, 1.3rem)
- Body: Abstract snippet (2-3 lines truncated)
- Footer: Technology tags + metadata
- Gold accent bar appears on hover (top border, 4px)

**Stat Card (Dashboard)**
- Icon: Circular badge (48px–56px, gradient background, border)
- Number: Playfair Display 900, 2.5rem–2.75rem
- Label: Inter 600, 0.85rem, uppercase
- Hover: Gold accent bar + lift

### Forms

**Input Fields**
- Background: `--color-surface`
- Border: `1.5px solid --color-border`
- Border radius: `10px`
- Padding: `12px 16px`
- Font: Inter 400, 0.9rem
- Focus: `--color-border-focus` border + ring shadow (3px, low opacity)
- Hover: Border color intensifies

**Textarea**
- Same as input, but `min-height: 120px`
- Vertical resize only

**Select Dropdown**
- Same as input
- Custom dropdown arrow (SVG)
- Padding-right: `44px` (room for arrow)

**File Input**
- Dashed border: `2px dashed --color-border`
- Border radius: `12px`
- Padding: `32px 24px`
- Background: `--color-surface-alt`
- Icon: Upload icon (2.5rem, muted)
- Hover: Gold border + lift effect

**Checkbox/Radio**
- Custom styled with accent color
- Focus: Ring outline

### Tables

**Structure:**
- Header: `--color-surface-alt` background, bold uppercase labels
- Rows: Alternating subtle background on hover
- Borders: Light horizontal lines between rows
- Padding: `18px 20px` cells

**Header:**
- Font: Inter 700, 0.8rem, uppercase
- Letter spacing: 0.08em
- Border-bottom: `2px solid --color-border`

**Hover State:**
- Row background: Light gold tint (`rgba(184, 137, 47, 0.04)`)
- Cursor: pointer

### Badges

**Status Badge**
- Padding: `5px 12px`
- Border radius: `20px` (pill shape)
- Font: Inter 600, 0.75rem, uppercase
- Letter spacing: 0.04em

**Variants:**
- Approved: Green background + dark green text
- Pending: Yellow/gold background + brown text
- Rejected: Red background + dark red text
- Needs Revision: Blue background + dark blue text

**Tag Badge (Technology)**
- Padding: `6px 14px`
- Background: Light green tint
- Border: `1px solid` (darker green)
- Border radius: `20px`
- Hover: Darker background + lift

### Navigation Links

**Public Nav Links:**
- Font: Inter 600, 0.9rem
- Padding: `10px 18px`
- Border radius: `8px`
- Hover: Light background tint
- Active: Gold gradient background + border

**Sidebar Nav Links:**
- Font: Inter 600, 0.875rem
- Padding: `10px 20px`
- Color: `--sidebar-text` (cream/ivory)
- Icon: Left-aligned emoji
- Hover: `--sidebar-hover` (gold tint)
- Active: `--sidebar-active` (gold background) + bold text

### Modals and Dialogs

**Overlay:**
- Background: `rgba(0, 0, 0, 0.5)` (semi-transparent black)
- Backdrop blur: `4px`

**Modal Card:**
- Background: `--color-surface`
- Border radius: `16px`
- Padding: `32px`
- Max-width: `600px`
- Shadow: `--shadow-lg`
- Animation: Fade + scale in

**Header:**
- Title: Playfair Display 800, 1.5rem
- Close button: Top-right corner (×)

### Toast Notifications

**Position:** Top-right corner (fixed)  
**Appearance:** Slide in from right  
**Duration:** 4 seconds auto-dismiss  

**Structure:**
- Background: Status color (success/danger/info/warning)
- Text: White
- Border radius: `10px`
- Padding: `14px 18px`
- Shadow: `--shadow-md`
- Close button: × icon

**Variants:**
- Success: Green background
- Error: Red background
- Warning: Gold background
- Info: Teal background

### Error Pages

**Layout:**
- Centered vertically and horizontally
- Max-width: `540px`

**Icon:**
- Size: `6rem`
- Opacity: `0.5`
- Animation: Floating (subtle up-down motion)

**Title:**
- Font: Playfair Display 900, 2.5rem
- Text: "404 — Page Not Found" format

**Description:**
- Font: Inter 400, 1.05rem
- Line height: 1.7

**Actions:**
- Primary button: "Return Home"
- Secondary button: "Browse Projects" (if applicable)

---

## Responsive Design

### Breakpoints

```css
/* Mobile-first approach */
/* Small mobile: < 480px */
@media (max-width: 480px) {
  - Single column layouts
  - Reduced font sizes (2rem headings)
  - Full-width buttons
  - Stacked navigation
}

/* Mobile: 481px – 768px */
@media (max-width: 768px) {
  - Two-column grids where appropriate
  - Sidebar becomes drawer
  - Reduced padding (24px)
}

/* Tablet: 769px – 1024px */
@media (max-width: 1024px) {
  - Three-column grids
  - Sidebar static (not sticky)
  - Moderate padding (32px)
}

/* Desktop: 1025px+ */
/* Default styles, full layouts */
```

### Mobile Adaptations

**Navigation:**
- Public navbar: Hamburger menu for links
- Sidebar: Slide-out drawer with overlay

**Forms:**
- Inputs: Larger touch targets (min 44px height)
- File uploads: Simplified UI
- Buttons: Full-width on mobile

**Cards:**
- Single column grid
- Reduced padding (20px)

**Tables:**
- Horizontal scroll wrapper
- Reduced column count (hide non-essential)

**Hero Sections:**
- Stacked layout (content → image)
- Reduced text size
- Simplified CTA layout

---

## Accessibility

### Implemented Features

**Semantic HTML:**
- Proper heading hierarchy (H1 → H2 → H3)
- `<nav>`, `<main>`, `<article>`, `<section>` elements
- Form labels associated with inputs

**Keyboard Navigation:**
- All interactive elements focusable via Tab
- Focus indicators visible (ring outline)
- Logical tab order
- Enter/Space activates buttons

**Screen Reader Support:**
- ARIA labels for icon-only buttons
- `role` attributes for custom components
- `aria-label` for navigation regions

**Color Contrast:**
- Light mode: Dark green text on ivory background (WCAG AAA)
- Dark mode: Ivory text on dark green background (WCAG AAA)
- Status badges: High contrast text

**Focus States:**
- Visible ring outline: `0 0 0 3px rgba(7, 59, 43, 0.1)`
- Color: `--color-border-focus`

**Forms:**
- Labels visible for all inputs
- Error messages in proximity to fields
- Required fields marked

---

## Theming

### Theme Toggle

**Location:** Navigation bar (top-right)  
**Icon:** Sun (light mode) / Moon (dark mode)  
**Persistence:** `localStorage.ca-theme`  
**Default:** System preference (`prefers-color-scheme`)

**Implementation:**
```javascript
// theme.js
localStorage.setItem('ca-theme', 'light' | 'dark');
document.documentElement.setAttribute('data-theme', theme);
```

**CSS Approach:**
```css
:root, [data-theme="light"] { /* light mode colors */ }
[data-theme="dark"] { /* dark mode colors */ }
```

### Theme Variables

All colors, shadows, and radii defined as CSS custom properties:
- Instant theme switching (no reload)
- Consistent across all components
- Easy maintenance

---

## Animation and Transitions

### Micro-Interactions

**Standard Transition:**
```css
transition: all 0.2s ease;
```

**Hover Effects:**
- Buttons: Background darken + 1px lift
- Cards: Shadow enhance + 2px–4px lift
- Links: Background tint

**Loading States:**
- Skeleton screens (pulsing gray rectangles)
- Spinner: Rotating circle (CSS animation)

**Error Page Icons:**
- Floating animation:
  ```css
  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }
  ```

**Page Transitions:**
- Flash messages: Fade in from top
- Toasts: Slide in from right
- Modals: Fade + scale in

---

## Design System Maintenance

### File Structure

```
static/css/
├── themes.css    # Color variables, theme definitions
└── style.css     # Component styles, layouts
```

### Adding New Colors

1. Define in `themes.css` for both themes
2. Use CSS custom property: `var(--new-color)`
3. Document usage in this file

### Adding New Components

1. Design component following existing patterns
2. Implement in `style.css`
3. Test in both light and dark modes
4. Verify keyboard navigation and screen reader
5. Document in this file

---

## Design Credits

**Color Palette:** Custom academic palette inspired by traditional university branding  
**Typography:** Playfair Display (Google Fonts), Inter (Google Fonts)  
**Icons:** Unicode emoji (cross-platform compatibility)  
**Inspiration:** Institutional archives, library systems, academic journals

---

**CampusArchive Design System** — Built for the Kiro Buildathon, August 2026
