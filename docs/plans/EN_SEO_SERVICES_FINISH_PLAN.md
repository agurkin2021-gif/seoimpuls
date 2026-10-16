# SEOImpuls — EN `/seo-services/` controlled completion plan

**Owner instruction:** 2026-10-16 — finish **this catalogue only**, follow the written plan in order and preserve context after every operation. No other EN service-page content rewrites, no RU/ES content edits, no changes to `main`, production, DNS, GSC or redirects without separate authorization.

**Source of truth:** this file + `CHATGPT_PROJECT_CONTEXT.md` (both checked in every new session). Branch `white-seo-rebuild`. Source page `content/services/_index.md`, EN catalogue partial `layouts/partials/en-services-catalog.html`, catalogue data `data/en_seo_catalog.json`, existing cards in `layouts/partials/services-hub.html`. Preview: https://agurkin2021-gif.github.io/seoimpuls/seo-services/ . Production URL is reserved but **not deployed**.

## Invariants / acceptance contract

- **Homepage `/`** owns `professional seo services` and hiring/provider-selection. **EN catalogue `/seo-services/`** owns choosing an SEO work scope by problem, output and responsibility. Specific `/seo/`, `/services/keyword-research/`, `/services/seo-consultation/` own depth and inquiry; keep those URLs unchanged. No fabricated extra indexed pages for 23 workstreams.
- Current approved H1: `Choose the Right SEO Work for Your Website`. HTML title: `SEO Audits, Keyword Research & Consulting | SeoImpuls`. Keep self canonical and breadcrumb. Do not rename without measured intent evidence.
- The **23 workstreams in four groups** represent possible areas to *scope and assess*, not 23 priced/off-the-shelf guaranteed service packages. No fictitious experience, team size, cases, clients, fixed pricing, CTR/ranking/AI citations, or link spam offers.
- Existing illustration is expressly hypothetical. A verified customer case or true before/after report **cannot be invented**; production-ready proof requires real sanitized, consent-cleared evidence.
- Each scoped edit: log changed files, baseline, reason/intent, tests with run IDs and their actual conclusions, unresolved risks and exact next action in `CHATGPT_PROJECT_CONTEXT.md` **in the same commit**. Never call PASS before the workflow finishes. Update this plan's status in the same commit for every phase transition.
- Hugo test must pass `hugo --minify --noBuildLock`, `python3 scripts/verify_en_services_route.py`, `python3 scripts/whitehat_content_gate.py --site public --strict`, context guard, Pages preview, browser QA at 390/768/1280. Validate generated HTML, not only raw Markdown or assertions written to match source. Check `robots`, canonical, hreflang, sitemap, OG, title, JSON-LD, images, links, CTA, keyboard, layout and top-of-page visual. Screenshot artifacts and test logs are evidence, not rankings.
- **Release blocked** absent Google Search Console historical URL/queries/inbound-link data, actual live HTTP redirect/404/410 strategy, verified content portfolio and explicit owner deployment approval. Preview has `noindex,nofollow` and must remain noindexed.

## Ordered work — do not skip unclosed gates

| ID | Priority | Scope | Acceptance gate | Status |
|---|---|---|---|---|
| 0 | P0 | Baseline: read repository context, catalogue, Google SERP snapshots, homepage/service content and previous QA; map known blockers | Evidence paths and known limitations recorded | **DONE — 2026-10-16, before plan** |
| 1 | P0 | Buyer journey: move the existing three-choice *problem → appropriate service → deliverable* selector to immediately after the three hero service cards, **before** 23-workstream catalogue. Preserve 3 linked routes, no duplicate selector, fixed-scroll anchors and mobile layout | Hugo + strict gate + route QA, Playwright at 390/768/1280 and preview; exactly one selector above catalogue | **DONE — 63f39bb; strict/Hugo/Pages/390-768-1280 PASS** |
| 2 | P0 | Commercial truth: audit all 23 workstreams against known service commitments, About/FAQ and their linked pages. Mark specialties as conditional scope; do not assert verified capabilities without evidence; preserve truthful ethical boundary | Each scope categorized as linked active service / conditional assessed work, no contradiction and no new URLs | **NEXT** |
| 3 | P1 | Demonstrable output: improve genuine problem/evidence/output sample clarity and a clearly labelled reproducible *sample format*, not a fake client case. Ground real proof only in client-approved records if supplied | No fabricated data, clear example/disclaimer, evidence and acceptance criteria; real case flagged **BLOCKED_EXTERNAL** until provided | TODO |
| 4 | P1 | Workstream conversion without doorway pages: for each of the 23 categories, give a coherent path to ask about that work, not invented separate service pages/prices; maintain three deep commercial URLs | Contextual workstream-to-contact navigation, descriptive anchors, no dead ends/placeholder routes | TODO |
| 5 | P1 | Multilingual correctness review (read-only RU/ES), overlap and keyword-role consistency; qualify EN/RU/ES `hreflang` as equivalents or record decision for coordinated localization, no unapproved locale edits | A URL-level equivalence matrix, no false claim of localization readiness; concrete unresolved items tracked | TODO |
| 6 | P0 | Full final EN catalogue SEO + page experience gate: production-base HTML and noindexed preview, title/H1/meta/OG/robots/canonical/schema/hreflang/sitemap, performance hypotheses with no invented CrUX, linked resources, responsive 390/768/1280, keyboard, header, cookie, footer and no fake claims | All supported automated checks pass and screenshots inspected; unresolved external blockers distinguished from bugs | TODO |
| 7 | P0 | Final decision record: summarize actual completed checks, unverified signals, release/migration blockers, next step. **Do not touch another page automatically.** | Context and plan updated with commit SHAs and specific CI run IDs, `CODE_QA_PASS` only if proved | TODO |
| X | External | Google Search Console 3–6 months + client-approved real examples, portfolio/capability confirmation, prod redirect mapping and publisher approval | Only close after obtaining actual data and authorization; no presumptions | **BLOCKED_EXTERNAL** |

