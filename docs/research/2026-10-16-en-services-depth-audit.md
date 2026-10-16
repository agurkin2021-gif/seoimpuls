# SEOImpuls — focused English SEO services catalogue deep audit

Date: 2026-10-16. Scoped preview: https://agurkin2021-gif.github.io/seoimpuls/seo-services/.
Repository: agurkin2021-gif/seoimpuls, `white-seo-rebuild`. Production, DNS, `main`, EN homepage and RU/ES content out of scope.

## Search intent and cannibalization boundary
- Homepage `/`: `Professional SEO Services`, selecting an SEO provider, full-funnel hiring and company trust.
- `/seo-services/`: what kind of SEO work fits which problem; scope, common outputs and links to three real detailed service pages. Do not write a second full-service-provider landing page.
- `/seo/`: deep technical audit offer. `/services/keyword-research/`: query research and URL mapping. `/services/seo-consultation/`: consultative diagnosis and planning.
- Existing 23 workstreams **are not 23 independently purchasable or already completed packages**, so don't generate 23 keyword-doorway landing pages or fabricated prices, studies or placement metrics.

The prior reproducible (parameterized, not physically US-located) Google Web SERP top-10 and URL inventory are documented in `docs/research/2026-10-15-en-services-serp-and-architecture.md`. A new public web sampling on 2026-10-16 found:
- https://www.webfx.com/seo/learn/seo-services-list/ — buyer-focused service types, deliverables and pricing/comparisons; a long educational list, not a narrow service selector.
- https://thestacc.com/blog/what-are-seo-services/ — describes eight typical services and cautions against whole-menu-by-default purchases.
- https://agenciaroco.com/en/which-includes-an-seo-service/ — framing of audit, content, architecture and measurement as scope based on business needs.
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide — clear unique page purpose, organized content, descriptive anchors, useful page content.
These links are **reference observations, not a new certified Google top-10 ranking**. Current GSC demand, local organic difficulty, conversion and competitor traffic remain unverified.

## Verified starting-point issues (Opera screenshot and current GitHub source)
1. **Repeated visual**: first technical SEO card and third consultation card show the same magnifier/SEO-growth artwork. This undermines distinct service selection even though URL, label and alt differ.
2. **First-viewport delayed media**: previous template applied `loading=lazy` to second/third first-row illustrations. On initial Opera screenshot the cards briefly displayed large empty backgrounds before images loaded.
3. **Long catalogue needs a table of contents**: 23 workstreams/4 groups span many screens. The first category list begins without links to the other categories, reducing usability for users seeking local, international, ecommerce or research work.
4. **Hash heading hidden**: opening `#seo-work-technical` with sticky header showed the category heading above the visible area. Section scroll offsets were not specified.
5. **Weak evidence demonstration**: existing content said `typical output` repeatedly but offered no concrete, falsifiable artifact example. Buyer cannot see how work would be verified.
6. **Generic text anchors**: the 3 deeper workstream links all said `View detailed service`; descriptive links are preferable for accessibility and search context.
7. **Buyer cost question missing**: no fixed prices should be fabricated, but factors affecting quotation and schedule need a useful explicit answer.

## Scoped changes
- Keep URL `/seo-services/`, H1 `Choose the Right SEO Work for Your Website` and HTML title `SEO Audits, Keyword Research & Consulting | SeoImpuls`; preserve self canonical, sitemap, hreflang, existing 3 real service target URLs.
- EN-only `layouts/partials/services-hub.html`: use a CSS/HTML consultation workflow diagram instead of a duplicate photo. This is **not an image or client-case claim**, and no external assets/downloads are added. Remaining two first-row WebP images are eager-loaded, with priority high only for the first.
- EN-only `layouts/partials/en-services-catalog.html`: add five jump links (4 category anchors + example report), `scroll-margin-top` for anchored sections, descriptive service links. Add one **explicitly hypothetical** output example explaining potential indexing problem, required evidence, conditional action and acceptance checks; no implied client result.
- `data/en_seo_catalog.json`: add an FAQ on the factors determining cost/time; no fixed price, deadlines or guaranteed ranking.
- Targeted Hugo and Playwright audits updated to check 23/4/3 inventory, five in-page anchors, one distinct consult illustration, 4 evidence rows, 5 FAQs, exactly 3 detailed link labels, JSON-LD BreadcrumbList without BlogPosting, and hash position below sticky navigation on 390/1280.

## Risks and acceptance criteria
- All edits remain inside English catalogue and its EN-scoped shared partial branch. Other sites, `main`, production and unrelated locales must not change.
- Rebuild Hugo `--minify`; GitHub Actions strict whitehat content gate must pass, including no retired paths or link-spam language.
- Live preview Playwright 390/1280: HTTP 200, unique H1, exact title and canonical, no overflow or failed media, no broken local links/JS/network errors, responsive 1/3-column top grid, 23 workstreams + 4 groups + three entry routes, 5 TOC anchors and actual fixed-header scroll geometry.
- Independently inspect preview screen layout and query examples after Pages deployment. Green CI is not evidence of real production 301, indexing or commercial performance.
- GSC and production HTTP redirects are unavailable/not authorized; status `RELEASE_BLOCKED` regardless of lab QA results.

## Mobile 390px follow-up (after previous QA)
- Playwright screenshot at 390×844 showed all three initial cookie buttons in full-width rows. On this single EN catalogue, display Accept/Reject side-by-side with unchanged labels, equivalent priority and at least 44px height; Manage Preferences stays visible and accessible below. All consent functionality remains unchanged.
- Each six-workstream group now ends with a descriptive `Back to categories` link. `#seo-catalog-title` gets 120px scroll-margin for the sticky header.
- Added regression checks: 5 TOC links, four return links, corresponding anchor, two-column mobile consent actions with all three original buttons. New CI and screenshot evidence required before acceptance.
