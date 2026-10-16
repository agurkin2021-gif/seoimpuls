# SEOImpuls English homepage — consistent content rail

Date: 2026-10-16. User identified uneven widths and the left edges of the header, Home breadcrumb, main sections and footer. The source previously used incompatible padding values: desktop content 120px versus header 18px, breadcrumb 34px and footer 32px (confirmed with Playwright on the exact generated HTML).

## Corrective layout
- Establish one centered 1280px max-width shell for the EN homepage only.
- Use the same content inset for header/logo, Home breadcrumb, all regular page sections and footer contacts: 32px wide screens, 24px tablet, 18px phone. Inset bordered process/contact surfaces start on the same rail as the service cards; headings inside those bordered surfaces intentionally retain interior padding.
- Eliminate extra negative margins and the old 120px EN content offset that made middle sections appear narrower.
- Scope all CSS to the `en` homepage conditional in `layouts/index.html`; do not edit global templates or RU/ES sources.
- Preserve seven service cards, hero SVG, contents, routes and commercial claims.

## Acceptance
Browser must confirm equal x-coordinates for header brand, Home breadcrumb, hero/services/section headings, process and contact borders, and footer contacts (±2px), plus matched right rail at 390, 768, 1280 and 1600px. Require strictly passing Hugo, browser screenshots and WCAG diagnostic, plus a manual check of the published noindex preview. A screenshot without DOM-coordinate checks does not prove alignment.
