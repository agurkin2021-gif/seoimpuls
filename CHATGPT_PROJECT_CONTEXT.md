# SEOImpuls — основной контекст проекта (читать первым)

## 2026-10-16 — EN HOME UNIFIED CONTENT RAIL (PENDING QA)
- Browser baseline confirmed actual horizontal mismatch: width 1280px: header logo x18, Home breadcrumb x34, hero/services x120, footer contacts x32; width 768px: x16/x32/x120/x32; width 390px: x12/x28/x34/x18. This is the precise defect reported by owner and not a subjective styling dispute.
- EN-only HTML style in `layouts/index.html` now establishes centered 1280px frame, shared gutters 32/24/18px, removes conflicting `-1rem` width/margins and 120px content indent; aligns header/breadcrumb/content/footer rails. Contact panel borders share the service-card rail; heading inside panel remains intentionally inset. RU/ES templates, texts and other URLs untouched.
- EN/RU browser test adds numeric x-coordinate assertions with ±2.1px tolerance at 390,768,1280,1600px and logs coordinates `EN_HOME_RAIL_QA`. Existing seven-service, responsive, SEO and RU isolation checks stay.
- STATUS **SOURCE_COMMITTED / STRICT_PENDING / VISUAL_BROWSER_PENDING / PREVIEW_PENDING**. Do not call corrected until Playwright/Opera measurement proves it. No changes to main or production.
- Next check relevant Actions on this commit, correct any actual failures, visually inspect published preview and preserve noindex.


## 2026-10-16 — EN homepage header/breadcrumb/content/footer left-edge audit (measurement phase)
- Owner reports header/footer and the “Home” breadcrumb not sharing one left baseline with page content; asks to correct specifically this geometry, not reopen content/SEO or redesign another page.
- Source inspection verifies incompatible gutters: English homepage sections inherit desktop `padding-left:120px` (old floating-contact clearance), header/breadcrumb use `18px`, footer uses `32px` on wide desktop; mobile uses mixed `12px/16px/18px`. This accounts for visible x-offsets but pixel baseline requires browser measurement.
- Added **read-only** Playwright DOM-rectangle logging to the existing EN/RU homepage audit at 390, 768 and 1280px. No site markup, CSS or content changed in this measurement commit.
- STATUS: MEASUREMENTS_PENDING, next inspect exact logged `HOME_LEFT_EDGE_BASELINE`, choose a unified EN-home-only content rail and fix; assert actual browser pixels and verify unchanged RU/ES and production.


## DESIGN STAGES 02 AND 03 — 2026-10-16 (STAGE 03 QA PENDING)
- **Stage 02 VERIFIED:** commit `db1f4dd890814428c0a6cb48323a45b262be0a41`, only EN homepage visuals, seven distinct inline semantic SVGs and rebalanced result/service-action hierarchy; RU/ES unaffected in rendered EN-only branch. GitHub Actions strict #38964863183 PASS; preview #38964863211 PASS; EN/RU 390/768/1280 Chrome #38964863069 PASS; general 390/768/1280 Chrome #38964863300 PASS; a11y #38964863130 PASS; context #38964863073 PASS. Manually opened live GitHub Pages noindex preview via Opera with `?design=db1f4dd#services`: icons rendered, headings and outcome panels visibly aligned. These are browser/CI checks, not field CWV or owner's final visual signoff.
- Stage 03 targets continuing EN-home-only flatness, confirmed by opening `#how-it-works` in connected Opera: a box of three boxes, standalone wall of definition text, three generic deliverable tiles, then three FAQ cards. Change exclusively EN-home stylesheet in `layouts/index.html`: process becomes 3-step connected timeline (mobile vertical); service definition becomes editorial 2-column explanation at ≥1080px; deliverables become a structured 3-row document ledger; FAQ entries become unobstructed questions with vertical rules; enquiry CTA becomes a distinct concluding panel. No copy, commercial claims, links, service choices or other pages changed.
- **Stage 03 STATUS: SOURCE_EDIT_COMMITTED / STRICT_QA_PENDING / VISUAL_MOBILE_TABLET_DESKTOP_PENDING / PREVIEW_PENDING / PRODUCTION_UNTOUCHED.** Footer's large floating bar is still separate issue; do not claim resolved. Need verify all workflows, EN+RU responsive/screenshots and final browser navigation before acceptance.
- Next: inspect Stage 03 GitHub Actions and published EN preview; correct actual visual defects and then address any remaining homepage-only visual issue independently. No edits to inner pages, RU/ES, main, production.


## DESIGN STAGE 02 — 2026-10-16: EN HOMEPAGE SERVICE INDEX (PENDING QA)
- Owner delegated full art direction for the homepage after completing hero Stage 01, with explicit command to work independently. Scope remains EN homepage ONLY; RU/ES, inner pages, main branch and production are not editable.
- Baseline confirmed in published GitHub Pages preview and Opera: seven cards share effectively the same panel and number treatments; the information-heavy grid has weak visual differentiation compared to the designed hero.
- Changed EN-only `layouts/index.html` markup/CSS under `.seo-central--art-directed` plus new `layouts/partials/en-home-service-glyph.html`: seven line-art vector glyphs illustrate audit, research, page structure, location, international search, consultation, monthly iteration. Restrained geometric palette matches hero, with clear title > description > report/result > action rhythm, a featured monthly service, editorial labels and improved whitespace. No new external fonts/assets/JS, fabricated ranking statistics, changed text, service choices, routes, canonical or schema. RU/ES are outside render condition.
- Browser service QA updated to assert seven distinct, correctly mapped inline glyphs and preserve RU's existing CSS-only numbered markers; workflows watch the new partial for future changes.
- **STATUS: SOURCE_COMMIT_IN_PROGRESS / STRICT_BUILD_PENDING / RESPONSIVE_390_768_1280_PENDING / PREVIEW_PENDING / BROWSER_REVIEW_PENDING / PRODUCTION_UNTOUCHED.** Do not claim QA pass before examining actual runs.
- Next: verify strict and published preview workflows; inspect visual screenshots at 390, 768 and 1280, check no overlap/overflow and compare RU unaffected, then correct discovered deficiencies before any later section design.


