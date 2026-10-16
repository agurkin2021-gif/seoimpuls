# EN homepage palette, hierarchy, and contrast audit — 2026-10-16

## Scope and observed preview
- Branch: `white-seo-rebuild`, previous head `597fbc5f289b55bc6f3a2e76a944f216f185fe5e`.
- Inspected the English homepage via Opera Browser Connector at `https://agurkin2021-gif.github.io/seoimpuls/` (hero; service-card index; bottom CTA; fixed footer). This is a noindex development preview, not production.
- No assumptions about conversions from hue alone: color association is contextual. Here, emphasis is judged through CTA consistency, visual salience, information hierarchy, and contrast.

## Current palette and objective checks
- Page backdrop: #070b14, hero #07101f, service cards #0a1b2e; section hierarchy remains dark blue/graphite, restrained and visually coherent.
- Main heading #f1f5fb on #07101f = 17.40:1; introductory text #b8cadd on #07101f = 11.36:1.
- Services description #bed0de on #0a1b2e = 10.97:1; service label #91aec0 on #0a1b2e = 7.46:1; service link #83d5e2 on #0a1b2e = 10.40:1.
- Hero primary button #071321 on #59c1d0 = 8.86:1; bottom primary originally white on #1f739f = 5.24:1. Both exceeded AA 4.5:1, but the unrelated backgrounds/text colors diminished the single-primary-action hierarchy.
- Contrast figures use the WCAG sRGB relative-luminance formula for opaque CSS values; they are not a substitute for every browser-composited/state check.

## Finding, adjustment, and limits
1. Keep restrained navy surfaces and light copy. A larger palette change is not supported by a readability or UX defect in screenshots.
2. Use the same teal primary CTA with dark lettering and equivalent outlined secondary CTA across hero and closing contact block, with EN-only CSS custom properties. The bottom primary action is now visually the same action class as the first-screen primary action.
3. Retain WhatsApp green and Telegram blue as service-brand identifiers in fixed footer. Those are functional recognizable icons, not competing content-section semantic colors.
4. Add a visible 3px keyboard focus outline for hero and contact action buttons.
5. Do not repaint icons, alter content, spacing, header/footer, localized pages, or production. Verify mobile widths, keyboard focus, and post-change browser rendering after GitHub Actions. Pre-existing hero rail test may still fail on inner-vs-outer measurements; treat separately.

## Status
Design decision and CSS edit prepared, not yet QA accepted. Await strict Hugo/preview and actual browser checks on new preview commit.

## Runtime finding and corrective follow-up
- Opera test of initial normalization candidate `61a6cfef10` showed the contact CTA's real text was WHITE, not the proposed dark color, due to a stronger legacy EN-only visited/hover/focus rule declaring `color:#fff!important`.
- That rendered combination #ffffff on #59c1d0 = **2.11:1**, below 4.5:1 for normal text. Corrective patch changes the old rule to `var(--seo-en-action-fg,#071321)!important`, maintaining 8.86:1 across link states, and disables a global ::after neon halo for the closing panel buttons.
- New candidate requires Pages and Opera recheck; previous contrast 8.86:1 was an *intended* CSS combination, not the initial candidate's effective rendering.
