# Design System Document: The Analog HUD

## 1. Overview & Creative North Star
The Creative North Star for this design system is **"The Analog HUD."** 

This system rejects the sterile, flat nature of modern utility apps in favor of a "Tactical Softness." We are aiming for the tactile precision of a vintage high-end synthesizer crossed with the advanced legibility of a near-future Augmented Reality interface. By pairing hyper-modern "Space Grotesk" and "Inter" typography with pixelated iconography and extreme corner radii, we create a visual tension that feels both nostalgic and cutting-edge. 

To move beyond the "template" look, designers must embrace **intentional asymmetry** and **tonal depth**. Layouts should feel like a series of projected modules rather than a rigid grid. Overlapping elements and layered transparencies are encouraged to simulate the depth of a multi-lens optical display.

---

## 2. Colors: Tonal Depth over Structural Lines
The palette is rooted in a deep charcoal foundation (`#131313`) punctuated by a desaturated, "aged" yellow (`#D4C483`). This is not a high-contrast "construction" yellow; it is a muted, sophisticated gold that suggests high-end instrumentation.

### The "No-Line" Rule
**Explicit Instruction:** You are prohibited from using 1px solid borders to define sections or containers. 
Boundaries must be created through background color shifts. For example, a `surface-container-low` component should sit directly on a `surface` background. The change in hex code is the border. This creates a "soft" transition that feels organic to an AR display.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers. Use the `surface-container` tiers to define "Z-space":
- **Base Layer:** `surface` (#131313)
- **Primary Modules:** `surface-container-low` (#1c1b1b)
- **Nested Controls:** `surface-container-high` (#2a2a2a)
- **Active Overlays:** `surface-container-highest` (#353534)

### The "Glass & Gradient" Rule
To achieve a premium HUD feel, use **Glassmorphism** for floating panels. Apply a `surface-variant` color at 60% opacity with a `20px` backdrop blur. 
**Signature CTA Texture:** For primary buttons or critical HUD readouts, apply a subtle linear gradient from `primary` (#f1e09c) to `primary_container` (#d4c483) at a 135-degree angle. This adds "soul" to the component that a flat hex code cannot achieve.

---

## 3. Typography: The Tactical Mix
We utilize a high-contrast typographic pairing to reinforce the "Retro-Soft" aesthetic.

- **Display & Headlines (Space Grotesk):** This is our "Technical" voice. For headlines, use `headline-lg` or `headline-md`. To lean into the retro-game feel, use **All-Caps** with a letter-spacing of `0.05rem`. This mimics the look of pixel-font readouts while maintaining the premium legibility of a modern sans-serif.
- **Labels & Micro-copy (Space Grotesk):** Small labels (`label-sm`) should be treated like data-points in a cockpit—highly legible, uppercase, and often colored in `primary` to denote interactive or status-driven data.
- **Body & Titles (Inter):** For long-form modding instructions or descriptions, use `body-md`. Inter provides the "Modern" half of the system, ensuring the UI doesn't feel like a toy.

---

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows are often too heavy for a dark theme. Instead, we use **Tonal Layering**.

- **The Layering Principle:** Depth is achieved by "stacking." A `surface-container-lowest` card placed on a `surface-container-low` section creates a natural "recessed" effect.
- **Ambient Shadows:** When an element must float (like a modal or tooltip), use an extra-diffused shadow: `Y: 20px, Blur: 40px, Color: #000000 (8% opacity)`. This simulates ambient occlusion rather than a harsh light source.
- **The "Ghost Border" Fallback:** If an element lacks sufficient contrast (e.g., in high-glare AR simulations), use a "Ghost Border": the `outline-variant` token at **15% opacity**. Never use 100% opacity for lines.
- **Soft Roundness:** Every container—unless it is a full-screen background—must use the `xl` (3rem) or `lg` (2rem) roundedness scale. This "pill-like" geometry softens the tactical nature of the dark theme.

---

## 5. Components

### Buttons
- **Primary:** High-roundness (`full`), background `primary`, text `on_primary`. No border.
- **Tertiary:** `label-md` typography in `primary` color, no background. Use for low-priority HUD actions.
- **States:** On hover, primary buttons should shift to `primary_fixed_dim`. Use a `0.2s` ease-in-out transition to mimic a powering-up filament.

### HUD Chips
- Used for mod categories or status tags. 
- **Style:** Background `surface-container-highest` with `label-sm` (Space Grotesk, All-Caps). Use a leading "pixel" (a 4x4px square) in `primary` to indicate selection.

### Modding Input Fields
- **Style:** A `surface-container-low` background with a `DEFAULT` (1rem) corner radius. 
- **Focus State:** Instead of a border, use a 1px `primary` underline or a subtle `primary` outer glow (4px blur, 10% opacity).
- **Icons:** All icons must be pixel-inspired but "refined"—avoid jagged edges; use a consistent 2px stroke width to match the typography's weight.

### Cards & Lists
- **The "No Divider" Rule:** Forbid the use of line dividers between list items. Instead, use a `spacing-4` (0.9rem) vertical gap or alternating subtle background shifts between `surface-container-low` and `surface-container-lowest`.

### Progress Gauges (AR Specific)
- Horizontal bars using `primary_container` for the track and `primary` for the fill. The fill should have a slight "glow" effect using a `0 0 10px` blur of the primary color.

---

## 6. Do's and Don'ts

### Do:
- **Do** use `spacing-16` and `spacing-20` for generous padding around modules to create an "Editorial" feel.
- **Do** overlap elements (e.g., a floating pixel icon slightly breaking the boundary of its container) to create depth.
- **Do** use `primary` sparingly. It is a "tactical light"; if everything is yellow, nothing is important.

### Don't:
- **Don't** use pure white (#FFFFFF). All "white" text should be `on_surface` (#e5e2e1) to prevent eye strain in dark environments.
- **Don't** use sharp corners. Sharp corners break the "Retro-Soft" immersion.
- **Don't** use standard Material Design ripples. Use subtle opacity fades (100% to 70%) for interaction feedback.