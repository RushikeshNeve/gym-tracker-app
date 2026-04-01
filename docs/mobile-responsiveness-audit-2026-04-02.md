# Mobile Responsiveness Audit - 2026-04-02

## Scope
- Device profile: iPhone 12 viewport via Playwright
- Base URLs tested: `/today`, `/dashboard`, `/workouts`, `/workout-timetable`, `/nutrition`, `/hydration`, `/body-metrics`, `/cardio`, `/progress`, `/progress-photos`, `/exercise-library`, `/weekly-review`
- Sources used:
  - Playwright screenshots saved under `mobile-audit/scripted`
  - DOM/overflow report in `mobile-audit/scripted/report.json`
  - Page/component code under `frontend/src`

## Executive Summary
The app is partially mobile-friendly already because most pages collapse into a single column, but mobile quality is inconsistent. The main issues are:
1. Shared mobile navigation labels overflow and feel cramped on every tab.
2. Some shared header/card patterns stay too horizontal on phones, which makes action areas feel squeezed.
3. The workout page produces horizontal overflow on mobile and is the least stable layout.
4. The body-metrics page is currently broken entirely because of a hooks-order bug.
5. Most remaining tabs are usable, but they need smaller spacing, better header stacking, and safer action wrapping to feel native on phones.

## Route-by-Route Findings

### `/today`
- Status: Usable on mobile.
- Good:
  - Hero collapses into a readable single column.
  - Checklist and summary cards stack cleanly.
- Issues:
  - Bottom mobile nav labels are too long and overflow/truncate.
  - Some card header rows are tight when status chips and text sit together.

### `/dashboard`
- Status: Usable, but dense.
- Good:
  - Main dashboard stacks into one column.
  - KPI grid and section flow are readable.
- Issues:
  - Chart value labels are cramped on narrow widths.
  - Hero summary/action panel is visually wide and should stack more gently.
  - Bottom nav overflow repeats here too.

### `/workouts`
- Status: Problematic on mobile.
- Good:
  - Main sections exist in the right order for a phone workflow.
- Issues:
  - Horizontal overflow detected (`docScrollWidth` wider than client width).
  - Section header actions are too wide for mobile.
  - Hero summary and multi-button toolbars are crowded.
  - This is the most important page to optimize because it is primary task flow.

### `/workout-timetable`
- Status: Generally usable.
- Good:
  - Showing only the selected day is much better for mobile than rendering all days.
- Issues:
  - Weekly split selector and block cards can feel busy.
  - CTA/action areas should wrap more cleanly on small screens.
  - Bottom nav overflow repeats here too.

### `/nutrition`
- Status: Usable but very long.
- Good:
  - Single-column stacking works.
  - Meal options, AI analysis, timeline, and detail panel all render.
- Issues:
  - Page is extremely tall on mobile and relies on long scroll.
  - Several action/button clusters would benefit from more deliberate stacking.
  - Shared card/header spacing is a bit oversized for phone usage.

### `/hydration`
- Status: Usable.
- Good:
  - Quick-add and history stack cleanly.
- Issues:
  - Shared header/card patterns still feel a little oversized.

### `/body-metrics`
- Status: Broken.
- Issues:
  - React hooks-order violation crashes the page: `Rendered more hooks than during the previous render.`
  - This is not only a responsiveness issue; it blocks use entirely on mobile and desktop.

### `/cardio`
- Status: Usable.
- Good:
  - Form stacks well.
  - Presets/history remain readable.
- Issues:
  - Shared section header and nav issues remain.

### `/progress`
- Status: Usable but long.
- Good:
  - Sections collapse into a vertical analytics feed.
- Issues:
  - Very long page on mobile.
  - Shared nav/header spacing issues remain.

### `/progress-photos`
- Status: Usable.
- Good:
  - Upload/comparison/gallery sections stack acceptably.
- Issues:
  - Console warning for duplicate React keys (not mobile-specific, but should be fixed later).
  - Shared nav/header spacing issues remain.

### `/exercise-library`
- Status: Usable but dense.
- Good:
  - Search and filter flow is available on mobile.
- Issues:
  - The filter chip wall is visually heavy on small screens.
  - Shared nav/header/card spacing issues remain.

### `/weekly-review`
- Status: Usable.
- Good:
  - Summary, reflection cards, and editor stack correctly.
- Issues:
  - Shared action/header wrapping should be improved.

## Shared Component Findings
- `MobileNav`
  - Long labels (`Dashboard`, `Log Workout`, `Exercise Library`) overflow/truncate on a phone-width footer nav.
- `SectionCard`
  - Header is always a horizontal row, which is fragile on mobile when the `action` area contains buttons or chips.
- `PageHeader`
  - Large desktop-style title/action balance works, but mobile needs smaller title sizing and better action stacking.
- `Card`
  - Padding is slightly too generous on mobile for data-entry-heavy screens.
- `QuickActionStrip`
  - Works conceptually, but buttons should be more mobile-first in width and alignment.

## Fix Plan
1. Stabilize shared mobile layout primitives.
   - Make section headers stack on mobile.
   - Reduce card/header padding on small screens.
   - Make page header actions full-width on mobile.
   - Tighten app-shell spacing.
2. Fix mobile navigation.
   - Shorten labels and prevent footer nav overflow.
3. Repair the body-metrics crash.
   - Move hooks so render order is stable.
4. Fix workout-page overflow and density.
   - Make action groups wrap.
   - Remove wide mobile-only minimum widths.
   - Stack controls and buttons more safely.
5. Improve chart/readability and other shared dense sections.
   - Tighten chart spacing/font sizes for mobile.
   - Let common action groups wrap instead of forcing horizontal layouts.
6. Re-test all tabs in mobile viewport after implementation.

## Success Criteria
- No horizontal overflow on core routes.
- No crashes on `Body Metrics`.
- Primary tabs remain readable and tappable on iPhone-width screens.
- Shared headers/cards/actions feel intentionally designed for mobile, not just collapsed from desktop.