## VERIFIED DESIGN PASS 01 — 2026-10-16: EN HOMEPAGE HERO ONLY
- Final visually tested EN-home source includes original `0866d028bc529b349cf55731b8d221bff120dd2b`, SVG root fill correction `abf729c4f364d6dd2b1b33fc96a35e882bae9492`, and workflow trigger fix `38fd0f314c7bcd77a99d6f7054ff0b5debec478c`. Only EN homepage hero uses `seo-central--art-directed` and inline SVG `layouts/partials/en-home-hero-diagram.html`; all seven services, EN title/H1, CTAs, canonical/schema, other page source unchanged. RU/ES unaffected. No production publication.
- **PASS strict Hugo/sitewide/SEO/whitehat** [#38963265262](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38963265262). **PASS noindex Pages preview** [#38963265166](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38963265166). **PASS dedicated EN/RU Chromium browser on 390/768/1280** [#38963265170](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38963265170): figure present and labeled on EN; absent in RU; SVG has zero external media references; no copy/diagram overlap, broken internal paths, horizontal overflow, or JS/network failures; service topology and links remain correct. **PASS English general visual browser** [#38963265179](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38963265179); **PASS automated accessibility diagnostic** [#38963265211](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38963265211); **PASS mandatory context guard** [#38963265216](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38963265216).
- Manually opened updated noindex EN preview `https://agurkin2021-gif.github.io/seoimpuls/?design=38fd0f` in Opera: black connector-fill polygon from initial proof is gone; clean angular cyan lines link three informational panels. Inspected GitHub Actions screenshot artifact `12074300233` (latest source) in original 390/768/1280 browser captures, including first fold after cookie rejection: 390 and 768 stack the diagram below text; 1280 uses balanced adjacent columns; diagram is legible and does not collide with content. No copied photography, no invented numbers. Existing high/tall 768 tablet header and 390 cookie-consent overlay are separate later EN-home UX candidates, not repaired in Stage 01.
- **STATUS EN_HERO_DESIGN_STAGE_01_COMPLETE / STRICT_QA_PASS / RESPONSIVE_BROWSER_PASS / PREVIEW_PUBLISHED_NOINDEX / MANUAL_SCREENSHOT_REVIEW_PASS / OWNER_VISUAL_ACCEPTANCE_NOT_YET_GIVEN / PRODUCTION_UNTOUCHED.**
- Scope lock remains **English HOME ONLY**. Further design passes may refine EN-home-only seven service card graphics, section rhythm and existing EN header/cookie UX if authorized within homepage work, but no other page. Do not conflate this first-screen pass with a finished sitewide design. Field CWV and full manual WCAG compliance not established.


## QA TRIGGER FIX — 2026-10-16: EN HOME DIAGRAM AUTO-TESTING
- The new EN-only SVG partial is stored in `layouts/partials/en-home-hero-diagram.html`. Browser, responsive EN/RU comparison and axe workflows previously watched `layouts/index.html` but not the SVG partial, so a one-file visual change could skip all browser checks.
- Add this partial to push path filters of `.github/workflows/en-home-browser-audit.yml`, `.github/workflows/en-services-browser-audit.yml` and `.github/workflows/en-home-accessibility.yml`. No site content, pages, CSS or diagram edited in this commit; source SVG root fill fix remains from `abf729c4f364d6dd2b1b33fc96a35e882bae9492`.
- STATUS: WORKFLOW_TRIGGER_CORRECTION_COMMITTED / FRESH_BROWSER_QA_PENDING. Require strict Hugo, noindex preview, mobile/tablet/desktop EN + RU-isolation visual checks. Do not call design accepted until result inspected. Production/main/RU/ES untouched.


## DESIGN PASS 01 — 2026-10-16: EN HOMEPAGE SVG VISUAL REFINEMENT
- Initial EN-home-only source commit `0866d028bc529b349cf55731b8d221bff120dd2b`: double-column hero with self-contained SVG system map, original texts/CTAs/7 services unchanged; RU/ES source markup not altered. All initial CI checks PASS: strict Hugo/sitewide [#38962796380](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38962796380), noindex Pages preview [#38962796625](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38962796625), dedicated EN+RU 390/768/1280 Chrome [#38962796645](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38962796645), general EN browser [#38962796555](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38962796555), accessibility diagnostic [#38962796345](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38962796345), context guard [#38962796450](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38962796450).
- Manually opened actual working EN Preview in connected Opera `?design=0866d0`. Composed heading / matte technical map visually balanced in two columns at desktop; visual inspection caught a REAL SVG defect: central connecting stroke also had unintended black fill because root SVG had default fill behavior. Corrected `layouts/partials/en-home-hero-diagram.html` root to `fill="none"` so path geometries retain only deliberate strokes. This second source change does NOT affect page content, metadata, links, RU/ES or any other page.
- STATUS **VECTOR_FIX_COMMITTED / QA_RERUN_PENDING / OWNER_VISUAL_REVIEW_PENDING / PRODUCTION_UNTOUCHED**. Initial green tests do not certify latest one-line SVG fix; verify fresh strict/preview/browser/axe/context runs and inspect EN desktop and narrower screenshots again.
- Scope lock: only EN homepage first-screen design; no other pages, no RU/ES changes. Next after pass: consider EN-homepage cards only when owner indicates to continue or by maintaining same-page design work.


## CURRENT DESIGN PASS 01 — 2026-10-16: EN HOMEPAGE HERO ONLY
- Latest owner lock: redesign **only English homepage**. Do not move to any other page; RU/ES must render unchanged. The user delegated art direction; source of truth and acceptance criteria: `docs/design/EN_HOME_VISUAL_STAGE_01.md`.
- Baseline (before source change): EN preview first screen has flat headline + two buttons above plain seven-card grid, no central visual focal point. Shared `.seo-central--en` styles apply to RU, so added a separate EN-only `.seo-central--art-directed` root; styling is gated by language `en`, and graphic partial `layouts/partials/en-home-hero-diagram.html` is rendered ONLY in EN hero.
- Stage-01 implementation: asymmetric heading/buttons and self-contained matte technical SVG representing search intent → website pages → technical checks. Existing title/H1, description, CTAs, all seven services, routes, meta/SEO, footer and content blocks preserved. No new fonts/images/JS requests; no false ranking/conversion data. RU and ES markup/appearance deliberately unchanged.
- Regression checks: expanded `scripts/audit_en_services_browser.cjs` to examine hero figure/semantics and copy-vs-figure collisions at 390,768,1280, confirm RU design absent and retain original seven-card URL, SEO and browser tests.
- STATUS **SOURCE_EDIT_PENDING_QA**; strict Hugo build, noindex preview deployment, Playwright and visual screenshot review remain UNVERIFIED until actual runs. No production/server/DNS/CDN changes. Same-commit context requirement observed.
- Next: verify GitHub Actions for exact new source revision; inspect published EN preview and full EN 390/768/1280 screenshots, correct any fit/accessibility issues. Only after confirmed accept Stage 01 consider the next EN homepage section. Do not touch unrelated pages.


## VERIFIED CONSOLIDATION — 2026-10-16: EN/RU 7 CARDS, PREVIEW LIVE
- Exact source commit `44d3252725ecf7b03237d27893d4652db31ec1c1` in `white-seo-rebuild`, 11 files including both service data files, both QA scripts, combined Playwright test, workflow guards, mandatory context, AGENTS and decision record. Previous 10 cards replaced by 7 mirrored EN/RU cards: (1) SEO Audit including Technical SEO; (2) Keyword Research including competitor review; (3) On-Page SEO including content improvements; (4) Local SEO; (5) International SEO; (6) SEO Consultation; (7) SEO Retainer featured. Old standalone detailed service pages and paths stay; ES unchanged; production not deployed.
- **STRICT QA PASS** [#38961666769](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38961666769). This verifies Hugo build, current EN + RU service topology, proper three native RU/four EN detailed routes, scopes, affiliate safeguards, sitemap and whitehat. **WORKING PREVIEW NOINDEX PASS** [#38961666839](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38961666839). **EN/RU responsive service browser PASS** [#38961666883](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38961666883) on 390/768/1280: respective one/two/three column grids, all 7 matched service IDs, full-width featured Retainer, direct routes/anchors, no broken internal paths, JS/network failures or horizontal overflow; screenshots saved as browser artifact. **EN general visual browser PASS** [#38961666920](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38961666920); **automated accessibility diagnostics PASS** [#38961666733](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38961666733); **context guard PASS** [#38961666830](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38961666830).
- Also manually opened actual English and Russian working preview in connected Opera at `https://agurkin2021-gif.github.io/seoimpuls/` and `https://agurkin2021-gif.github.io/seoimpuls/ru/` with cache-bust `?review=44d3252`. Screenshots showed both first folds and updated service cards: 01 SEO Audit/SEO-аудит сайта, 02 Keyword Research/Подбор ключевых слов, 03 On-Page SEO/Оптимизация страниц и контента; no visible first-fold content regression.
- **LIMITS:** no new quantitative Google search demand or exact-market organic top-ten for each merged category; classification is scope consolidation, not evidence that removed labels have zero commercial demand. No owner final sign-off on text, no manual inspection of all 390/768 screenshots or real mobile devices, no field Core Web Vitals/performance or production deployment.
- **STATUS SOURCE_COMMITTED / STRICT_QA_PASS / EN_RU_RESPONSIVE_BROWSER_PASS / PREVIEW_PUBLISHED_NOINDEX / OWNER_RU_COPY_REVIEW_PENDING / PRODUCTION_UNTOUCHED**.
- **NEXT:** user to review Russian page wording and scope; separately authorized redesign later. Do not modify other pages or production.


## CURRENT WORK — 2026-10-16: EN + RU HOME SERVICE CONSOLIDATION 10 → 7
- Explicit owner instruction: reduce the number of commercial cards AND reduce them on the Russian homepage. Existing 10-card state was only a taxonomy, not evidence of individual keyword-demand volumes. Design decision is merge overlapping scopes; see `docs/research/2026-10-16-en-ru-home-service-consolidation.md`.
- The seven approved EN/RU IDs in order: `seo-audit`, `keyword-research`, `on-page-seo`, `local-seo`, `international-seo`, `seo-consultation`, `seo-retainer`. Technical SEO -> Audit (crawl/indexation/redirects/performance); competitor analysis -> Keyword Research (only scoped competitor findings); SEO Content Optimization -> On-Page (headings, text, links, page recommendations). Local/International, Consultation and monthly Retainer remain distinct, with final Retainer full-width.
- Changed `data/en_home_services.json`, `data/ru_home_services.json` (10→7), explanatory comment in `layouts/index.html`, strict EN route test, RU parity/scope test, Playwright EN/RU browser test and its triggering workflow, and sitewide static QA assertions. Existing EN four detail URLs retained, RU three native detail URLs retained; cards without real detail page still link to language-specific contact. No new route/redirect or edits to standalone service pages. ES unchanged.
- QA status at source commit: EDITED_PENDING_STRICT_QA / PREVIEW_PENDING / EN_RU_RESPONSIVE_QA_PENDING / OWNER_CONTENT_REVIEW_PENDING. Need verify results after commit; do not invent PASS. Public production, main, DNS, CDN remain UNTOUCHED. No new verified regional keyword volumes or GSC conversion data.
- NEXT: inspect strict GitHub Actions, noindexed GitHub Pages EN/RU and Chromium 390/768/1280 screenshots; repair any failed real or stale asserts, logging changes in same commit. Then owner may review Russian wording before design.


## ACCEPTED RU CONTENT PREVIEW + CODE QA — 2026-10-16
- Exact content source `948fda1e212a5145823f285f0233ff3e47112e9f` and QA/navigation fix source `1cddbf07a817a967cbbeec31f4a579872f36c34e`, branch `white-seo-rebuild`. RU page URL `/ru/`, current H1 `Профессиональные SEO-услуги`, Title accordingly. Content mirrors EN's 10 service categories and commercial disclosures but is OWNER REVIEW COPY, not signed-off commercial promises or separately verified RU SERP-localized SEO.
- **PASS strict rebuild:** [#38959926699](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38959926699) including Hugo EN/RU/ES build, sitemap/metadata and schema checks, RU H1, 10 matching service IDs, scope/FAQ/process copy, local detail routes and all contextual affiliate safeguards. Initial earlier strict failure due old RU home VPS affiliate expectation corrected and then passed. **PASS preview:** [#38959926688](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38959926688) published working GitHub Pages noindex site. **PASS context guard:** [#38959926692](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38959926692). **PASS unchanged EN browser:** [#38959926620](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38959926620).
- Opera manually opened refreshed `https://agurkin2021-gif.github.io/seoimpuls/ru/?review=1cddbf07`: RU Title/H1, current Russian service descriptions, 10 cards, 3 native RU detail links and RU contact anchors are visible in rendered browser accessibility tree and desktop screenshot. Verified malformed RU header nav paths from initial revision are now corrected in preview: `Главная` -> `/seoimpuls/ru/`, `SEO-услуги` -> `/seoimpuls/ru/uslugi/`, `Техническое SEO` -> `/seoimpuls/ru/seo/`. No operating production deployment.
- **LIMITS:** RU responsive screenshots at 390/768/1280 have NOT received dedicated mobile browser visual QA; do not claim perfect layout/accessibility or fully validated regional RU search intent. RU detail landing copy outside home was not rewritten. RU monthly Retainer has no localized detail page and correctly links to contact. The user requested content review first, not a graphic redesign.
- **STATUS RU_HOMEPAGE_CONTENT_MIRRORED / STRICT_QA_PASS / PREVIEW_PUBLISHED_NOINDEX / DESKTOP_RENDER_INSPECTED / OWNER_COPY_REVIEW_PENDING / PROD_UNTOUCHED**.
- **NEXT:** owner to review Russian promises/scope and request specific corrections; only then freeze copy and proceed with deliberate design. Do not change other pages or production without explicit authorization.


## QA FOLLOW-UP — 2026-10-16: RU homepage affiliate guard + preview menu
- Source `948fda1e212a5145823f285f0233ff3e47112e9f`: GitHub Pages working preview published successfully in action [#38959523159](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38959523159), RU HTML title/H1 and all 10 cards confirmed in Opera, all RU links to 3 existing native detail pages and RU contact anchor confirmed. Mandatory context-guard PASS [#38959523190](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38959523190). Hugo and RU content QA PASS inside strict run.
- Strict run [#38959523174](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38959523174) **FAILED** after RU checks because `scripts/verify_contextual_affiliates.py` still expected 2 affiliate VPS links on old RU home (new RU page has zero, matching current EN commercial content). Changed expected affiliate placements only by removing `ru/index.html` from whitelist; 4 remaining approved placements on ES home and localized web-development pages are still required and checked for nofollow sponsored, visible affiliate disclosure and destination. Any future unapproved RU-home affiliate fails.
- Opera RU preview actual top navigation URLs for RU menu were malformed under GitHub Pages subpath `/seoimpuls/ru/seoimpuls/.../`; RU-only conditional normalizes the already-prefixed `/seoimpuls/` menu path before applying Hugo `relLangURL`, leaving prod URLs/EN/ES untouched. Must confirm after new preview publication that `Главная`, `SEO-услуги`, `Техническое SEO` work under preview.
- STATUS CORRECTION_COMMITTED_QA_PENDING / PREVIEW_RECHECK_PENDING / OWNER_COPY_REVIEW_PENDING / PRODUCTION_UNTOUCHED.
- NEXT verify strict + preview on this revision, inspect RU navigation and rendered layout; record results. Same-commit context update preserved.


## CURRENT WORK — 2026-10-16: Russian homepage matching EN for owner copy review
- Owner asked to be able to understand/correct every commercial promise because they do not read English. Scope is current **RU homepage /ru/ only**, not rewriting unrelated RU pages, EN/ES or the active site.
- RU homepage is generated by `layouts/partials/ru-home-content.html` with `data/ru_home_services.json` (10 cards, IDs and order matching EN) and `data/ru_home_copy.json` (hero, terms, 3-step process, definition, 3 deliverable examples, 3 FAQ, contact). `content/_index.ru.md` is current RU Title/Description. `layouts/index.html` selects RU partial and enables existing EN responsive home CSS for RU as well; EN/ES view branches unchanged. RU former unrelated VPS affiliate card and old eight-point offer are no longer on this preview homepage; existing RU detailed service pages remain.
- Three cards link to existing localized detailed pages: `/ru/seo/`, `/ru/uslugi/semanticheskoe-yadro/`, `/ru/uslugi/seo-konsultaciya/`. Other seven link to `/ru/#contact-project`. No fake translated Retainer landing or English page represented as Russian. Same ten work areas, commercially important disclaimers as EN; no invented fixed prices, deadlines, rankings or automatic website edits. User is to review/correct actual offering; this copy is not signed off.
- Old strict RU expectations for VPS cards, old H1 and CTAs replaced with `scripts/verify_ru_home_review.py` verifying exact RU H1, 10 matching EN IDs, sections, data copy, URL anchors, native details, limits and no old gray material. EN/ES independent checks remain, old ES VPS-card test stays scoped to ES.
- Source status: `COMMITTED_PENDING_QA`. Do not claim strict/preview/mobile PASS until their results have been observed; GitHub branch history identifies this exact commit (self-SHA cannot be embedded in its own hash). Production/main/DNS/CDN unchanged; preview from allowed noindex GitHub Pages only.
- Next: inspect GitHub Actions strict/preview statuses, open /ru/ working preview and compare main page at desktop and mobile widths. Fix genuine issues with same-commit context. Then owner reviews Russian commercial claims; only after content agreement resume design work.


## ACCEPTED SOURCE + QA — 2026-10-16: EN SEO RETAINER
- Exact implementation source `68563b9ef543eb5ef3b2696513b832b61164ab8a` on `white-seo-rebuild`. New URL `/seo-retainer/`, EN source `content/seo-retainer/index.md`, HTML Title/H1 `SEO Retainer | SeoImpuls` / `SEO Retainer`; root breadcrumb Home > SEO Retainer; page buttons target `/seo-retainer/#start` and `/seo-retainer/#first-month`; no reused service images.
- EN homepage `data/en_home_services.json` contains previous nine cards plus featured 10th SEO Retainer; direct detail link reaches new page. Other 9 cards and 3 earlier EN landing routes unchanged. No EN services intermediate hub. Separate from consultation/audit; honest scope, first month, ongoing work log, reporting, monthly advanced fee by proposal, client changes/approval, FAQ; no fabricated prices, hours or rankings.
- **PASS** strict Hugo build/EN-RU-ES/sitemap/metadata/schema/reciprocal hreflang/whitehat: [#38947741871](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38947741871). New retainer WebPage + BreadcrumbList, no BlogPosting.
- **PASS** preview noindex subpath/deployment [#38947741897](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38947741897); URL https://agurkin2021-gif.github.io/seoimpuls/seo-retainer/ . Context guard **PASS** [#38947741976](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38947741976).
- **PASS** dedicated Playwright 390/768/1280 [#38947741909](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38947741909): EN home 10 cards, 1/2/3 grid columns, old nine labels+new retainer, 4 direct service page URLs, all H1/Title/canonical/JSON-LD, no images in cards, no broken routes, JS/network errors, horizontal overflow, covered text, hidden #services anchor. New page all 10 sections, no false SEO Services crumb, full URL anchors valid, zero page images, zero overflow at all three widths. All fail=[]; full-page retainer screenshots generated as workflow artifact.
- General EN home visual/a11y previously passed for same home CSS source at [#38947257042](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38947257042) and [#38947256954](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38947256954); home WCAG diagnostic PASSED on earlier same home source at [#38947067221](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38947067221). Desktop manual Opera Preview inspected for new retainer: correct Home > SEO Retainer and buttons point to its own anchors; initial desktop fold looks aligned with existing theme.
- **LIMITS:** desktop preview visually inspected; responsive screenshots were captured and checked automatically, but not separately opened for manual pixel inspection; formal WCAG, real mobile devices/field CWV, actual GSC impression overlap, worldwide exact top-10 and buyer conversion remain unverified. No claim of ranking success.
- **STATUS CODE_QA_PASS / RESPONSIVE_BROWSER_PASS / PREVIEW_PUBLISHED_NOINDEX / DESKTOP_MANUAL_VISUAL_PASS / OWNER_REVIEW_PENDING / PRODUCTION_UNTOUCHED**.
- Next action: owner review of preview and terms before any eventual production authorization. No change to main, production, DNS, CDN or RU/ES content. Do NOT auto-deploy.


## QA NAVIGATION FIX — 2026-10-16
- Read the newly published noindex GitHub Pages preview of `/seo-retainer/` using connected Opera; Title/H1/content and desktop layout rendered. Found two real navigation defects: the content page inherited a draft `SEO Services` breadcrumb from the `content/services/` source directory, and builder buttons `#start`/`#first-month` became homepage `/#...` because `relURL` resolved them against the site root.
- Relocated the source to `content/seo-retainer/index.md` (same public canonical `/seo-retainer/`; deletes old source path) to make breadcrumb Home > SEO Retainer. Changed button URLs explicitly to `/seo-retainer/#start` and `/seo-retainer/#first-month`; preview path prefix should then be applied correctly.
- Extended 390/768/1280 Playwright checks to load retainer page and verify breadcrumbs, rendered sections, navigation targets, no page images/overflow and capture full-page screenshots. Updated workflow path filter. Old QA result cannot prove this new source passes.
- STATUS: EDITED_QA_PENDING / PREVIEW_RECHECK_PENDING / PRODUCTION_UNTOUCHED. Next verify branch actions + actual preview and mobile screenshots.


## QA FOLLOW-UP — 2026-10-16: SEO Retainer correctly marked WebPage
- Initial source commit `8fa09a41`: Hugo compiled; existing EN home schema and three legacy service page SEO routes passed. Strict and Pages actions stopped at `scripts/verify_en_services_route.py` because new `/seo-retainer/` was marked BlogPosting by an explicit commercial-page whitelist in `layouts/partials/head/seo.html`. This is a REAL schema misclassification, not a test-only failure.
- Corrected whitelist to include `services-seo-retainer` so the page is WebPage + BreadcrumbList, without changing generic article BlogPosting or RU/ES schema. No production changes.
- STATUS: EDITED_QA_PENDING / STRICT_RECHECK_PENDING / PREVIEW_RECHECK_PENDING. Next: inspect new Actions and browser test results; then update exact pass/fail evidence.

## CURRENT WORK — 2026-10-16: SEO Retainer EN landing and featured homepage block
- OWNER INSTRUCTION: add a distinct SEO Retainer service with a visible EN homepage block; user selected keyword after worldwide Google Ads Planner results (100–1000/mo, 0% QoQ/YoY, low Ads competition), despite 15-region mixed informational/commercial SERP. Full findings in `docs/research/2026-10-16-en-seo-retainer-serp.md`.
- New `content/services/seo-retainer/index.md` -> `/seo-retainer/`, Title/H1 `SEO Retainer`, body includes onboarding and first-month review, monthly planning/approved edits, specific monthly work log, reporting, approval/access, scope limits, refusal of critical fixes, upfront monthly fee as agreed in proposal, FAQs and contact.
- EN only: `data/en_home_services.json` and `layouts/index.html` expand existing nine service cards by a tenth full-width featured Retainer card with direct detail link, custom CSS no graphics, no removal of nine categories, no new redundant services hub.
- Static/browser/preview QA scripts and workflows updated; EN intent remains separate from technical audit, keyword research, consultation and general Professional SEO Services homepage. RU/ES content unchanged; production, CDN, GSC, main untouched.
- STATUS: EDITED_QA_PENDING / PREVIEW_PENDING / NO PRODUCTION DEPLOYMENT. Next: observe strict Hugo/whitehat/context guard, noindex Preview and Chrome 390/768/1280 screenshot audits; repair failures in same-commit-context follow-ups. Owner review required before any deployment.


## ACCEPTED CODE / BROWSER / PREVIEW — 2026-10-16: NINE PLAIN SEO SERVICE AREAS
- The homepage visual/content source from bb9b418 remains unchanged through test-only commits 1510891 and b389ede. Nine buyer-facing service cards are visible in the working Preview, not merely in source, with primary H2 SEO Services for Your Business and three valid EN service detail links plus six links to the same-page project enquiry.
- **PASS** strict Hugo, EN/RU/ES generated routes, self-consistent SEO schema, whitehat content and retired routes: [#38926019064](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38926019064).
- **PASS** published GitHub Pages working preview including robots noindex and all direct links/anchors: [#38926018915](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38926018915).
- **PASS** updated dedicated Chromium [#38926019059](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38926019059): cards=9 and grid columns 1/2/3 at 390/768/1280 CSS px respectively; fail=[], JS/network errors=[], broken internal routes=[], fixed shortcut overlaps=[]; 01..09 original bespoke lightweight CSS marks; no card images.
- **PASS** EN home browser [#38925456144](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38925456144): rendered heading structure, no horizontal overflow at 390/1280, no broken images or internal links. **PASS** axe automated diagnostic [#38925456100](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38925456100): zero confirmed violations at 390/1280; still reports incomplete checks for 2 ARIA and 104 contrast nodes, not WCAG certification.
- Manual connected Opera refreshed published Preview with cache-bust ?review=b389ede04: desktop first-fold screenshot visibly shows title, hero, section H2 and three equal-width service cards, no former empty two-column process imbalance. Accessibility tree confirms all nine service headings and absence of old additional list. Manual mobile screenshot/field CWV/verified query volumes/GSC overlap not completed.
- Navigation no longer singles out technical audit; EN process lies after the nine-card grid. Hero second CTA now goes to contact, not redundant adjacent process. No old images, fabricated client proof, guaranteed rankings, new URLs or automatic written-plan/implementation claims.
- **STATUS EN_HOMEPAGE_CODE_QA_PASS / RESPONSIVE_AUTOMATION_PASS / DESKTOP_MANUAL_VISUAL_PASS / PREVIEW_PUBLISHED_NOINDEX / OWNER_REVIEW_PENDING / PRODUCTION_UNTOUCHED.**
- NEXT: changes ONLY on explicit owner instruction. Remaining UX note: full-width floating Contacts bar dynamics, tall 768 nav/cookie wall 390, human WCAG contrast/ARIA review and precise keyword volumes. Keep entire task scoped to EN homepage; no source edits were needed after confirmed tests.


## 2026-10-16 — EN nine-area follow-up: stale localized / preview asserts, site source unchanged
- Feature source bb9b418: Hugo and homepage JSON-LD PASS, EN browser Chrome direct-services 390/768/1280 [#38925456308](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38925456308) PASS (9 cards and 01–09 CSS marks, no failed internal paths/network/JS/overflow/shortcut collisions); home screenshot browser [#38925456144](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38925456144) PASS, axe [#38925456100](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38925456100) PASS (manual accessibility still open).
- Previous QA-only 1510891 corrected EN route parser; on its run strict #38925752480 stopped at old EN-only assertion requiring previous card2Url data field, while RU/ES still correctly use that field; now gate checks RU/ES only and checks exactly 9 EN data-driven areas. Preview #38925752323 passed route/schema/whitehat but stopped at obsolete hero #how-it-works secondary link; preview gate now expects approved new contact-project target.
- Browser test now measures **actual nine-card grid columns** rather than surrounding block display, expecting 390=1, 768=2, 1280=3. No visual/site code changed in this commit; rebuild/preview/browser must rerun on exact new head.
- STATUS EDITED_QA_PENDING / PRODUCTION_UNTOUCHED. Next: verify all Actions and GitHub Pages preview, inspect actual desktop/mobile screenshots; do not confuse old failed assertions with site defects.


## 2026-10-16 — EN nine-area QA gate repair, site source unchanged
- Prior feature commit bb9b418 Hugo --minify + homepage schema PASS, but strict/Pages build intentionally stopped at stale `scripts/verify_en_services_route.py` expecting old three EN cards; traceback showed empty old-aside selectors because new nine articles use a section. Corrected parser to collect the nine EN service IDs/marks and 3 detail + 6 scoped enquiry links; rejected legacy scope duplication. EN page HTML, CSS, site links and RU/ES not modified.
- Updated embedded strict sitewide expected text to match the already-changed scope pricing wording and SEO delivery-time disclaimer, not lower requirements. All checks must be rerun on this commit. Context guard on prior bb9b418 PASSED, WCAG automation PASSED; prior strict+Pages failed due old test and cannot count as pass.
- STATUS CODE_QA_PENDING / VISUAL_QA_PENDING / PRODUCTION_NOT_DEPLOYED. Next: observe full CI and browser logs, correct real issues only.


## 2026-10-16 — EN HOME OWNER OVERRIDE: BROAD CUSTOMER-FACING SEO SERVICES (QA PENDING)
- Owner states current three visible cards are NOT all SEOImpuls services. Changed **EN homepage only** to nine clear SEO work areas: SEO Audit; Keyword Research; On-Page SEO; Technical SEO; SEO Competitor Analysis; SEO Content Optimization; Local SEO; International SEO; SEO Consultation. Data file `data/en_home_services.json` defines simple customer problems, scoped examples of results, three existing direct detail routes and six contact-anchor enquiries. No new URLs or fixed-package promises.
- Layout `layouts/index.html` renders nine balanced lightweight CSS-only service cards above a compact process, removes the redundant EN supplementary-services list, fixes the unnecessary large empty process panel, differentiates hero CTA to an enquiry, retains one H1 and existing schema. SEO definition/deliverables/FAQ/contact updated to avoid implying only three kinds of work or unconditional written plans/edits. EN front matter `content/_index.md` and EN nav in `hugo.toml` aligned; no old service image reuse. CSS scoped to EN only.
- Regression gates updated: `scripts/verify_en_services_route.py`, `scripts/audit_en_services_browser.cjs`, `scripts/audit_en_home_accessibility.cjs`, `.github/workflows/rebuild-qa.yml`. Project rules/plans updated, previous three-cards-only decisions superseded.
- Buyer-market terminology sampled in 2026-10-16 public search and Google Search Central, but precise query volume, organic keyword difficulty, actual user market GSC and exact physical-location Google top-10 UNVERIFIED. No false ranking numbers/cases/prices. Actual capabilities such as direct implementation or local profile editing require scoped agreement.
- **STATUS EDITED_QA_PENDING / NOT PRODUCTION-DEPLOYED** until strict Hugo/whitehat, Pages noindex, Chrome 390/768/1280, axe and actual preview visuals pass on this exact revision. Work remains limited to EN homepage and direct test/nav dependencies. Next: inspect CI and browser screenshots and resolve any actual failures; do not change RU/ES or other EN detail pages.


## RULE 2026-10-16 — Do not reference live brand domain
User explicitly prohibits citing/linking to the currently operating SEOImpuls domain during the redesign. Work exclusively from GitHub branch `white-seo-rebuild` and its preview URL. Do not open the live domain to compare or audit it, do not include its URL in replies, and do not cite it as evidence. Production/DNS/CDN remain untouched. This is a permanent communication and audit-scope rule for follow-up sessions, even if older project docs mention the production address.
Only project documents updated in this commit (AGENTS.md and CHATGPT_PROJECT_CONTEXT.md); no site code, deployment, URL, locales or design changed.


## AUDIT — 2026-10-16: EN HOMEPAGE VISUAL + CONTENT BALANCE
- Docs-only audit `docs/research/2026-10-16-en-home-balance-audit.md` completed against EN source and refreshed GitHub Pages preview (?audit=20261016a), current branch prior head 06dac77d; NO homepage HTML, CSS, JS, URLs, other locale, production or deployment changes.
- Confirmed accepted 3 paid EN offerings and only 3 non-commercial scope lines, self-consistent canonical/Title/H1 as previously tested; prior strict/preview/browser/axe PASS retained for unchanged source, not newly re-run today.
- **P1 OPEN:** first-fold process panel substantially oversized/empty vs narrow paid service cards; duplicative 01/02/03 across steps, offers and deliverables; header singles out Technical SEO Audit; hero/process implies automatic “practical plan” although consultation written plan is separately scoped; broad SEO Audit card labels a Technical SEO Audit URL; “Keyword Research & Clustering” remains jargon.
- **P2 OPEN:** redundant hero/definition/deliverables/FAQ/CTA explanation, non-distinct hero buttons; full-width Contacts bar animation not geometry-certified; 768 nav tall and 390 cookie wall; commercial H3 cards lack dedicated visible group H2. Source/preview differences due to stale browser tab were cleared by re-navigation.
- No fabrication of case studies, screenshots, prices, search-volume claims or previous rejected hypothetical noindex example; real ranking/traffic, live CrUX, exhaustive geo SERP and GSC remained unverified.
- **STATUS AUDIT_DOCUMENTED / CODE_UNCHANGED / PRODUCTION_UNTOUCHED.** Next: owner-directed EN homepage layout/buyer-message improvements; re-run all QA and update this file with each subsequent change.

## ACCEPTED CODE + VISUAL QA — 2026-10-16: EN HOMEPAGE BUYER COPY SIMPLIFICATION
**SCOPE:** EN homepage only; owner has not approved another page or production publication.
- Exact content/layout source `755e52d` introduced 3 brief non-commercial supporting SEO tasks instead of 8 apparent services, only 3 main cards, no old `seo-icon-google.svg` EN illustration; 3 original EN CSS service marks remain.
- User-facing SEO copy now explains website audit for an existing site, keyword research/clustering before a site exists, and consultation as guidance. Concrete deliverables: Website Audit Report, Keyword Research Spreadsheet, Consultation Priorities; no automatic written consultation plan/implementation promise. Updated pricing/timing and contact CTA `Discuss Your SEO Project`.
- **STRICT PASS** on final QA-only head `50965ff`: [#38918895547](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38918895547). GitHub Pages noindexed preview **PASS**: [#38918895213](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38918895213). Context guard PASS: [#38918895395](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38918895395).
- Same unchanged site source browser **PASS**: [direct 390/768/1280 #38918077643](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38918077643), [home visual 390/1280 #38918077646](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38918077646), [automated axe 390/1280 #38918077640](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38918077640). All dedicated Chrome arrays `fail:[]`, no broken routes, network/JS faults, horizontal overflow or fixed social-icon text overlaps. H1 `Professional SEO Services`, Title, 3 child routes and canonical unchanged.
- Screenshots artifact [#12054026326](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38918077643/artifacts/12054026326) downloaded/inspected at mobile 390, tablet 768, desktop 1280; three simple supporting text rows legible, links/card panels intact. No comprehensive WCAG certification: axe reported 0 confirmed violations, with 2 ARIA and 62 contrast incomplete nodes at both checked sizes. Full-width floating Contacts bar, 768 header, 390 mobile cookie wall, oversized 1280 process box and detailed field CWV not fixed by current request.
- **STATUS CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / COPY_SIMPLIFICATION_DONE / OWNER_REVIEW_PENDING / PRODUCTION_NOT_DEPLOYED**. Current documentation commit records evidence only, no site code changes.


## 2026-10-16 — EN HOMEPAGE QA: UPDATE BUSINESS-DEFINITION EXPECTATIONS (PENDING)
- Source `755e52d` unchanged: simplified 8 extra scope blocks to 3 examples with search-facing names, plain-language buyer copy.
- Strict run #38918491957 passed the new parser-based 3-row count and stopped in the downstream sitewide-copy assertion, which still required the previous literal phrase `keyword research can start before a website exists` and `website changes are separately agreed`. New EN definition explicitly says `You can order keyword research for a business idea before you have a website` and `does not include website changes unless separately agreed`. This is the same factual scope expressed more clearly; outdated exact-text assertions are corrected without dropping the meaning checks.
- Site source not modified; only `.github/workflows/rebuild-qa.yml` and context/plan updated in this commit. New strict+Pages must pass; dedicated Chromium/visual/axe tests already passed on exact source `755e52d` but manual screenshots and final QA still to be recorded.
- Owner lock: work only on EN homepage, no changes to other pages or production.


## 2026-10-16 — EN 3-LINE SCOPE STATIC TEST MINIFICATION FIX (QA PENDING)
- New source `755e52d` Hugo compilation and JSON-LD home checks PASS. Strict #38918077584 and Pages preview #38918077632 stopped at the EN-only supporting-scope static assertion: it counted only `data-home-field="offerItem...` with quotes in minified HTML. Hugo minifier omits optional quote characters. This is an invalid assertion, NOT proof that page renders 8 items.
- Same source responsive Chrome dedicated #38918077643 PASS, general home #38918077646 PASS and axe #38918077640 PASS. Screenshot review remains to be completed.
- Corrected both static and sitewide CI verification to count **actual parsed LI `data-home-field` attribute values via HTMLParser**, requiring exactly `offerItem1`, `offerItem2`, `offerItem3`. No page HTML/CSS/text changed in this follow-up. New strict/Pages runs must pass before acceptance; exact source content remains commit `755e52d`.
- Only home scope checks and documentation changed; never auto-start a different page or deploy production.

## ACTIVE WORK — 2026-10-16: EN HOMEPAGE BUYER SIMPLIFICATION (QA PENDING)
Owner directs: «Приоритет — сначала сократить восемь дополнительных блоков и исправить тексты для клиентов». Authorized scope **ONLY EN homepage**; do not start any other page, change existing EN detail service page content, RU/ES, production, main, DNS or GSC.
- Replace 8 falsely independent supporting scope tiles with only 3 short explanatory lines: Competitor research; Page and content improvements; Fixes and follow-up. Clarify optional, separately scoped work; no new commercial products or routes. Use compact one-column EN-only styling. RU/ES old 8-row source remains guarded and untouched.
- Rewrite home meta description, definition, standalone keyword spreadsheet deliverable, realistic audit/consultation outcomes, pricing/time FAQ and CTA in plain language for business owners **with or without a website**. Consultation written plan is *not* implied automatically: writing remains separately scoped.
- EN old decorative `seo-icon-google.svg` will no longer render because its item is localized-only; original files preserved in Git. Three primary cards remain CSS 01/02/03, with untouched internal URLs `/technical-seo-audit/`, `/keyword-research/`, `/seo-consultation/`; all SEO Title/H1/canonical/hreflang untouched.
- Targeted file changes: `content/_index.md`, EN conditional markup/styles in `layouts/index.html`, `scripts/verify_en_services_route.py`, `scripts/audit_en_services_browser.cjs`, current EN homepage assertions within `.github/workflows/rebuild-qa.yml`, active plan and this journal.
- Status **EDITED_QA_PENDING** until strict Hugo+whitehat, Pages/noindex, Chrome 390/768/1280, home browser, WCAG automation and screenshots are checked. Any older PASS is irrelevant for changed content. No production deployment or automatic page change.


## 2026-10-16 — Read-only post-change audit of EN homepage
- Report written to `docs/research/2026-10-16-en-home-post-css-audit.md` using source `00881d5`, current docs-only head `98763ec`, actual Pages preview, Actions #38914027341/#38914027471/#38914027320/#38914027575/#38914027393 and screenshots #12052215561.
- Technical build and three SEO routes are GREEN. Three CSS-only service marks intact, 0 old image tags within main cards, 0 broken internal routes or measured social icon overlaps.
- **P1 CONTENT GAP:** 8 additional scope tiles recreate service-choice confusion beyond 3 actual offers; website-only pricing/CTA phrasing contradicts keyword research without a website.
- **P2:** Old `/uploads/seo-icon-google.svg` remains in EN supplementary section; desktop process/card height imbalance and duplicate 01/02/03; tablet 768 header wraps; mobile 390 consent covers substantial viewport; heavy SEO jargon / unclear standalone keyword deliverable.
- **P2 VERIFY:** full-width floating Contacts bar intersection not measured beyond social icons; screenshot stitched bar alone is insufficient to confirm permanent obstruction.
- **P3:** axe has zero confirmed violations but 72 contrast/2 ARIA incomplete nodes; manual confirmation pending. No Lighthouse/CrUX/SERP validation.
- **STATE: CODE_QA_PASS / CONTENT_UX_CHANGES_REQUIRED / OWNER_REVIEW_PENDING / PRODUCTION_NOT_DEPLOYED**. This task changed only audit documentation and root context, not site code or other pages. No fixes or automatic next page.


## 2026-10-16 — EN RESPONSIVE CSS SERVICE MARKS: CODE + VISUAL QA PASS, OWNER REVIEW PENDING
- Accepted immutable source: commit `00881d5`. EN homepage `/#services` now uses three **original CSS-only** numerical markers (01 / 02 / 03); zero old graphic `img` elements in the three service cards. Original SVG files are retained in Git; the brand logo, unrelated images, RU/ES and existing service detail pages remain unchanged.
- Strict Hugo/sitewide whitehat **PASS**: [#38914027341](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38914027341). GitHub Pages preview/noindex **PASS**: [#38914027471](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38914027471). Context guard **PASS**: [#38914027698](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38914027698). EN homepage visual Chrome **PASS**: [#38914027575](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38914027575). Automated axe WCAG diagnostic **PASS**: [#38914027393](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38914027393) (not full WCAG certification).
- Dedicated direct-services browser Chrome [#38914027320](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38914027320) **PASS** at all 390 / 768 / 1280 px. Exact measured CSS marks: 38×38 / 38×38 / 46×46 px. Each service-card `imageCount=0` and labels 01/02/03; service route paths unchanged. All `fail:[]`, no broken internal links, JS/network faults, horizontal overflow, or text overlap with floating WhatsApp/Telegram shortcuts. Header/anchor clearance: 390 115/81, 768 192/171, 1280 115/79.
- Downloaded screenshots [#12052215561](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38914027320/artifacts/12052215561) and **manually inspected** `390-services.png`, `768-services.png`, `1280-services.png`: no visible clipping or overlap; 390 one card per row, 768 two plus one full width, desktop right column with three stacked cards.
- Prior revision `5d5c281` had a genuine CSS grid mark-width defect, now corrected and re-tested on `00881d5`. Previous failed run cannot count as pass for earlier source.
- **CURRENT STATUS: CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / OWNER_REVIEW_PENDING / PRODUCTION_NOT_DEPLOYED.** This latest documentation-only commit does not alter site visuals. Do not restore legacy artwork to EN service cards or work on another page without the owner's explicit instruction.


## 2026-10-16 — EN CSS MARK SIZE CORRECTION (CI PENDING)
- First new CSS-only service-card iteration `5d5c281`: Hugo strict #38913678211 PASS, Pages preview #38913678395 PASS, general homepage visual browser #38913678362 PASS, axe WCAG automated #38913678269 PASS, context #38913678442 PASS. Dedicated 390/768/1280 service browser #38913678415 FAIL due to genuine **new mark aspect ratio** defect: marker rectangles were 20.8×38 at 390, 18.4×38 at 768, 22.3×46 at 1280. Images in cards = 0 and original routes/no-overlap checks otherwise passed. CSS grid child width:100% resolved to narrow intrinsic track.
- Targeted fix explicitly sizes the CSS mark itself to `clamp(38px,4vw,46px)` in both dimensions; parent stays responsive. No page copy, image files, other service pages or production changes. Browser and strict/preview must re-run to confirm; do not borrow prior PASS.
- OWNER SCOPE: only EN homepage service-card visual; no automatic move to another page.



## 2026-10-16 — НОВОЕ ПОРУЧЕНИЕ: НЕ ИСПОЛЬЗОВАТЬ СТАРЫЕ ИЗОБРАЖЕНИЯ В EN КАРТОЧКАХ, ДЕЛАТЬ СОБСТВЕННЫЙ АДАПТИВ
Владелец: «картинки пока наши не используем, будем делать свой адаптив». Ограниченная реализация: только три карточки услуг английской главной; прежние SVG-иконки в них заменены на собственные CSS-маркеры 01/02/03, без новых изображений или дополнительных запросов ресурсов.
- В `layouts/index.html` добавлены только EN-условия, собственные градиенты/рамки/числовые маркеры и адаптивные стили. RU/ES fallback сохраняет старые изображения; исходные assets не удалялись. Логотип, другие картинки и внутренние страницы не менялись.
- Три прямые ссылки `/technical-seo-audit/`, `/keyword-research/`, `/seo-consultation/`, главный H1/Title, SEO metadata, canonicals, hreflang, страницы услуг и якорь `#services` не менялись.
- Новые проверки `scripts/verify_en_services_route.py` и `scripts/audit_en_services_browser.cjs` проверяют отсутствие `img` в EN карточках, 3 CSS-маркера с корректной геометрией, исходные assets в репозитории, ссылки, 390/768/1280, плавующие WhatsApp/Telegram и отсутствие переполнения.
- НЕ трогать production, main, RU/ES и другие EN страницы; не начинать следующую страницу автоматически.
- **EDITED_QA_PENDING**, пока не завершены Actions Hugo strict + Pages preview + Chromium 390/768/1280 и визуальная проверка скриншотов. Предыдущие PASS для старой версии не являются доказательством нового варианта.


## CURRENT FINAL TECHNICAL STATUS — 2026-10-16, EN SERVICE KEYWORD ROUTES
**OWNER_REVIEW_PENDING, NOT DEPLOYED TO PRODUCTION.** Latest content/layout source commit 833cb99; no other pages may be started without explicit new owner instruction.
- Exact 3 commercial EN routes validated in Hugo output: /technical-seo-audit/ has HTML Title "Technical SEO Audit | SeoImpuls", one H1 "Technical SEO Audit", canonical self; /keyword-research/ similarly "Keyword Research"; /seo-consultation/ similarly "SEO Consultation". EN homepage title/H1 "Professional SEO Services", homepage menu/hero Services link to #services; three direct service cards. No EN /seo/, /seo-services/, /services/, /services/keyword-research/, /services/seo-consultation/ in built candidate, sitemap or internal links. RU/ES language sources unchanged; hreflang reciprocal to valid new EN service URLs. Commercial EN page schema is WebPage not BlogPosting.
- PASS: strict Hugo/sitewide whitehat [#38912159752](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38912159752); Pages Preview [#38912159880](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38912159880); context guard [#38912159761](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38912159761).
- PASS: three-service Chromium at 390/768/1280 [#38912159784](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38912159784): HTTP 200, 3 exact direct links, valid Title/H1/canonical/schema, no obsolete catalogue, internal links checked, no runtime/network errors, no horizontal overflow; floating WA/TG collision against **ALL** main homepage text `[]` at all three widths. Services-anchor section top vs header bottom at 390=115/81, 768=192/171, 1280=115/79. Tablet desktop footer override and EN reserved 120px left rail accepted; shortcut icons themselves left fixed and unchanged.
- PASS: general home visual browser [#38912159853](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38912159853), axe WCAG **automated diagnostic** [#38912159768](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38912159768). These are automated checks, NOT a formal WCAG conformance or Google CWV ranking certification.
- Screenshots [artifact #12050378578](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38912159784/artifacts/12050378578) downloaded and MANUALLY examined at 390/768/1280 (first/services views, desktop full). Observed clear 3 services and no text overlap at final 120px rail. No new images/source fake proof.
- **STATE: CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / OWNER_REVIEW_PENDING / PRODUCTION_NOT_DEPLOYED**. Exact SEO search volume and national rank not verified; URL keyword is intent-alignment, not ranking promise. Greenfield old URL redirects not applied on live server.
- This acceptance record updates only docs/context, not the accepted source. Next: wait for owner's instruction, not automatic work on any other page.


## 2026-10-16 — EN FLOATING ICON TRANSITION RAIL 120px (QA PENDING)
- Strict Hugo/whitehat #38911715468 PASS, preview #38911715464 PASS, EN home visual browser #38911715555 PASS, axe WCAG #38911715467 PASS for preceding EN 64px rail. Stricter direct services browser #38911716000 caught a real collision outside card boundaries during dynamic footer movement, despite screenshots sometimes appearing okay.
- Actual overlap rectangles: 768 WhatsApp x32..76 over text starting x64, Telegram x46..90 over heading starting x64; 1280 WhatsApp x35..83, Telegram x58..92 over explanatory paragraph starting x64. Original 64px rail is inadequate for moving shortcuts.
- Kept footer and shortcut animation unchanged. Increased EN-home content left rail (all viewport widths >=768) from 64px to **120px**, leaving at least 28px safety beyond observed rightmost shortcut at x92. Direct browser continues to inspect all homepage text and records exact bounding rectangles, not just cards.
- No other page, link, URL, title, H1 or locale source changes. Status EDITED_QA_PENDING until new strict + Pages + 390/768/1280 browser, screenshots inspected. Do not proceed to unrelated pages.


## 2026-10-16 — MANUAL VISUAL FINDING: 1280px shortcut overlap below service cards (QA PENDING)
- First combined strict/Hugo #38911153927 PASS, preview #38911153919 PASS, three-way direct service browser #38911154181 PASS at 390,768,1280, EN home browser #38911153939 PASS, axe diagnostic #38911154116 PASS. The previous automated service browser inspected floating icon collisions only with texts INSIDE the 3 service cards.
- Downloaded screenshot artifact #12049823824 and manually inspected 390,768,1280 initial/services. **Found a real remaining 1280px visual regression**: fixed WhatsApp/Telegram shortcuts at far left overlap first line of the "What Are Professional SEO Services?" explanation immediately below 3 cards. Do NOT claim final visual PASS yet.
- Expanded EN home 64px reserved left text/content gutter from 768–1199 to ALL widths >=768, preserving original fixed icon positions and footer animation. Expanded dedicated Chrome overlap test to check all readable elements inside .seo-central--en, not just card text, and log exact bounding rectangles. No global CSS/shared footer changes.
- Status EDITED_QA_PENDING; new strict, Pages, browser 390/768/1280, WCAG and screenshot inspection required. Work remains limited to authorized EN home/direct service route architecture; other languages' content and production untouched.


## 2026-10-16 — EXACT 768px FOOTER BREAKPOINT + QA COPY CORRECTION (RUNS PENDING)
- EN homepage browser #38910448011 still showed 768px fixed shortcut overlap in service cards (390 and 1280 PASS); fresh screenshot #12050445799 shows the readable text starts at x64, but at exactly 768 the legacy mobile footer rule still renders Contacts inside top header while desktop floating rules apply simultaneously. This is a real breakpoint conflict independent of extra left gutter. Scoped EN-only 768px footer fix mirrors the prior accepted EN catalogue fix: body.footer-floating .custom-footer--en-home position fixed, hidden bottom -96px and normal popup bottom 0. No change to global footer or WA/TG shortcuts. Browser QA now logs any overlapping button/text rectangle coordinates, without weakening its fail condition.
- Strict #38910447930 all routes, schema, hreflang and retired URL validations PASS and reached final sitewide EN text gate, which expected old homepage explanatory phrases. Updated this specific QA to the newly approved plain-language business definition, keeping content and SEO assertions strict. The earlier broad-string replacement had accidentally altered localized menu expected path to /ru/technical-seo-audit/ and /es/technical-seo-audit/; corrected assertions to preserve actual /ru/seo/ and /es/seo/ localized menus, no locale files modified.
- Preview #38910447841 SUCCESS, homepage visual #38910447974 SUCCESS and WCAG automated diagnostic #38910447779 SUCCESS for the source before this follow-up; new follow-up code still needs fresh CI.
- Current state **EDITED_QA_PENDING**; only new verified runs can close. No live production, DNS, GSC or another language content edit.


## 2026-10-16 — FOLLOW-UP FIXES: PREVIEW CANONICAL, RU/ES MENU, 768px ICON COLLISION (QA PENDING)
- First new-route GitHub Actions after de1e05e validated all three new service URL/Title/H1/metadata/WebPage/hreflang tests against production-base Hugo. Full strict #38909786931 then found two real obsolete outgoing anchor links /seo-services/ from RU/ES service-catalogue language switchers. These are automatically rendered by the SHARED header, not from RU/ES source. Scoped header fix: when switching from local services catalogue RU/ES to EN, go to the existing EN homepage /#services, not the retired EN catalogue. No RU/ES source copy or localized URL edit.
- Preview #38909786575 failed because dedicated route QA assumed production host canonical. Real preview build uses https://agurkin2021-gif.github.io/seoimpuls/; the test now accepts production or known GitHub Pages origin while still enforcing exact route, Title, H1, canonicals and reciprocal hreflang.
- Browser services #38909786373 390/1280 passed but at 768 viewport detected WA/TG fixed icon overlap with homepage service text. Screenshot artifact #12049059512 verified floating WhatsApp icon and nearby text collision under service cards. Scoped EN-home CSS reserves a 64px left content rail on 768–1199 widths while leaving floating buttons fixed in their original position. No global footer changes.
- This follow-up commit changes ONLY EN home CSS in layouts/index.html, conditional shared header links, preview-aware EN route checks, context and direct-architecture plan. **EDITED_QA_PENDING** until strict + Pages + Chrome confirm. No production/DNS/GSC edit or other page content changes.


## 2026-10-16 — QA feedback after commit 3289214, script-only correction
- Hugo built successfully. Dedicated 3 EN route checks passed Title/H1/canonical/hreflang/schema for /technical-seo-audit/, /keyword-research/, /seo-consultation/.
- Full strict #38909519843 and Pages #38909519450 stopped only at stale test assertion seeking literal "keyword-research" in document anchor IDs. Existing valid keyword page uses anchors "what-is-included", "methodology", "deliverables"; fixed assertion to check those meaningful IDs. No content/page source change for this correction.
- Browser service-selector #38909519226 failed starting test webserver readiness because workflow still curled retired /seo-services/ (404); now curls existing /.
- Code remains EDITED_QA_PENDING until fresh Hugo, Pages and browser tests pass. Do not start any other page automatically.


## ACTIVE OWNER ORDER (2026-10-16): HOMEPAGE DIRECT EN SERVICES, EXACT PHRASE IN URL+TITLE+H1
Supersedes earlier page lock ONLY /seo-services/: user showed homepage existing service cards, ordered no extra /seo-services/ page, questioned /services/ prefix and then insisted /seo/ must become a real target-keyword URL with matching title.
- EN homepage owns Professional SEO Services, direct 3 service cards at /#services; menu and primary CTA also go to /#services. Keep existing illustrations and customer-friendly wording. Remove lower duplicate service selector.
- EN technical old /seo/ -> /technical-seo-audit/: Title Technical SEO Audit | SeoImpuls; H1 Technical SEO Audit. Main phrase technical seo audit; secondary phrase technical seo services only in supporting text. Existing SERP observations and fresh market examples corroborate buyer intent, not demand/position statistics.
- EN keyword old /services/keyword-research/ -> /keyword-research/: Title Keyword Research | SeoImpuls; H1 Keyword Research; clustering remains included and can be ordered for a business without a website.
- EN consulting old /services/seo-consultation/ -> /seo-consultation/: Title SEO Consultation | SeoImpuls; H1 SEO Consultation.
- EN /seo-services/ made a draft, old /services/ alias removed, all 5 old EN URLs removed from candidate generation/linking. No current production URL or redirect changes.
- RU/ES content sources and native URL patterns remain unchanged; bilingual hreflang must point to live new EN routes. EN service schema corrected from BlogPosting to WebPage only for these three services. About/FAQ/menu are necessary EN link dependents.
- Update only this assigned architecture and its tests; no unrelated pages, main or production changes. Context written in same commit. New plan: docs/plans/EN_DIRECT_SERVICES_ARCHITECTURE.md.
**EDITED_QA_PENDING:** strict Hugo/Pages/Chrome not yet run on these staged edits; do not claim passing or release. Do not automatically start next pages.


## 2026-10-16 — ПОСЛЕДНЯЯ ПРИНЯТАЯ ТЕХНИЧЕСКАЯ ВЕРСИЯ EN /seo-services/ (OWNER REVIEW PENDING)
- **ONLY /seo-services/** — вторую страницу не считать закрытой до решения владельца; запрет самовольного перехода на любые другие страницы остаётся в силе.
- Рабочий исходник `9266336`: три реальных коммерческих предложения **SEO Audit / Keyword Research / SEO Consultation** с понятными предпринимателю результатами и исходными изображениями (включая semantic illustration `semantika-1788907052-q46-1788907068324.webp`); нет повторных 3 карточек выбора. Дополнительно только 2 информационные карточки SEO Competitor Analysis / On-Page SEO, без новых коммерческих URL/тарифов. Сбор ключевых слов возможен до готового сайта; результат — таблица с группами запросов.
- Проверка **PASS**: Hugo + strict white-hat #38905365028, Pages preview/noindex #38905365102, context #38905364899, Chrome 390/768/1280 #38905365160. Логи Chrome на всех ширинах `fail:[]`, HTTP 200, 3 основные карточки, 0 вторичных дублированных selector-карточек, 2 дополнительные группы / 6 примеров, 0 old 23-card workstreams, 0 битых внутренних ссылок, JS/network ошибок, horizontal overflow. Telegram/WhatsApp fixed icons (768/1280) не пересекают текст.
- Скриншоты артефакта #12048086527 скачаны и изучены вручную (390,768,1280 first/category + 1280 full). Нет замеченного обрезания текста, перекрытия и критических визуальных дефектов. Это не гарантия полного WCAG или коммерческой конверсии.
- **STATUS: CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / OWNER_REVIEW_PENDING**, не "идеально", не production release. Текущий документационный коммит только фиксирует результаты проверки неизменного кода `9266336`. Только отдельная команда владельца позволяет переходить к другой странице.


## 2026-10-16 — MORE PRECISE EN /seo-services/ UX: NO REPEATED SERVICES (QA PENDING)
OWNER SCOPE LOCK: work ONLY EN /seo-services/. DO NOT switch to any other page without a new explicit user instruction; do not touch main, production, homepage, RU, ES or specialist pages.
- Latest buyer-friendly source e7f9188 PASSED strict Hugo #38904642890, Pages Preview #38904642446, Chromium 390/768/1280 #38904642723 and context #38904642597. Screenshot artifact #12048005196 manually examined. Found non-critical but real UX issue: the same 3 linked services were visible twice (hero image cards + a duplicate 3-choice selector); two of them were reiterated in a 4-area scope matrix. This overcomplicated selection for a non-SEO business owner.
- Current targeted revision removes the repeated 3-choice selector and redundant SEO Audit/Keyword Research scope entries; retains exactly 3 actual commercial offers with images and plain-language descriptions; only 2 **informational, non-published as product** entries remain below: SEO Competitor Analysis and On-Page SEO. They are separately scoped only if actually deliverable; no new indexed URLs or false service claims.
- Edited files ONLY `data/en_seo_catalog.json`, `layouts/partials/en-services-catalog.html`, `scripts/verify_en_services_route.py`, `scripts/audit_en_services_browser.cjs`, the active plan and this context. Existing Title, H1, SEO metadata, 3 service URLs, 3 original images, CTA, example, FAQ, language links, floating contacts and production remain intact.
- Status **EDITED_QA_PENDING** for this exact iteration. The previous green CI runs do not verify this source revision. Next: inspect strict Hugo + noindexed Pages Preview + Chrome 390/768/1280 and screenshots; fix only any proven EN /seo-services/ defect. Never auto-transition.


## АКТИВНАЯ ЗАДАЧА 2026-10-16 — понятные услуги с поисковыми запросами (QA PENDING)
**ВЫШЕСТОЯЩИЙ ЗАПРЕТ: работать только с EN /seo-services/; не переходить на другие страницы без новой прямой команды владельца.** Продакшен, main, домашняя EN страница, /seo/, соседние EN услуги, RU и ES — не изменять.
- Новый запрос владельца: названия услуг должны включать узнаваемые англоязычные SEO-поисковые фразы, но описания обязаны быть понятны владельцу обычного бизнеса, не специалисту по SEO: проблема → польза → результат.
- В каталоге остаются только **3 реально опубликованных коммерческих направления**: SEO Audit (URL /seo/), Keyword Research (URL /services/keyword-research/), SEO Consultation (URL /services/seo-consultation/). В карточки добавлены короткие человеческие описания результата; оригинальные изображения сохранены.
- Для Keyword Research явно объяснено, что сбор поисковых фраз и их группировка (clustering) — самостоятельная услуга с результатом в электронной таблице; работа возможна до появления сайта. Оригинал рисунка /uploads/semantika-1788907052-q46-1788907068324.webp сохранён без изменений.
- 4 информационные карточки содержат темы SEO Audit, Keyword Research, SEO Competitor Analysis, On-Page SEO и объясняют их без жаргона. Последние два направления НЕ объявлены подтверждёнными отдельными продуктами и не получили новых URL/цен: лишь возможный согласуемый объём работ.
- H1 EN каталога специально изменён с "Choose the Right SEO Work for Your Website" на "Find the Right SEO Service for Your Business" в связи с новым поручением; SEO Title "SEO Audits, Keyword Research & Consulting | SeoImpuls", URL и canonical сохранены. Сокращён профессиональный жаргон в FAQ, CTA, примере и процессе; внутренний проверяемый QA-отчёт сохранён, но скрыт в разворачиваемом блоке, чтобы не перегружать посетителя.
- Изменяются только `content/services/_index.md`, EN-ветка `layouts/partials/services-hub.html`, `data/en_seo_catalog.json`, `layouts/partials/en-services-catalog.html`, `scripts/verify_en_services_route.py`, `scripts/audit_en_services_browser.cjs`, одна проверка H1 /seo-services/ в `.github/workflows/rebuild-qa.yml`, `docs/plans/EN_SEO_SERVICES_SIMPLIFICATION_PLAN.md` и этот контекст. Изображения/детальные страницы/домены/публикация на основном сервере не тронуты.
- Публичные конкурентные страницы подтверждают употребимость названий услуг как формулировок, но **нет проверенной частотности или достоверного локального Google SERP top-10**. Не объявлять это измерением поискового спроса.
**ТЕКУЩИЙ СТАТУС: EDITED_QA_PENDING; после Git-коммита проверить Hugo/strict, Pages noindex, Playwright 390/768/1280 и скриншоты. Не объявлять PASS до подтверждённых результатов. После проверки всё равно оставаться на /seo-services/ до команды владельца.**



## /seo-services/ ACCEPTANCE EVIDENCE — 2026-10-16 (OWNER REVIEW PENDING)
- Current page source `46bc35e` and EN-only assertion fix `462aa03`. New page is accessible in **GitHub Pages preview**; original production server untouched.
- Latest strict Hugo + EN page assertion + sitewide whitehat gate **PASS**: [Actions #38899685820](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38899685820). Pages preview / noindex deployment **PASS**: [#38899685817](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38899685817). Context guard **PASS**: [#38899685925](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38899685925).
- EN responsive browser checks **PASS** on exactly unchanged page HTML/CSS/JS source `46bc35e`: [#38899499592](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38899499592) at 390,768,1280; each `fail:[]`, exactly 3 main services, 3 buyer choice paths, 4 informational scope areas, 12 examples, 0 old 23 workstream tiles, 0 granular email CTAs; links, meta, breadcrumb JSON-LD, canonical, keyboard FAQ, interactive sample link and layout validations passed. 768px floating contact icons 2, text collisions 0; 1280 icons 2, collisions 0; no horizontal overflow, JS/failed networks/broken URLs.
- Screenshots from artifact [#12044858940](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38899499592/artifacts/12044858940) downloaded and MANUALLY inspected: 1280-full, 390-full, 768-category and viewport-first screenshots. Observed four areas laid out 2×2 desktop/tablet and single column mobile; no obvious clipping or overlap in examined views. Screenshot evidence is not a complete accessibility or usability certification.
- **STATUS: CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / OWNER_REVIEW_PENDING**. Never call page "closed" unless owner approves. Next owner-facing action: evaluate the simplified second page. **Absolutely do not switch to any other page without explicit new owner command.** Historical GSC/migration blockers are irrelevant to this greenfield rebuild.



## EN /seo-services/ TARGETED QA SCRIPT FIX — 2026-10-16
- Initial source change `46bc35e` compiled successfully under Hugo but full rebuild and Pages preview checks #38899499369/#38899499275 FAIL at EN-only `scripts/verify_en_services_route.py`: script still searched retired heading `SEO Work We Can Scope`, so selector ordering assertion failed.
- Corrected ONLY this stale expected heading to rendered `What SEO Work May Include` in the EN page validation script. No source/site content change in this fix; full strict/Pages/Chrome QA must rerun. Browser #38899499592 remained in progress at diagnosis.
- Status EDITED_QA_PENDING. Owner page lock /seo-services/ unchanged; never pivot automatically.



## /seo-services/ UX REDESIGN SOURCE — 2026-10-16 (QA PENDING)
OWNER LOCK: only EN `/seo-services/`, do not move to any other page without explicit new owner command.
- Previously shown 23 separate workstream-style tiles (with 20 granular mailto requests) now replaced by 4 concise descriptive scope areas, each 3 task examples (12 total), NOT independent packages.
- Three real services / 3 hero cards / 3 problem-to-service choices and approved H1, Title, canonical are preserved. No new indexed URL. FAQ wording clarified, specialist capabilities qualified; verifiable internal QA and illustrative finding remain.
- Source modified ONLY `data/en_seo_catalog.json` and `layouts/partials/en-services-catalog.html`; targeted EN QA scripts `scripts/verify_en_services_route.py` and `scripts/audit_en_services_browser.cjs` adjusted without dropping SEO head/schema/mobile/contact proof checks.
- No homepage, /seo/, child service sources, RU/ES, main or production edits; no production deployment.
- Status **EDITED_QA_PENDING**: Hugo strict/Pages/Chrome 390,768,1280 including screenshots must be checked AFTER commit. Prior PASS was for earlier 23-tile version.
- Continue ONLY this page until user instructs otherwise.


## АКТУАЛЬНОЕ ПОРУЧЕНИЕ — 2026-10-16: ВОЗОБНОВИТЬ ТОЛЬКО ВТОРУЮ EN СТРАНИЦУ
PAGE_SCOPE_LOCK_2026_10_16: EN /seo-services/ ONLY. NOT CLOSED. NO AUTO-PIVOT.

Владелец прямо сказал: «возвращаем вторую на доработку и сам не переходи на другие страницы без моей команды». Второй страницей в текущем проекте является каталог EN `/seo-services/`. Отменить предыдущий вывод «вторая закрыта», а также намеченный автоматический переход к `/seo/`. **Только пользователь имеет право разрешить начать следующую страницу** — даже после полностью зелёного CI и завершённого аудита каталога.

Причина повторного открытия: клиенту трудно воспринимать 23 карточки SEO-направлений; многие из них — компоненты более крупных работ, а не 23 отдельные понятные услуги. Исходники `data/en_seo_catalog.json` и `layouts/partials/en-services-catalog.html` проверены; текущая разметка содержит 23 подробных карточки, 20 частных email CTA и три самостоятельные коммерческие страницы. Нет 23 отдельных URL, поэтому нет доказанной прямой межстраничной каннибализации; присутствуют смысловая дубликация, избыточный выбор и возможное размывание интента.

ТЕКУЩИЙ ПЛАН (приоритет выше старого «FINISH_PLAN»): `docs/plans/EN_SEO_SERVICES_SIMPLIFICATION_PLAN.md`.
1. Сохранить URL, Title, H1, canonical и три реальные услуги/дочерних целевых URL.
2. Упростить блок со списком работ: убрать 23 равноправные подробные карточки и 20 контактных ссылок; показать максимум четыре понятные группы типичных задач как **состав работ**, а не как самостоятельные продаваемые услуги. Явно различать опубликованные и неподтверждённые специализированные направления.
3. Сохранить честное описание объёма, результата и ограничений, реальный QA-доказательный пример и FAQ, но удалить дубли и упоминание «23 пакетов» в клиентском интерфейсе.
4. Обновить ограниченные **только этой страницей** сценарии статической и браузерной проверки под новый UX, не ослабляя проверки SEO, schema, мобильности, контактов, floating кнопок, наличия реального proof и непротиворечивости предложения.
5. Выполнить Hugo + strict gate, GitHub Pages noindex preview, Playwright 390/768/1280. Старые PASS относятся к старому исходнику и НЕ подтверждают новый UX.
6. По окончании **остаться на `/seo-services/`**; не выполнять `/seo/`, главную, другие EN страницы, RU/ES или production. Не предпринимать следующие этапы сайта, пока владелец явно не даст новую команду.

Все изменения фиксировать с обновлением `CHATGPT_PROJECT_CONTEXT.md` в ТОМ ЖЕ коммите. Сам основной сервер, DNS, Search Console, редиректы и `main` не трогать.



## АКТУАЛЬНОЕ РЕШЕНИЕ ВЛАДЕЛЬЦА — 2026-10-16: НОВЫЙ САЙТ С НУЛЯ
GREENFIELD_MODE_2026_10_16: ACTIVE

Владелец сообщил, что существующий seoimpuls.com НЕ ИМЕЕТ поискового трафика, и прямо указал: «забудь про сам сайт не грузись, делаем всё заново». Это новое поручение ПЕРЕКРЫВАЕТ прежние ограничения, требовавшие проверки исторического трафика, GSC и поштучного согласования миграции старых URL как условия продолжения проекта.

**Стратегия:** разрабатывать SEOImpuls как новый сайт с чистой архитектурой на ветке `white-seo-rebuild`. Старый production, старые URL, обратные ссылки, GSC, исторические редиректы и сопоставление legacy-страниц больше НЕ ЯВЛЯЮТСЯ рабочими зависимостями и НЕ должны задерживать разработку новых страниц. Считать отсутствие трафика утверждением владельца, не выдавать его за собственное измерение. Старые миграционные документы — архивная история, не активный план.

**Сохранить результаты уже проделанной НОВОЙ работы:** проверенные EN главная `/` и EN каталог `/seo-services/` остаются в новой сборке; не удалять их и не переделывать без реального дефекта. Этапы 0–7 старого плана каталога завершены и не требуют повторного запуска. Предыдущая команда работать ТОЛЬКО над каталогом заменена текущим разрешением продолжить пересборку всего сайта.

**Новый план с этой даты (активный):**
1. Зафиксировать собственную EN URL/intent-архитектуру от нуля. Главная отвечает за `professional seo services` и выбор исполнителя; каталог `/seo-services/` — за выбор вида SEO-работ. Разделить интенты дочерних коммерческих страниц; избежать каннибализации, не плодить 23 тонкие страницы без основания.
2. Следующий EN объект после каталога — `/seo/` (technical SEO / audit). Проверить имеющийся SERP-срез на актуальность и релевантность; сделать узкий on-page/HTML/schema аудит и точечную переработку страницы, не затрагивая принятые главную и каталог.
3. Затем по одной завершить `/services/keyword-research/` и `/services/seo-consultation/`, каждая со своей семантикой, содержанием и QA.
4. Довести остальные необходимые EN страницы, навигацию, footer, About, FAQ, Contact, Privacy; исключить старое несоответствующее предложение из *нового* публичного HTML. Никаких придуманных кейсов, опыта, тарифов или гарантий.
5. Создать самостоятельные RU и ES версии по их реальным интентам, с согласованными URL, canonical/hreflang и без потерь функциональности.
6. Выполнить sitewide quality gate: Hugo, HTTP/HTML маршруты в новой сборке, 1 H1, Title/meta, индексируемость в релизе, noindex на предпросмотре, schema, sitemap, внутренние ссылки, адаптивность 390/768/1280, доступность и отсутствие реальных ошибок. Никакой обязательной проверки legacy GSC и старых 301 перед продолжением новой сборки.
7. Выпуск на production — отдельно, только после явного разрешения владельца. Работа с GitHub Pages preview разрешена; основной сервер/DNS/CDN/GSC по-прежнему не изменять без отдельного указания.

**Обязательные правила:** каждую правку сайта и документации сопровождать обновлением этого контекста в том же Git-коммите; работать только в `white-seo-rebuild`, не менять `main`; соблюдать честное white-hat позиционирование и поэтапные SERP/on-page/visual проверки. Предыдущие положения о GSC/301/клиентских доказательствах как универсальных блокерах релиза отменены: нельзя выдумывать клиентские результаты, но наличие кейсов не обязательно для новой версии без таких заявлений.

**Текущее состояние:** EN главная и `/seo-services/` приняты по существующему QA; остальная новая EN/RU/ES сборка IN_PROGRESS. **Следующее действие:** приступить к отдельной EN странице `/seo/` по новому плану, начиная с проверки исследования, интента, текущего source/rendered HTML и границы с `/seo-services/`. Это новая санкционированная фаза, а не ошибочное переключение из старой сессии.



## АКТУАЛЬНЫЙ СТАТУС И ОБЛАСТЬ РАБОТЫ — 2026-10-16 (исправление после перехода не на ту страницу)

- **Единственная текущая EN-страница владельца: `/seo-services/` (каталог SEO Services).** Переключение ассистента на `/seo/` было ошибочным; владелец явно вернул работу к каталогу. `/seo/`, главная, другие EN-страницы, RU/ES, `main` и production остаются вне области изменений.
- По `docs/plans/EN_SEO_SERVICES_FINISH_PLAN.md` этапы 0–7 завершены. Последняя принятая правка HTML/CSS/JS каталога — `ad90cbd`; Hugo/strict #38888649717 PASS, предпросмотр #38888649363 PASS, браузерный 390/768/1280 #38888649421 PASS, context #38888649376 PASS. Повторная проверка Opera показала каталог с тремя вариантами выбора и четырьмя группами работ; `content/services/_index.md` после принятого этапа не менялся.
- Последний ошибочный переход зафиксирован **только документами** в коммите `189651d`: `docs/plans/EN_TECHNICAL_SEO_PAGE_PLAN.md`, `docs/research/2026-10-16-en-technical-seo-serp-intent.md` и контекст. Эти документы сохранены как история, а НЕ активное поручение. Они **не дают разрешения** редактировать `/seo/`.
- Состояние каталога: **CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / RELEASE_BLOCKED**. Внешние блокеры: GSC/история URL, HTTP 301/404/410 на сервере, RU/ES контентное соответствие и рынки, подтверждённые клиентские доказательства, отдельное разрешение на production. **Без новых фактов не менять подтверждённую страницу ради видимости работы.**
- Следующее действие в разрешённой области: read-only контроль `/seo-services/` и основанная на фактических данных проверка любого нового дефекта. Не начинать `/seo/` или другие страницы; не публиковать production и не заявлять готовность миграции.

КРИТИЧЕСКОЕ ПРАВИЛО ПОЛЬЗОВАТЕЛЯ: ПОСЛЕ КАЖДОГО ИЗМЕНЕНИЯ ПРОЕКТА обновлять ЭТОТ ФАЙЛ в том же Git-коммите, что и изменение. Никаких коммитов с правкой сайта без обновления контекста. Если изменения внесены через несколько технических коммитов, каждый такой коммит обязан содержать актуализацию этого файла. Журнал должен позволять начать работу в другом чате без восстановления истории переписки.

## ТЕКУЩИЙ ПРИОРИТЕТ — EN services hub после завершения главной (решение владельца 2026-10-15)

- **2026-10-16: владелец потребовал продолжать только EN `/seo-services/` до полного контрольного аудита и устранения проверенных визуальных/интентных недостатков. Другие EN service pages НЕ начинать.**

- Владелец завершил работу над английской главной `/` и **отдельно разрешил** перейти к английскому каталогу услуг. Главная заморожена по контенту; разрешены только точечные зависимости ссылок при изменении адреса каталога.
- Рабочая версия каталога: **`/seo-services/`** на ветке `white-seo-rebuild`; прежний `/services/` — только HTML alias, **не серверный HTTP 301**. Интент: выбор SEO-работ по проблеме и результату. 23 направления — возможные виды работ в согласованном объёме; три действующие специализированные страницы остаются точками входа. Главная владеет `professional seo services` / выбором SEO-исполнителя.
- Английские дочерние `/seo/`, `/services/keyword-research/`, `/services/seo-consultation/` — отдельные целевые страницы, в этой фазе не переименовывать. **Не изменять RU `/ru/` и ES `/es/`** до отдельной команды. `main` и производственный сервер `seoimpuls.com` не затрагивать.
- SERP top-10 и map см. `docs/research/2026-10-15-en-services-serp-and-architecture.md`. Приоритет: изолировать интент каталога от главной, не выдавать `seo services list` за ключ каталога без оснований, не придумывать услуги/кейсы/цены.
- Предыдущая версия EN-каталога прошла Hugo/Pages/Playwright 390/1280 на `6099121`. **Нынешняя EN-страница (код `3878934`) прошла полный CODE_QA_PASS, strict white-hat gate и RESPONSIVE_VISUAL_QA_PASS на 390/1280** (Actions #38846778912, #38846778800; Pages #38846778882). Это не означает релиз, миграцию или GSC-проверку.

## 1. Проект, доступ и границы

- Название: SEOImpuls.
- Производственный сайт: https://seoimpuls.com/.
- Приватный GitHub-репозиторий: https://github.com/agurkin2021-gif/seoimpuls.
- Система: Hugo Extended, языки английский в корне, русский /ru/, испанский /es/.
- main — архив исходной версии; white-seo-rebuild — ветка для переделки.
- Ни в коем случае не изменять производственный сервер, DNS, CDN и Search Console без отдельного прямого разрешения пользователя.
- Никакой публикации исходного сайта через GitHub Pages. Никаких auto-deploy на сервер.
- Прежние SEO-материалы содержат предложения из области манипулятивного линкбилдинга. Сохранённый исходник НЕ является новой одобренной редакцией сайта.
- Секреты, данные доступа, SSH, .env, персональные данные и служебные дампы не включать в Git. Репозиторий приватный, но это не заменяет санитарную проверку.

## 2. Бизнес-цель и критерии

Полная постраничная пересборка сайта под настоящее, полностью белое SEO — не словесная маскировка серых методов. Исключить коммерческие предложения массовых обратных ссылок, автоматического размещения (XRumer, GSA, XEvil), PBN и сателлитов, Tier-каскадов, искусственного DR, ссылочного спама и обещаний гарантированного топа. Услуги предлагать только такие, которые команда реально оказывает. Реальные направления: technical SEO, on-page SEO, диагностика индексации, семантика и исследование интентов, информационная архитектура и перелинковка, стратегия контента, international SEO, SEO-консультации. Не придумывать кейсы, достижения или клиентов.

Каждая страница:
1. Инвентаризация исходного URL, текущего содержимого, Title, H1, canonical, hreflang, внутренних ссылок.
2. Актуальный SERP top-10 без рекламы по целевому языку/гео; intent map, конкуренты, gaps; отделять проверенные данные от гипотез.
3. Новый уникальный запрос/интент, Title, H1, URL, meta, контент. Не каннибализировать соседние страницы.
4. Сохранение дизайна/структуры и работоспособности, проверка мобильной версии, ссылок, structured data, alt, доступности.
5. Обоснованная миграция старых URL: 301 только к семантически соответствующему преемнику; иначе 404/410 и убрать из sitemap и внутренних ссылок.
6. Сборка Hugo, проверка английского, русского, испанского адресов; контроль отсутствия серых услуг и вводящих в заблуждение обещаний.
7. Обязательно в ТОМ ЖЕ КОММИТЕ обновить этот файл с тем, что сделано и проверено, нерешёнными вопросами и следующим действием.

## 3. Исходники / импорт — состояние на 2026-10-15

- Пользователь загрузил полный архив с сервера: Seoimpuls-all-sources-2026-10-15.zip (92 745 534 байта).
- В рабочей среде подготовлена очищенная копия: SeoImpuls_GitHub_ready.zip, 20 920 516 байт, 2886 файлов, суммарно 35 713 843 байта без сжатия.
- SHA-256 подготовленного ZIP: 764e5fc804588a7877b78143047d0e8fe823d85866b4e14139fd3525c55dc70a.
- В подготовленной копии Hugo source, контент, шаблоны, CSS/JS, статические файлы, админка, _vendor, правила сборки, docs/IMPORT_AUDIT.md, docs/REBUILD_PLAN.md, docs/URL_INVENTORY_BASELINE.csv.
- Из проекта исключены публикация server-current/public, конфигурация сервера и доступа, старые backup, node_modules, временные и посторонние файлы.
- Исходная копия для работы не равна гарантированно побайтово опубликованному состоянию: публикация VPS в архиве может отличаться.
- Подготовленный ZIP находится в беседе ChatGPT и требуется для первичной загрузки. После успешного импорта оставлять ZIP в репозитории не нужно.
- В среде ChatGPT исходники не удалось отправить прямым git push (сетевая среда не разрешает доступ к github.com). Через подключённый GitHub доступно редактирование текстовых файлов, но не прямая загрузка ZIP как двоичного Git-объекта.

IMPORT_STATUS: completed

## 4. Порядок ввода репозитория

1. Репозиторий приватный, уже создан пользователем с README.md на main.
2. В main добавляются этот контекст, AGENTS.md, документация и безопасный импортный GitHub Actions workflow в одном коммите. GitHub Pages не включать.
3. Нужно загрузить SeoImpuls_GitHub_ready.zip в корень main через Add file > Upload files. Архив меньше лимита веб-загрузки GitHub.
4. Workflow import-source.yml проверяет контрольную сумму, структуру и содержимое ZIP, собирает Hugo, удаляет ZIP из отслеживаемого Git, коммитит исходники + актуализирует данный контекст и создаёт white-seo-rebuild.
5. Проверить вкладку Actions и наличие content/, layouts/, hugo.toml в main, а также рабочей ветки. При неудаче импортного job смотреть журнал; не утверждать, что источники в GitHub, пока этого не видно.
6. После успешного импорта выполнять исправления только в white-seo-rebuild с синхронным контекст-логом. Не менять main, не включать Pages и не развёртывать в продакшн.
7. Перед новым чатом прочитать AGENTS.md и этот файл прямо из репозитория, проверить фактическое состояние GitHub/Actions и продолжить с секции 6 «Следующее действие».

## 5. Журнал изменений (новые записи сверху; обновлять в каждом коммите)
### 2026-10-16 — EN homepage eight-to-three simplified scope and buyer text: confirmed QA
- Exact site source 755e52d retained. Full strict #38918895547, Pages #38918895213, context #38918895395 PASSED after minifier-tolerant attribute and approved buyer-copy test fixes (50965ff).
- Direct Chrome #38918077643 PASS (390,768,1280) all fail arrays empty; home browser #38918077646 PASS and axe #38918077640 PASS automated. Reviewed downloaded source screenshots artifact #12054026326, no visible clipping of concise work lines.
- Eight added work blocks are now 3 supportive, non-purchasable text examples. All site-only CTAs and high-level keyword deliverables clarified for businesses without a website. Old supplemental SVG no longer renders on EN. RU/ES output source unchanged; three target EN URL, Title/H1 and internal links unchanged.
- Outstanding unrelated visual/UX issues from original audit remain (full-width Contacts footer verification, 768 header, mobile consent, 1280 process whitespace, manual axe incomplete contrast/ARIA). Code/visual QA PASS for *this scope*, owner still to accept, production unchanged.
- This change is only docs/research/context QA recording, not source modifications; do not move to other pages automatically.

### 2026-10-16 — Update stale CI buyer-definition phrase assertions (PENDING strict)
- Strict #38918491957 got past EN supporting-scope parsing but downstream copy assertion expected literal legacy wording. Updated expected phrases to equally strict, current plain language for keyword research without a site and separate website changes.
- No HTML/CSS/content changes: source 755e52d remains. New strict and Pages CI pending, browser/home/axe source tests passed.
- Scope EN homepage only; no next page or production.

### 2026-10-16 — Correct brittle quote-based static scope assertions
- Strict #38918077584 / Pages #38918077632 failed in scripts/verify_en_services_route.py due to counting quoted attributes after Hugo minification. A parser-based LI count is now required in both static and sitewide validations.
- HTML source unchanged from commit 755e52d. Browser 390/768/1280 #38918077643 PASS, home visual #38918077646 PASS and axe #38918077640 PASS on source, screenshots still to inspect.
- Fix committed with context and plan; await fresh strict+Pages CI. No other page or production edits.

### 2026-10-16 — Simplified EN homepage eight scope tiles to three plain supporting tasks (PENDING QA)
- Owner requested less confusing supporting work and copy suitable for business owners. Three linked main service cards kept unchanged; eight additional tile-like work lines replaced with 3 short examples, explicitly not separately sold packages. EN-only compact styling.
- Home intro, SEO description, deliverables, pricing/timing FAQ and CTA clarify keyword research without a ready website and results as agreed documents or advice (not guaranteed implementation or rankings).
- Updated EN static/browser/sitewide assertions, active plan, this context in SAME commit; RU/ES unaffected, service page source/URLs untouched, no production.
- Tests not executed yet: EDITED_QA_PENDING. Next inspect strict build/preview/390-768-1280/browser/WCAG/screenshot only for EN home.


### 2026-10-16 — Completed read-only EN home post-change audit
- Inspected preview, source, exact CI and all three responsive screenshots. New report `docs/research/2026-10-16-en-home-post-css-audit.md` records verified passes, P1/P2/P3 issues, risk limits and prioritized fixes.
- No source HTML/CSS/JS, SEO URLs, page contents, RU/ES, main or production edit in this commit. Home stays awaiting owner content/UX acceptance; do not advance automatically.

### 2026-10-16 — Custom responsive EN service cards: final QA accepted for source 00881d5
- All 6 Actions PASS: strict #38914027341, Pages/noindex #38914027471, context #38914027698, direct Chrome 390/768/1280 #38914027320, home visual #38914027575 and axe WCAG automation #38914027393.
- Browser verified 3 exact direct routes, 01/02/03 square CSS marks at 38/38/46px and ZERO previous card img requests, 0 broken routes or overlaps with fixed WA/TG, 0 console/network errors or horizontal overflow.
- Screenshot artifact #12052215561 downloaded and manually viewed at 390, 768 and 1280: cards remain legible and stacked/grid-aligned, no visible clipping. No claim of real-user CWV or certified WCAG.
- This acceptance documentation updates context, active plan and AGENTS guard only; site source unchanged from 00881d5, production untouched.
- **OWNER_REVIEW_PENDING**: only user may authorize next page or reuse of any old image assets.


### 2026-10-16 — Repair CSS-only icon width from actual 390/768/1280 Chrome measurements
- On previous source 5d5c281, all major build/preview/visual/accessibility workflows passed, but dedicated CSS mark dimension check failed: 20.8×38, 18.4×38, 22.3×46 respectively.
- Root cause: grid child width:100% computed against intrinsic grid track rather than intended icon box. EN-only mark now explicitly square with clamp(38px,4vw,46px). No old images reintroduced; no other pages changed.
- QA PENDING until new strict/preview/browser screenshot review.


### 2026-10-16 — Custom CSS-only responsive marks for three EN home services
- Owner asked not to reuse legacy service artwork. Replaced exactly the three EN home service icon pictures with lightweight numbered CSS marks. No new image files; no assets deleted; other languages and detail pages are untouched.
- EN homepage template styles and two targeted verification scripts modified; this project context and direct-service plan updated in same commit. All primary service URLs/Title/H1 and SEO architecture retained.
- QA status EDITED_QA_PENDING until new strict/Pages/browser/screenshot evidence; no deployment to seoimpuls.com.
- Next: inspect new QA and mobile/tablet/desktop screenshots. Remain within current requested scope until new owner direction.


### 2026-10-16 — Accepted technical QA of direct EN service URLs and no-overlap homepage
- Source 833cb99; Hugo strict #38912159752, Pages #38912159880, context #38912159761 PASS. Chromium direct EN selection #38912159784 390/768/1280 fail:[], 3 direct service links, correct Title/H1/canonical and accurate WebPage schema/hreflang; old EN catalogue/URL paths absent. Home browser #38912159853 PASS; axe automated #38912159768 PASS.
- Manually reviewed artifact #12050378578 viewport and desktop screenshots. All fixed floating contact collision arrays empty for all homepage readable copy; desktop/tablet spacing accepted. This docs-only acceptance commit makes no page-source changes and does not deploy production.
- Owner must authorize any next page. State CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / OWNER_REVIEW_PENDING.


### 2026-10-16 — Raise EN-only content clearance from 64px to 120px based on measured motion
- Full-text collision test #38911716000 caught WA/TG bounding rects reaching horizontal x92 during popup/scroll movement, overlapping headings at x64; 390 PASS, 768/1280 FAIL. Scope: only EN home CSS, no shortcut animation/position changes. Set content left padding 120px for widths >=768 to guarantee measured clearance; strict + browser retest pending. Context/plan in same commit, no production.


### 2026-10-16 — Fix screenshot-confirmed fixed icons over downstream homepage copy at 1280
- Although recent pipeline passed, artifact #12049823824 shows WhatsApp/Telegram shortcuts on top of the explanation paragraph below three cards at 1280. Enlarged EN left content rail to >=768, and browser QA checks ALL homepage text rather than cards only. Only EN template, EN browser QA and same-commit context/plan changed. New QA pending; no production or unrelated page work.


### 2026-10-16 — Fix EN-only exact 768 footer media conflict, improve collision evidence and correct final CI text assertions
- After passed preview/home browser/axe, remaining strict gate #38910447930 failed on old homepage copy expectation (not a site error); current main browser still flagged 768 floated icon overlap. Reinstated fixed-footer bottom behavior at 768 for EN homepage only, preserving existing animated popup; same 64px text rail remains. Browser reports bounding rects if any overlap persists. CI localized menu assertions restored to /ru/seo/, /es/seo/.
- Modified only layouts/index.html, EN browser QA script, rebuild-qa workflow and context/plan. Strict/preview/browser after this fix pending; no page beyond authorized EN direct-architecture task.


### 2026-10-16 — Fix preview baseURL and localized switcher and 768px floating overlap, pending CI
- Initial redirect-free EN route compilation and all three detailed SEO URL/Title/H1 checks PASS. Strict retired-route gate detected 2 RU/ES hub header EN language links to retired /seo-services/; conditional header routes only those to /#services. Preview static QA supports known preview baseURL and keeps detailed SEO constraints. Chromium services audit showed 768px WhatsApp overlap; EN-home tablet content gutter added. No unrelated sources changed. QA after this patch is PENDING.


### 2026-10-16 — Fix stale QA references after EN direct-URL rollout
- Original 3289214 first Actions strict #38909519843 and Pages #38909519450 compiled site and validated 3 EN routes but stopped on outdated keyword page anchor assertion; service browser #38909519226 attempted retired URL in readiness curl. Updated only affected EN QA scripts and same-commit context/plan. No service content changes. New test runs pending.


### 2026-10-16 — EN direct homepage links / keyword-aligned service URLs: source plan before CI
- User orders no EN services intermediary, removing /services/ prefix and changing vague /seo/ to the technical seo audit query. Implement direct homepage 3 cards /#services and name/title/URL alignments.
- EN service leaf URLs are /technical-seo-audit/, /keyword-research/, /seo-consultation/, matching H1 and Title; only EN link dependencies and tests updated. EN catalog drafted, old 5 EN URLs retired from new build.
- RU/ES raw pages retained; intended reciprocal hreflang, accurate WebPage schema for EN service pages. No live/prod/GSC edits or invented ranking-volume claims.
- Current status EDITED_QA_PENDING; exact Hugo/strict/preview/Chrome results required. No automatic work on next page.


### 2026-10-16 — 3 main cards + 2 supporting areas: final QA and screenshot evidence
- Source `9266336` simplified buyer journey by removing repeated three-way chooser, leaving 3 linked service cards and 2 informational potential work types. No other page affected.
- FULL CI PASSED on exact source: #38905365028 strict build, #38905365102 preview, #38905364899 context and #38905365160 Chrome all 390/768/1280. All browser fail arrays empty; no contact shortcut overlap, overflow, broken links or JS/network issues.
- Artifacts #12048086527 inspected manually at mobile, tablet and desktop; no visual blocker observed. SEO Title, H1, canonical, metadata, images, direct routes and preview noindex unchanged from passing code.
- This new commit changes ONLY `CHATGPT_PROJECT_CONTEXT.md` and `docs/plans/EN_SEO_SERVICES_SIMPLIFICATION_PLAN.md` to record QA, does not edit site sources. Current page **CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / OWNER_REVIEW_PENDING**; no auto-transition or production publication.


### 2026-10-16 — Remove redundant service-choice duplication after screenshot review (CI PENDING)
- Reviewed fresh screenshots #12048005196 of passing e7f9188. Found 3 primary linked services repeated in separate chooser and again in informational matrix; navigation unnecessarily confusing.
- Kept 3 original service cards, associated images, simple benefits and SEO keywords. Removed the second 3-choice UI and its old JSON data. Reduced supporting scope overview to 2 informative possible activities: competitor research and on-page page improvements (6 brief examples, no new commercial URLs).
- Revised only the EN-specific catalogue data and partial + EN page testing scripts, active plan and same-commit context. No other page/production edit.
- Status EDITED_QA_PENDING. Next: inspect new CI/browser and screenshot evidence, remain on /seo-services/ until direct owner instruction.


### 2026-10-16 — EN /seo-services/ buyer-friendly search-facing service language (new version, QA pending)
- Владелец просит писать услуги простым языком для бизнес-клиента, сохранив реальные SEO-ключевые формулировки. Вторую страницу переписали: SEO Audit / Keyword Research / SEO Consultation — три основные услуги с чётким результатом.
- Сохранена иллюстрация семантического ядра и самостоятельный сбор/группировка запросов без готового сайта. Дополнительные SEO Competitor Analysis и On-Page SEO только как краткие варианты работ по отдельному согласованию, без новых коммерческих страниц и обещаний.
- Новый H1 "Find the Right SEO Service for Your Business"; URL, SEO title и canonical без изменения. FAQ, CTA и пример понятнее; внутренний технический QA пример свёрнут, ссылки на фактические проверки остаются.
- Изменены исключительно источники EN /seo-services/, соответствующие EN-ограниченные QA и этот журнал с планом; другая страница и production не изменены. Строгие и визуальные тесты ещё не завершены — **EDITED_QA_PENDING**.
- Следующий этап: проверить сработавшие Actions Hugo/strict/Pages/Playwright 390/768/1280; при необходимости исправить только дефекты этой страницы. **Запрещено самостоятельно переходить к другому URL.**


### 2026-10-16 — EN /seo-services/ simplification: all automated + manual screenshot QA passed
- New source 46bc35e (four work areas / 12 examples / 3 services); targeted static test heading correction 462aa03 (no HTML change).
- Hugo/strict #38899685820 PASS; GitHub Pages preview #38899685817 PASS; context guard #38899685925 PASS; browser on identical rendered code 46bc35e #38899499592 PASS at 390/768/1280.
- Browser fail arrays empty; category anchor/header visibility pass; floating WA/TG icon overlaps at 768/1280 = 0, no broken links, overflow, runtime/network errors. Manually inspected screenshots from #12044858940: 390 full, 768 category, 1280 full and first viewports; no obvious layout defect observed.
- Changed files in this QA acceptance record ONLY `CHATGPT_PROJECT_CONTEXT.md` and `docs/plans/EN_SEO_SERVICES_SIMPLIFICATION_PLAN.md`. All page source, tests, other pages, main/production unchanged from latest passing runs.
- STATUS: CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / OWNER_REVIEW_PENDING. Page remains open pending explicit owner acceptance; DO NOT auto-advance to any other URL.


### 2026-10-16 — Correct obsolete EN catalogue test heading (CI PENDING)
- Rebuild #38899499369 and preview #38899499275 failed because scripts/verify_en_services_route.py retained old catalogue title in selector-order assertion. Hugo build passed.
- One EN test string updated to the verified new heading; no HTML, CSS, other page or production edit. Resubmit CI, inspect browser test #38899499592 separately.
- All new UX QA remains PENDING and only /seo-services/ is authorized.


### 2026-10-16 — Simplified EN catalogue source and acceptance checks (pending CI)
- Replaced 23 equal-weight scope cards and 20 mailto CTAs with four clear non-commercial work areas (12 brief examples), preserving 3 actual linked service options and buyer problem selector.
- Refined first FAQ, confirmed specialist fit disclaimer, preserved QA proof, original URL, H1, Title, schema/meta rules and mobile fixed-contact protection.
- Updated EN-only static and Chrome tests to reject old 23-card DOM and check new concise 4/12/0 structure. No tests yet executed for this commit: **EDITED_QA_PENDING**.
- Exact files: data/en_seo_catalog.json, layouts/partials/en-services-catalog.html, scripts/verify_en_services_route.py, scripts/audit_en_services_browser.cjs, docs/plans/EN_SEO_SERVICES_SIMPLIFICATION_PLAN.md, CHATGPT_PROJECT_CONTEXT.md. No other page content changes.
- Next: review triggered Hugo/strict/Pages/Chrome 390-768-1280 CI and screenshots, fix only proven issues on this page. No other page without owner instruction.


### 2026-10-16 — Owner scope lock: reopen only EN /seo-services/ for customer simplification
- Владелец вернул вторую EN страницу /seo-services/ на доработку и запретил ассистенту самовольно переходить к другим страницам даже после завершения.
- Причина: клиентский интерфейс с 23 SEO-направлениями перегружен и содержит смысловые пересечения (3 published, 14 component, 6 conditional); реальных service landing pages только 3.
- Создан отдельный план упрощения; прежние этапы 0–7 каталога остаются историческими PASS прежней версии, но статус «закрыта» отменён: **REOPENED / UX_REDESIGN_IN_PROGRESS**. /seo/ NOT AUTHORIZED.
- Изменены только документы `CHATGPT_PROJECT_CONTEXT.md`, `AGENTS.md`, `docs/plans/EN_SEO_SERVICES_FINISH_PLAN.md`, добавлен новый план; source HTML/CSS/JS и production не менялись.
- Следующее действие: изменить исключительно EN каталог + его QA проверки с контекстом в общем коммите; затем проверить Actions и визуально 390/768/1280; не переключаться ни на какую другую страницу.


### 2026-10-16 — Решение владельца: greenfield rebuild вместо миграции старого сайта
- Владелец сообщил об отсутствии трафика на текущем сайте и распорядился перестать учитывать старый сайт, создавать новый с нуля.
- Снят GSC/исторический URL/301/410 preflight как блокирующее условие разработки. Старые migration research и URL maps остаются историческим архивом; их предложения не применять автоматически.
- Принятые новая EN главная и `/seo-services/` сохраняются. Следующая страница по новой очереди — EN `/seo/` с отдельным SERP-first аудитом. 23 работы каталога не превращаются в тонкие дочерние URL.
- Изменён только `CHATGPT_PROJECT_CONTEXT.md` (решение и новая дорожная карта); HTML/CSS/JS, sitemap, production, main, DNS, редиректы и GitHub Pages не менялись. QA существующего кода этим коммитом не заменяется.
- Новый релиз потребует sitewide проверки и отдельной санкции на развёртывание, но не доказательств трафика отсутствующего legacy.
- Далее: инвентаризация EN `/seo/` в рабочей ветке, SERP/intent/overlap аудит, затем узкий page commit с контекстом.


### 2026-10-16 — EN /seo-services/ live URL migration preflight (read-only, release still blocked)
- Active owner scope remains EN `/seo-services/` only. Opera opened production `/link-building-services/` (legacy Link Building Services), `/services/` (nginx 404 page), `/seo-services/` (nginx 404 page), `/robots.txt`, and live root/EN sitemaps. These are browser observations, **not raw HTTP status/header chain measurements**. Live EN sitemap lists old `/link-building-services/` service routes; Pages preview EN sitemap lists `/seo-services/` and three specialist routes. Preview `/services/` is an HTML alias, not verified HTTP 301.
- Recorded URL-by-URL *candidate* migration logic in `docs/research/2026-10-16-en-services-production-url-preflight.md`. Critically, old link-building catalogue and Tier/DR pages must NOT be blanket 301'd to the new clean services catalogue. Existing old keyword and consultation pages are only conditional, semantically plausible successors and await GSC/URL-level evidence. No additional page editing authorized.
- **No HTML/CSS/JS/content, live site, DNS, GSC, hreflang, production redirect or alias change.** Accepted catalogue stages 0–7 remain done. Migration release still **BLOCKED_EXTERNAL** (history/inbound links, actual redirects, locale parity, verified client proof, separate owner authorization). Next: obtain evidence before any production plan, not speculative edits.



### 2026-10-16 — NEW /seo/ scope: GitHub access restored; SERP snapshots and controlled plan saved
- HISTORICAL NOTE, SUPERSEDED BY OWNER CORRECTION ABOVE: Assistant proposed moving from completed EN catalogue to `/seo/`, user initially said to proceed, but subsequently clarified that `/seo-services/` remained the authorized scope. The apparent authorization was a mistaken inference; the `/seo/` plan is inactive. Retry after connector access failure was about continuation, not a permanent scope change. GitHub read/write and Opera confirmed restored. Branch `white-seo-rebuild` baseline HEAD `1d5eaf2`. EN homepage and catalogue remain frozen, as do other service pages, RU/ES, main and production.
- Read `AGENTS.md`, `docs/SEO_PAGE_WORKFLOW.md`, existing `content/seo/index.md` and historical intent report; opened /seo/ preview in Opera. Current Title/H1 `Technical SEO Services & Audits`; route /seo/ remains canonical target; current text emphasizes technical audit but gives equal sections to On-Page, Keyword/Content, International, potentially overlapping established specialist pages.
- **SERP evidence:** Google Web first ten result titles/URLs for `technical seo services` and `technical seo audit services`, English/US-parameter request `hl=en&gl=us&pws=0&udm=14&num=10`, desktop Opera 2026-10-16. Direct providers and editorial/directories mixed; physical US IP and search volume NOT verified. Detailed URLs, competitor evidence and gap matrix saved in `docs/research/2026-10-16-en-technical-seo-serp-intent.md`.
- **Critical template issue:** shared `layouts/partials/head/seo.html` emits `BlogPosting` for every `.IsPage` including /seo/. Next target is rendered HTML confirmation and EN /seo/-only correction, not a global change.
- New ordered plan `docs/plans/EN_TECHNICAL_SEO_PAGE_PLAN.md`: gates 0–1 done, 2 IN_PROGRESS, 3 NEXT. Both added in this docs-only commit alongside context. **Current status: BASELINE_AUDITED / SERP_SNAPSHOT_OBSERVED_GEO_UNVERIFIED / CONTENT_REVISION_PENDING / RELEASE_BLOCKED**.
- Exact next: verify /seo/ generated HTML schema and semantics on working branch; make narrow template fix with same-commit context; run strict Hugo / Pages / browser QA with CI evidence before accepting. No original page or server edit yet.



### 2026-10-16 — EN catalogue final QA acceptance and decision record
- Step 6 accepted after `ad90cbd`: Hugo strict #38888649717 PASS, GitHub Pages #38888649363 PASS, Playwright at 390/768/1280 #38888649421 PASS, context guard #38888649376 PASS. Fresh screenshots from #12039969650 inspected; WhatsApp/Telegram remain floating where intended and at 768 their overlap count with catalogue text is exactly 0. No broken links, JS/network errors or horizontal overflows.
- Step 7 final record: `docs/research/2026-10-16-en-services-final-qa.md` added and plan moved to Step 6 DONE / Step 7 DONE. No site/HTML/CSS/JS changes in this documentation-only commit.
- Explicit page status: **CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / RELEASE_BLOCKED**. Unresolved external dependencies: 3–6 months GSC, actual live redirect map, historical backlink/URL risk, RU/ES translation parity and Spanish target, genuinely authorized client examples, and production approval. Preview remains noindexed; main/production untouched.
- Exact next action: stop EN catalogue iteration here; wait for required external evidence and separate owner decision on migration/localization/production. Do not automatically start another SEO service page.


### 2026-10-16 — Step 6 768px floating-contact visual correction (CI PENDING)
- Previous commit `94b8dac` confirmed after interruption: strict QA #38854675025 PASS, Pages preview #38854675100 PASS, browser 390/768/1280 #38854675233 PASS, context guard #38854675106 PASS. Head: indexable production-base HTML with self canonical, OG/Twitter/hreflang; preview workflow strips conflicting index robot and uses only noindex.
- Manually inspected CI screenshot artifact #12027180571: 768-category shows fixed WhatsApp and Telegram shortcuts overlapping the beginning of `When`/`Work` text in the left column. Automated QA missed it because it checked overflow/footer collision but not icons versus text.
- Narrow correction: `layouts/partials/en-services-catalog.html` reserves 44px inline safe gutter only for EN catalogue at 768–1199px, preserving both floating shortcuts; no shared footer/other pages/RU/ES edits. `scripts/audit_en_services_browser.cjs` checks bounding-rectangle intersections against visible catalogue content after anchor navigation.
- Acceptance status: **CODE_EDITED_QA_PENDING**. Await new Hugo strict/Pages/Chrome/context runs, visually inspect 768/390/1280 screenshots; do not claim Step 6 DONE or production release. Next: after pass, record step 6 acceptance and proceed to step 7 final decision record, with external migration/locale/customer evidence blockers retained.


### 2026-10-16 — Step 6 deep head/keyboard QA and unambiguous preview noindex
- Added production-base generated HTML checks for EN document language, meta description, single index robots, OG title/description/URL and Twitter card in `scripts/verify_en_services_route.py`; Playwright now gathers SEO head report and tests keyboard TOC link activation + FAQ details Enter key on 390/768/1280. Existing Title/H1/canonical/hreflang/broken-link/23-workstreams assertions intact.
- Preview workflow previously prepended `noindex,nofollow` while leaving `index,follow` present, generating contradictory robots tags. Updated **preview-only** GitHub Actions transformation to strip old robots meta and insert exactly one `noindex,nofollow`; verifies EN homepage/catalogue and RU/ES catalogue samples. Production-base stays indexable in build; actual production server unchanged.
- Step 6 **EDITED_QA_PENDING**: strict Hugo, preview and Chrome must pass; diagnostic OG values not yet inspected; no real-user CWV claimed. Plan/context updated with this commit. Other website content untouched.


### 2026-10-16 — Step 5 read-only EN/RU/ES hreflang and buyer-intent equivalence matrix
- Audited EN `/seo-services/` plus actual RU `/ru/uslugi/`, ES `/es/servicios/`; read 4 corresponding technical/keyword/consultation sets, `hugo.toml` locale codes, shared `translationKey` and `layouts/partials/head/link.html`. Report `docs/research/2026-10-16-en-services-hreflang-equivalence.md` records URL matrix, source intent and explicit limitations.
- Key finding: broad service-selection task matches but EN has 23 scoped workstreams with 3 primary routes; RU/ES have 4 cards including website development and lack the 23-workstream directory. Reciprocity is technically checked, **full linguistic/content equivalence NOT verified**. Spanish configured `es-ES` despite local-market expressions; target region must be explicitly confirmed later. Do not assume Spain or Argentina automatically.
- NO RU/ES edits, no shared canonical/hreflang changes, no production migration. Step 5 **AUDIT_DONE / CONTENT_EQUIVALENCE_PARTIAL**, future localization/market decision BLOCKED_EXTERNAL. Plan Step 6 NEXT — EN page final comprehensive technical/visual/accessibility gate.


### 2026-10-16 — STEP 4 DONE: 23 contextual paths verified, no doorway URLs
- Step 4 source `13de711` preserves three genuine service detail links and gives 20 components/conditional specialties context-specific email inquiries with encoded subject names. Conditions are labelled truthfully. No new landing pages or price promises.
- Hugo strict #38853823350 PASS, Pages #38853823391 PASS, context #38853823361 PASS, Playwright #38853823263 PASS at 390/768/1280; 23 workstream links, exactly 20 mailto, no href placeholders, link/JS/network/overflow errors. Inspected screenshot artifact #12026660158; workstream links readable on desktop.
- Plan STEP 4 DONE, STEP 5 NEXT: read-only RU/ES equivalence/keyword overlap review. Production, RU/ES and EN sibling contents remain unchanged.


### 2026-10-16 — Step 4 contextual enquiry path for every catalogue workstream
- EN `layouts/partials/en-services-catalog.html` now renders three existing detailed service links plus 20 topic-specific `mailto:support@seoimpuls.com` links. Published service remains `Review [name]`, documented components `Discuss [name] scope`, six conditional specialties `Check availability for [name]`. Email subject contains exact workstream name; no contact data sent before the user intentionally clicks, no JavaScript/form backend, no new pages or invented prices/results.
- Updated Hugo static HTML parser and Playwright three-viewport checks to enforce exactly 23 contextual workstream links, 20 mailto enquiries, 3 deep routes, valid subjects and no placeholder href. Plan Step 4 IN_PROGRESS pending strict Hugo/Pages/Chrome evidence. Home, RU/ES, sibling service pages, main and production untouched.


### 2026-10-16 — STEP 3 DONE; real first-party QA proof distinct from hypothetical SEO scenario
- Completed source evidence block in `d98a5e3`, corrected markup-aware verifier in `218abbd`. Hugo strict #38853455473 PASS, Pages #38853455351 PASS, context #38853455458 PASS; Playwright #38853326385 PASS for the identical HTML before test-only fix, all three viewports 390/768/1280 with verified sample/links/disclaimer. Screenshot artifact #12026171699 desktop sample inspected for readability, proper 4-part hypothetical noindex example plus clearly marked **real internal QA, not client case**.
- Underlying actual measurement: #38851634798 observed 768 section top120 vs sticky header171 (FAIL); #38851849354 retest section192/header171 PASS. No claims of SEO ranking, customers or revenue. Plan Step 3 DONE; Step 4 NEXT: add a contextual inquiry path for each of the 20 workstreams without standalone pages, retain three deep URLs.


### 2026-10-16 — Step 3 source QA corrected for emphasized non-client disclaimer
- Source `d98a5e3` built under Hugo but route QA failed because it searched unbroken literal `not customer results`. Actual HTML correctly emphasizes the negation as `<strong>not</strong> customer results`, so the generated markup is truthful; string test was brittle. Fixed only `scripts/verify_en_services_route.py` to assert the actual HTML disclaimer and two traceability links. No site content changes.
- Step 3 IN_PROGRESS: repeat full strict/Pages/Chrome 390/768/1280; verified internal QA remains a first-party test, never a customer result or rankings case.


### 2026-10-16 — Step 3: documented internal QA evidence without fabricated client results
- Added one directly reproducible evidence→fix→acceptance item to `layouts/partials/en-services-catalog.html`: a real internal 768px sticky-header overlap discovered by Playwright #38851634798 (section top 120 vs header bottom 171), corrected to tablet scroll-margin 192 and verified by passing #38851849354 (section192/header171). Links point to actual public GitHub Actions run records; proof explicitly says **internal site QA, NOT a customer case, client result or Google ranking outcome**.
- Preserved existing hypothetical `noindex` example with its illustrative disclaimer. Added narrow static + browser checks for exact real proof block, two traceability links and disclaimer. No new service/price/credential/URL promises or changes to homepage/RU/ES/production.
- Plan STEP 3 IN_PROGRESS: new Hugo strict, Pages and Playwright 390/768/1280 must pass. Real client-approved audit report remains external blocker (no invention).


### 2026-10-16 — STEP 2 DONE, verified 23-item commercial scope evidence
- Step 2 completed on source `30e1c72`, retaining `f7563f5` page data and visible truth labels: 3 published service pages, 14 agreed-scope components and 6 conditional specialties; all 23 have documentary evidence or explicit evidence gaps in `docs/research/2026-10-16-en-services-scope-evidence-matrix.md`. No unsupported specialist certification or client work claimed.
- Hugo strict sitewide #38852948774 PASS; Pages #38852948660 PASS; context #38852948983 PASS; Playwright #38852948749 PASS at 390/768/1280, all 23 categories and 3/14/6 distribution, no broken links, JS/network failures, overflow or header/footer collision. Reviewed 390/1280 category screenshots artifact #12025483380.
- Plan Step 2 DONE, Step 3 NEXT: deliver reproducible, truthfully labelled evidence format, not a fabricated client case. Do not edit sibling pages or production.


### 2026-10-16 — Step 2 QA test corrected: select catalogue lede not buyer selector lede
- Initial 3/14/6 source `f7563f5` passed Hugo strict/Pages (#38852787628/#38852787684) and context guard, with 390/768/1280 browser DOM confirming all status counts and no visual/route/JS failures. Browser #38852787605 failed the new `scopeLegendPresent` assertion only because `querySelector('.seo-catalog__lede')` returned the earlier buyer-decision intro, not the adjacent catalogue lede after the directory heading.
- Updated only `scripts/audit_en_services_browser.cjs`: scope text now read from `#seo-catalog-title + .seo-catalog__lede`, matching the intended DOM. No HTML, offers, data, other locales or production changes. Plan Step 2 still **IN_PROGRESS / QA_PENDING**, rerun browser/Hugo/Pages.


### 2026-10-16 — Step 2 commercial truth: classify all 23 white-hat workstreams
- Reviewed `content/seo/index.md`, `content/services/keyword-research/index.md`, `content/services/seo-consultation/index.md`, `content/about/index.md` and `content/faq/index.md` against all 23 cards. Added `docs/research/2026-10-16-en-services-scope-evidence-matrix.md` with one evidence/limitation row per card. No external claims about actual completed client projects or team capabilities.
- `data/en_seo_catalog.json`: all 23 entries now have explicit `scope_status`: 3 published EN detailed service pages, 14 components of agreed audit/research/consultation work, 6 specialized conditional topics requiring capability and site fit confirmation. `layouts/partials/en-services-catalog.html` displays neutral text status on each card and clearly explains the categories; no new URLs/prices/guarantees, no case studies.
- Updated targeted static and browser tests to enforce statuses 3/14/6 and disclosure; EN homepage, RU/ES and other EN content untouched. Step 2 **EDITED_QA_PENDING** until Hugo strict/Pages/390-768-1280 QA passes.


### 2026-10-16 — STEP 1 DONE; three-viewport verified handoff to commercial truth audit
- Completed ordered finish-plan step 1, source `63f39bb`: selector appears before 23-group directory; 3 exact deep-service paths kept, no duplicate. Full strict multilingual Hugo #38852257807 PASS; Pages #38852257602 PASS; context #38852257833 PASS; Playwright #38852257739 PASS at 390, 768, 1280 with no errors/overflow/broken routes.
- At 768 px header bottom 171, category anchor top 192; footer fixed to bottom y=741–800 (formerly overlapped header). 390 mobile and 768 tablet first viewport screenshots personally inspected from artifact #12025618382; mobile cookie consent retains parallel accept/reject and visible manage action.
- Plan Step 1 DONE, Step 2 NEXT: reconcile 23 scopes against real linked EN service pages/About/FAQ, without inventing specialist capabilities. Current source remains preview-only, production unchanged.


### 2026-10-16 — Step 1 visual QA: 768px floating footer overlaps header
- Prior tablet hash-offset fix `e3d8dee` passed Hugo strict build #38851849386, preview #38851849373, context guard #38851849394 and browser #38851849354 at 390/768/1280. Anchor 768 top 192 > header bottom 171, and no overflow/JS/broken-link failures.
- **Manual 768 screenshots** from artifact #12025467020 exposed an untested real visual issue: Contacts/footer appeared across the top viewport and obscured/covered the header logo. Root cause in shared old CSS: `@media (min-width:768px)` fixes footer, later `@media(max-width:768px)` sets footer `bottom:auto` but doesn't override the more specific fixed position; exact 768 suffers bottom:auto fixed placement.
- Changed only EN catalogue-specific `layouts/partials/en-services-catalog.html`: at exactly 768px restore explicit fixed-footer bottom -96px / visible 0px, no changes to shared header/footer/RU/ES or homepage. Updated Playwright `scripts/audit_en_services_browser.cjs` to detect footer overlapping header on 768. Plan Step 1 remains IN_PROGRESS until new 390/768/1280 screenshots and CI are green and visually inspected.


### 2026-10-16 — Step 1 tablet hash-offset regression, source fix
- Initial Step 1 commit `f9bc7bb`: Hugo strict QA #38851634622 PASS, Pages #38851634633 PASS, context #38851634739 PASS. Browser #38851634798 FAIL: 390px PASS and 1280px PASS, but 768px `sectionTop 120` is behind sticky header bottom `171`; first 768 QA exposes a real breakpoint issue.
- Adjusted **only scoped EN catalogue partial CSS** at tablet widths 641–1020px to `scroll-margin-top:192px` on group/matching/scope/example/FAQ sections and catalog heading target. 390 and 1280 retain 120px. Plan status stays **STEP 1 IN_PROGRESS**, full 390/768/1280 browser rerun pending. No homepage/RU/ES/sibling page/production changes.


### 2026-10-16 — Controlled plan Step 1: move problem-to-service decision before catalogue
- Follow `docs/plans/EN_SEO_SERVICES_FINISH_PLAN.md`, STEP 1 IN_PROGRESS. Changed only `layouts/partials/en-services-catalog.html` (exactly one 3-choice selector moved after the three EN hero cards and before 23 workstreams), `scripts/verify_en_services_route.py` (HTML order/no duplicate assertion), `scripts/audit_en_services_browser.cjs` (390/768/1280 + selector order + expected grid), and EN-only Playwright workflow triggers and artifact label to include partial/data edits. Updated plan and this context in SAME COMMIT.
- Preserved all 23 workstreams, four group navigation, existing Title/H1/URL/canonical, existing 3 child URLs, illustrations, hypothetical sample output, EN homepage and all RU/ES source untouched. No production deployment.
- **EDITED_QA_PENDING**: need CI strict/Hugo + Pages and Chrome screenshots at 390/768/1280 before STEP 1 can become DONE. Subsequent Step 2 is portfolio/truth reconciliation of 23 conditional workstreams, NOT a new list of pages.


### 2026-10-16 — Persistent controlled finish plan for EN /seo-services/
- User explicitly instructed: write and store a step-by-step plan in GitHub, then execute without losing continuity. Created `docs/plans/EN_SEO_SERVICES_FINISH_PLAN.md` (strict ordered steps 0–7 and external blockers; status STEP 1 NEXT). No site/layout/code edits in this **planning-only** commit.
- Enforced immutable scope: only EN catalogue; homepage `professional seo services` frozen; RU/ES/other EN pages read-only; no production/GSC changes. Frontmatter Title/H1 and current valid URL retained. All changes and status transitions must update this context AND the plan in the same commit, with CI evidence before declaring PASS.
- Step 1 is buyer-choice section reorder **before** 23 workstreams. Remaining jobs: commercial truth review, non-fabricated proof format, conversion paths, hreflang equivalence read-only audit, full 390/768/1280 SEO/visual QA and terminal release-blocker report.
- Next: apply Step 1 small scoped site change; CI and visual evidence required. Existing 2026-10-16 QA baseline remains last proven site state until new tests pass.


### 2026-10-16 — EN catalogue final full QA after mobile polish (no site code changes)
- Verified last site/UI commit `3878934c97b59070a875c3e0be710c31058f2f4d`: Hugo full rebuild and strict white-hat release gate GitHub Actions **#38846778912 PASS**; GitHub Pages working preview **#38846778882 PASS**; context guard **#38846779134 PASS**; English catalogue Playwright Chromium **#38846778800 PASS**. URL: https://agurkin2021-gif.github.io/seoimpuls/seo-services/ .
- Browser 390px: HTTP 200, one approved H1, correct distinct HTML Title and self canonical, three clickable main service cards, four categories with 23 workstreams, three choice paths, five category/example TOC links, four return links, one distinct consultation diagram, 4-field **illustrative not actual** work-output example, five FAQ questions, no broken links or JS/network errors, no overflow. Responsive grid 1 column. Anchored section top 120px, sticky header bottom 81px. Cookie banner shown with exactly three buttons; Accept/Reject equal-size two-column grid and Manage Preferences visible below.
- Browser 1280px: corresponding structure and links PASS, top grid 3 columns, anchor top 120px / sticky header bottom 79px, no overflow or broken media. Three footer contacts retained; unverified social/map blocks not shown. No JSON-LD parsing errors or false BlogPosting label. Screenshots and full audit JSON artifact **#12023079816** from workflow #38846778800.
- Independently inspected recent Opera live Preview: updated top three cards (first two optimized WebP plus distinct schematic third), 4-category jump nav, readable multi-column workstream grid, the evidence/acceptance example, and FAQ. Inspected 390px screenshots before consent and after dismissal. Last mobile cookie visual review: Accept/Reject parallel, Manage option present. No further critical page-specific defect demonstrated by present evidence.
- **Status EN `/seo-services/`: CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / CONTENT_SCOPE_REVIEW_PASS for this iteration; NOT CLAIMED IDEAL OR READY FOR PRODUCTION.** No changes to main/homepage/RU/ES/other individual services/live VPS. 23 areas represent scoping options, not 23 active pricing packages or real customer case studies. Organic competition, indexing/GSC traffic, external inbound links and production HTTP redirects remain unverified; production `RELEASE_BLOCKED`.
- OWNER SCOPE: DO NOT MOVE TO OTHER SERVICE PAGES WITHOUT USER'S NEW EXPLICIT REQUEST. Next work on same catalog only if new concrete issue or live/GSC data appears. No auto-deploy or URL migration.


### 2026-10-16 — EN catalogue mobile overlay and return-navigation refinement
- Scoped UX follow-up after inspecting exact **390px Playwright first-screen** artifact #12023247166 from completed run #38846194397 and desktop/mobile Opera. All earlier QA PASS on `1c74327`: Hugo/strict check #38846194508, Pages #38846194406, context guard #38846194396 and 390/1280 browser run #38846194397. Anchor geometry: 390px section top 120 / sticky header bottom 81; 1280px 120 / 79, both clear. 23 workstreams, 4 groups, 3 choices, no broken local paths or JS failures.
- Remaining observed mobile UX issue: unchosen GDPR banner uses **three full-width vertically stacked buttons**, masking too much of the first screen. Rather than remove consent or change the global banner, applied CSS **only in EN `en-services-catalog.html`** to put clearly labeled Accept and Reject on the same equal-sized row with Manage Preferences on a second row. No consent logic, default, storage or tracking behavior changed; Russian/Spanish and homepage unaffected.
- Added one `Back to categories` anchor after each of the four long workstream groups; heading `#seo-catalog-title` gains scroll-margin for direct return links. Kept all workstreams and the visual evidence demo. Extended static QA and 390/1280 Playwright checks for four return anchors, heading scroll margin and 390px 2-column consent buttons with 3 choices.
- Current **EDITED_QA_PENDING** for this focused visual follow-up; must run Hugo/strict, Pages, context guard and browser, then inspect mobile 390 screenshot. Not approved for production release or GSC redirects.


### 2026-10-16 — EN SEO catalogue depth/visual/buyer evidence audit (scope locked to /seo-services/)
- Owner explicitly blocked advancing to other pages until EN `/seo-services/` is comprehensively polished. Deep page-only audit in `docs/research/2026-10-16-en-services-depth-audit.md` (current source + live Opera 1st-screen, hash navigation, bottom FAQ; comparator references with clear SERP caveats). Baseline: 23 scoped types and 3 linked primary offers were technically valid but no TOC for 4 groups, clipped hash headings under sticky header, repeated first/third magnifier hero art, top-row lazy image flash, generic inner links, no illustrative evidence format and missing price/schedule factor FAQ.
- Planned code changes in this commit: EN guarded `layouts/partials/services-hub.html` substitutes an accessible pure-HTML/CSS 3-step consultation visual (Review / Prioritize / Plan) for the repeated generic graphic, and eager-loads remaining two above-fold images; EN `layouts/partials/en-services-catalog.html` adds 5 category/output jump links with scroll-margin compensation, descriptive deep-link names, and one explicitly hypothetical evidence→fix→acceptance example (not a fabricated case). `data/en_seo_catalog.json` gains one honestly conditional FAQ about costs and timelines. No new commercial URLs, fake packages, client claims, results or promises.
- `scripts/verify_en_services_route.py` and `scripts/audit_en_services_browser.cjs` now enforce 5 navigable anchors, 1 distinct consultation diagram, evidence example with 4 fields, 5 FAQ questions, descriptive 3 links, valid non-BlogPosting schema and real 390px/1280px anchor-to-header geometry, retaining earlier canonical/hreflang/sitemap/redirect/route checks.
- **Status: EDITED_QA_PENDING** until GitHub Actions Hugo strict gate, Pages and Playwright browser screenshots PASS. This is a scoped EN page change; EN home, other EN service pages, RU/ES, repo main and live VPS untouched. After QA inspect preview visually and perform follow-up gaps audit; production remains RELEASE_BLOCKED pending GSC/live URL migration and user authorization.


### 2026-10-16 UTC / 2026-10-15 AR — EN 23-workstream catalogue final acceptance
- Last source commit `0a91a30e3cd12d8c8a9bf0ed54771c9f9b7de84f` introduced a separate EN HTML Title via `seo_title` without changing the approved H1. Actual connected Opera Preview at `https://agurkin2021-gif.github.io/seoimpuls/seo-services/?v=0a91a30` displayed browser title `SEO Audits, Keyword Research & Consulting | SeoImpuls`. H1 remains `Choose the Right SEO Work for Your Website`. No homepage metadata change.
- Final same-commit GitHub Actions: context guard #38844710214 **PASS**; full Hugo multilingual rebuild/route/strict-whitehat gate #38844710186 **PASS**; Pages Preview #38844710177 **PASS**; 390px & 1280px Chromium #38844710221 **PASS**. Browser logs: HTTP 200, one H1, three linked service cards, four groups, 23 workstreams, three choice panels, 13 checked local routes, no broken links, image load failure, JS/network error or horizontal overflow; responsive grid 1 col at 390 and 3 cols at 1280. Screenshots and audit JSON saved in Actions artifact #12022508854.
- Previous full 1280 and 390 screenshot artifacts from `62d87d6` were visually reviewed. Three-card top remains coherent, responsive scoped-work grid fits without overflow. First and third lead images are similar; cosmetic differentiation is optional, not a release blocker for this page.
- **Status: CODE_QA_PASS + RESPONSIVE_VISUAL_QA_PASS for EN /seo-services/**; catalog content constructed with conditional work scopes rather than 23 guaranteed full-service packages. URL remains `/seo-services/` canonical; `/services/` fallback is HTML alias, not production server 301. Three existing deeper links preserved, no new SEO landing URLs. English homepage frozen; RU/ES source, `main` and live server untouched.
- **RELEASE_BLOCKED for entire site:** no live production deployment approval, no recent GSC old-URL / incoming-link/traffic evidence, no authorized production HTTP 301/410 migration, no final overall locale/content acceptance. Next authorized task should be a scoped English individual service page/intent audit (existing technical, keyword and consultation pages first), followed by locale/sitewide migration work. Do not auto-deploy or invent new independent pages for all 23 subtopics.


### 2026-10-15 AR — Decouple EN catalog HTML Title from H1, retain commercial intent ownership
- After `4caa5cd`, GitHub Actions context #38844530073 PASS and full Hugo rebuild QA #38844530063 PASS, including strict anti-spam gate and unchanged RU/ES routes; prior published preview #38844411228 PASS. Responsive browser audit #38844041118 PASS 390/1280 for the full 23-workstream catalogue. Connected Opera reopened live preview and verified key headings, category labels and content in the accessibility tree.
- Final on-page check found that `layouts/services/list.html` used the page H1 front-matter `.Title` as HTML `<title>`. The approved SEO architecture deliberately requires a **different** title: `SEO Audits, Keyword Research & Consulting | SeoImpuls` (commercial and specific) versus H1 `Choose the Right SEO Work for Your Website` (navigational comparison). Implemented `seo_title` parameter in **only** English `content/services/_index.md`; EN service-list template reads it with fallback to prior `.Title`. RU/ES same template branch unchanged.
- Updated both `scripts/verify_en_services_route.py` and `scripts/audit_en_services_browser.cjs` to strictly assert the exact approved HTML Title separately from H1. Canonical, meta description, 23 scopes, cards, homepage text, noindex/301 plan, partner links and production untouched.
- **EDITED_QA_PENDING** until new Hugo/Pages/390/1280 checks for the exact Title pass. Then record final QA and stop page editing, leaving only separate GSC/production migration and sitewide release decisions.


### 2026-10-15 AR — Synchronize final rebuild QA gate with approved EN catalogue H1
- EN expanded catalogue `/seo-services/` is built and published to **GitHub Pages preview**, run #38844411228 PASS, after strict white-hat gate was satisfied. Rebuild run #38844411236 validated all preceding HTML/source checks, RU/ES integrations, migrations, affiliates and the strict anti-spam gate; it then failed **only in the final embedded EN-H1 assertion** inside `.github/workflows/rebuild-qa.yml`, which still expected the old catalogue `SEO Services & Practical Deliverables`. New rendered H1 is the owner-approved `Choose the Right SEO Work for Your Website`.
- Updated one assertion in `.github/workflows/rebuild-qa.yml` to the approved H1; no weakening of checks. The dedicated route QA `scripts/verify_en_services_route.py` and 390/1280 browser QA had already tested this new H1 accurately (browser run #38844041118 PASS).
- No content/site source, URL, titles, production, EN homepage, RU/ES or main edits in this QA-only commit. **Pending:** re-run Hugo rebuild/context/Pages and verify final green CI status before considering code QA complete. Full production release still requires GSC migration and owner approval.


### 2026-10-16 UTC / 2026-10-15 AR — Clarify no-manipulative-links FAQ and pass strict release check
- New full catalogue browser QA **PASS** run #38844041118 for both 390px and 1280px (23 workstreams, four groups, 3 entry cards, no overflow, broken local links, browser errors or failed image loads). Context guard passed, targeted Hugo route assertions fixed in `ea92b35`.
- Rebuild QA #38844200291 and Pages Preview #38844200353 then failed **strict whitehat content gate**, despite previous steps passing: new FAQ negatively mentioned `backlinks`, which the gate flags as legacy visible copy even in a denial. No prohibited product was actually offered, but current published copy made the machine gate fail. Exact finding `/seo-services/index.html | legacy_visible_copy | backlink`.
- Updated **only** `data/en_seo_catalog.json` FAQ question/answer to clearly refuse automated placements, purchased ranking links, networks and artificial authority metrics without using a term that the sitewide gate treats as a promoted legacy offer. Strict gate logic itself not weakened. Separate permitted earned editorial outreach remains non-guaranteed.
- This commit changes one EN catalogue content string only; no URL, H1, title, homepage, RU/ES, production or other service offering modifications. **EDITED_QA_PENDING** for the follow-up Hugo/Pages and browser runs; production release still separately gated.


### 2026-10-15 AR — Correct static HTML class assertion after Hugo minification
- New EN catalogue commit `62d87d6` built successfully under Hugo and Playwright responsive QA run #38844041118 **PASS**: 390px and 1280px HTTP 200, 23 workstreams, four groups, three choice paths, three linked entry cards, 13 local links checked at each width, no broken links, overflow, image, JavaScript or network failures. Both layouts verified through live DOM at CI; screenshots saved in the run artifact. Context guard #38844041255 PASS.
- Rebuild QA #38844041104 and Pages Preview #38844041129 **FAIL**, not due to website HTML: `scripts/verify_en_services_route.py` searched a literal `class="seo-catalog__group"`, but Hugo `--minify` legally removes unneeded attribute quotes. The browser test using DOM `querySelectorAll` reliably counted 4/23/3.
- Fixed only `scripts/verify_en_services_route.py` to count CSS class tokens using `HTMLParser` and `Page.class_counts`. This checks semantic rendered output independently of minifier formatting. No SEO page, data, CSS, routes, EN homepage, RU/ES or production changes.
- Current status: **CODE_QA_PARTIAL / VISUAL_BROWSER_PASS** until the re-triggered Hugo/Pages tests succeed. Next: verify green runs and inspect 390/1280 screenshots, then commit final QA status with context.


### 2026-10-15 AR — Expand EN /seo-services/ to 23 scoped white-hat SEO workstreams
- Explicit owner request: list all legitimate SEO work areas without competing with homepage primary `professional seo services` query. New EN catalogue intent: problem → task → typical deliverable → appropriate start page. Full matrix and SERP evidence limits recorded in `docs/research/2026-10-15-en-services-complete-catalog.md`.
- Title/H1 for EN catalogue: `SEO Audits, Keyword Research & Consulting | SeoImpuls` / `Choose the Right SEO Work for Your Website`; existing URL `/seo-services/` kept. English homepage H1, Title, metadata, and other source files unchanged.
- Updated `content/services/_index.md` (EN metadata, first-screen selection answer, existing three service cards retained, duplicated generic text builder blocks removed). Added `data/en_seo_catalog.json` (23 scoped activities grouped 6+6+6+5); new EN-only `layouts/partials/en-services-catalog.html` renders problem, assessment, output, three selection paths, scope steps, ethical limits, FAQ and contact. Shared `layouts/partials/services-hub.html` changed only in `en` guard. No new thin routes, unverified cases/prices, link spam services, guarantees or invented link placements.
- Updated `scripts/verify_en_services_route.py` and `scripts/audit_en_services_browser.cjs` for new H1/intro, 23 cards, four groups, and prior canonical/aliases/SEO/390/1280 checks.
- **EDITED_QA_PENDING:** all file edits staged in one Git commit with this context; Hugo build, GitHub Pages preview, context guard and real browser visual QA must be inspected after commit. Old 390/1280 PASS was on prior 3-card version, not evidence for new 23-workstream version.
- Operational boundary: `main`, RU and ES content, DNS, production `seoimpuls.com`, GSC and deployment unchanged. Next: inspect generated HTML and new Actions; resolve confirmed regressions with separate context-logged commit; then final focused EN catalogue intent/cannibalization review. GSC/live migration and sitewide release gates still pending.


### 2026-10-15 — EN services hub: first successful 390/1280 visual QA and context-priority correction
- Scope: only `CHATGPT_PROJECT_CONTEXT.md` on `white-seo-rebuild`; preceding script-fix commit `6099121730ab`. Corrected outdated top-of-file priority (it still said EN homepage only) to match explicit owner authorization for `/seo-services/` confirmed in AGENTS.md and section 6. **No site file/content/styles/URL/RU/ES/production edits in this commit.**
- Verified GitHub Actions for `6099121`: content context guard run **#38840975820 PASS**; Hugo rebuild QA **#38840975931 PASS**; GitHub Pages Preview **#38840975836 PASS**; dedicated EN SEO catalog browser audit **#38840975773 PASS**, job #116780728234.
- Browser logs: 390px HTTP 200, 1 H1, grid 1 column, 3 service cards, 13 local routes checked, no broken links, no overflow, no JS/network faults, `fail:[]`. 1280px HTTP 200, grid 3 columns with same validation, `fail:[]`. Checked valid JSON-LD parse, loaded images, canonical, nav, footer without unverified social/map claims, contact links. Screenshots 390/1280 first/full and `audit.json` stored in artifact **#12020632894**: https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38840975773/artifacts/12020632894 . Inspected full screenshots at both sizes: no observed cut-off or grid breakage; first/third images are visually similar/near-duplicate, optional targeted visual polish, not a broken asset.
- Status: **CODE_QA_PASS + RESPONSIVE_VISUAL_QA_PASS for EN catalog**, NOT READY_FOR_RELEASE. Search-volume/ranking/physical-US SERP location not validated; GSC and live HTTP 301 migration untouched. Sitewide RU/ES and legacy route audit block production approval.
- Next: if further EN hub content edits are requested, revisit distinct buyer-choice gaps and small visual duplication, keeping broad `Professional SEO Services` on homepage; otherwise continue next permitted EN page under the same workflow. Full release requires separate owner approval.


### 2026-10-15 — Fix EN SEO catalog browser audit crash without changing page content
- Scope: branch `white-seo-rebuild`; only `scripts/audit_en_services_browser.cjs` and this context file. Parent commit `3ee217e24cae`.
- Verified GitHub Actions job #116775668421 (run #38839371024) crashed at 390px after DOM checks with `TypeError: URL is not a constructor` at line 49, then Chromium remained open and the job timed out/cancelled after 12 minutes. Previous run #38838692026 had the same defect. This was **a QA script failure**, not established page content/visual failure.
- Fix: rename the conflicting Node `URL` constant to `PAGE_URL` so the native `new URL(...)` parser works; explicitly close Chromium in the fatal exception handler so test errors terminate instead of timing out. No URL, title, design, CTA, service content, RU/ES source, `main` or live server changes.
- Evidence before fix: Hugo production-base QA #38839370929 PASS; GitHub Pages Preview #38839371005 PASS. After this fix: **VISUAL_QA_PENDING** until a new EN catalog Playwright workflow run reaches both 390px and 1280px and its evidence is reviewed. Do not call page visually approved yet.
- Next: inspect the triggered EN catalog workflow, fix any concrete page or test faults with a separate context-logged commit; then finish catalog on-page/intents audit, keeping homepage distinct. Release remains blocked pending full sitewide gate and actual production migration/GSC review.


### 2026-10-15 — Make EN services browser QA deterministic; avoid per-link HTTP delays
- First dedicated Playwright workflow #38838692026 remained in `Run responsive Chrome diagnostics` longer than expected without granular stage logs. Hugo QA #107 and Pages #48 passed; Opera independently confirmed public EN hub renders all 3 images after lazy loading, correct 3-column desktop layout, direct service selection text and removal of generic footer links/map.
- Updated **only the audit script** `scripts/audit_en_services_browser.cjs`: replace repeated HTTP subrequests with direct existence checks for generated local Hugo HTML/static targets; add stage logging at page/DOM/cookie/diagnostic steps. This is a QA reliability change, not a content or site layout change. Keep screenshot and responsive metadata tests.
- Re-run the browser workflow; inspect actual artifact before claiming 390/1280 PASS. RU/ES and production unchanged.


### 2026-10-15 — EN catalog dedicated visual QA at 390 and 1280px
- Last scoped catalog selection+footer commit 7a5da8d9 verified in Hugo QA #106 and Pages Preview #47 PASS; Opera observed the EN-only direct choice paragraph, three valid service cards and zero generic social links. RU/ES and other EN source left unchanged.
- Added dedicated Chromium script `scripts/audit_en_services_browser.cjs` and triggered workflow `.github/workflows/en-services-browser-audit.yml`. At 390x844 and 1280x800 it checks SEO title/H1/canonical, intro, exactly 3 service card URLs, CSS responsive columns 1/3, image loading, footer real contacts and no unverified map/social, sitemap-relevant links, JSON-LD syntax, JS/network/broken link errors and horizontal overflow; produces screenshots and JSON.
- No website content edits in this commit. New QA run must pass before claiming page visually accepted.


### 2026-10-15 — EN SEO services catalog buyer-intent and visual gap fixes
- URL change completed in commits 44b2da53, 8447c02d, 3da878cb, 8c47e968: Hugo QA #105 PASS, Pages Preview #46 PASS. Opera verified `https://agurkin2021-gif.github.io/seoimpuls/seo-services/` Title `SEO Services & Practical Deliverables | SeoImpuls`, 3 legitimate service links and header new URL. Alias /services redirects (Hugo HTML, not HTTP301); children unchanged.
- Discovered live EN catalog partial laid out four desktop columns for three cards, leaving empty cell. Updated `layouts/partials/services-hub.html` EN-only three-column grid (two tablet, one mobile) and a short direct choice-answer paragraph before cards, clarifying audit/keyword/consultation service selection (no invented offerings or guarantees).
- On EN catalog only, generic social-account links and unrelated location map were visible in footer; `layouts/partials/footer.html` now detects `$isEnServicesHub`, suppresses only the footer-right generic social/map block, retains real WhatsApp/Telegram/email and unmodified EN homepage logic and other languages. EN-only footer wrapper CSS avoids empty-grid layout.
- Extended route validation to assert catalog choice paragraph and absence of unverified social/map nodes. Preview/Hugo/browser checks pending for this commit, do not claim PASS yet. RU/ES and other EN page content, main and production untouched.


### 2026-10-15 — Update Pages preview EN hub link assertion after canonical URL rename
- Hugo QA #104 PASS, including dedicated service URL assertions: new `/seo-services/` canonical/H1/Title, three child links, RU/ES reciprocal hreflang, old `/services/` HTML alias, EN language sitemap without duplicate.
- Pages #45 failed solely in preview post-build hardcoded link assertion expecting `/seoimpuls/services/` in homepage instead of updated `/seoimpuls/seo-services/`. Corrected this assertion in publish-preview.yml; no website HTML, CSS, RU/ES or production changes.
- Next re-run Pages and verify new hub, old alias and actual link routing in Opera.

### 2026-10-15 — Correct English service hub sitemap QA for multilingual Hugo sitemapindex
- After HTML Title fix 8447c02d, Hugo #103 and Pages #44 still failed **only** on service QA sitemap assertion: script searched `public/sitemap.xml` for the hub, but this multilingual Hugo site generates root `sitemapindex` with linked `public/en/sitemap.xml`, `public/es/sitemap.xml`, `public/ru/sitemap.xml`.
- Independently opened published GitHub Pages sitemap index and English sitemap in Opera; old `/services/` is in `/en/sitemap.xml` in prior stable build. QA false positive confirmed; actual new page output/canonical/H1/links/hreflang and alias tests already passed earlier in script.
- Updated `scripts/verify_en_services_route.py`: XML-parse sitemap index, then English sitemap, assert new hub present and old alias absent, rather than text-regex root index. No site HTML, URL, style, RU/ES source or production changes in this commit. Need CI rerun before QA accepted.


### 2026-10-15 — Fix confirmed missing EN services catalog Title during route migration
- New `/seo-services/` canonical migration commit 44b2da53 triggered Hugo QA #102 and Pages #43, both FAIL at targeted check: HTML `<title>` was only `SeoImpuls` rather than scoped `SEO Services & Practical Deliverables | SeoImpuls`. This is an actual on-page defect in section template, not false keyword gap.
- Fixed **only the EN service hub title** in `layouts/services/list.html` via Hugo named `title` block. RU/ES section title behavior remains prior `SeoImpuls`, all other page templates and EN homepage unaffected. New URL, alias, reciprocal hreflang and all link changes from previous commit remain.
- Re-run Hugo QA/Pages and targeted service route script; later errors may need separate evidence-based fixes. Do not claim deployment until both pass.


### 2026-10-15 — Rename English service catalog to /seo-services/
- From user-suggested descriptive keyword path, renamed EN section hub canonical to `/seo-services/`, leaving EN child pages `/services/keyword-research/` and `/services/seo-consultation/` intact. Selected intent: **compare genuine offered services and deliverables**, unlike homepage `professional seo services` hire-provider intent. URL is not ranking guarantee.
- Existing old Preview `/services/` gets Hugo static redirect alias (NOT HTTP 301). Updated EN home CTA / service variable, EN navigation, About and FAQ links only as dependencies; RU/ES source untouched and hreflang auto-points at new EN URL. Production currently 404 on both and unchanged.
- Updated strict Hugo QA expectations and Pages workflow; new generated-HTML script `scripts/verify_en_services_route.py` enforces canonical and breadcrumb, service link integrity, reciprocal hreflang, homepage/About/FAQ routes, old alias not duplicate, sitemap and unchanged child URLs. Migration recorded in `docs/seo-url-migration-register.csv`.
- GitHub Actions must be checked before claiming success; current step is URL architecture only, separate future on-page page-level content audit. No live server 301 applied; GSC_PENDING.

### 2026-10-15 — EN /services/ stage authorized; research keyword-rich URL and independent SERPs
- Owner explicitly moved to English `/services/` after EN homepage completed, then suggested replacing generic path with a descriptive keyword. Scoped stage now covers EN services hub and EN-only navigation/link dependencies, not broad rewrites of main or RU/ES.
- Connected Opera inspected Preview `/services/`, production `/services/` and `/seo-services/` both currently 404. Took Google Web desktop `seo services`, `seo services list`, `types of seo services` snapshots with `hl=en&gl=us&pws=0&udm=14`; followed and recorded **exact top10 organic URLs for seo services list**. Competitor intent split: `seo services` generally provider-hire (home owns), `seo services list` mostly 10–20 types and agency comparisons, while our hub is **only 3 genuine services**.
- Research and intent map in `docs/research/2026-10-15-en-services-serp-and-architecture.md`: homepage = provider-selection, catalog = choose service and deliverable, child audit/keyword/consultation = specifics. Candidate clean hub URL `/seo-services/` descriptive, **not a ranking guarantee**. Current URLs are preview; no GSC demand for candidate query known.
- Updated `AGENTS.md` user-approved phase scope to permit EN hub and necessary EN-only crosslinks. This research-only commit does not yet rename URL, change production, or touch EN main page content.
- Next: one carefully scoped URL migration/refactor with content/canonical/menu/FAQ/About/QA and old URL fallback; prevent service keyword cannibalization. Strict Hugo, Pages and browser checks before calling complete.


### 2026-10-15 — EN homepage Organization/WebSite schema verified; external Google test unavailable
- Schema implementation commit dd09eff9 passed Hugo QA #99, Pages Preview #40 and Chromium 390/1280 #10. Strict Python generated-HTML guard confirmed two valid EN-home JSON-LD nodes (`WebSite`, `Organization`), correct homepage description/canonical/logo/publisher @ids, no collective `Person` or one-item BreadcrumbList; RU/ES home schema unchanged.
- Actual Google Pages logo asset 487×229 loaded in connected Opera. External Google Rich Results Test on GitHub Preview returned `URL unavailable to Google` / crawl failed; therefore **external Google validation was not completed**, do not claim it passed. Preview intentionally noindex and production domain untouched.
- Full evidence and future test limits recorded in `docs/research/2026-10-15-en-home-schema-audit.md`. EN homepage H1/content/visual/footer unchanged. Other EN pages still defer nonarticle BlogPosting semantic issue until separately authorized.
- Next priority: user-confirmed EN homepage schema accepted in Preview; GSC/proof/target-geo/production deployment remains outstanding. No speculative markup additions.


### 2026-10-15 — EN homepage Schema.org correction isolated from RU/ES
- Owner requested immediate microdata improvements without waiting for other pages. Inspected current schema partial and official Google Organization/Breadcrumb guidelines. Before: EN homepage emits WebSite with false collective `Person: SeoImpuls Team`, lacks Organization, and one-item BreadcrumbList; generic description not page-specific. Original 487×229 `static/SEOIMPULS_logo.webp` exists.
- Scoped only EN-home path in `layouts/partials/head/seo.html`: two linked JSON-LD entities `Organization` (SeoImpuls name, home URL, real 487×229 logo) and `WebSite` (name, home URL, EN language, owner-approved meta description, publisher @id link). No Person or homepage BreadcrumbList. Avoids addresses, legal/review/agency claims.
- Preserved existing RU/ES home WebSite/Breadcrumb outputs and untouched internal EN pages, including their later-to-fix BlogPosting use. Added `scripts/verify_en_home_schema.py` strict built-HTML assertions to Hugo and Pages builds and triggered Chromium browser QA on schema partial edits. Research `docs/research/2026-10-15-en-home-schema-audit.md`.
- Status at commit creation: build/Pages/Chromium/Google Rich Results **PENDING**, do not claim success. No deployment to seoimpuls.com or main; no user-facing content/layout change.
- Next: verify strict CI and Pages, check page JSON-LD in browser/Google test, and update context with results. GSC/proof/geo still pending.


### 2026-10-15 — Owner risk reversal: remove hypothetical noindex problem from EN homepage
- Owner says avoid risks and maximize clarity. The illustrative `noindex` SEO audit scenario was misleading on the commercial main page despite disclosure and not required for search intent. **Fully retired that visual block**, without replacing it or expanding page copy.
- In `layouts/index.html`: removed exactly the `seo-en-home-example` markup and all its EN-only CSS, including mobile rules and sticky-header scroll margin. Kept `What You Receive` three real service-output descriptions, `Which SEO Service Fits Your Website?`, pricing/time FAQ, SEO CTA, H1/meta/canonical and footer animation unchanged.
- In `.github/workflows/rebuild-qa.yml`: replaced assertions demanding example presence with negative regression guard forbidding its heading/text and anchor from rendered EN homepage. RU/ES and all other EN pages left intact; branch `white-seo-rebuild` only, main/production untouched.
- `docs/research/2026-10-15-en-home-competitor-white-space.md` updated to mark the suggested specimen **rejected for homepage**; remains background research only. CI Hugo/Pages/Chromium/axe required after commit; no premature PASS claim.
- Next: confirm strict Hugo and Pages, reopen current Preview, independently run Chromium 390/1280 and axe light/dark; confirm example absent and homepage structure stable. GSC/proof/physical geo remain unverified.


### 2026-10-15 — EN illustrative SEO finding live and validated, handoff checkpoint
- Owner-approved sample in `What You Receive` added in b646dbe8; small anchor-offset CSS fix in 443f5e87 to prevent sticky header obscuring `#seo-en-example-title`. Direct stable link: https://agurkin2021-gif.github.io/seoimpuls/#seo-en-example-title .
- **Verified after final CSS fix:** Hugo strict rebuild QA #96 PASS, GitHub Pages Preview #37 PASS, automatic Playwright 390/1280 browser audit #8 PASS, axe WCAG dark/light audit #5 PASS. In Opera, direct example link displays title, label, four finding cells and footer. Last full-page Chrome audit confirms no horizontal overflow, broken images/links, JS failures, H1/canonical/JSON-LD regressions, desktop floating footer / mobile ordinary footer intact.
- Example is **explicitly hypothetical, not a real client case**, with conditional priority, evidence (HTTP/robots/canonical/GSC if available), approval/implementation ownership, acceptance verification and no indexing/ranking guarantee. Scope EN homepage only; RU/ES, all other EN pages, main and production seoimpuls.com unchanged.
- All automated WCAG checks returned zero confirmed violations; `incomplete` reports still require manual review; not full compliance certification. GSC_PENDING, GEO_PHYSICAL_UNVERIFIED, PROOF_REQUIRED remain. Do not broaden claims or create fictional cases.
- Next: authenticated GSC overlap of `/` vs `/services/`, market relevance, real proof; defer further site edits absent data.


### 2026-10-15 — EN example deep-link heading is no longer obscured by fixed header
- Prior commit b646dbe8 published and validated: Hugo QA #95 PASS, Pages Preview #36 PASS, Chrome responsive run #38831630098 PASS (390/1280px: no overflow, image/link/JS errors, correct H1/meta/canonical/footer), axe WCAG run #38831630071 PASS (zero confirmed violations dark/light, CTA keyboard focus preserved). Visually reviewed full-page 390/1280 PNGs from Chromium artifact.
- Opening the published example via `#seo-en-example-title` in Opera showed its H3 partly hidden behind the sticky top header because the heading is an in-page anchor. Added `scroll-margin-top:126px` to that EN-only example H3 selector in layouts/index.html. No impact on normal page layout, content, mobile vs desktop grid, RU/ES, other EN pages, production or main.
- Next: verify Hugo/Pages and direct-anchored link in Opera; inspect header offset. Update status in context if finished.


### 2026-10-15 — EN homepage illustrative SEO audit finding approved and implemented
- Owner explicitly authorized placing one example of a verifiable SEO recommendation after `What You Receive`. New EN-only card in `layouts/index.html`: `Illustrative audit finding — not a client case` / `An important page excluded by noindex`. Fields cover issue, HTTP/robots/canonical evidence, approval/implementation responsibility and acceptance check. High priority only if page intended for indexing; technical check does not guarantee Google indexing or rankings.
- Compact two-column desktop, one-column mobile `<dl>` with dark styling matching current site. Hugo template guard `{{ if eq $lang "en" }}` preserved; RU/ES, other EN pages, original popping footer, URL/H1/meta, production/main untouched.
- Updated EN generated HTML CI assertions in `.github/workflows/rebuild-qa.yml`, competitor gap document and context same commit. Hugo QA, GitHub Pages and browser/axe validation required after publish; do not claim passed yet.
- Next: verify Hugo+Preview and actual sample in Opera, run Chromium at 390/1280, WCAG, inspect new section visually. Then continue GSC/proof only with evidence.


### 2026-10-15 — Audited competitive whitespace beyond baseline SERP gaps
- Compared six directly competing organic landing URLs from owner-approved `professional seo services` Google Web top 10; direct providers coalition SEO + homepage, Netlynx, Blue Media, Thrive and Americaneagle (5 unique brands). Excluded directories Clutch, Semrush, RevenueBase, Bark for like-for-like provider UX comparisons.
- Observed all providers explain services, several have cases, reports, pricing/timelines, so generic SEO copy does not differentiate SEOImpuls. Six inspected landing pages **did not visibly disclose a worked SEO recommendation record with affected URLs, evidence, implementation owner and acceptance test**; similarly no explicit read-only Search Console access note or "when not to order SEO" decision rule found. These are **page snapshot observations, not proof of competitors' missing internal capabilities/site-wide content**.
- Sourced buyer pain from Google Search Central guidance (written explanation, read-only GSC initial audits) and Reddit discussions (actionable deliverables, named URLs, ownership). Full evidence, comparison, limitations and ranked differentiators saved as `docs/research/2026-10-15-en-home-competitor-white-space.md`.
- Highest-value proposed differentiation: clear illustrative SEO finding record (NOT a fake case) and read-only access reassurance. No site edits in this research commit. H1 remains `Professional SEO Services`. Next: establish actual handoff practice before implying guaranteed deliverables; only then implement one scoped EN-home specimen and QA at 390/1280.
- RU, ES, other EN pages, main and production untouched. GSC_PENDING / PROOF_REQUIRED / GEO_PHYSICAL_UNVERIFIED.


### 2026-10-15 — EN-home WCAG contrast and light/dark keyboard QA accepted
- EN bottom CTA contrast correction (eb900c69) had Hugo #91 PASS and Pages #32 PASS; visible Preview checked with Opera. Dark axe #38829064787 PASS: zero confirmed WCAG A/AA violations at 390/1280 and eight EN CTA keyboard focus states with 3px outlines.
- Light-theme follow-up audit commit da5d2b31: axe #38829420871 PASS. Both **light and dark theme**, 390 & 1280px: 0 confirmed WCAG A/AA violations, CTA focus gate PASS. `incomplete` axe flags persist (aria-prohibited-attr 2, color-contrast 77) and still require manual review.
- PSI preview report obtained in Opera: mobile Performance 98, Accessibility 95 BEFORE fix, Best Practices 100, SEO 66 due intentional preview noindex. No CrUX field data. Do not treat SEO 66 as live production audit, or infer post-fix PSI score from axe.
- GSC property inaccessible through present Opera session (public about/login). Query-to-URL cannibalization remains GSC_PENDING. Windsor.ai was surfaced as possible user-authorized GSC connector, not connected. No direct access/metrics claimed.
- Final evidence + caveats recorded `docs/research/2026-10-15-en-home-accessibility-and-pagespeed.md`. User instruction: EN home only, RU/ES/production/main untouched. Next: authenticated GSC 3–6 months report and verified specialist proof; otherwise avoid speculative SEO rewriting.


### 2026-10-15 — Expand WCAG regression checks to light theme after dark CTA fix
- Confirmed EN-only bottom CTA color+focus fix eb900c69: Hugo QA #91 PASS, Pages #32 PASS, independent Chromium axe #38829064787 PASS: **zero confirmed WCAG A/AA violations** on dark theme at 390/1280, CTA focus outline 3px (8 keyboard focus samples). Axe `incomplete` items require human review; cannot certify full WCAG.
- Updated only `scripts/audit_en_home_accessibility.cjs` to run axe-core again in existing light theme at both widths and block confirmed serious/critical violations there too; restores dark before keyboard trace. No visual site content/CSS change, RU/ES/prod untouched.
- Current light-mode audit run pending; next analyze exact elements and fix scoped EN-home issues if confirmed.


### 2026-10-15 — Correct verified EN-home WCAG CTA contrast and keyboard focus
- New Chromium axe WCAG diagnostic run #38828758946 (390/1280) confirmed **serious color-contrast 2.24:1** on EN bottom CTA `Discuss Your Website` (text #a9a9b3 on #1f739f, required >=4.5:1); main CTA keyboard focus lacked clear outline. See `docs/research/2026-10-15-en-home-accessibility-and-pagespeed.md`.
- Applied scoped CSS **only to EN homepage** in `layouts/index.html`: white high-contrast bottom CTA text normal/visited/hover/focus and explicit cyan 3px `:focus-visible` outline on EN CTA buttons. No other EN pages, RU/ES, footer animation, production, H1/meta or link routes altered.
- Strengthened `scripts/audit_en_home_accessibility.cjs` to fail serious/critical axe violations and invisible keyboard focus on named EN CTAs. GitHub Actions Playwright axe rerun and Page preview still to verify. No invented credential/case evidence.
- PSI mobile on public **noindex preview**: 98 Performance, 95 Accessibility, 100 Best Practices, 66 SEO (preview intentionally noindex), FCP 0.9s, LCP 0.9s, TBT 0ms, CLS 0, Speed Index 3.8s. No field CrUX data for preview.
- GSC direct URL in Opera redirected to login/about; hence GSC_PENDING and cannibalization not quantified. Next verify Axe/Preview, then evaluate light mode and if necessary fix distinct issues with evidence.


### 2026-10-15 — EN homepage next QA: WCAG and real PageSpeed evidence
- Owner asked to continue beyond completed SERP/on-page and 390/1280 browser QA. Examined next evidence needs before editing content.
- Connected Opera cannot read SEOImpuls Google Search Console: direct property URL redirects to publicly available Search Console about/sign-in page. Treat GSC_PENDING; no invented impressions, click trends or cannibalization metrics.
- Public Google PageSpeed Insights mobile run on Preview `https://agurkin2021-gif.github.io/seoimpuls/`: lab Performance 98, Accessibility 95, Best Practices 100, SEO 66; FCP 0.9s, LCP 0.9s, TBT 0 ms, CLS 0, Speed Index 3.8s. Preview lacks Chrome UX field data ("Нет данных") and is intentionally noindex, accounting for SEO indexing audit failure; these numbers do not represent production seoimpuls.com nor field CWV. Accessibility Lighthouse flags insufficient foreground/background contrast, element unspecified so further axe investigation required.
- Added `scripts/audit_en_home_accessibility.cjs` and `.github/workflows/en-home-accessibility.yml`: isolated Chromium axe WCAG 2.2 A/AA diagnostic + keyboard tab-focus trace at 390/1280px, outputs JSON artifact. Runs on relevant EN homepage/template/style changes. No content, RU/ES, main or production changes.
- Current audit run pending; next inspect specific axe nodes before applying scoped CSS changes. User-approved floating footer must remain intact.


### 2026-10-15 — EN-home Google top10 competitor register & intent closure QA finalized
- Created `docs/research/2026-10-15-en-home-professional-seo-competitors.csv` with all ten final URLs from live Google Web query and source parameters, plus entity/type/gap signals. Duplicate Coalition URL is preserved as two actual result URLs. Direct Google browser location was undetermined, so strictly geolocated US rankings NOT asserted.
- Finalized `docs/research/2026-10-15-en-home-professional-seo-serp.md` with exact main intent ownership, gap implementation/commits and limitation flags: SERP_SNAPSHOT_VERIFIED, GEO_PHYSICAL_UNVERIFIED, GSC_PENDING, PROOF_REQUIRED.
- Three EN homepage SERP gap implementation commits c21cc128, c3853d95, f19b17a0 passed Hugo strict QA #85/#86/#87 and Pages #26/#27/#28; browser Opera visually confirmed the new blocks, FAQ and About links.
- New automatic EN 390/1280 Chromium run #38826904019 PASS: HTTP 200, one exact H1, correct production canonical/meta, valid WebSite/BreadcrumbList JSON-LD, all images/URLs functional, no JS or overflow, popup footer intact. Existing preview only. No site content changed in this record/CSV commit.
- **Unresolved:** authentic case studies/team credentials, target market US physical geolocation and ranking competitiveness, GSC query-to-page overlap with /services/, real CrUX and full WCAG; no claim of guaranteed rankings or READY_FOR_RELEASE.
- Next: investigate GSC/geo evidence before changing main SEO key, and obtain verified trust proof; user scope remains EN homepage only, RU/ES/production untouched.


### 2026-10-15 — EN home 390/1280 browser QA now runs on future page changes
- Latest buyer pricing/timing/scope commit f19b17a0 published on GitHub Pages (#28); Hugo strict site QA #87 requires confirmation. Research and gap mapping are in `docs/research/2026-10-15-en-home-professional-seo-serp.md`.
- Updated only `.github/workflows/en-home-browser-audit.yml` to auto-run existing Playwright Chromium audit at 390 and 1280 px whenever EN home content, shared home template, header/footer or corresponding CSS is changed. No live HTML/CSS site edits in this commit, RU/ES and production untouched.
- Test triggers on this workflow commit to verify current EN page after all 3 intent-gap additions. Expected screenshots + JSON artifact. Next: inspect run and confirm all visuals, links, canonical, schema, no broken images/JS, no horizontal overflow.


### 2026-10-15 — EN homepage SERP gap 3: transparent pricing/timing/scope answers
- Following service-choice commit c3853d95 (Pages #27 and Hugo QA #86 PASS; Opera confirmed three existing service routes and EN heading), added EN-only "Pricing, Timing & SEO Scope" with 3 buyer questions: how SEO price is scoped, difference between deliverables and Google ranking timelines, and choosing only necessary services.
- No made-up prices, fixed retainer plans, guaranteed rankings, deliverable timing, staff numbers or invented credentials. Linked to existing /faq/ and /about/ for detailed policies/trust. Content addresses top10 SEO buyer SERP features (commercial comparison, pricing, timetable).
- EN-only 3-column cards with one-column mobile; blocking HTML assertions and research log updated. RU/ES, other EN pages and production untouched. QA/Preview of THIS commit pending.
- Next: verify visual+Hugo/Pages, then on-page audit of intent coverage and unresolved proof/physical geo; separate actual GSC/KD checks before claiming overall competitive strength.


### 2026-10-15 — EN homepage SERP gap 2: route buyers to correct SEO work
- Prior gap #1 commit c21cc128 (definition of professional SEO services) passed Hugo QA #85 and Pages #26; Opera confirmed specialist-not-agency wording.
- Added EN-only `Which SEO Service Fits Your Website?` block with three truthful service entry points and links: technical SEO assessment (/seo/), keyword/intent mapping (/services/keyword-research/), and focused SEO consultation (/services/seo-consultation/). No retainer, industry specialization, performance guarantee or invented offer created.
- Responsive three-column desktop and one-column mobile presentation, with direct descriptive anchor text and keyboard focus style. RU/ES and supporting EN pages left intact. No H1/meta/canonical changes.
- Updated blocking EN HTML QA and gap audit. Current build/Preview needs verification; next step buyer price/timing expectations on EN homepage if these pass.


### 2026-10-15 — EN homepage SERP gap 1: clear professional SEO service definition
- SERP evidence documented in `docs/research/2026-10-15-en-home-professional-seo-serp.md` (direct Google Web top10 with gl=us; physical geolocation unverified): buyer intent requires a clear direct explanation of what professional SEO services mean, distinct from the agency promises in many results.
- Added EN-only H2 "What Are Professional SEO Services?" and ~75-word people-first response before detailed EN service areas in `layouts/index.html`. Accurate provider stance: SEO specialists, not a general agency; technical/on-page/keyword/content possibilities depend on the site; scope and implementation responsibility are agreed, rankings not guaranteed.
- EN-only scoped CSS for desktop/mobile. No H1, title, URL, footer, other EN supporting page, RU/ES or production changes.
- Added blocking generated-HTML QA for answer/agency distinction, updated research. CI/Preview for this commit pending; next step verify then address buyer service-choice gap separately.


### 2026-10-15 — Parameterized Google top-10 and EN-home intent gap map recorded
- Direct Opera Google Web SERP on 2026-10-15 for `professional seo services`, `hl=en&gl=us&pws=0&udm=14&num=10`: 10 organic results resolved to final URLs, no sponsored entries included. Google browser could not determine physical location — US IP/location NOT VERIFIED. First 10: Coalition SEO, Clutch, Netlynx, Semrush directory, Coalition homepage, Blue Media, Thrive, RevenueBase, Bark, Americaneagle. Two Coalition URLs, three directories, one local marketplace; buyer-selection/commercial intent.
- Analyzed page headings plus adjacent `seo services`, `technical seo services` and `keyword research services` SERPs; home owns provider-selection, supporting URLs own specialist detail. Content gaps: direct explanation, service-choice pathways, price/timing expectations, verification/accountability. Proof, price tables, testimonials and credentials need owner-supplied evidence — do not invent. No automated SEO KD/US-only demand inferred from Ads competition.
- Detailed competitor snapshot, links, caveats, gap/intent map and implementation spec saved `docs/research/2026-10-15-en-home-professional-seo-serp.md`. This research-only commit does not modify live site source. RU/ES/main/production untouched.
- Next: implement one EN-home semantic block at a time, test Hugo strict gate, Preview and source context; target SERP_SNAPSHOT_VERIFIED (parameters), GEO_PHYSICAL_UNVERIFIED, GSC_PENDING.


### 2026-10-15 — EN homepage responsive QA final acceptance record
- Playwright run #38823700740 PASS, following the earlier #38823101622 PASS. Both 390px and 1280px: HTML 200, 1 H1 correct, production canonical, page-specific meta description populated, OG description, valid JSON-LD WebSite/BreadcrumbList, 0 image failures, 0 broken internal URLs, 0 browser JS errors, no horizontal overflow. Cookie notice dismisses; footer static on mobile and floating/revealing on desktop.
- Confirmed meta description `Technical SEO audits, on-page optimization, keyword research, content strategy and international SEO — with clear priorities and defined deliverables.` is present under `meta name="Description"`. The initial case-sensitive selector warning was false and corrected.
- Desktop/mobile screen evidence stored under GitHub Actions artifact `seoimpuls-en-home-390-1280` and durable findings `docs/research/2026-10-15-en-home-technical-visual-audit.md`. Potential P2 mobile consent height (~295/844 px) and unmeasured CTA contrast are review items, not confirmed blockers.
- Remaining: country-fixed SERP top10, GSC, real-user Core Web Vitals, keyboard/color contrast, reciprocity with future RU/ES changes. No production site or EN content edits in this audit pass.
- Next: owner decision on P2 visual polish and/or proceed with independent SERP/GSC and CrUX audit.


### 2026-10-15 — Completed reproducible EN home 390/1280 audit and documented evidence
- Browser audit #38823101622 PASS. Chromium at 390 and 1280 px: HTTP 200, one correct H1, correct production self canonical, no horizontal overflow, 4/4 images loaded, 0/13 broken local links, no JS/page network failures, JSON-LD syntax valid (WebSite, BreadcrumbList), desktop footer floating and mobile footer static, cookie consent dismissible.
- Screenshots and audit.json saved in GitHub Actions artifact `seoimpuls-en-home-390-1280` (6 PNG files plus JSON, retained 14 days). Full durable report: `docs/research/2026-10-15-en-home-technical-visual-audit.md`.
- Confirmed mobile cookie notice initially covers ~295/844px viewport height, dismiss button works (P2 UX). Other P2 possible final CTA contrast and lower whitespace require objective checks.
- The initial empty meta-description field in audit.json came from a case-sensitive test selector; actual Hugo template generates `<meta name="Description" content=...>`. Corrected Playwright selector to case-insensitive in this commit. No claim of missing meta description; verify new rerun content.
- SERP/GSC, CrUX Core Web Vitals, keyboard/contrast, reciprocal multilingual hreflang and production remain not fully audited. No HTML/site-content edits.
- Next: inspect rerun meta description and retain scoped EN homepage state; propose separate P2 improvements only after user review.


### 2026-10-15 — Browser audit parser fixed for placeholder hash links
- Chrome audit #38822048771 browser log revealed `HOME_QA_FATAL page.evaluate: SyntaxError ... querySelector '#'`: source page contains a placeholder href="#" intercepted later by page JS. This was a bug in the *audit script*, not proof of a site rendering failure.
- Updated only `scripts/audit_en_home_browser.cjs` anchor test to record "#" as a placeholder and resolve actual fragments via `getElementById()` instead of calling invalid selector `querySelector("#")`. Preserved existing bounded screenshot phases from commit 616e5bd.
- No production or EN home content change; RU/ES unchanged. Browser audit retry required before claiming 390/1280 completion.
- Next: inspect rerun logs and screenshot artifact, document technical and visual findings with severity.


### 2026-10-15 — Harden EN browser audit against screenshot hangs
- Initial audit Chromium runner successfully installed browser and built Hugo but screenshot/diagnostic step took longer than expected.
- Added per-stage logs, bounded 12-second screenshot timeouts and screenshot warnings, and blocked unnecessary external Google font loads in the ephemeral test browser. This changes only `scripts/audit_en_home_browser.cjs`, not live site or production.
- New audit workflow auto-runs for this commit. Earlier run #38822048771 may overlap. Compare both if available; do not claim any 390/1280 result until summaries/screenshots are retrieved.
- RU/ES, main and production untouched. Next: read new browser audit logs and artifacts.


### 2026-10-15 — Reproducible EN-home responsive browser audit added
- User authorized detailed technical/visual audit of English homepage only; no RU/ES or other EN page modification.
- Opera live Preview screenshot and accessibility tree verified visible H1, logo, SVG service images, 8 service areas, 3 deliverables, contacts, and internal paths. Desktop cookie consent banner covers part of the service cards before dismissal; expected overlay vs blocking UX needs viewport tests.
- Added `.github/workflows/en-home-browser-audit.yml` and `scripts/audit_en_home_browser.cjs` to build existing Hugo site and run isolated Playwright Chromium lab checks at 390 and 1280 CSS px, capture screenshots and collect HTML, CSS overflow, links, images, JSON-LD, JS errors, footer behavior and cookie overlay. Workflow stores screenshots and JSON in a GitHub Actions artifact. Audit script does NOT write to site content or production.
- Browser audit run for THIS commit still pending. No claim of 390/1280 success until artifact and logs are read; production seoimpuls.com, main, RU/ES untouched.
- Next: inspect audit Actions run, screenshot evidence and failed checks; record severity and fix only confirmed EN-home regressions in separate scoped commits. Google SERP/GSC and real-user CWV still pending.


### 2026-10-15 — Restore original animated footer popup on English homepage
- Owner reported English homepage footer no longer popped up as before. Root cause: EN-only visual CSS from c8631964 forcibly set `.custom-footer--en-home {position:static!important}`, overriding the existing global `body.footer-floating .custom-footer` fixed/animated behavior.
- Removed only the EN-only static-position override and the related desktop overrides that erased footer reserve space and moved cookie consent banner. Original shared CSS and footer JS floating/scroll/idle/popup logic remain untouched.
- Kept existing EN-home contacts-only presentation (WhatsApp, Telegram, email). RU/ES unchanged. Did not reintroduce generic unrelated social links or unverified embedded map.
- Added `scripts/verify_en_footer_popup.py` and blocking steps in both rebuild QA and Pages Preview workflow to protect original footer animation and generated EN footer markup. Browser scroll interaction still requires follow-up verification after publication.
- No main, production, DNS, H1/CTA/content changes. Next: verify workflows and test actual scroll/idle/reveal behavior in browser; inspect mobile footer and cookie consent placement.


### 2026-10-15 — EN homepage commercial blocks QA confirmed in Opera
- Subtitle commit 439eae23: GitHub Pages #14 PASS, Hugo QA #73 PASS; Opera confirmed approved text.
- Service-area cards commit 6dca9e29: Pages #15 PASS, Hugo QA #74 PASS; Opera confirmed service heading and agreed-scope text.
- Deliverables cards commit e6623ae1: Pages #16 PASS, Hugo QA #75 PASS; Opera confirmed three scoped outputs.
- Final buyer CTA commit ed27a5a8: Pages #17 PASS, Hugo QA #76 PASS; Opera confirmed new heading, copy, Telegram and consultation URLs.
- Opera confirmed four EN supporting targets (/services/, /seo/, /services/keyword-research/, /services/seo-consultation/) open without 404.
- These tests do not establish organic ranking, complete 390/1280px visual QA, accessibility or page speed. SERP_UNVERIFIED; GSC_PENDING. No production, main or RU/ES changes.
- Next: EN-home desktop/mobile visual and technical QA, then geo-fixed real Google SERP and GSC.


### 2026-10-15 — EN homepage buyer CTA clarified and commercial blocks completed
- Previous deliverables commit e6623ae1: Pages workflow #16 and Hugo rebuild QA #75 both PASS; Opera confirmed "What You Receive" and all three scoped outcomes on live Preview.
- Edited ONLY EN conditional CTA section in layouts/index.html. H2 now "Discuss Your Website’s SEO Priorities"; new paragraph explains what information the visitor should share (website, target market, current SEO problem) and the next step (discuss scope and deliverables) without promising positions. Retained Telegram and SEO consultation links.
- Updated blocking EN QA assertion; no edits to H1, meta, other EN pages, RU/ES, main or production.
- Next after this commit: verify Pages/Hugo and live English CTA/links in Opera. Then review EN-home overall layout at 390px/1280px, structured data, image assets, accessibility and SERP/GSC, which remain unverified until tested.


### 2026-10-15 — EN homepage outcomes distinguished from service areas
- Previous service areas commit 6dca9e29 verified in GitHub: Pages workflow #15 PASS, rebuild QA #74 PASS. Opera confirmed EN services heading, coverage text and visible scope qualification in live Preview.
- Added an English-only responsive "What You Receive" section in layouts/index.html after service coverage. Three *conditional* examples: Prioritized SEO Findings, Keyword-to-Page Map, Verification Plan. They describe outputs supported by existing English SEO/keyword/consultation pages, not guaranteed universal package contents.
- New EN-only CSS for 3-column desktop, 2-column intermediate and 1-column mobile; separate from RU/ES styling. No edits to other pages, title, H1, metadata, navigational routes, main or production.
- Updated blocking EN generated-HTML QA; CI/Preview for THIS commit pending. Next: verify new page in Opera and adjust final consultation CTA for clarity if required.


### 2026-10-15 — EN homepage service areas separated from generic deliverables
- After homepage subtitle commit 439eae23, Pages workflow #14 and rebuild QA #73 PASS, and Opera verified new subtitle in actual Preview.
- Replaced EN-only `homeJson` "What an SEO Engagement Delivers" mixed list with "What Our SEO Services Cover": eight explicitly scoped service areas (technical/indexation, on-page, keyword research, content, architecture, performance, international SEO, implementation/measurement). Content grounded in current /seo/ and EN service offerings; no guaranteed ranking or invented proof.
- Added EN-only explanatory text that only agreed work is included, and EN-only two-column service cards with one-column mobile fallback. RU/ES markup and content values untouched.
- Extended blocking EN generated-HTML QA for service coverage and scope disclaimer. Real Pages/Opera checks for THIS commit are pending.
- Next: confirm Hugo/strict/Pages PASS and live EN appearance. Then create a distinct short "What You Receive" outcomes section with deliverable examples conditional on the agreed scope, without repeating every service.


### 2026-10-15 — EN home subtitle grounded in actual service scope
- Compared EN homepage copy with current `/seo/`, `/services/`, keyword-research and SEO-consultation content; those support technical audits, on-page, keyword research, content strategy, international SEO and scoped deliverables.
- Changed **only EN** `content/_index.md` description, which renders the homepage hero subtitle and meta description: "Technical SEO audits, on-page optimization, keyword research, content strategy and international SEO — with clear priorities and defined deliverables.".
- Removed unsubstantiated "experienced specialists" and overly sweeping "Complete SEO solutions"; retained broad professional SEO commercial intent without promising rankings. H1 `Professional SEO Services`, offers, URLs and other languages unchanged.
- Updated EN generated-HTML QA subtitle assertion and research note. CI/Preview publication of THIS commit pending and require direct verification in Opera. SERP_UNVERIFIED / GSC_PENDING.
- Next: inspect published subtitle and QA, then restructure the EN homepage commercial service list and deliverables without duplicating the existing specialized service pages.


### 2026-10-15 — Fix preview root-relative links after live Opera validation
- Opera verified commit 2398c4c4: EN homepage H1 "Professional SEO Services" and approved subtitle display; GitHub Pages workflow #12 and rebuild QA #71 both successful.
- Found a confirmed preview-path defect: unquoted Hugo-minified `href=/services/`, `href=/seo/`, `href=/#how-it-works` were not rewritten by the previous quote-only regular expression and linked to the wrong GitHub Pages root.
- Fixed ONLY .github/workflows/publish-preview.yml preview publishing transform to handle quoted AND unquoted root-relative href/src/action/poster/content/srcset, preserving already correct /seoimpuls/ paths and protocol-relative URLs. Added blocking post-transform tests for EN homepage internal links and anchors, including no links escaping the Preview subdirectory.
- Source content, Title/H1, actual production URLs, main and RU/ES text unchanged. This is a preview-hosting infrastructure correction; no deploy to seoimpuls.com.
- Next: verify build/Pages of THIS commit, reopen published EN homepage using Opera and check exact CTA destinations; do not assert success before new workflow passes.


### 2026-10-15 — EN homepage primary H1 set to Professional SEO Services
- User confirmed using Google Keyword Planner screenshot: phrase `professional seo services` shows 1k–10k average monthly searches under **All locations / English / Google**; advertising competition LOW (not organic ranking difficulty). Frequency is a broad bucket and target-country organic SERP difficulty remains unverified.
- Updated ONLY English content/_index.md: H1/Title changed from "SEO Services: Technical Audits, Keywords & Content Strategy" to "Professional SEO Services". Visible subtitle/meta description changed to the owner-approved "Complete SEO solutions from experienced specialists: technical SEO, on-page optimization, keyword research, content strategy and international SEO.".
- Updated EN homepage generated-HTML QA assertion in .github/workflows/rebuild-qa.yml to check new H1 and visible subtitle, and documented keyword selection and uncertainty in the EN research note. No homeJson/URLs/design edits.
- Opera browser connection verified in this session: published Pages Preview initially displayed previous H1 and subtitle, with the expected `/seoimpuls/` subpath on page; this commit will auto-trigger fresh Preview publishing. Browser validation of the *new* commit still required.
- RU/ES pages unchanged; main and production https://seoimpuls.com/ untouched. Next: verify Actions/preview and check EN H1/subtitle live; independently repair wrong Preview root-relative links before relying on CTA click tests, without altering production URL semantics.


### 2026-10-15 — Context checkpoint aligned with actual EN-home progress
- Updated section 6 of CHATGPT_PROJECT_CONTEXT.md with current EN-home visual/commercial commits, accurate Preview URL, strict EN-only scope, and exact pending CI/browser/SERP/GSC checks. Removed obsolete Pages setup sequence from next action.
- Updated AGENTS.md outdated repository privacy and Pages wording: repository is PUBLIC; isolated preview for white-seo-rebuild is permitted; main/production remain out of scope. No visual/site content change in this checkpoint.
- QA note: source checks confirmed Title/homeJson JSON validity, revised routes and EN-only template guards; **no direct browser or Hugo Actions run evidence** retrieved by this session yet.
- Next: follow section 6, verify CI + rendered EN at 390/1280px.


### 2026-10-15 — EN homepage commercial intent and routing refinement
- After EN-only visual commit c8631964, refined ONLY content/_index.md and conditional EN block in layouts/index.html. H1/Title now "SEO Services: Technical Audits, Keywords & Content Strategy"; meta/hero description describes scope and verifiable deliverables.
- Main hero CTA now /services/, card1 retains /seo/ and card2 routes to /services/keyword-research/ with matching intent. Added brief scope/deliverables explanation and CTA to existing SeoImpuls Telegram plus /services/seo-consultation/. No unverified guarantees/cases/geographic claims.
- Updated .github/workflows/rebuild-qa.yml EN homepage assertion, and added docs/research/2026-10-15-en-home-commercial-refinement.md with public competitor reference and SERP_UNVERIFIED/GSC_PENDING caveats.
- RU/ES content and output branches intentionally unchanged by logic; only EN content added in shared template. CI and browser verification on THIS commit are pending. Production/DNS/main untouched.
- Next: inspect Hugo/strict/Preview workflow, check rendered EN page at 390/1280px and images/links; then QA commercial content and document remaining GSC/SERP blockers.


### 2026-10-15 — EN homepage visual hierarchy and footer repaired
- EN-only visual update: new scoped layout styling in layouts/index.html; removes non-wrapping oversized H1 and forced 440px height from the English process card; presents three process stages as compact numbered items; balances two service cards beside them. Mobile rules for <=1020/767/620px.
- EN homepage footer only: compact, normal-flow contacts with WhatsApp, Telegram and email. Hidden from this page (not deleted from data) nine social links whose destinations are generic platform homepages and the unverified Austin map fallback. Remaining RU/ES site output remains on existing shared design.
- This is the first visual iteration, not an approved final design. No Title/meta/H1 text changes, no cross-page content changes, no production or DNS changes. CI and visual browser checks after this commit are pending.
- Next: inspect new Preview at 390/1280px; then tighten English homepage commercial intent/CTA routing and test generated EN HTML without changing RU/ES.


### 2026-10-15 — EN homepage preview visual asset repair
- Existing files confirmed in repository: static/SEOIMPULS_logo_tight.webp and static/uploads/seo-icon-search-optimization.svg, seo-icon-search-marketing.svg, seo-icon-google.svg. User screenshot showed broken logo and cards on GitHub Pages under /seoimpuls/.
- Changed EN-only template URL handling to Hugo relURL for header logo and all three homepage SVG icons, honoring preview baseURL. RU/ES asset markup kept as before.
- English footer social links had blank font icons in the preview. Retained each link and aria-label but replaced EN-only font glyph with visible two-character label as dependency-free fallback. RU/ES untouched.
- QA limitations: live browser visual check not performed; CI/Pages automatically triggered by this commit. Follow-up: check preview logo, cards and footer and responsive layout. Do not claim full SEO/UX QA.
- No production, DNS, main or non-EN content changes.


### 2026-10-15 — Owner scope narrowed to EN homepage only
- New explicit instruction: work exclusively on English homepage `/` now. Other English pages later, Russian and Spanish only after the English version is finished and approved.
- This commit changes only AGENTS.md and CHATGPT_PROJECT_CONTEXT.md. No website content, images, scripts, templates, URLs, production, or DNS altered.
- Prior next-step `services-hub.html` audit is deferred unless an EN homepage-specific dependency is demonstrated. Next: inspect current EN homepage and audit its actual visual/SEO defects individually, then propose/implement scoped corrections.


### 2026-10-15 — Restore WhatsApp and Telegram icons in published preview
- User screenshot: footer WhatsApp and Telegram shortcuts were blank squares on GitHub Pages preview; source footer relied on Font Awesome `fab` glyphs, whose icon font is not reliably available in this preview.
- Replaced only those two icon glyph nodes in layouts/partials/footer.html with self-contained inline SVG using currentColor, preserving original anchor URLs, labels, shortcuts, JS selectors, and footer layout. No changes to site-wide icons or page content.
- Existing Hugo Actions and Pages preview need to run for this commit. Visual preview and mobile QA still pending verification; no changes to production server, DNS, main, or site routing.
- Next: confirm build and Page deployment; inspect footer at desktop/mobile width and check social links. Then return to services-hub review.


### 2026-10-15 — Pages environment branch rule corrected; preview redeployment triggered
- GitHub environment screenshot confirms `github-pages` now permits `white-seo-rebuild` instead of `main`, without required reviewers or wait timer. Previous attempts were blocked by deployment branch restriction.
- Context-only commit triggers the preview workflow after the permission change. Site content, production, DNS, main untouched. New preview success and actual URL must still be verified.
- Next: verify Pages workflow completion, HTTP and assets on preview, then proceed with services-hub audit.


### 2026-10-15 — Restore standard Pages deployment after manual activation
- User screenshot confirms Settings → Pages → Build and deployment Source: GitHub Actions is saved. The public preview still returned GitHub Pages 404, so no working URL may yet be claimed.
- Removed enablement: true from actions/configure-pages@v5, because Pages has now been initialized manually and the action should use standard site configuration.
- This commit triggers Publish SEOImpuls working preview again. No site content, DNS, live host or main branch changes. Actual deployment must be verified in Actions, and URL must return site rather than 404 before claiming success.
- Next: inspect new preview workflow. If failure persists, capture failing job error to identify repository Pages deployment restrictions.


### 2026-10-15 — Retrigger preview after GitHub Pages configuration
- User confirmed Settings → Pages → Build and deployment → Source: GitHub Actions enabled. Previous preview runs failed before deployment while Pages was not initialized.
- Context-only commit to white-seo-rebuild intentionally triggers the existing push-based Publish SEOImpuls working preview workflow again. No site content, production server, DNS, main, or hosting changes.
- Publication and browser URL remain UNVERIFIED until the new workflow run succeeds and preview is reachable.
- Next: inspect workflow and preview URL; if failed, fix the actual deployment error.


### 2026-10-15 — Attempt automatic GitHub Pages enablement after first preview failure
- First preview run failed at actions/configure-pages@v5: Get Pages site failed / HTTP 404 Not Found. Hugo build, strict white-hat and retired URL checks had passed; artifact/deploy steps were not reached.
- Updated .github/workflows/publish-preview.yml to use actions/configure-pages@v5 enablement: true, requesting automatic Pages activation for the now-public repository. A successful deployment is NOT assumed before observing the new run.
- If automatic enablement is rejected by GitHub permissions, manually use Settings → Pages → Source: GitHub Actions. Do not touch main, production seoimpuls.com, DNS or server.
- Next: inspect new Publish SEOImpuls working preview run and open the live preview URL only after success.


### 2026-10-15 — Automatic visual preview workflow added
- New .github/workflows/publish-preview.yml builds the white-seo-rebuild branch as a standalone GitHub Pages preview at https://agurkin2021-gif.github.io/seoimpuls/ after each push.
- Preview is explicitly noindex and uses a /seoimpuls/ path compatibility rewrite for root-relative HTML/CSS URLs. Source, production domain, main, server and DNS unchanged.
- GitHub Pages must be enabled in Settings > Pages > Build and deployment > Source: GitHub Actions. Private-repository plan eligibility and successful first deployment are NOT yet verified. The preview URL is a target, not confirmed live until the Pages action succeeds.
- Release QA still BLOCKED by unperformed real SERP/GSC/visual/URL migration checks; publishing preview is not production approval.
- Next: verify preview workflow run and real visual navigation. Then audit services-hub.html as planned.


### 2026-10-15 — Shared homepage fallback copy hardened across EN/RU/ES
- The current head 220e1957 had Hugo build #38802848725 PASS and context guard #38802848651 PASS, including blocking strict white-hat gate and contextual affiliate validation.
- In layouts/index.html replaced fallback defaults for first services card and homepage process items 1, 4 and 5 for all languages. Fallback no longer offers backlink packages, algorithmic link-weight promises or behavioral-factor ranking manipulation. New copy describes technical audit, search intent, content, canonical/indexation and measured outcomes.
- No explicit page homeJson values, homepage URLs, partner links, CSS or other templates changed. Actual rendered content can differ because localized homeJson overrides fallbacks. No new business claims.
- New GitHub Actions required after this commit. Further audit needed for services-hub.html legacy card-ranking heuristics and residual fallback metadata. Full SERP, GSC, visual and live migration QA pending. Server/main/Pages not touched.

### 2026-10-15 — Strict white-hat content gate promoted to blocking CI
- Previous affiliate verification commit e3b94255: GitHub Actions #38802644342 PASS, context #38802644970 PASS. Precisely 6 disclosed VPS affiliate links across 4 reviewed RU/ES pages passed contextual destination/rel checks; scan: 30 retired URLs, 44 HTML files, zero general gray-content or legacy-route findings.
- .github/workflows/rebuild-qa.yml now runs scripts/whitehat_content_gate.py --site public --strict as a BLOCKING step after the contextual affiliate validation and diagnostic scan. The previous commented-out strict command is removed.
- Sitewide machine QA is NOT proof of complete SERP, live redirects, rendering/accessibility or indexing. Real Google SERP country/device/date and Search Console, 390px/1280px browser screenshots, Core Web Vitals and live migration are still explicitly pending.
- No live server, main, DNS or GitHub Pages changes. CI for THIS commit needs confirmation; then perform remaining template-fallback audit and external/browser/GSC review before release approval.

### 2026-10-15 — Context-aware affiliate checks replace blanket endpoint ban
- EN FAQ wording update fa4c1eaa: pending/verified in Actions separately; source adjustment kept its migration guidance.
- Confirmed actual previous rendered affiliate inventory: exactly 6 links across RU/ES homepages (2 each) and RU/ES clean web-development pages (1 each). All are explicitly labeled partner/affiliate and rel sponsored nofollow, but use /go/vdsina/ with data-seo-cloaked-href client interception. Original referral destination and noindex endpoint remain unchanged.
- Added scripts/verify_contextual_affiliates.py: BLOCKING CI for exactly these four topical pages, 2+2+1+1 links, destination URL, noindex on redirect page, correct href, JS target, visible disclosures and rel attributes. Additional links/pages or mismatched targets fail.
- Updated scripts/whitehat_content_gate.py: removed blanket /go/vdsina/ LEGACY_ROUTES prohibition and unrelated_affiliate_endpoint flag ONLY BECAUSE separate strict contextual validator is executed in .github/workflows/rebuild-qa.yml. General gray content/path rules unchanged. This is not broad affiliate whitelisting or permission for arbitrary placements.
- CI of THIS commit must be confirmed, including any new red flags. Main, live server, DNS, Pages untouched. Strict release readiness still contingent on fully blocking other conditions, SERP, GSC, visual QA, live migrations.
- Next: review CI, run strict sitewide content gate as additional blocking build step once no remaining gray findings; harden template gray fallback copy; then catalog release dependencies, GSC and real browser visual QA.

### 2026-10-15 — EN FAQ migration guidance clarified without gray-service terminology
- Previous ES homepage commit 25fedcd4: Hugo QA and context guard PASS; diagnostic found 7 issues in 6 HTML. One /faq/ flag came from neutral use of the word backlinks in a URL migration answer.
- content/faq/index.md: replaced that single word with the more precise reader-facing «incoming external links»; kept the warning to assess visibility, link history and equivalent destination before URL changes. No deletion of valid SEO explanations; Title, H1, canonical, scope and other FAQ content unchanged.
- New GitHub Actions require confirmation; affiliate redirect /go/vdsina/ remains per owner request. All other 6 findings are affiliate-route classification, not automatic evidence of Google violations. No server/main/Pages changes.
- Next: implement context-aware affiliate checker with allowlisted relevant destination pages and rel/disclosure checks, retaining the endpoint, then run strict diagnostic separately and mark remaining GSC/visual/real SERP blockers.

### 2026-10-15 — ES homepage converted from ranking-factor claims to helpful SEO workflow
- Previous RU homepage commit abbe7833: Hugo Actions #38800292702 PASS, context #38800292764 PASS. RU home H1/self canonical, genuine SEO links and visible VPS partner disclosure checked, scanner 8 findings/6 HTML, 30 retired routes, RELEASE BLOCKED.
- Rewritten content/_index.es.md homeJson all general "ranking factors" except previously corrected and disclosed VPS hosting item6. New H1/Title «SEOImpuls — servicios SEO y posicionamiento orgánico». First hero CTA now /es/servicios/ matching «Servicios SEO»; secondary remains /es/about/.
- New process blocks: technical audit, keywords and intent, unique architecture, useful on-page copy, multilingual canonical/hreflang, optional hosting, implementation and Search Console measurement. Deprecated backlink/behavioral signal claims removed. Kept original VDSina partner URL, card2 details, visible "enlace de afiliado" text and no guaranteed indexing message.
- .github/workflows/rebuild-qa.yml updated ES old builder CTA destination test and added ES full homepage test: H1/canonical, relevant internal links, no link/behavior rank manipulation. docs/research/2026-10-15-es-home-review.md explains intent ownership and SERP_UNVERIFIED status.
- CI for this commit pending; shared homepage fallbacks may still contain gray wording even when explicit homeJson overrides it. Plan a separate hardening audit of the template before release. Main/live server unchanged; full GSC/SERP/visual QA pending.
- Next after Actions: inspect English FAQ scanner flag and shared homepage fallback, then contextual affiliate endpoint checker. Strict release still BLOCKED.

### 2026-10-15 — RU homepage repositioned as genuine SEO agency rather than ranking manipulation
- Previous ES technical SEO commit c7dc09e1: Hugo #38799702534 PASS and context #38799702511 PASS; H1/canonical/EN+RU hreflang, anchors and local service links checked; 30 retired URLs, 44 HTML, 9 scanner findings in 6 files; release BLOCKED.
- content/_index.ru.md: retained single homepage architecture and VPS partner card, revised H1/Title/Description «SEOImpuls — SEO-продвижение и техническое SEO», switched primary hero action to /ru/uslugi/ matching «SEO-услуги». Replaced all 7 other old "factors of ranking" blocks with verifiable service process: technical audit, keyword research, clear intent mapping, on-page work, international SEO, implementation and Search Console measurement.
- Explicitly removed promotional copy on backlinks, behavioral signals, link authority and claims of guaranteed search results. Kept original offerItem6 and card2VPS affiliate URL/disclosure EXACTLY unchanged with transparent sponsored/nofollow link processing.
- Updated old RU strategy-builder CTA test for correct /ru/uslugi/ destination; new workflow test asserts RU H1, canonical, important internal URLs, no legacy copy and visible hosting disclosure. Documentation docs/research/2026-10-15-ru-home-review.md records intent and limitation SERP_UNVERIFIED, visual/GSC not tested.
- Current CI PENDING; may reveal template fallback or conflicting copy. Next after PASS: separate ES /es/ homepage process rewrite without disrupting VPS affiliate. Main/production/DNS/Pages unchanged.

### 2026-10-15 — ES technical SEO page rebuilt under focused audit intent
- Previous RU SEO commit 52fbfa39: Hugo #38799279460 PASS and context #38799279389 PASS, with H1/canonical/EN+ES hreflang, four technical section anchors, real internal links; scanner 10 issues/7 HTML, 30 retired routes, RELEASE BLOCKED.
- Replaced content/seo/index.es.md at unchanged /es/seo/ canonical. New Title/H1 «Auditoría SEO técnica y optimización web», 11 useful sections explaining crawling/indexation, redirection, canonical, on-page, content intent, hreflang/international SEO, audit deliverables and limitations. Avoided generic rank/backlink promises and overlap with existing ES keyword research, consultation and catalog.
- Reused existing images/icons and Hugo design; retained translationKey=seo-overview for EN/RU alternates. Public competitor comparison and SERP_UNVERIFIED status documented in docs/research/2026-10-15-es-technical-seo-review.md (NOT exact geo-fixed Google top10).
- Updated GitHub rebuild QA with checks for ES H1/self canonical/EN+RU alternate, four anchors and real service links, no old link-selling visible copy. This commit's CI result PENDING.
- No live traffic/GSC/visual approval, no server/main/Pages changes, strict release still BLOCKED. Next after CI: assess full RU and ES homepages for remaining gray or behavioral-promotion copy and clean them one by one, respecting affiliate card disclosure.

### 2026-10-15 — RU technical SEO page rebuilt for diagnostic intent
- Previous ES About commit cfb14ac5: Hugo QA #38798766459 PASS, context #38798766384 PASS. RU/ES About now brand/navigational, with no unverified old statistics or link-selling claims; retired URLs 30, 44 HTML, diagnostic 11 findings/8 files, RELEASE BLOCKED.
- Rewrote content/seo/index.ru.md in place at /ru/seo/ (URL unchanged, preserving existing link signals). Title/H1 «Технический SEO-аудит и оптимизация сайта». Converted generic/unsupported marketing copy into 11 blocks covering crawl/indexability, HTTP redirects, canonical/robots/sitemap, on-page structure, content intent separation, international SEO and practical issue priority.
- Preserved translationKey=seo-overview; kept menu/Hugo builder and existing design. Added genuine internal links /ru/uslugi/, /ru/uslugi/semanticheskoe-yadro/, /ru/uslugi/seo-konsultaciya/ and no link-selling claims or guaranteed positions. Source image assets already exist.
- Comparison and independent commercial SEO intent: docs/research/2026-10-15-ru-technical-seo-review.md. Public examples are SERP_UNVERIFIED, NOT claimed as geo-fixed Google top 10. QA in .github/workflows/rebuild-qa.yml verifies generated H1, self canonical, EN/ES hreflang, four section anchors, local links and no obsolete promotion.
- This commit's CI PENDING; all main/production/DNS/Pages untouched. No fabricated results; actual Search Console, exact SERP and 390/1280px visual tests pending.
- Next: after PASS, rewrite ES /es/seo/ with Spanish technical SEO intent and matching anchors, then RU/ES homepages and EN FAQ. Whole-site release gate remains BLOCKED.

### 2026-10-15 — ES About rewritten for verifiable company presentation
- Previous RU About commit 585839d4: Hugo QA #38798382949 PASS; context #38798382835 PASS; 30 retired URLs/44 HTML, 12 scanner findings in 9 pages, RELEASE BLOCKED. RU About H1/canonical/EN+ES hreflang, service links and removal of old 2900+/1690+/rating claims verified.
- Replaced content/about/index.es.md with new «Sobre SEOImpuls»: business approach, technical SEO/semantics/consultation/site-development service scope, fact-based validation, historic Kwork caveat and contact CTAs. Removed old link selling and unverified historical aggregate ratings/counts. Retained existing Kwork.com profile as reference, not proof of current SEO service outcomes.
- New doc docs/research/2026-10-15-es-about-review.md records claim audit. CI check in .github/workflows/rebuild-qa.yml verifies ES About H1/canonical, EN/RU hreflang, services/technical SEO links and no unsupported historic metrics.
- CI for this commit PENDING; all website/sitewide release gate issues, exact SERP/GSC and visual QA remain open. Main/production/DNS/Pages unchanged. 
- Next: after CI, rebuild technical SEO /ru/seo/ and /es/seo/ under same URLs with genuine technical diagnostic intent (avoid competing with /ru/uslugi/ and /es/servicios/); then homepages and FAQ.

### 2026-10-15 — RU About revised to verifiable white-hat agency scope
- Previous ES soft commit ce3b3b1a: Hugo #38797895399 PASS and context #38797895380 PASS. /es/soft/ draft, fallback card2 no longer uses /es/soft/; 30 retired URLs / 44 HTML, 13 diagnostic findings in 10 files, RELEASE BLOCKED.
- Replaced content/about/index.ru.md with new H1 «О SEOImpuls», clear description and six structured blocks: practical approach, real service scope, transparent deliverables, historical Kwork evidence caveat, localized service CTAs and contact. Old link-selling pitch and unverified 2900+/1690+/5.0/69% aggregates removed from the new page. Associated historical Kwork URL retained as reference, NOT proof of white SEO service results.
- No fabricated business milestones, employees or guaranteed rankings. docs/research/2026-10-15-ru-about-review.md explains what was removed and evidence limitations. .github/workflows/rebuild-qa.yml tests RU About canonical/H1, EN/ES alternate, real service links and no legacy statistics.
- CI for this commit PENDING; full RU/ES localization, visual QA, GSC and live redirect work still incomplete. Main, production, Pages and partner route unchanged.
- Next: after CI, separately rewrite ES /es/about/ to the same honest scope, preserving ES natural phrasing. Then RU/ES technical SEO and homepages one at a time; EN FAQ after.

### 2026-10-15 — Empty ES /soft/ disabled and homepage fallbacks hardened
- Previous RU/ES catalog commit 6423127c: Hugo build #38797215145 PASS, context #38797215007 PASS. RU & ES each have 4 service cards including legitimate independently scoped website development, 29 retired URLs across 45 HTML, 15 audit findings/11 affected pages, RELEASE BLOCKED. EN remains 3 cards.
- content/soft/index.es.md: draft:true; /es/soft/ content had only an empty builder block and no useful SEO software; old URL added to docs/retired-routes-en.txt. Original remains in main, no server 410/redirect to affiliate.
- layouts/index.html: removed deprecated card2 fallback to /es/soft/ or /soft/. Second homepage card is rendered only when homeJson supplies an explicit URL; EN/RU/ES homeJson already contain such URLs, so current real destinations unchanged. The approved hosting referral stays; non-contextual forced redirects stay removed.
- See docs/research/2026-10-15-es-soft-retirement.md for route evidence. New CI will verify ES software absent, no stale source fallback, and explicit second card exists on all three homepages.
- New commit build/context guard pending. Other remaining release blockers: RU/ES homepage and /seo/ copy, RU/ES About, EN FAQ, explicit affiliate route conservative scanner flag. GSC, exact SERP top-10 and visual QA still missing.
- Next: verify CI then separately clean RU and ES About pages; keep brand claims verifiable and no invented clients. Site main, production, DNS, Pages unchanged.

### 2026-10-15 — RU/ES catalogs include independent website development service
- Previous ES dev commit 4cbbe2d1: Hugo #38796764348 PASS, context #38796764349 PASS, 29 retired routes, 45 generated HTML, 15 diagnostics/11 files; RU/ES H1, canonical, mutual hreflang, relevant links and sponsored affiliate labels passed. No live deploy; new site-dev offer needs current business/pricing confirmation before production.
- Added a fourth honest card to content/services/_index.ru.md at /ru/uslugi/razrabotka-saitov/ and content/services/_index.es.md at /es/servicios/desarrollo-web/. Source images reused; old 3 SEO service cards not moved. Added content explanation distinguishing site development from audits, keyword research and consultation. EN catalog remains 3 while EN web dev translation is draft.
- Updated .github/workflows/rebuild-qa.yml strict RU and ES service-catalog checks to 4 exact expected cards and continued reciprocal EN/RU/ES hreflang for existing translated SEO services. Rationale docs/research/2026-10-15-ru-es-catalog-website-development.md.
- CI for current commit PENDING; correct any card pairing or link issues before moving on. Old web-development pages remain retired only in rebuilt Hugo, not live; all 301/410 decisions pending GSC. Full release remains BLOCKED.
- Next: remove /es/soft/ empty service from candidate and check no incoming links; then clean RU/ES About and SEO overview/Home and FAQ. Preserve explicit /go/vdsina/ affiliate redirect without misleading automatic /soft/ rewrites.

### 2026-10-15 — ES website development migrated from satellite mixed offer
- Previous RU website-development commit e82b4843: Hugo build #38796288559 PASS and context guard #38796289464 PASS. Retired routes 28, 45 generated HTML, 17 diagnostic findings in 11 pages, RELEASE BLOCKED. New RU /ru/uslugi/razrabotka-saitov/ canonical, related SEO links and properly disclosed optional VPS affiliate checked.
- Replaced content/services/website-creation/index.es.md with legitimate scoped web-development page at /es/servicios/desarrollo-web/ (H1 «Desarrollo web a medida para empresas»). Removed satellite/ranking claims and made pricing of US$75/$16 historical and subject to confirmation. Existing translationKey services-website-creation retained, with ES and RU as available variants; EN version remains draft.
- Old /servicios-de-link-building/creacion-de-sitios-web/ added to docs/retired-routes-en.txt. SEO intent, public competitor examples and migration caveats in docs/research/2026-10-15-es-web-development-migration.md. Real exact Google top-10 SERP, GSC/live HTTP/referring links, and actual current business rates still UNVERIFIED. No production 301/410.
- .github/workflows/rebuild-qa.yml now checks generated RU/ES mutual hreflang, titles, canonical, local related links and clearly labeled sponsored/nofollow VPS referral. CI result for this commit PENDING.
- The new website development page is not yet a fourth card in the RU/ES SEO services catalog: expand catalogs after checking pages and confirming product terms; do not disturb three existing SEO intents or fake an EN page.
- Main, live server, DNS, GitHub Pages and partner endpoint unchanged. Next: CI; decide whether to add RU/ES website development as complementary cards; then remove /es/soft/ empty archive and rewrite RU/ES SEO/About/home copy.

### 2026-10-15 — RU website creation migrated out of old link-selling namespace
- Baseline commit c07b0c29: Hugo #38794930874 PASS and context guard #38794930526 PASS; 27 retired routes and 20 informational audit findings in 11 HTML; release BLOCKED.
- Inspected content/services/website-creation/index.ru.md: legacy product combines honest responsive website development with a satellite package and other questionable claims. Replaced with a practical, bounded website-development offer using real source capabilities: small landing/multipage sites, semantic markup, mobile layout, basic technical SEO, conditional DNS/HTTPS and handover; NO satellite packages or ranking guarantees.
- New clean candidate URL /ru/uslugi/razrabotka-saitov/, Title/H1 «Разработка сайтов на чистом коде», preserved translationKey=services-website-creation and relevant image. Historical $75/$16 is labeled not an approved present tariff; confirm current business offering and terms before release. Clearly labeled optional VPS referral /go/vdsina/ with sponsored/nofollow must be checked in generated HTML.
- Old /uslugi-linkbildinga/sozdanie-saitov/ appended to docs/retired-routes-en.txt; no live redirect/410. docs/research/2026-10-15-ru-web-development-migration.md documents a publicly sampled competitor comparison (NOT exact Google top 10), intent, gaps, URL migration and unknown GSC. Updated blocking QA to verify H1, canonical, internal links, old URL absence, and single explicitly disclosed affiliate.
- Current commit CI pending. Full original kept in main. RU/ES catalogs still show exactly three already-reviewed SEO offers; development service is not added as a fourth card until both locales and offering scope are checked. Existing EN translation remains draft.
- Next: check current CI; separately rebuild ES /servicios-de-link-building/creacion-de-sitios-web/ at /es/servicios/desarrollo-web/, preserving translationKey and reviewing pricing. Then consider RU/ES catalog cards together and move to /es/soft/. No live server, DNS, Pages or main changes.

### 2026-10-15 — RU/ES architecture quality gate confirmed; remaining issues inventoried
- Previous ES catalog commit 91a86bf5: GitHub Actions #38794561199 PASS (Hugo, 27 retired routes over 45 HTML, 3-page RU/ES/EN catalog + keyword + consultation reciprocal hreflang, canonical and cards), context #38794561487 PASS. Whole-site diagnostic 21 findings in 12 HTML; site release BLOCKED.
- Fixed content/services/_index.ru.md: removed the leftover negative advertising reference to artificial Domain Rating and link networks; instead clarified verification criteria. This is only a local copy correction; 3 RU cards and all paths unchanged.
- Added docs/research/2026-10-15-remaining-sitewide-issues.md with exact affected page groups, planned remediation order and clear separation between gray offers and permitted explicitly labelled /go/vdsina/ affiliate.
- Complete RU/ES canonical and translation architecture is verified in static CI; not a claim that all RU/ES copy, SERP or visual QA is finished. No server, DNS, GitHub Pages, production redirects or main changes.
- New context-only/copy commit needs its own CI confirmation; target is <=20 remaining scanner findings (no broad unjustified suppression). Next step: audit/rebuild RU/ES website-creation old pages under independent genuine intent or retire them safely, preserving historical signals after GSC.

### 2026-10-15 — ES clean SEO catalog replaces link-selling hub
- Previous ES consultation commit fc75fac8: Hugo #38794106882 PASS, context #38794106978 PASS, ES consultation new H1/canonical/EN-RU alternates and old URL retirement; 26 retired routes, 38 diagnostics in 16 HTML, RELEASE BLOCKED.
- content/services/_index.es.md rebuilt as /es/servicios/ with H1/Title «Servicios SEO para sitios web», 3 honest cards linking /es/seo/, /es/servicios/investigacion-palabras-clave/, /es/servicios/consultoria-seo/; translationKey services retained.
- content/_index.es.md: homepage brand SEO title/description, first service card and link corrected (VPS affiliate block retained). content/seo/index.es.md catalog CTA corrected; layouts/index.html ES fallback labels, URLs, SEO icon corrected; hugo.toml ES menu now has Servicios SEO catalog and SEO técnico detail.
- Old /servicios-de-link-building/ added to docs/retired-routes-en.txt for build/link/sitemap gate. docs/research/2026-10-15-es-services-architecture.md maps unique intents and notes SERP_UNVERIFIED. NOT a same-intent redirect to the new clean catalog.
- QA extended for ES hub 3 cards, title/canonical, menu, homepage, three-way EN/RU/ES canonical/hreflang for hub/keyword/consult. New Actions for current commit PENDING; strict release remains BLOCKED by other gray RU/ES and sitewide QA. Main, DNS, server, Pages unchanged.
- Next: inspect all latest Actions, verify no broken links and hreflang, inventory remaining legacy gray active pages and review website creation. Then full post-page SERP/on-page audit RU/ES and final release test; live migration requires separate owner authorization.

### 2026-10-15 — ES SEO consultation migrated to clean service URL
- Previous ES keyword migration commit 47926dc5: Hugo CI #38793772992 PASS and context guard #38793772952 PASS. New /es/servicios/investigacion-palabras-clave/ H1/canonical/EN-RU alternates passed; 25 retired URLs, site scanner 44 findings/18 affected pages. RELEASE BLOCKED.
- Rebuilt content/services/seo-consultation/index.es.md at /es/servicios/consultoria-seo/ with H1 «Consultoría SEO para sitios web», advisory search intent and distinct content from ES keyword/technical pages. Replaced corrupt legacy description, unlimited lifetime support and link-selling offers; old US$350/three hours explicitly historical pending confirmation.
- Updated two old-link references in ES catalog from /servicios-de-link-building/consultoria-seo/ to new /es/servicios/consultoria-seo/. Retired former URL in docs/retired-routes-en.txt. Same-intent 301 only PROPOSED at future production migration; main and live site unchanged.
- docs/research/2026-10-15-es-consultation-migration.md documents competitor comparisons (SERP_UNVERIFIED, no exact geo-fixed top-10) and intent/limitations. New QA checks built ES canonical/H1 and EN-RU hreflang, new keyword link and absence of old URL; CI pending.
- Next: after PASS build ES /es/servicios/ clean catalog, update ES menu/home/SEO CTA, verify old hub absence, reciprocal hreflang and all three service destinations. Then cross-locale SEO QA, remaining legacy pages still BLOCKED.

### 2026-10-15 — ES keyword research migrated to clean commercial URL
- Previous RU services hub commit 5a9543f8: Hugo #38793415941 PASS, context #38793416117 PASS; /ru/uslugi/ self canonical, EN hreflang, three live SEO service cards, new menu/home link, 24 retired URLs and 50 whole-site diagnostic findings; RELEASE BLOCKED.
- Rebuilt content/services/keyword-research/index.es.md under /es/servicios/investigacion-palabras-clave/ with Title/H1 «Investigación de palabras clave para SEO»; own commercial intent, eight detailed content sections, historical US$90 conditional on scope and no ranking guarantees. translationKey remains services-keyword-research, enabling EN and RU hreflang.
- Updated exact two ES old inbound references from /servicios-de-link-building/palabras-clave/ in old ES catalog and ES website-creation source, registered old URL in docs/retired-routes-en.txt. Same-intent 301 only proposed for future live migration.
- Search-intent evidence in docs/research/2026-10-15-es-keyword-migration.md, SERP_UNVERIFIED (not exact Google top 10/geo). QA checks ES H1/canonical/RU/EN alternates and absence of old route. New CI pending; ES hub still old until consultation and then parent migration. No server/main changes, visual QA and GSC pending.
- Next: verify this CI, then ES consultation /es/servicios/consultoria-seo/ with old-hub inbound link update, then clean ES catalog /es/servicios/.

### 2026-10-15 — RU clean SEO catalog and primary navigation rebuilt
- Previous RU consultation commit f956fcbc passed Hugo #38792517329 and context guard #38792517336. True RU keyword and consultation pages now exist independently of the old link-building namespace.
- content/services/_index.ru.md: new canonical /ru/uslugi/, H1 «SEO-услуги для сайта», only 3 truthful cards for /ru/seo/, /ru/uslugi/semanticheskoe-yadro/ and /ru/uslugi/seo-konsultaciya/; translationKey services retained for EN/RU/ES alternates. No old link-selling/satellite offer in this new catalog.
- Updated RU main in content/_index.ru.md, CTA inside content/seo/index.ru.md, RU navigation in hugo.toml (catalog plus separate technical SEO), RU homepage template fallback/card copy and icon in layouts/index.html. Old /uslugi-linkbildinga/ added to docs/retired-routes-en.txt for build and link checking.
- Report docs/research/2026-10-15-ru-services-architecture.md records intent ownership, sample evidence and SERP_UNVERIFIED; no unverified rank proof claimed. The other languages and shared EN services source unchanged.
- CI of this commit pending: generated RU catalog with exactly 3 correct card hrefs, self canonical, EN hreflang, RU homepage link, menu and old retired route absence must pass. Main, server, DNS, Pages untouched. No final 301/410 decisions; full release still BLOCKED (other RU and ES legacy pages, GSC, visual QA).
- Next after CI: ES keyword /es/servicios/investigacion-palabras-clave/ and consultation /es/servicios/consultoria-seo/, then /es/servicios/ catalog with homepage, menu and hreflang. Maintain per-commit context.

### 2026-10-15 — RU SEO consultation migrated to independent white SEO URL
- Previous RU keyword commit 516da541 CI #38792210897 PASS, context guard #38792210910 PASS: /ru/uslugi/semanticheskoe-yadro/ H1/canonical/en-us alternate, old URL retired and no stale links, 68 diagnostic findings in 20 HTML. Release BLOCKED.
- Replaced content/services/seo-consultation/index.ru.md with substantive white SEO advisory content at /ru/uslugi/seo-konsultaciya/; retained translationKey for EN/ES matching, clear advisory vs technical-audit vs semantic clustering intent. Removed corrupt source meta and claims of perpetual support, mass link-selling topics, ranking guarantees. Prior $350/three hours explicitly marked historical pending confirmation.
- Updated exact referring RU hub links /uslugi-linkbildinga/seo-konsultaciya/ → /ru/uslugi/seo-konsultaciya/; registered old route as candidate withdrawn in docs/retired-routes-en.txt (only proposed future relevant 301, NOT live). New source evidence doc docs/research/2026-10-15-ru-consultation-migration.md with SERP_UNVERIFIED sample competitive pages.
- New QA validates generated H1, canonical, hreflang EN, real RU keyword internal link and old route absence. CI for THIS commit pending. RU hub still displays old category/name and is next. Main/production untouched, visual QA and GSC pending.
- Next: rebuild RU /ru/uslugi/ as the legitimate non-gray catalog, change homepage card and RU primary navigation; inspect cross-language and legacy hub links. Then ES analogues.

### 2026-10-15 — RU keyword research migrated to independent white SEO URL
- Previous commit f312bb56: Hugo build #38791068670 PASS and context #38791068844 PASS; old sales 21 routes removed, 45 HTML; sitewide scanner 74 findings in 20 HTML, RELEASE BLOCKED.
- Rewritten content/services/keyword-research/index.ru.md: new canonical /ru/uslugi/semanticheskoe-yadro/; H1/Title «Сбор семантического ядра и кластеризация запросов», commercial intent distinct from /ru/seo/, original translationKey preserved. Eight meaningful sections: input, formats, intent clustering, methodology, deliverables, pricing caveat, FAQ, contact. Historical $90 is explicitly pending confirmation; no false guarantees.
- Updated RU catalog inbound links and old website-creation embedded keyword-service link from /uslugi-linkbildinga/sbor-semanticheskogo-yadra/ to /ru/uslugi/semanticheskoe-yadro/. Registered withdrawn candidate old URL in retired-route manifest to fail on remaining links/HTML/sitemap. New research docs/research/2026-10-15-ru-keyword-migration.md with competitor URLs and explicit SERP_UNVERIFIED: search examples are NOT exact verified Google top-10.
- Tests for this commit require Hugo build, new page canonical/H1 and absence of old URL, link audit, context guard; live 301 has NOT been applied and must await GSC and live traffic/referrers, no server or main changes. Existing RU catalog still has old parent namespace until its own migration and is not release-ready.
- Next: after CI, rebuild RU consultation with independent /ru/uslugi/seo-konsultaciya/, then replace RU catalog and homepage/menu references, and finish ES equivalents. Visual QA still pending.

### 2026-10-15 — ES artificial Domain Rating offer and misleading catalog links retired
- Previous ES Backlinks commit bda3c0d3: Hugo + retired URL check #38790748502 PASS; context #38790748461 PASS. Candidate: 46 HTML, 20 retired URLs, 80 diagnostics in 21 pages, RELEASE READINESS BLOCKED.
- content/services/domain-rating/index.es.md now contains only a draft archival stub under /servicios-de-link-building/domain-rating/; full historical page remains in main. Old artificially elevated third-party metric service is no longer offered in rebuilt site.
- In content/services/_index.es.md removed exactly two old cards: «Domain Rating» button misleadingly linking to '/' and matching unl inked image. Existing genuine consulting/semantics/site-creation elements unchanged; no claims of their full quality readiness.
- docs/retired-routes-en.txt adds /servicios-de-link-building/domain-rating/ and docs/research/2026-10-15-es-dr-retirement.md records migration decision. This commit must pass Hugo, retired-route and context guard QA.
- All six direct old RU/ES gray service page candidates (RU link strategy, backlinks, DR; ES link strategy, backlinks, DR) are retired. But two parent catalogs still have legacy URL/name/content, and RU/ES homepage/SEO/service content needs further work. Full strict release gate BLOCKED.
- No production HTTP changes, 301/410, Page publication, GSC export, browser/visual QA, or new affiliate removal. Main and server unchanged.
- Next after CI: inspect residual whole-site scanner and plan clean /ru/uslugi/ and /es/servicios/ with same-intent migration of genuine keyword research/consultation before retiring parent legacy hubs. Do not auto-redirect gray hubs to generic pages.

### 2026-10-15 — ES Backlinks discontinued page and fake catalog CTA withdrawn
- Previous ES link-strategy commit 29e6cb9c: CI #38790360032 Hugo+retired-routes PASS; context guard #38790360037 PASS; 19 retired URLs across 47 HTML, 85 diagnostic findings/22 affected pages, release BLOCKED.
- content/services/backlinks/index.es.md replaced in white-seo-rebuild with a small draft-only stub; full original saved in main. Old URL /servicios-de-link-building/backlinks/.
- content/services/_index.es.md: removed exactly two obsolete blocks, including a fake «Backlinks» button formerly pointing to homepage '/' and a matching image without a destination. True commercial SEO services kept intact.
- Added URL to docs/retired-routes-en.txt, report docs/research/2026-10-15-es-backlinks-retirement.md. New CI must confirm output and links; GSC, 301/410, external links and live audit still missing. Main, production and /go/vdsina/ unchanged.
- Next: when CI PASS, ES artificial Domain Rating page and misleading button/image; then review remaining old RU/ES hubs and legitimate service migration. Strict release gate BLOCKED.

### 2026-10-15 — ES paid tier link strategy retired and homepage link corrected
- Previous RU DR commit d26527d7: Hugo and retired URL CI #38790050825 PASS; context guard #38790050904 PASS. Retired URL count 18 over 48 HTML; diagnostic findings 93 in 23 files; RELEASE READINESS BLOCKED.
- /servicios-de-link-building/estrategia-de-link-building/: old multi-level link sales removed from the white-seo-rebuild candidate by replacing content/services/estrategia-de-link-building/index.es.md with an unpublished draft stub; full original remains in main.
- Two matching blocks (catalog image and button) removed in content/services/_index.es.md. content/_index.es.md newsUrl changed from retired page to /es/news/. In docs/retired-routes-en.txt added old URL; docs/research/2026-10-15-es-linkstrategy-retirement.md records scope/URL migration.
- CI for this commit is still pending; check generated HTML and sitemap, incoming links and missing target /es/news/. No live 301/410, GSC, browser or PageSpeed verification done. Other genuine services and VDSina affiliate endpoint untouched. Source main and production not modified.
- Next after CI: retire ES Backlinks and artificial DR cards; then replace old catalog hubs with new legitimate taxonomy and migrate keyword research/consultation after SERP/GSC.

### 2026-10-15 — RU artificial DR service withdrawn from candidate
- RU Backlinks commit 0aca4373: Hugo / retired-route check #38789774355 PASS; context guard #38789774377 PASS. Candidate: 49 HTML, 17 retired URLs, 101 scan findings in 24 files; release BLOCKED.
- /uslugi-linkbildinga/uvelechenie-domen-reytinga/ has been replaced in the working branch by a minimal draft stub; full original remains in main. The previous offering sold artificial growth of Ahrefs Domain Rating rather than a legitimate Google SEO deliverable.
- content/services/_index.ru.md: removed exactly two matching image/button blocks, preserving the genuine keyword research, consultation and website creation cards. Added route to docs/retired-routes-en.txt. See docs/research/2026-10-15-ru-domain-rating-retirement.md.
- Upcoming CI must verify Hugo build, absence of retired URL and incoming links, and updated context. No server 301/410, GSC/referring links not reviewed, original main and /go/vdsina/ unchanged.
- RU direct gray-service page pass is complete, but RU legacy hub, homepage and legal service pages still require substantial SEO/URL work. Next: ES estrategia, backlinks and DR in independent commits, then migrate legitimate services and hub.

### 2026-10-15 — RU paid backlink package unpublished and catalog links removed
- Previous commit 60c2937b: Hugo build and retired-route check #38789334524 PASS; context guard #38789334373 PASS. Scanner 108 findings / 25 affected files across 50 HTML; 16 retired routes all absent; release still BLOCKED.
- Old route /uslugi-linkbildinga/obratnye-ssylki/ removed from candidate public output. Instead of leaving the large commercial copy in the working branch, content/services/obratnye-ssylki/index.ru.md replaced with a minimal draft-only archival stub; full original remains untouched in main.
- Exactly two catalog entries (button and image) removed from content/services/_index.ru.md, without changing legitimate keyword research, consultation and website creation entries. Added the old URL to docs/retired-routes-en.txt. Assessment: docs/research/2026-10-15-ru-backlinks-retirement.md.
- The draft and generated URL/link checks must pass GitHub Actions for this commit before next page. No actual server 410/301, GSC not exported, canonical/referring links unverified, no action on production or affiliate endpoints.
- Next: after CI PASS, audit/retire RU artificial Domain Rating page, then ES link strategy, backlinks and DR, each separately and with persistent context.

### 2026-10-15 — RU link-building sales page retired
- Previous white-seo-rebuild commit 5fb8666e: GitHub Actions 38788366497 (Hugo and retired route validation) PASS and 38788366136 (context guard) PASS. 15 retired URLs, 51 HTML pages, 117 informational scan findings in 26 files; release blocked.
- content/services/linkbilding/index.ru.md: draft:false → true; old URL /uslugi-linkbildinga/linkbilding/ no longer appropriate (paid tiered links via forums/blogs).
- content/services/_index.ru.md: removed exactly 2 matching image/button blocks. content/_index.ru.md: replaced old home newsUrl with /ru/news/; all other homepage elements retained. Registered the URL in docs/retired-routes-en.txt; details in docs/research/2026-10-15-ru-linkbuilding-retirement.md.
- Test before declaring pass: new Hugo Actions and context guard, no generated former page/inbound links, /ru/news/ destination. No live 301/410 and no production, main, Pages or affiliate endpoint changes.
- Next: after passing CI, retire RU /uslugi-linkbildinga/obratnye-ssylki/, then RU artificial DR, followed by ES equivalents. Preserve genuine keyword research and consulting content.

### 2026-10-15 — ES satellite/microsite sales withdrawn from candidate
- Previous RU satellite commit 1def6013: Hugo build #38788100026 PASS, context guard #38788099520 PASS, retired routes 14 / 52 HTML PASS, diagnostic 123 findings in 27 HTML files, RELEASE READINESS BLOCKED.
- content/services/desarrollo-de-micrositio/index.es.md: draft:false → true for /servicios-de-link-building/desarrollo-de-micrositio/. The source bundled microsites/satellites with guaranteed first-page Google positions and authority placements; this is withdrawn without pretending the same intent is served by honest SEO services.
- Removed exactly two matched ES catalog blocks (image + button) in content/services/_index.es.md and added route to docs/retired-routes-en.txt. Scope/risk documented in docs/research/2026-10-15-es-microsite-retirement.md. No changes to other catalog entries.
- No live HTTP 301/410, no change to main, GitHub Pages or production. GSC/referring links and live URLs are UNKNOWN; future REVIEW_BEFORE_410 decision remains conditional. Contextual affiliate /go/vdsina/ preserved; gray page affiliate link simply no longer generated.
- This commit's Actions still pending. The four requested RU/ES Tier and satellite URLs are now draft in work branch; must verify Actions and check remaining risks before claiming complete sitewide white SEO.
- Next: verify new CI; inspect all remaining legacy RU/ES catalog pages, SEO homepages, sitemap, source and HTML; prioritize disarming both old link-building hubs and sales of backlinks/DR, then verify lawful same-intent service migrations.

### 2026-10-15 — RU satellite promotional page removed from candidate
- Previous ES Tier commit 25051e7c: Hugo #38787834456 PASS and context guard #38787834442 PASS. Retired-route check: 13 URLs over 53 HTML, zero stale links; 131 whole-site diagnostic findings in 28 files, release BLOCKED.
- Source content/services/sozdanie-satellitov/index.ru.md → draft:true for /uslugi-linkbildinga/sozdanie-satellitov/. Current page bundled site creation with satellite ranking schemes, guaranteed Google Top and paid authority placements, hence not a legitimate same-intent white SEO replacement.
- Removed exactly two corresponding RU catalog blocks (image and button) in content/services/_index.ru.md, keeping other services for their own audit. Added route to docs/retired-routes-en.txt for CI; rationale docs/research/2026-10-15-ru-satellites-retirement.md.
- Main/production/Pages untouched; no 301/410 actions on server. GSC/live indexing/backlink analysis still pending. Genuine website development to be evaluated separately under independent legitimate intent. VDSina explicit endpoint unchanged, but affiliate reference inside retired gray content no longer rendered.
- New CI pending; next: verify result, then separately retire ES legacy satellite/microsite page and its 2 catalog cards. Whole site still RELEASE READINESS BLOCKED.

### 2026-10-15 — ES Tier 1–2–3 withheld and removed from ES catalog
- RU Tier commit 603d15b9: Hugo #38787608283 PASS and context guard #38787608200 PASS; retired check 12 URLs/54 HTML, whole-site diagnostic 140 findings/29 affected files, RELEASE READINESS BLOCKED.
- content/services/tier-1-2-3/index.es.md: draft false → true for /servicios-de-link-building/tier-1-2-3/. Removed precisely two blocks referencing this URL (ES catalog image and corresponding button) from content/services/_index.es.md. Other catalog products left for separate passes.
- Registered /servicios-de-link-building/tier-1-2-3/ in docs/retired-routes-en.txt; generated pages, internal links and sitemap are validated by scripts/verify_retired_routes.py in GitHub Actions. Context/evidence: docs/research/2026-10-15-es-tier-retirement.md.
- The old Tier transaction is not equivalent to a legitimate technical SEO service, so no artificial 301 to generic SEO. Future 410 merely proposed pending live/GSC/referring-link audit; production, main and Pages unchanged. The affiliate redirect /go/vdsina/ was not removed.
- New CI pending, then RU satellite /uslugi-linkbildinga/sozdanie-satellitov/ page and exactly matched catalog card, followed by ES microsite/satellite. Strict release gate still BLOCKED.

### 2026-10-15 — RU Tier 1–2–3 removed from Hugo candidate and service cards
- Previous commit f8c1985c: Hugo rebuild + RU/ES CTA and retired URLs #38787065170 PASS; context guard #38787065220 PASS. Baseline diagnostic had 151 issues across 30/55 HTML files, RELEASE READINESS BLOCKED.
- Source content/services/tier-1-2-3/index.ru.md: draft:false → true for /uslugi-linkbildinga/tier-1-2-3/. Removed exactly two referring builder blocks (image + button) from content/services/_index.ru.md, without editing the remaining catalog cards.
- Added /uslugi-linkbildinga/tier-1-2-3/ to docs/retired-routes-en.txt. The blocking verify_retired_routes.py tests generated HTML pages, links and sitemap. Research and migration rationale in docs/research/2026-10-15-ru-tier-retirement.md. Existing pricing or Tier-network SEO copy is not repurposed.
- No new white SEO service pretended to fulfil the old tier package. Future 410 candidate remains only a migration plan pending GSC/live/backlink audit. /go/vdsina/ partner redirect and other related, genuinely contextual placements kept; links inside retired gray page vanish as that page is unpublished.
- This commit's CI is pending; next is confirm both checks and fix any remaining references before proceeding to ES Tier. Main/server/Pages unchanged; strict sitewide gate remains BLOCKED.

### 2026-10-15 — ES legacy SEO Strategy Builder retired; homepage entry points corrected
- Предыдущий RU step commit 0426a46e: GitHub Actions Hugo+retired-route+RU hero validation #38786675935 PASS, project context #38786676085 PASS. Было 152 находки в 31 из 56 HTML; strict release gate BLOCKED.
- content/strategy-builder/index.es.md: draft:true; /es/constructor-estrategias-seo/ перестаёт генерироваться обычным Hugo. Старый контент сочетал link-building tactics и контролируемый рост позиций, поэтому не подходит для новой белой SEO-компании.
- content/_index.es.md: heroBuilderUrl → /es/seo/, heroCasesUrl → /es/about/, offerItem8 убрал ссылку на старый конструктор. layouts/index.html: испанские подписи CTA → «Servicios SEO» / «Sobre nosotros», ES fallback → /es/seo/. EN/RU CTA не менялись.
- docs/retired-routes-en.txt: добавлен /es/constructor-estrategias-seo/. В .github/workflows/rebuild-qa.yml добавлен парсер generated ES HTML, проверяющий реальные URL, подписи и наличие страниц назначения. docs/research/2026-10-15-es-builder-retirement.md описывает SEO-решение и отсутствие live-редиректа.
- Файл контекста обновлён в том же коммите. GitHub Actions данного коммита ещё предстоит проверить; при найденных старых ссылках исправить конкретный источник. Исторический URL не получает 301/410 до live/GSC проверки. Страницы ES SEO/About остаются legacy и требуют последующего SERP/контент-аудита, не считать их готовыми.
- Далее: CI, затем по одной отключать RU/ES услуги Tier/сателлитов с сохранением честной тематической партнёрки на отдельных уместных страницах. Main/production/Pages без изменений. Строгий релизный gate BLOCKED.

### 2026-10-15 — RU legacy SEO Strategy Builder retired; homepage entry points corrected
- Предыдущий коммит e493ca97: GitHub Actions Hugo #38784891265 PASS, project context #38784891338 PASS. ES VPS CTA с корректным affiliate disclosure сохранена. Для всей сборки ранее 154 замечания; strict release gate не пройден.
- content/strategy-builder/index.ru.md для /ru/konstruktor-seo-strategii/: draft=false → true. Устаревший конструктор продвигал линкбилдинг/схемы; не подменяем его новой услугой с тем же URL.
- content/_index.ru.md: heroBuilderUrl → /ru/seo/, heroCasesUrl → /ru/about/, offerItem8 больше не направляет на старый инструмент. Это корректировка навигации, не полный SERP/контент-аудит RU главной; остальные старые коммерческие фрагменты пока остаются.
- layouts/index.html: тексты RU CTA согласованы с целями («SEO-услуги» и «О компании»); fallback для RU и EN уже снятых конструкторов не создаёт ссылки на /ru/konstruktor-seo-strategii/ и /seo-strategy-builder/. ES CTA/fallback на существующий ES конструктор пока не изменён, он следующий по очереди.
- docs/retired-routes-en.txt: добавлен /ru/konstruktor-seo-strategii/. .github/workflows/rebuild-qa.yml проверяет отсутствие HTML и ссылки, наличие целевых RU SEO/About страниц и правильную подпись CTA. docs/research/2026-10-15-ru-builder-retirement.md — миграционная оценка.
- GitHub Actions нового коммита необходимо подтвердить: при остаточной ссылке из шаблона/контента блокирующая проверка должна упасть. Никаких 301/410 на сервере; исходный main сохранён. Strict whitehat gate всё ещё BLOCKED. SERP_VERIFIED/visual QA для RU не проводились.
- Следующее действие: проверить CI и при необходимости устранить конкретные старые ссылки; затем отдельным коммитом отключить ES SEO Strategy Builder и исправить ES главную. После этого пройти RU/ES Tier и сателлиты постранично.

### 2026-10-15 — ES homepage: честная маркировка VPS-партнёрки
- Предыдущий RU homepage commit e8a32067: GitHub Actions Hugo build, RU generated copy guard и context guard PASS.
- В content/_index.es.md (homeJson) старый текст Hosting de red privada заменён на размещение сайтов/приложений, к VPS-карточке добавлено «enlace de afiliado». offerItem6 получил одну тематическую партнёрскую CTA и уточнение, что VPS не гарантирует индексацию/позиции Google.
- URL партнёра и код остались ровно прежними. Добавлен docs/research/2026-10-15-es-home-affiliate-audit.md; в .github/workflows/rebuild-qa.yml проверяется сгенерированный ES HTML.
- Это точечная корректировка старой ES главной, а НЕ полная локализация, не SERP top-10 и не visual QA; релизный gate всё ещё BLOCKED. Новые Actions требуют подтверждения, main/production/Pages не тронуты.
- Следующее: проверить CI и новый affiliate inventory, затем работать с RU/ES strategy-builder (старые серые рекомендации) и Tier/satellite страницами по одной, до постраничного SERP-аудита коммерческих страниц.

### 2026-10-15 — RU homepage: тематическая и прозрачная VPS-партнёрка
- Предыдущий commit cb1e4882: удалён static/ru/soft/index.html с ложным переходом на партнёрский VPS, original /go/vdsina/ сохранён. GitHub Actions build + retired URLs и context guard PASS.
- Правка ТОЛЬКО content/_index.ru.md (homeJson): изменены VPS-карточка и offerItem6. «Хостинг приватных сетей» заменён на обычное размещение сайтов, явно подписано «партнёрская ссылка», без утверждения, что VPS обязательно улучшает индексацию. Точное значение партнёрского URL и код оставлены прежними.
- В docs/research/2026-10-15-ru-home-affiliate-audit.md сохранён scope/evidence. В .github/workflows/rebuild-qa.yml добавлены проверки реально сгенерированной RU главной (текст, маркировка, отсутствие сетей и необоснованного SEO-обещания).
- Текущий коммит требует GitHub Actions проверки; visual QA и SERP RU НЕ проводились, RU homepage ещё содержит другие legacy тексты и не готова к релизу. ES homepage будет отдельным проходом, не подменять перевод автоматикой. Main и продакшен не менялись.
- Следующее: проверить Actions; затем аналогичная локальная правка ES homepage с disclosure и без gray/private-network and ranking claims. После этого разбирать gray strategy pages.

### 2026-10-15 — Удалён обманчивый статический /ru/soft/ redirect из кандидата
- Автоматический inventory #38783627099 PASS и context guard #38783627134 PASS для коммита 34f576b7. Сборка 58 HTML, 14 партнёрских ссылок на 9 страницах; 13 с JS-перехватом, 14 без disclosure непосредственно в тексте ссылки. Это не доказательство отсутствия disclosure в другом месте.
- Файл static/ru/soft/index.html являлся meta refresh + JS переходом /ru/soft/ → /go/vdsina/ с подписью Continue. Это нерелевантная подмена, не программный раздел; удалён ТОЛЬКО из белой рабочей ветки.
- В docs/retired-routes-en.txt добавлен /ru/soft/ (файл исторически назван EN, но CI может проверять любой URL). Добавлено исследование docs/research/2026-10-15-ru-soft-referral-retirement.md. Основной /go/vdsina/ и реферальный код сохранены.
- Нет изменений main, server, GitHub Pages или фактического production redirect. Новый GitHub Actions тест должен подтвердить отсутствие URL и входящих ссылок в generated site; без его результата не считать законченным.
- Другие размещения RU/ES страниц старых ссылочных схем и Tier в очереди; разумные VPS-ссылки будут сохранены с disclosure и rel.
- Следующее: проверить GitHub Actions, затем отдельно исправить раскрытие партнёрства на RU/ES homepage VPS-карточках и VPS-фрагментах; не переписывать остальные страницы без аудита.

### 2026-10-15 — Per-page affiliate link inventory introduced
- Previous commit 58fa3d43: Hugo build #38780153578 PASS and context guard #38780153599 PASS. The /go/vdsina/ affiliate endpoint remains as requested; no automatic /soft/ redirect rewrites remain.
- Discovered VDSina references in RU and ES homepages (card2 VPS and infrastructure text), RU strategy-builder banner, and default VDSina banner in the shared strategy-builder template. These are source-level candidates, NOT automatically approved placements or complete rendered enumeration.
- Added scripts/audit_affiliate_links.py to inspect all generated HTML anchors and report source URL, anchor label, rel sponsored/nofollow, cloaked target and potential misleading labels. Added docs/research/2026-10-15-affiliate-placement-inventory.md and a diagnostic step to .github/workflows/rebuild-qa.yml.
- No existing referral link, partner code or server redirect removed. The full strict sitewide gate still blocks unresolved placements and gray material, and this diagnostic does not change its decision. Main, live server and GitHub Pages untouched.
- This new commit requires its own Actions validation. Next: read exact affiliate report; for each relevant referral add visible disclosure, keep rel; retire misleading placements on gray or unrelated pages. Only then adjust final gate without blanket exemptions.

### 2026-10-15 — Уточнение политики партнёрских переходов: оставлять уместные
- Владелец прямо разрешил сохранять реферальные переходы, если они действительно относятся к содержанию страницы. Это исправляет прежнее чрезмерное правило безусловно удалять /go/vdsina/.
- Подтверждено в источниках: layouts/partials/affiliate-link-cloak.html заменял ссылки /soft/, /ru/soft/, /es/soft/ на партнёрский VPS; layouts/partials/affiliate-link-attrs.html делал те же URL alias к /go/vdsina/. Такие подмены вводят посетителя в заблуждение.
- Убраны только три подмены Soft в affiliate-link-cloak.html и их alias из affiliate-link-attrs.html. **Явный URL /go/vdsina/ и его статический redirect сохранены**, существующие явные партнёрские ссылки не удалялись и исходный партнёрский код не менялся.
- Обновлены docs/SEO_PAGE_WORKFLOW.md, docs/WHITE_HAT_RELEASE_READINESS.md и AGENTS.md: уместность, видимая пометка партнёрства, rel sponsored/nofollow, запрет скрытого hijack навигации. Добавлен проверочный шаг в .github/workflows/rebuild-qa.yml.
- Последний до правки коммит 969f7502: GitHub Actions Hugo/retired-route PASS и context guard PASS. CI текущего коммита предстоит подтвердить. Старый whitehat scanner пока блокирует /go/vdsina/ без контекстной проверки; не ослаблять его до отдельной allowlist/ссылочного аудита. Релиз BLOCKED, RU/ES остаются неочищенными. Main, сервер и Pages не затронуты.
- Следующее действие: проверить CI; затем инвентаризировать размещения /go/vdsina/ в видимых страницах, удалить нерелевантные CTA, подготовить строгую проверку тематических affiliate placements, оставляя сам endpoint.

### 2026-10-15 — Blank EN Software page excluded from Hugo
- Previous strategy builder change 113bf180: Hugo/retired routes QA and context guard PASS.
- Source content/soft/index.md: empty content section (one blank builder block, no real utility), draft:false -> true. Existing /soft/ added to docs/retired-routes-en.txt so CI checks it is not published or linked.
- Issue remains: layouts/partials/affiliate-link-attrs.html and affiliate-link-cloak.html can repurpose soft URLs as /go/vdsina/; static/go/vdsina/index.html remains. This is NOT solved by drafting the content page; specific separate template cleanup is next.
- No production redirects/410 done. New CI pending. Main, DNS and site server unchanged. EN/ES/RU tools require distinct legitimate service plans, not placeholder pages.
- Next: confirm CI and eliminate unrelated affiliate-alias behavior in shared templates and static endpoint with links audit.

### 2026-10-15 — Old English SEO Strategy Builder hidden from candidate
- Previous website-creation commit 5806f7de: Hugo/retired-routes #38778332743 PASS, context #38778332779 PASS. Diagnostic scanner: 167 findings in 35 of 60 HTML, versus earlier baseline 300 in 55 of 66. This is internal audit output, not a Google penalty measure.
- content/strategy-builder/index.md /seo-strategy-builder/: added draft: true to prevent the legacy strategy generator from publishing its old page while it remains based on unsuitable SEO practices. Existing script/template source stays available in main.
- Added /seo-strategy-builder/ to docs/retired-routes-en.txt for a blocking generated HTML/sitemap/link test. No live URL/status modification or deployment. RU/ES builder pages remain and need separate work.
- This commit's CI is pending. Future legitimate tool needs independent intent/SERP audit and real white-hat recommendations, not superficial wording changes.
- Next: verify CI then inspect EN /soft/ and legacy affiliate redirect separately; remove them only after route/reference review. Context and production rules unchanged.

### 2026-10-15 — EN website creation page temporarily disabled
- Previous 052a215d: build #38777959133 PASS; context guard #38777959083 PASS.
- Existing content/services/website-creation/index.md mixes ordinary website development with unrelated legacy services under /link-building-services/website-creation/. Changed only draft:false to true.
- Registered the candidate-disabled URL in docs/retired-routes-en.txt and documented the rationale in docs/research/2026-10-15-en-website-creation-review.md.
- Website development itself is not rejected. REVIEW_BUSINESS_OFFER remains; a separate authentic offer and SERP study must precede any new page and redirect. No changes to main or production; CI for new commit pending.
- Next: verify CI; audit old category, software and strategy-builder pages and internal links.

### 2026-10-15 — EN legacy microsite/satellite advertising page withdrawn
- Последний коммит Tier 76a82a6f: rebuild/retired route check и context guard завершились PASS в GitHub Actions. Production и main не тронуты.
- Аудит content/services/microsite-development/index.md: старый URL /link-building-services/microsite-development/ предлагал satellite websites, размещение бренда за ежемесячную оплату, передачу ссылочного авторитета и обещания Google Top. Это не эквивалент реальной заказной веб-разработки, а смешанное предложение, которое нельзя оставлять в white SEO.
- Страница переведена в draft: true, путь добавлен в docs/retired-routes-en.txt, обоснование в docs/research/2026-10-15-en-microsites-retirement.md. Не утверждаем, что самостоятельные microsites запрещены всегда.
- 301/410 на живом сервере НЕ сделаны. Реестр миграции содержит REVIEW_BEFORE_410 до получения GSC/live/backlink evidence. Возможную настоящую услугу website development проверять отдельно и под самостоятельный интент.
- QA этого коммита ещё ожидает GitHub Actions. RU/ES и другие legacy материалы всё ещё публикуются в candidate; strict gate не пройден.
- Следующее: проверить CI; затем раздельно проверить EN website creation (настоящая услуга или PBN) и old link-building section parents/soft/strategy builder, не менять main/production.

### 2026-10-15 — EN Tier 1–2–3 link networks withdrawn from Hugo
- GitHub Actions f2319734: rebuild + retired route check #38777434146 PASS; context guard #38777434159 PASS. Сервер и main неизменны.
- source content/services/tier-1-2-3/index.md for URL /link-building-services/tier-1-2-3/: changed draft: false → true. Карточки и ссылки, встроенные в эту уже закрытую публикацию, перестают генерироваться обычным Hugo.
- Добавлен URL в docs/retired-routes-en.txt для обязательной проверки неприсутствия в sitemap, HTML и внутренних ссылках. В миграционном реестре отмечен RETIRE_410 (только план для релиза, не live response).
- Данный коммит требует собственного Hugo QA + context guard; пока не заявлять полную очистку сайта, ES/RU и другие EN направления всё ещё legacy.
- Дальше: подтвердить Actions; исследовать EN /link-building-services/microsite-development/ на предмет реальной самостоятельной ценности (не автоматически считать все microsites неэтичными), затем принять KEEP/REWRITE/RETIRE с фиксацией.

### 2026-10-15 — EN Domain Rating page set to draft
- После проверки commit b0ca69fb: Hugo/retired URL QA #38777051315 PASS; context guard #38777051329 PASS.
- content/services/domain-rating/index.md: draft=false → true для /link-building-services/domain-rating/. Новое предложение услуг намеренно не включает повышение сторонних SEO-метрик.
- docs/retired-routes-en.txt дополнен старым URL, чтобы тестировать отсутствие HTML, sitemap и внутренних ссылок. Исходный main и действующий сайт не менялись; будущий HTTP 410 лишь предварительное решение, без GSC/live-аудита.
- Проверка этого изменения в Actions ещё не подтверждена; следующий шаг — подтвердить CI, затем по одной разобрать EN Tier 1-2-3 и связанные ссылки.

### 2026-10-15 — EN tiered link-building offer withdrawn from candidate
- Предыдущий коммит c5445d93: GitHub Actions rebuild #38776716307 PASS, context #38776715896 PASS. Автоматические подстановки серых карточек в общем services-hub исправлены, регрессионный retired-route тест подтверждён в CI.
- Обновлён content/services/link-building/index.md для старого URL /link-building-services/link-building/: draft:false → true и showOnHome:true → false. Страница продаёт tiered ссылочное продвижение, а не отдельную легитимную SEO-услугу; корректного same-intent преемника нет.
- Добавлен URL в docs/retired-routes-en.txt; регрессия проверяет отсутствие публикации, ссылок и sitemap. Отчёт docs/research/2026-10-15-en-link-building-retirement.md документирует обоснование и риски.
- Docs/seo-url-migration-register.csv уже содержит RETIRE_410 как ПРЕДЛОЖЕНИЕ; фактические live 404/410/301 НЕ выполнялись. GSC, referring links и визуальная проверка остаются pending.
- Новый Hugo build + retired-route QA и context guard требуют проверки GitHub Actions для этого коммита. Strict whitehat gate всё ещё BLOCKED из-за других старых URL, EN/RU/ES не опубликованы.
- Следующий шаг: проверить CI; затем та же поштучная процедура для EN /link-building-services/domain-rating/ с предотвращением ссылок на draft.

### 2026-10-15 — Защита от автоматически создаваемых ссылок на отключённые услуги
- Шаг текущего плана: проверка входящих ссылок на EN /link-building-services/backlinks/ (страница уже draft: true). В прямых ссылках новых EN content/_index.md, content/seo/index.md, content/services/_index.md, keyword-research, seo-consultation, hugo.toml и header.html точного URL не обнаружено; динамический шаблон services-hub.html формировал URL из текста/типа карточек и дополнительно самостоятельно вставлял Tier 1-2-3. Это системный дефект, независимо от отсутствия прямой строки в EN контенте.
- Изменён layouts/partials/services-hub.html: убраны выдуманные fallback URL backlink/DR/tier/link-building и принудительное добавление Tier/consultation карточек; карточка без явного корректного URL или корректной imageLink не выводится, URL кнопки имеет приоритет над ссылкой картинки. Не изменялись существующие URL реальных услуг. RU/ES устаревшие карточки с прямыми gray ссылками требуют отдельного прохода.
- Созданы scripts/verify_retired_routes.py и docs/retired-routes-en.txt (на данный момент только /link-building-services/backlinks/). Проверка анализирует все сгенерированные HTML, ссылки/динамические data URL, наличие физического HTML и sitemap. Добавлен отдельный блокирующий этап в .github/workflows/rebuild-qa.yml.
- Сборка Hugo и проверка контекста предыдущего коммита 0cb681d7 проверены PASS в Actions #38775570230 и #38775570803. Для текущего коммита новые Actions ещё требуется подтвердить; выполнение CI не гарантирует релизной готовности.
- Оставшиеся риски: другие старые EN страницы всё ещё рендерятся, RU/ES тоже; JS-ссылки вне указанных HTML-атрибутов, реальный browser QA, live статусы и GSC не проверены; strict whitehat gate BLOCKED. main и production не изменены.
- Следующее действие: проверить CI новых тестов, при найденных остатках разобраться с конкретными файлами; затем по одной выводить старые EN услуги /link-building-services/link-building/, domain-rating и tier-1-2-3 с учётом входящих ссылок и миграционного реестра.

### 2026-10-15 — Зафиксирован регламент постраничной SEO-переработки
- Создан docs/SEO_PAGE_WORKFLOW.md: утверждена последовательность baseline → удаление серых услуг EN → переработка EN → RU → ES → полный QA → отдельное разрешение релиза. В него входят реальная проверка SERP top-10 с гео/датой, межстраничная каннибализация, содержательные требования и stop-gates.
- AGENTS.md дополнен обязательным чтением регламента. Важное разграничение: успешный Hugo/CI не является свидетельством качественного SEO, готовности к релизу или отсутствия старых промо.
- Проверено GitHub Actions по предыдущему коммиту e8d81a0a: rebuild QA #38774652226 PASS; context guard #38774652215 PASS. Полный strict whitehat content gate не пройден.
- Сайт, шаблоны, main и сервер не менялись; добавлена только документация процесса.
- Проверка этого коммита в GitHub Actions будет доступна после push; следующий конкретный шаг — найти/устранить внутренние ссылки EN на уже выключенную /link-building-services/backlinks/, затем другие EN legacy направления.

### 2026-10-15 — EN массовое размещение backlinks исключено из Hugo (первая legacy-страница)
- Предшествующие GitHub Actions: rebuild #38774047519 PASS, context guard #38774047402 PASS. Эти PASS не означают готовности к релизу.
- Файл content/services/backlinks/index.md: исключительно `draft: false` заменено на `draft: true`. Страница /link-building-services/backlinks/ должна перестать генерироваться Hugo и попадать в sitemap; источник остаётся для учёта миграции, main не изменён.
- Причина: продажа массовых ссылок для ранжирования. В реестре миграции кандидат RETIRE_410, НЕ реальная 410 на сервере. Никакого нерелевантного редиректа на /services/ или главную.
- Риски: старые внутренние ссылки на URL могут оставаться; полный strict gate всё ещё заблокирован. Проверки нового коммита Hugo/Actions ещё не подтверждены.
- Следующее: проверить CI, отключать прочие EN серые услуги отдельно с проверкой ссылок; RU/ES потом.

### 2026-10-15 — Global RU/ES menus and language-switcher cleanup
- Whole-site audit GitHub Actions #38774047519: Hugo and individual EN page QA PASS; informational scanner found 300 issues across 55 of 66 HTML (195 legacy nav, 29 old public routes, 75 visible-text flags, 1 affiliate endpoint). RELEASE READINESS BLOCKED; this is baseline, not ranking penalty evidence.
- Edited hugo.toml: removed ES/RU menu items naming link building and empty software, introduced clean localized SEO links /es/seo/, /ru/seo/.
- Edited layouts/partials/header.html: removed hardcoded old-language URL exceptions and forced fallback to legacy link-building hubs; untranslated languages now fall back to respective locale home instead.
- Added docs/research/2026-10-15-global-menu-cleanup.md with evidence and limitations; improved build QA to inspect localized primary navigation.
- Not yet ready: old RU/ES SEO pages and homes are still original, as are gray service pages; scanner will continue BLOCKED. Production and main untouched.
- Next: verify localized nav QA, then retire or rewrite legacy public pages and draft empty software/strategy builder by language; avoid redirecting unrelated content.

### 2026-10-15 — Sitewide release-readiness blocker scanner
- FAQ QA #38773548639 PASS и контекст #38773548616 PASS. Все изменения только white-seo-rebuild.
- Добавлен scripts/whitehat_content_gate.py: сканирует generated HTML EN/RU/ES, sitemap и навигацию на старые ссылки, услуги ссылочного продвижения, PBN, Tier/DR, инструмент-автоматизацию, рефералку VPS. В режиме --strict статус ошибки блокирует релиз.
- Добавлен docs/WHITE_HAT_RELEASE_READINESS.md с обязательными этапами: замена/удаление старых услуг, безопасная миграция URL, локализация, QA.
- Изменён .github/workflows/rebuild-qa.yml: шаг информативного sitewide-сканирования выводит BLOCKED при обнаружении остатков, но НЕ падает специально до завершения процесса. Сам успешный build НЕ ОЗНАЧАЕТ возможность публикации.
- Полный строгий gate и live/GSC/browser QA пока не пройдены; ожидаем старые услуги в EN/RU/ES, /soft/, /seo-strategy-builder/, /go/vdsina/.
- Следующее действие: проверить Actions и его список блокирующих страниц, затем начать обезвреживание старых публичных материалов по отдельным страницам с фиксацией будущего 301/410 и без live-сервера.

### 2026-10-15 — EN FAQ rewritten for buyer questions, trust and accuracy
- Previous About QA #38773315827 PASS, context guard #38773315866 PASS. Server untouched.
- Rewritten content/faq/index.md: preserved /faq/, unique Title/H1 «SEO Services FAQ» and meta; 13 real service questions including audit vs keyword research, GSC, migration, measured outcomes, timelines, scope and languages.
- Removed unsupported expectations for quick rankings; added direct internal links to legitimate white SEO pages and contacts.
- Added docs/research/2026-10-15-en-faq-intent.md: FAQ is a brand/support page, does not cannibalize specific commercial SEO pages, no fake SERP rank claim.
- Extended .github/workflows/rebuild-qa.yml with FAQ content/links/canonical/H1 checks; need confirm new Actions result.
- EN source areas still contain gray legacy pages and strategy builder; RU/ES not rebuilt; working branch not ready to publish.
- Next: sitewide risk inventory of legacy EN/RU/ES URLs, templates and visible navigation; resolve gray service pages as retired or draft in working branch after recording candidate mapping.

### 2026-10-15 — EN About SEOImpuls authenticity and trust rewrite
- Working branch white-seo-rebuild; consultation QA #38772846555 PASS, context guard #38772846622 PASS.
- Reworked content/about/index.md: About SEOImpuls H1, factual methods, boundaries, technical SEO, keyword research, content, consultation, evidence standards and contact.
- Removed unverified current ratings and aggregate Kwork numbers and historical link-service promotion from EN About; avoided inventing cases or generic claims about client results. Kept original /about/ URL and translationKey.
- New docs/research/2026-10-15-en-about-trust-audit.md records prior-claim risk and brand-intent ownership. No fake claim of generic query top-10 relevance.
- Expanded .github/workflows/rebuild-qa.yml H1/canonical/clean content/service links/anchors About checks; verify this commit in Actions.
- RU/ES remain legacy; server, DNS, production and main untouched.
- Next: confirm CI then replace thin EN FAQ and begin global audit for legacy gray URLs across all locales.

### 2026-10-15 — EN SEO consultation rebuilt and added to services catalog
- Working branch white-seo-rebuild; /services/ QA #38772264988 PASS, context guard #38772264795 PASS. Production unchanged.
- Rewritten content/services/seo-consultation/index.md: title/H1 «SEO Consultation & Strategy Review»; unique URL /services/seo-consultation/; prep, diagnostics topics, session boundaries, deliverables/outcomes, FAQ, contacts. Retained legacy published $350 and around three hours as reference terms to confirm; removed unverified lifetime support/case claims and link-building topics.
- Updated content/services/_index.md: third clean commercial card for consultation, new summary and corrected meta description.
- Updated docs/research/2026-10-15-en-services-catalog-intent.md and new docs/research/2026-10-15-en-seo-consultation-intent.md with intent ownership, ten comparison examples (not verified exact Google first-10), migration notes.
- Expanded .github/workflows/rebuild-qa.yml to verify consultation H1/canonical/anchors, no prohibited claims, /services/ directory link. New QA run pending.
- MAIN and production untouched; legacy consultation URL redirect not implemented, old gray pages still exist. Do not publish before full migration and multi-language audit.
- Next: check QA and context Actions; then audit/decommission legacy gray EN pages and all internal links without accidentally redirecting unrelated content.

### 2026-10-15 — Clean EN /services/ catalog and resolve keyword breadcrumb
- Предыдущий QA #38771883235: Hugo build PASS, SEO проверка keyword research FAIL из-за видимой надписи «Link Building Services». Причина: breadcrumb наследовал старый Title раздела services. Контекст guard #38771883177 PASS.
- Переделан content/services/_index.md: URL /services/, Title/H1 «SEO Services & Practical Deliverables», две реально легитимные услуги (technical SEO и keyword research), без backlink/DR/tier/satellites и негативных старых карточек.
- Изменено меню EN в hugo.toml: Services → /services/, Technical SEO → /seo/. Другие языки ещё в оригинальном состоянии.
- Добавлено исследование разделения запросов и архитектуры docs/research/2026-10-15-en-services-catalog-intent.md. Новый каталог намеренно навигационный, не дублирует подробную /seo/.
- QA workflow расширен на /services/ H1/canonical и проверку чистого breadcrumb у keyword research; новый запуск требуется подтвердить.
- Старый /link-building-services/ не перенаправляли: 301 в данном случае может быть нерелевантен, решение после GSC. Production не изменён.
- Следующее: проверить CI, далее SEO Consultation EN /services/seo-consultation/ и после этого добавить её в каталог с контекстом.

### 2026-10-15 — EN keyword research genuine SEO service page
- Ветка white-seo-rebuild. Страницы / и /seo/ ранее успешно прошли GitHub Actions, без деплоя.
- Переработан content/services/keyword-research/index.md: H1/Title Keyword Research & Search Intent Mapping; новый URL /services/keyword-research/, от старого /link-building-services/keyword-research/ нужен будущий релевантный 301 при отдельном разрешении.
- Реальные коммерческие интенты: query research, clustering, intent mapping, URL assignments, content gaps, deliverables, FAQ, условия и контакты. Цена $90 сохранена из существующего исходного предложения, без вымышленных сроков и объемов.
- SERP reference/intent study: docs/research/2026-10-15-en-keyword-research-intent.md, 10 примеров не являются точным Google top-10 по одному региону.
- Дополнены тесты Hugo и SEO в .github/workflows/rebuild-qa.yml; текущая QA требует проверки Actions. Изменения в main, сервере и GitHub Pages отсутствуют.
- ВАЖНО: каталог /services/ ещё не создан, старый /link-building-services/ содержит старые ссылки, ES/RU требуют миграции. Рабочая ветка пока не является готовой публикацией.
- Следующее действие: QA нового URL; создание корректного /services/ каталога и EN SEO консультации, чтобы устранить зависимость от старого линкбилдинг-раздела.

### 2026-10-15 — Inventory of legacy commercial URLs and provisional migration decisions
- /seo/ QA #38771057820 PASS; контекст #38771057945 PASS. Сайт на сервере не изменён.
- Созданы docs/seo-url-migration-register.csv (27 legacy коммерческих URL из Hugo content/services EN/RU/ES) и docs/SEO_URL_MIGRATION_POLICY.md с кандидатами 301, 404/410 или ручной бизнес-проверки.
- Это ПЛАН, а не применённые редиректы. GSC-данных о показах/кликах и реальных внешних ссылках ещё нет; окончательный статус каждого URL не подтверждён.
- Условие: 301 только для реального тематического преемника; серые услуги не маскировать и не вести на главную; при удалении проверять sitemap, canonical, hreflang, внутренние ссылки.
- Следующее действие: работа над законными коммерческими услугами (keyword research, consultation) и выделение чистого каталога /services/ без каннибализации / и /seo/; сначала SERP и проверка функционального предложения.

### 2026-10-15 — EN /seo/ deep rewrite
- Ветка: white-seo-rebuild. Homepage QA #38770565895 PASS; context guard #38770566048 PASS. Сервер не затронут.
- Изменён content/seo/index.md: новый уникальный H1/Title «Technical SEO Services & Audits», meta, сохранён исходный URL /seo/ и responsive template design=seo-overview.
- Удалены из новой EN страницы CTA на link-building, старые недоказанные обещания и расплывчатые тематические блоки. Добавлены технический аудит, on-page SEO, семантика, международное SEO, процесс, результаты работ, FAQ и проверяемые контакты.
- Исследование и разграничение интентов сохранены в docs/research/2026-10-15-en-seo-services-intent.md. Данные конкурентных примеров — не подтверждённый точный Google SERP top-10 одного региона.
- Обновлён .github/workflows/rebuild-qa.yml с проверками /seo/ H1, якорных разделов, устаревших ссылок и терминов. Новый Actions run ещё должен подтвердить build.
- Не публиковать сайт: остальные старые услуги, footer/soft, RU/ES и глобальная архитектура требуют очистки, карта 301/410 не готова.
- Следующий шаг: проверить Actions; затем детально разобрать старые коммерческие услуги и URL-mapping без редиректов на нерелевантную главную.

### 2026-10-15 — QA first run and HTML parser fix
- GitHub Actions #38770346654: Hugo EN/RU/ES/sitemap build PASS, homepage automated text/H1/link assertions reached process-anchor check, which failed with «SEO process anchor missing».
- Причина проверки: тест использовал поиск точной строки id="how-it-works" по минифицированному HTML. Hugo HTML minifier может убирать кавычки в безопасных атрибутах; такая проверка неустойчива.
- В .github/workflows/rebuild-qa.yml id атрибут теперь проверяется через HTMLParser, а не совпадение строки. EN homepage не изменялась; это исправление только QA.
- Context-guard #38770346469 PASS.
- Следующий шаг: дождаться нового rebuild-qa, проверить canonical и фактическое содержание output; если ошибки повторятся, документировать и исправить.

### 2026-10-15 — EN homepage: commercial-intent and white SEO rebuild
- Рабочая ветка: white-seo-rebuild. Main остаётся исходным эталоном.
- Зафиксирован успешный GitHub Actions импорт #38768910498: ZIP SHA проверен, Hugo EN/RU/ES/sitemap PASS, файлы доступны в main, ZIP удалён.
- Документирован конкурентный ориентир из 10 релевантных англоязычных страниц: docs/research/2026-10-15-en-home-serp-intent.md. Это выборка, не подтверждённый точный Google top-10 одного региона.
- Файлы: content/_index.md, layouts/index.html, hugo.toml. EN главная переписана под SEO Services; удалена из видимой EN версии ссылка на VPS и продвижение backlinks/DR, вместо фальшивой новости теперь реальный процесс, исправлены EN услуги меню и CTA.
- Добавлена .github/workflows/rebuild-qa.yml (только проверка, без публикации), проверяющая Hugo, три главные, sitemap и английский H1, canonical, старый контент и CTA.
- ПРОВЕРКИ: до завершения нового Actions workflow не заявлять, что обновлённая главная прошла build и UX-QA; необходимо проверить в Actions.
- НЕ ГОТОВО к публикации: /seo/ и другие EN-услуги, RU/ES, footer, устаревшие URL, реальный SERP geo-specific, responsive/visual проверки.
- Следующий шаг: проверить Actions и HTML EN главной; затем провести аудит и переработку EN /seo/, не трогая продакшн.

### 2026-10-15 16:26 UTC — Verified source import via GitHub Actions
- Uploaded ZIP matched the recorded SHA-256; files extracted into main.
- Hugo --minify build completed with EN/RU/ES homepage and sitemap checks.
- Source archive removed from repository in this commit; no GitHub Pages and no production deployment.
- Working branch white-seo-rebuild will be created from this imported commit.
- Next: check main file tree and working branch; then begin inventory and intent map.

### 2026-10-15 — Исправление импорта после первого запуска Actions
- Первый запуск Actions #38768517453: SHA ZIP OK, распаковка OK, Hugo build (EN/RU/ES/sitemap) OK, Git push FAILED.
- Подтверждённая причина: GITHUB_TOKEN отклонил запись `.github/workflows/build-check.yml` из архива (workflow permission). Ветка white-seo-rebuild ещё не существует; main пока содержит исходный ZIP.
- Изменён .github/workflows/import-source.yml: старые workflow архивируются в docs/legacy-workflows/ (не активируются), триггер расширен на изменение самого импортного workflow, чтобы повторить запуск при этом коммите.
- Обновлена запись контекста в том же коммите. Prod сервер и публикация GitHub Pages не затронуты.
- Дальше: проверить новый Actions run, наличие content/layouts в main и рабочей ветки; только после подтверждения начать white-hat переписывание.

### 2026-10-15 — Добавлена автоматическая проверка журнала изменений
- Создан workflow .github/workflows/context-guard.yml: для каждого нового коммита в white-seo-rebuild проверяется наличие изменения CHATGPT_PROJECT_CONTEXT.md в том же коммите.
- Workflow сигнализирует об ошибке в Actions при нарушении правила; он не заменяет защиту ветки GitHub и сам по себе не блокирует все прямые push.
- Изменения в сайт не вносились; источник всё ещё ожидает импорт.

### 2026-10-15 — Инициализация правил восстановления
- Создан приватный пустой репозиторий agurkin2021-gif/seoimpuls с README.md.
- Зафиксирован обязательный контекст-файл и инструкции для последующих чатов.
- Подготовлен workflow безопасного импорта проекта из ZIP. Сайт на сервере не изменён.
- Проверен локально подготовленный ZIP: 2886 файлов, повреждений ZIP не обнаружено, SHA-256 указан выше.
- На момент этого коммита ИСХОДНИКИ В GITHUB ЕЩЁ НЕ ЗАГРУЖЕНЫ. Не считать проект готовым к редактированию или публикации.
- Следующий этап: загрузка ZIP и успешный импорт GitHub Actions.

## 6. Следующее действие

**OWNER OVERRIDE 2026-10-16:** CSS-only EN service marks require new technical + 390/768/1280 visual acceptance. No switch to another page automatically; no legacy service image reuse on the home cards. Earlier instructions below are historical.


**LATEST ACCEPTANCE 2026-10-16:** EN main and exact-keyword three direct service URL architecture is code/visual QA PASS in new candidate; owner review pending, production untouched. Do not begin any other page without owner command. Prior NEXT notes superseded.


**LATEST 2026-10-16:** finish direct 3 services on EN homepage and exact URL↔Title↔H1 alignment; validate strict Hugo, preview, browser, sitemap/hreflang and record actual run results. Older NEXT entries superseded.


**ACTIVE 2026-10-16:** EN /seo-services/ has passed code/visual QA but remains owner-review-pending. Do not start another page automatically. Historical NEXT lines below are superseded.


**2026-10-16 CURRENT OVERRIDE:** EN /seo-services/ only; test new simplified 3 primary + 2 supplemental + zero duplicate selector source. Do not start or modify any other page automatically.


**OWNER-LOCK OVERRIDE (2026-10-16): EN /seo-services/ only. Newly edited business-friendly service names and cards need Hugo/strict, Pages preview and browser 390/768/1280 QA, then owner acceptance. Never switch page automatically. Older NEXT instructions below are superseded.**


**OVERRIDE 2026-10-16:** ONLY /seo-services/ has active edit permission; reopened for UX simplification of 23 confusing workstreams. Follow docs/plans/EN_SEO_SERVICES_SIMPLIFICATION_PLAN.md. Do not move to /seo/ or other pages unless the OWNER issues a separate command, even after QA passes. All older NEXT instructions below are historical and superseded.


**CURRENT GREENFIELD (2026-10-16):** По новому прямому распоряжению владельца сайт пересобирается с нуля, без зависимости от трафика, GSC, старых URL и legacy redirect preflight. Уже созданные новая EN главная и каталог `/seo-services/` сохраняются. Очередной EN объект — `/seo/`: SERP-first → intent isolation → on-page/schema → Hugo/strict/390-768-1280 QA. Исторический фокус ONLY `/seo-services/` ниже более не действует. Продакшен не трогать.

**HISTORICAL BELOW (superseded owner direction):**


**CURRENT (2026-10-16, corrected by owner): ONLY EN `/seo-services/` is in scope. `docs/plans/EN_SEO_SERVICES_FINISH_PLAN.md` steps 0–7 DONE. Continue evidence-backed read-only review; do not redo accepted work without a verified new defect. `/seo/` work and its plan are NOT active. Release remains blocked on GSC/history, redirect policy, RU/ES equivalence, real client authorization and a separate production decision. Freeze homepage, `/seo/`, other EN pages, RU/ES, `main`, production.**

SOURCE OF TRUTH: `docs/plans/EN_SEO_SERVICES_FINISH_PLAN.md` and this context in `white-seo-rebuild`. Owner instructed finish EN `/seo-services/` only, **work sequentially and update both documents in each commit**. Current plan: STEP 0 DONE, STEP 1 DONE (63f39bb, strict/Pages/Playwright 390/768/1280 all PASS). STEP 2 DONE — source 30e1c72, Hugo/Pages/Playwright 390/768/1280 passed, 23 entry matrix and 3/14/6 visible labels verified; STEP 3 DONE — honest first-party QA report verified in live-browser artifact; real customer evidence remains BLOCKED_EXTERNAL. STEP 4 DONE — three existing specialist routes + 20 topic-specific email enquiries all pass strict/Pages/Chrome 390/768/1280. STEP 5 AUDIT_DONE — read-only RU/ES relation matrix, translation parity partial, future multilingual work BLOCKED_EXTERNAL. STEP 6 DONE — source ad90cbd passed strict #38888649717, Pages #38888649363, Chrome #38888649421 and context #38888649376; 768px icons 2/overlaps 0. STEP 7 DONE — decision record docs/research/2026-10-16-en-services-final-qa.md. Page CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / RELEASE_BLOCKED. No next service-page action until separate owner decision and external evidence. Do not claim proof without evidence. Do not touch main, EN homepage or sibling service pages, RU/ES content or live server.

Current last-proven site: `3878934` plus record `1791892`, strict/Pages/390-1280 PASS, 23 workstreams/4 groups/3 deep links; title `SEO Audits, Keyword Research & Consulting | SeoImpuls`, H1 `Choose the Right SEO Work for Your Website`, canonical `/seo-services/`. Preview noindex; live site not changed. Plan Step 1 code changes, once committed, are **EDITED_QA_PENDING** until CI finishes. External release blocks: GSC and incoming link history, production 301/410 decisions, real proof/customer permission and owner production approval.

## 7. Формат обязательной записи после КАЖДОЙ правки

Дата / ветка / commit SHA (после коммита) / затронутые файлы и URL / причина и SEO-интент / выполненные изменения / проверки и конкретные результаты / известные риски и нерешённые задачи / точный следующий шаг. Каждую новую запись ставить первой в разделе 5; синхронизировать IMPORT_STATUS и «Следующее действие». При незавершённой задаче явно указывать статус, не подменять его словами «готово».
