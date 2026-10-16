# SeoImpuls EN homepage — control audit after responsive service-card changes
Date: 2026-10-16
Audited: / on GitHub Pages preview https://agurkin2021-gif.github.io/seoimpuls/
Branch HEAD at audit: 98763ec (docs-only). Unchanged site source: 00881d5.
Scope: READ-ONLY English homepage + links to three English service destinations. No code, live server or other pages modified.

## Evidence
- Source: content/_index.md, layouts/index.html, hugo.toml, footer/consent templates, direct-route verification scripts.
- Actual GitHub Pages preview accessibility tree: current 3 service options and entire EN homepage copy inspected.
- Screenshots: Chrome Actions #38914027320, artifact #12052215561 (390/768/1280 initial/services/full images) downloaded and visually inspected.
- Green CI against unchanged page source:
  - Hugo + strict whitehat #38914027341 PASS
  - GitHub Pages noindex preview #38914027471 PASS
  - EN 3 direct services Chromium 390/768/1280 #38914027320 PASS
  - EN general homepage browser #38914027575 PASS
  - axe automated accessibility #38914027393 PASS gate (incomplete cases exist)
  - same-commit context guard #38914027698 PASS

## Technical SEO and route integrity — PASS
- EN homepage H1 = Professional SEO Services; Title = Professional SEO Services | SeoImpuls; self-canonical = https://seoimpuls.com/ (production-base build).
- Visible description and social meta, WebSite + Organization JSON-LD parse correctly; staging preview is intentionally noindex/nofollow.
- Services menu + hero CTA reach /#services. Exactly three direct commercial pages:
  1. /technical-seo-audit/ (Technical SEO Audit H1/Title);
  2. /keyword-research/ (Keyword Research H1/Title);
  3. /seo-consultation/ (SEO Consultation H1/Title).
  Child URL/Title/H1/canonical, WebPage and BreadcrumbList JSON-LD, reciprocal hreflang and old English URL retirement passed the CI. No separate /seo-services/ catalog in generated output.
- 3 numbered custom CSS card icons 01/02/03: squares 38×38 px at 390 and 768, 46×46 at 1280. Zero <img> within any of the 3 main service cards.
- Chromium at all 3 widths: no broken internal links, JavaScript/network errors, horizontal overflow or detected intersection between fixed WhatsApp/Telegram icon bounds and homepage readable text. Service anchor remained clear of header.
- Current EN homepage has exactly 2 ordinary image requests in QA: SeoImpuls tight logo and one *old* decorative /uploads/seo-icon-google.svg in the supplementary service scope section. No claim of field performance or real search rankings.

## Findings — content and conversion gaps

### P1: Eight secondary scope cards recreate a confusing services menu
After 3 clear primary offers, 'What Our SEO Services Cover' displays eight equal-looking tiles: Technical SEO/indexing, On-page SEO, Keyword research, Content strategy, Site architecture, Performance/usability, International SEO, Implementation/measurement. A non-SEO buyer may treat them as eight separately sold services, while there are only 3 dedicated offers. This is an offer-clarity problem, NOT evidence of URL-level keyword cannibalization.
Action: combine overlapping tasks under the 3 actual services or compact into a short 'what may be included' explanatory block. No artificial new sales pages.

### P1: Website-only language conflicts with independent keyword research
Several visible fragments assume an existing site: 'We select the work that fits your website and goals', 'Discuss Your Website’s SEO Priorities', 'Discuss Your Website', 'Share your website'; pricing answer focuses on site size/number of URLs. However keyword research/clustering is sold as a standalone keyword spreadsheet even for projects with no site.
Action: address 'business or SEO project', allow product/topic/country/keyword-list brief without a website, and distinguish from technical audit inputs. Keep keywords in H1/Title but plain buyer copy.

### P2: Remaining old illustrated service asset
Although all 3 new main cards contain no old pictures, /uploads/seo-icon-google.svg remains displayed beside Performance & usability in the eight-tile overview. Existing SeoImpuls logo is fine. If owner restriction covers all service-specific illustrations on the EN homepage, replace the last decorative SVG with CSS; preserve file in Git.

### P2: Desktop top section waste and repeated 01–03 numbers
The 'From your goal to a clear result' process on the left is stretched to match 3 vertical service cards on the right, leaving a large empty lower half at 1280px. Both process and services have 01/02/03 marks, suggesting a common mandatory sequence when the three services are alternative choices.
Action: balance process/card heights and visually distinguish steps from services; no heavy artwork necessary.

### P2: 768px header height and 390px consent wall
At exactly 768px, header wraps into multiple rows (anchor uses 192px offset; top of header ends at approx. 171px). It works but occupies much of the first viewport. At 390px the initial cookie banner consumes a substantial portion of the 844px viewport with 3 vertically stacked actions, covering the start of the page until a choice is made.
Action: compact tablet header and mobile consent layout while retaining all accessible language choices/accept/reject/preferences.

### P2: SEO explanations and output still too technical
The hero/meta and eight tiles refer to 'canonical', 'crawl', 'indexability', 'Core Web Vitals', 'hreflang', etc., with insufficient plain business result descriptions. The 'What You Receive' block calls the keyword output 'Keyword-to-Page Map', but an existing website is not required and a grouped keyword spreadsheet may be the full purchased deliverable.
Action: preserve recognizable search terms in headings but explain problem, work and tangible result in simple language.

### P2: Full-width floating Contacts bar needs dedicated geometry QA
The strengthened Chrome test confirms *individual fixed social icon* bounds never overlapped readable homepage text at 390/768/1280; it does not comprehensively prove non-overlap for the whole animated full-width Contacts footer bar. Full-page screenshots show the bar stitched over intermediate content, but that alone cannot distinguish a real viewport obstruction from full-page screenshot rendering of position:fixed elements. Classification: REPRODUCTION_REQUIRED, not confirmed production defect.
Action: focused live scrolling/animation test of entire bar bounds and text focus targets.

### P3: Accessibility/manual review still outstanding
axe automated reports zero definite WCAG violations at 390/1280 in light/dark but lists INCOMPLETE checks: aria-prohibited-attr on 2 nodes and color-contrast on 72 nodes. Requires targeted manual/DOM investigation; avoid claiming WCAG certification. Browser visual QA also noted 2 href='#' anchors, likely JS-managed links (back-to-top/email), not proven broken.
No lab Lighthouse, field Core Web Vitals, real SERP top-10, keyword frequency, or conversion measurement was performed.

## Release decision and next work, restricted to EN homepage
Status: CODE_QA_PASS / ROUTE_SEO_PASS / AUTOMATED_RESPONSIVE_PASS / CONTENT_UX_CHANGES_REQUIRED / OWNER_REVIEW_PENDING / PRODUCTION_NOT_DEPLOYED.
Priority: 1) simplify eight scope tiles + site-only CTA; 2) remove residual old SVG under owner's no-legacy-art rule; 3) improve desktop balance/tablet header/mobile cookie UI; 4) add full Contacts-bar collision test and manual accessibility/contrast review. Re-run strict/preview/3 viewport QA after each actual code change. Do not edit other pages or deploy production without explicit owner instruction.