## Rules when reopening in a new chat

1. Read this plan, `CHATGPT_PROJECT_CONTEXT.md`, `AGENTS.md`, `docs/SEO_PAGE_WORKFLOW.md` from **current `white-seo-rebuild`**. Check GitHub branch HEAD and latest CI run states.
2. Take the first row marked `NEXT` / `IN_PROGRESS`. Determine whether code changed, whether the change was actually committed, whether screenshots/QA are complete. Never repeat a finished operation solely from chat memory.
3. Perform **only that row**, with its own narrow commit and context edit. Record CI IDs/conclusions and switch NEXT to the following row in a second documentation-only commit if necessary. Failures require fixing the *cause*, not bypassing the gate.
4. Keep all non-applicable user inputs and non-reproducible external results as open blockers with exact owner/dependency. Do not invent work you cannot verify or perform.
5. End only with explicit page status, confirmed test results, commit URLs and accurate remaining blockers.

## Baseline evidence

- `docs/research/2026-10-15-en-services-serp-and-architecture.md`: Google US-parameterized desktop search snapshots; physical US location and keyword demand **not** confirmed.
- `docs/research/2026-10-16-en-services-depth-audit.md`: detailed buyer gap and visual checks; last accepted source change `3878934`, acceptance record commit `1791892`.
- Latest prior CI: strict QA #38846778912 PASS, Pages preview #38846778882 PASS, responsive browser #38846778800 PASS, last documentation CI #38847116244/#38847116233 PASS.
- Technical limitation: Hugo-generated static fallback `/services/` is **not HTTP 301**; if production migration is authorized, handle at web server/CDN. Preview noindex is injected by deployment workflow.
- Current URL, meta, 23 workstreams, three deep links and source code may change only when the plan records a verified reason, not for a superficial keyword swap.

## Execution log

- 2026-10-16 — Plan created by owner instruction. Step 0 complete from repository evidence, Step 1 NEXT. No site code changed by this planning commit.

- 2026-10-16 — Step 1 source: moved exactly one 3-way buyer selector before the directory, preserved 23 workstreams, updated route & browser test ordering assertions and added 768px QA. Waiting for CI/preview screenshots before marking DONE.

- 2026-10-16 — Step 1 first Playwright run #38851634798 FAIL only at 768px: `sectionTop=120`, fixed header bottom `171`, anchor obscured; 390px top 120/header81 and 1280px top120/header79 PASS; full Hugo and Pages #38851634622/#38851634633 PASS. Updated only catalogue CSS tablet scroll margin to 192px; rerun required, no claim of completed QA.

- 2026-10-16 — Step 1 768px hash fix succeeded: Playwright #38851849354 PASS at all 390/768/1280, tablet sectionTop192 vs header171. Visual screenshot manual inspection then revealed the **footer at page top over the tablet header/logo** at exact 768px due overlapping desktop min-width 768 and mobile max-width 768 media rules. Added EN-catalogue-only footer bottom overrides at 768 and new browser collision test. CI/screenshots pending; do not call Step 1 done yet.

- 2026-10-16 — **STEP 1 DONE:** corrective source `63f39bb`; full Hugo/strict gate #38852257807 PASS, Pages #38852257602 PASS, context #38852257833 PASS, Chrome #38852257739 PASS, 390/768/1280 each `fail:[]`. At 768px header bottom 171 and scroll section top 192, footer fixed at y=741–800 (not over logo). Screenshots `seoimpuls-en-services-390-768-1280` artifact #12025618382 visually examined 390 and 768 first viewport, including contact placement, no header collision. No broken routes/JS/net and no overflow. Step 2 NEXT; do not start other EN pages.
