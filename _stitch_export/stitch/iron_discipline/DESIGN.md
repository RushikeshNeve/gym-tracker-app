# Design System: High-Discipline Accountability

## 1. Overview & Creative North Star
**The Creative North Star: "The Obsidian Monolith"**

This design system is built for the uncompromising. It rejects the "busy" clutter of traditional fitness apps in favor of a high-end, editorial experience that mirrors the discipline of the '75 Hard' challenge. The aesthetic is "Obsidian Monolith"—a UI that feels carved out of dark volcanic glass, where information is illuminated only when essential. 

We break the "standard app" template by utilizing **intentional asymmetry** and **high-contrast typography scales**. Large, aggressive metric displays are paired with generous breathing room (white space) to create a sense of focus and mental clarity. By overlapping elements and using varied tonal depths, we create a signature look that feels premium, authoritative, and custom-tailored for peak performance.

---

## 2. Colors & Surface Logic

The palette is rooted in a deep, near-black foundation, using high-intensity neon accents to signal success and urgency.

### Surface Hierarchy & Nesting
To achieve a "bespoke" feel, we move away from flat layouts. We treat the UI as a series of physical layers.
- **Base Level:** `surface` (#0E0E0E) – The foundation.
- **Section Level:** `surface-container-low` (#131313) – Large structural areas.
- **Component Level:** `surface-container` (#1A1919) – For standard cards and modules.
- **Focus Level:** `surface-container-highest` (#262626) – For elements requiring immediate attention.

### The "No-Line" & "Glass" Rules
*   **The No-Line Rule:** Do not use 1px solid borders to separate sections. Boundaries must be defined through background color shifts. For example, a `surface-container-low` card sits on a `surface` background without a stroke.
*   **Glassmorphism:** For top navigation and floating action bars, use `surface` at 60% opacity with a `20px` backdrop blur. This allows the primary colors of progress rings to bleed through, softening the interface.
*   **Signature Textures:** For high-value actions, use a subtle gradient from `primary` (#9CFF93) to `primary-container` (#00FC40).

---

## 3. Typography
We utilize a dual-font system to balance "High-Performance Data" with "Clean Readability."

| Role | Font Family | Token | Use Case |
| :--- | :--- | :--- | :--- |
| **Display** | Manrope (Bold) | `display-lg` (3.5rem) | Day counters, "75" streak numbers. |
| **Headline** | Manrope (Semibold) | `headline-lg` (2.0rem) | Page titles, "Daily Checklist." |
| **Title** | Inter (Medium) | `title-md` (1.125rem) | Section headers, card titles. |
| **Body** | Inter (Regular) | `body-md` (0.875rem) | Instructional text, notes. |
| **Label** | Inter (Bold) | `label-md` (0.75rem) | Small caps for metrics (e.g., "GALLONS"). |

**Editorial Strategy:** Use `display-lg` for large, center-aligned numbers to create a sense of scale and accomplishment. Body text should remain compact and tucked away to keep the focus on the data.

---

## 4. Elevation & Depth
In this system, depth is a function of **Tonal Layering**, not shadows.

*   **The Layering Principle:** Place a `surface-container-lowest` card on a `surface-container-low` section to create natural lift.
*   **Ambient Shadows:** If a floating effect is required (e.g., a "Complete Day" button), use a shadow with a 40px blur at 8% opacity, tinted with `primary` (#9CFF93) rather than black.
*   **The Ghost Border:** For accessibility, you may use `outline-variant` (#484847) at **15% opacity**. Never use 100% opaque borders; they break the "Obsidian" immersion.

---

## 5. Components

### Buttons & Interaction
*   **Primary Action:** Rectangular with `lg` (2rem) corner radius. Use the `primary` color (#9CFF93). Text should be `on-primary` (#006413) in Inter Bold.
*   **Secondary/Ghost:** Use `outline` tokens at 20% opacity. No fill.
*   **Checkboxes:** These are the heart of the app. When "Checked," use `primary_container` (#00FC40). When unchecked, use a high-contrast `surface-container-highest` (#262626).

### Cards & Data Lists
*   **The "No-Divider" Rule:** Never use horizontal lines to separate list items. Use `spacing-4` (1.4rem) of vertical space or a subtle shift to `surface-container-low` for every other item.
*   **Progress Rings:** Use `secondary` (#15A4FF) for "Water Intake" and `primary` (#9CFF93) for "Workout Completion." Stroke width should be thick (8px+) to feel "heavy" and disciplined.

### The "Streak" Component (Signature)
A bespoke component showing 75 small dots. Completed days use `primary`; current day uses `tertiary` (#FFD16F) with a pulse animation; failed days use `error` (#FF7351).

---

## 6. Do’s and Don’ts

### Do
*   **Do** use asymmetrical margins. For example, a headline might have a `spacing-8` left margin but a `spacing-12` right margin to create an editorial feel.
*   **Do** embrace "Empty Space." A premium feel is achieved when elements have room to breathe.
*   **Do** use `tertiary` (#FFD16F) sparingly—only for things that are "Pending" or "In-Progress."

### Don't
*   **Don't** use pure white (#FFFFFF) for body text. Use `on-surface-variant` (#ADAAAA) to reduce eye strain in dark mode.
*   **Don't** use standard "Material Design" shadows. They feel cheap and "out of the box."
*   **Don't** use rounded corners smaller than `md` (1.5rem) for main containers. Sharp corners feel "generic"; our `lg` (2rem) and `xl` (3rem) corners feel custom and modern.