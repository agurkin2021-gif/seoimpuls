# EN /seo-services/ — final QA and release decision (2026-10-16)

## Scope and immutable boundaries
- Working branch: `white-seo-rebuild`; accepted page source SHA: `ad90cbd214dd259bdc97cc09298727bf6f5613a8`.
- Preview: https://agurkin2021-gif.github.io/seoimpuls/seo-services/ (noindex preview only).
- Production target URL: https://seoimpuls.com/seo-services/ — **not deployed**.
- Homepage `/`, 3 specialist pages `/seo/`, `/services/keyword-research/`, `/services/seo-consultation/`, RU/ES source, main branch, live server, DNS and GSC not edited during this final step.

## Search intent and business truth
- Catalogue owns **choosing appropriate SEO work by problem and deliverable**; homepage owns professional SEO provider selection; 3 specialist URLs own detailed commercial service explanations.
- 23 workstreams grouped under 4 sections; truth labels: 3 established specialist services, 14 potential agreed-scope components, 6 conditional specialties subject to feasibility check. They are **not** 23 confirmed priced products.
- Every workstream has a next action: 3 specialist links plus 20 work-specific topic-encoded email enquiries.
- One deliberately hypothetical SEO sample and one reproducible internal visual/technical QA sample; no invented customer reviews, SEO rank results, false performance claims or unverified client case.
- SERP comparison research exists but is **not** a verified top-10 for one exact market/geolocation; do not label SERP_VERIFIED based on it.

## Evidence and acceptance
| Gate | Evidence | Outcome |
| --- | --- | --- |
| Hugo static build, strict white-hat audit, site-level route gates | [Actions #38888649717](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38888649717) | **PASS** |
| GitHub Pages preview deployment, preview noindex transformation | [Actions #38888649363](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38888649363) | **PASS** |
| Playwright Chrome 390, 768 and 1280 px, anchor, keyboard TOC, FAQ, buttons, links, metadata | [Actions #38888649421](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38888649421) | **PASS** |
| Context file updated in each source commit | [Actions #38888649376](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38888649376) | **PASS** |
| Visual evidence after 768px collision remediation | [QA artifact #12039969650](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38888649421/artifacts/12039969650) | Fresh 768 first/category, 390 first and 1280 first manually inspected; no blocking overlap noted. |

- 768px social links: **2 viewport-fixed buttons, 0 observed text rectangle collisions** after isolated EN catalogue responsive safe gutter (44px per side in 768–1199px). At 1280: 2 buttons, 0 collisions; at 390: not floating. Buttons remain available, footer behavior unchanged.
- Browser test on each viewport: expected page HTTP 200 in local static server, single H1, correct Title, meta description, one production-base robots tag `index,follow,max-image-preview:large`, canonical `https://seoimpuls.com/seo-services/`, OG/Twitter card metadata, 4 alternate language references, HTML/JSON-LD parse, keyboard TOC/FAQ, expected cards/scopes/links, 13 local route paths, no broken internal links, no JS/network failures and no page-wide horizontal overflow.
- Preview workflow removes conflicting production robots meta and inserts one `noindex,nofollow`, preventing contradictory preview indexing instructions. Passing test is **not** a claim about Google's chosen snippet or actual production indexing.
- No actual CrUX/LCP/INP/CLS real-user field measurement or complete WCAG certification; test covers only observed automated/browser cases.

## External dependencies: release remains blocked
1. Google Search Console 3–6 months of historical page/keyword data, live URL/index coverage and inbound links to decide which legacy URLs warrant relevant 301, 404 or 410. Hugo static alias is not an HTTP 301; redirects need live server/CDN changes after approval.
2. RU/ES language-equivalence and target-market decision; reciprocal `hreflang` is technically present but content parity is partial (EN 23 workstreams vs RU/ES 4 choices); this must be resolved in the coordinated locale phase, not hidden under a test PASS. Spanish `es-ES` market target remains unconfirmed.
3. Real verified client proof or explicit permission for identifiable/anonymous published reports, and explicit confirmation of skills/portfolio for specialties as applicable. Do not substitute invented testimonials.
4. Owner's separate, explicit permission to deploy production site and migration policy. Sitewide legacy URL/redirect effects must be validated in that separate phase.

**Decision:** EN catalogue has reproducibly passed code and tested responsive visual QA and is retained as the frozen accepted preview. Status: `CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / RELEASE_BLOCKED`. Do not rework other EN service pages or publish the target domain automatically. The next authorized phase requires external migration/locale/portfolio evidence and a separate production decision.
