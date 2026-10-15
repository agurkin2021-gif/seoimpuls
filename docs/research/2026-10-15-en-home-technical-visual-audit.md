# SEOImpuls — English homepage technical and visual control audit (2026-10-15)

Scope: English homepage / on branch white-seo-rebuild, plus *read-only* verification of destinations and templates. **No changes to production seoimpuls.com or RU/ES.**

## Reproducible evidence
- GitHub Actions run: https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38823101622 — PASS, Chromium Playwright on production-base Hugo build, tested 390×844 and 1280×800 CSS px. Audit artifact: seoimpuls-en-home-390-1280, contains six screenshots and audit.json.
- The live GitHub Pages preview was separately checked using Opera; its correct /seoimpuls/ internal routing had been verified previously. The automated screenshots run against local production-base Hugo build, not against the public Pages URL.
- Original runs #38822048771 and #38822499202 were affected by an *audit-script* bug parsing bare `href="#"`; corrected in f928b245 and subsequent run #38823101622 passed.

## Confirmed PASS in Chromium
| Check | 390px | 1280px |
|---|---|---|
| Homepage HTTP | 200 | 200 |
| H1 count and text | 1, Professional SEO Services | same |
| Title | Professional SEO Services \| SeoImpuls | same |
| Canonical | https://seoimpuls.com/ | same |
| HTML language | en-US | en-US |
| horizontal scroll overflow | none, scrollWidth=390 | none, scrollWidth=1272, viewport=1280 |
| broken images | 0 of 4 | 0 of 4 |
| internal URL HTTP errors | 0 of 13 | 0 of 13 |
| browser page errors / failed requests | 0 / 0 | 0 / 0 |
| JSON-LD parse errors | 0 | 0 |
| cookie consent dismissal | works | works |
| footer layout | static at page end (intended mobile) | position fixed; `footer-floating` on scroll, `footer-popup-visible` after idle |

- Four images loaded: header WebP logo plus three decorative SVGs with empty alt because adjacent text names the service.
- Valid JSON-LD root types: WebSite, BreadcrumbList. Syntax validity is not equivalent to Google Rich Results eligibility.
- H2/H3 hierarchy is coherent: delivery process, two service-card H3s, service scope, outcomes and three outcome H3s, enquiry.
- Hreflang emitted: en-us (root), es-es (/es/), ru-ru (/ru/), x-default (root). Full reciprocal translation intent/canonical audit **not performed**, as RU/ES are currently out of project scope.
- Page uses `robots=index,follow,max-image-preview:large` for the production-base build; GitHub Pages preview separately injects `noindex,nofollow`.
- Open Graph title and description render. Standard HTML description is emitted as `<meta name="Description" ...>` by `layouts/partials/head/meta.html`; this is an ASCII case variant, not a missing meta element. Initial Playwright selector was incorrectly case-sensitive; corrected in the later audit harness commit to use a case-insensitive attribute selector. Actual value should be checked in that rerun.

## Visual observations from screenshots
- 390px: logo, collapsed mobile navigation, H1 wraps into two lines, two full-width CTA buttons. Services and outcomes use one-column layout with no horizontal scroll. Page full height approx. 3686px.
- 1280px: H1 fits one line; process and two service cards arranged as intended. Service areas have two columns and outcomes three columns. No image placeholders or broken blocks.
- Cookie consent banner on **390×844** occupies a ~370×295px rectangle at bottom (~35% of viewport height), covering the lower first-screen content until dismissed. All three action buttons are visible and rejection succeeds. This is a **P2 UX observation**, not a blocking usability defect.
- Desktop consent banner occupies 940×167px and covers part of first-screen process/cards until dismissed; action controls remain visible.
- Desktop footer animates after scroll/idle; mobile footer stays at the page end. No overlap or content clipping detected *after cookie dismissal* in the screenshots.
- Potential P2 visual polish: lower CTA primary-button text appears less legible than the secondary button in screenshot. **Color contrast not instrumentally measured**, so WCAG failure is unproven. Also there is some lower-page whitespace before legal strip on desktop; verify design intent before touching.

## Still not verified — do not mark site final
1. Google real country/device organic SERP top-10, query difficulty and GSC historical impressions/clicks — SERP_UNVERIFIED / GSC_PENDING.
2. CrUX field Core Web Vitals (LCP, INP, CLS) and Lighthouse numeric lab values. The screenshot/DOM audit is not a performance certification.
3. Keyboard-only navigation and objective WCAG color contrast/focus indicators at both viewports.
4. Hreflang reciprocity/equivalence against future rebuilt RU and ES localizations.
5. Live `seoimpuls.com` production deployment, actual production redirects and index status — untouched.

## Severity and next action
- **P0 (blocking visual/technical):** none confirmed at 390 or 1280 in the tested build.
- **P1:** no confirmed broken HTML/routes/images/JS; SEO release remains gated by missing GSC/SERP and real-user metrics, not by a specific visual crash.
- **P2:** consent banner first-screen obstruction (dismissable), unmeasured final CTA contrast, desktop lower-page spacing.
- Continue EN-home only. Before production publication perform GSC/SERP, field CWV and keyboard/contrast checks; avoid speculative redesign of currently passing elements.
