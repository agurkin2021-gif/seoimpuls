# SEOImpuls: English direct service architecture
Date: 2026-10-16. STATUS: EDITED_QA_PENDING / OWNER_REVIEW_PENDING for new simplified EN homepage; no production deployment. Branch: white-seo-rebuild.

## Decision
- Remove English intermediary service catalogue /seo-services/ from the new generated site. The English homepage owns choosing an SEO service.
- Services menu and hero CTA use /#services, leading to three direct links.
- Three genuine service pages only; preserve original assets, service details and honest terms.
- Remove unnecessary English /services/ prefix and vague /seo/ slug. Make primary search phrase appear exactly in EN URL, HTML Title and H1.
- Do not create another indexed English services overview.

## Exact English keyword/URL ownership
Homepage: / ; H1 Professional SEO Services ; HTML Title Professional SEO Services | SeoImpuls.
Technical SEO audit: /technical-seo-audit/ ; H1 Technical SEO Audit ; HTML Title Technical SEO Audit | SeoImpuls.
Keyword research: /keyword-research/ ; H1 Keyword Research ; HTML Title Keyword Research | SeoImpuls.
SEO consultation: /seo-consultation/ ; H1 SEO Consultation ; HTML Title SEO Consultation | SeoImpuls.

The phrase technical seo audit is more specific to the existing diagnostic service than technical seo services. Available competitor/SERP examples establish the phrase is used in commercial pages, not Google search volume, difficulty or ranking.

## Dependency and safety rules
- Previous EN /seo-services/, /seo/, /services/, /services/keyword-research/ and /services/seo-consultation/ should not be generated in the new candidate or internally linked; mark them retired for candidate build. Production redirects are not authorized by this task.
- The EN hub content is retained as a Hugo draft, not deleted from Git history. RU/ES service directories remain unmodified and may still be localized pages.
- Hreflang on RU/ES technical, keyword and consulting translations must point to the new EN canonical URLs; no broken EN alternates for retired EN hub.
- EN service structured data must be WebPage instead of incorrect BlogPosting. Unrelated articles continue to use original schema.
- Keep English homepage main intent distinct from technical audit, keyword discovery and consultation. Do not invent sales, client cases, price guarantees or rankings.

## QA gates
1. Hugo build, title/H1/canonical/OG/robots exact, correct 3 EN URLs, old URLs absent from generated sitemap/links.
2. Strict white-hat gate, updated context guard, RU/ES unchanged source, reciprocal hreflang, preview noindex.
3. Real Chrome viewport checks 390/768/1280: 3 direct links, anchor menu/CTA and keyboard, images, no overlap from floating WhatsApp/Telegram, no broken routes/network/JS/overflow.
4. Inspect screenshots, record workflow runs and true outcomes in context. Separate owner acceptance and production authorization.

All gates PENDING until this current source is committed and tested. Do not proceed to other pages automatically.

## 2026-10-16 — First Actions QA diagnosis (not acceptance)
- Commit 3289214 Hugo compilation and new three route/title/H1/meta/schema/hreflang checks passed.
- Strict/Pages stopped on a test-only false expectation for "keyword-research" anchor ID; existing keyword page uses what-is-included, methodology, deliverables. Browser workflow readiness requested retired hub URL; changed readiness to homepage.
- Follow-up full strict/preview/browser evidence still needed. No code source modifications in test correction; no claim that all gates passed.

## 2026-10-16 — First real browser and preview corrections
- Strict #38909786931 reached retired-route gate after successful 3 EN commercial tests but reported RU/ES header language-switch links pointing to removed English hub. The localized sources stay intact; shared header conditional EN destination now uses /#services for those two hub pages only.
- Preview #38909786575 route verifier treated its preview canonical as seoimpuls.com, a false assertion; updated verifier allows exact production or GitHub Pages preview origin and checks each new route/hreflang against active build baseURL.
- Browser #38909786373 checks 390 and 1280 PASS, but 768 flagged fixed Whatsapp overlapping text; screenshots #12049059512 inspected. EN homepage reserves 64px left gutter from 768 to 1199 for hero, service, definition and other content blocks; floating icons unchanged.
- New QA runs required to prove corrections; prior production-base checks did not finish full strict release gate.

## 2026-10-16 — Responsive 768px and final whitehat assertions
- Production-base Hugo and all 3 new URL/H1/Title/schema/hreflang + retired-path gate passed in strict #38910447930. Last downstream text assertion incorrectly expected prior homepage wording; replaced with approved business-oriented explanatory phrases. Localized menu assertions restored to existing /ru/seo/, /es/seo/.
- Pages #38910447841 PASS, responsive home #38910447974 PASS, axe automated #38910447779 PASS. Direct service browser #38910448011 only failed on 768 floating icons (390 and 1280 succeeded).
- Screenshot #12050445799 showed exact breakpoint conflict (768 mobile footer appears at page top despite desktop fixed icons), corrected by an EN-home-only floating footer override at exactly 768. Browser collision check remains enabled, now includes rect coordinates.
- Follow-up CI unverified until the next Actions run; no production changes.

## 2026-10-16 — Visual review overrides initial automated acceptance
- Strict #38911153927 PASS; preview #38911153919 PASS; direct service browser #38911154181 PASS at 390/768/1280; general home browser #38911153939 PASS; axe WCAG #38911154116 PASS; but screenshots #12049823824 reveal fixed left WA/TG icons on top of the beginning of the below-cards text at 1280 (not caught by card-only collision test).
- EN-only content gutter (padding-left:64px) widened to apply at all widths >=768, not just tablets. Existing fixed WA/TG UI itself is unchanged. EN dedicated browser guard strengthened to check collision rectangles of the ENTIRE .seo-central--en text, not just the service-card text.
- Therefore prior checks do not constitute complete visual acceptance; source revision QA pending. Keep the EN route naming/Title/H1 solution already confirmed by page code checks.

## 2026-10-16 — Measured icon motion, corrected rail
- Strict/Pages/home/a11y passed prior 64px iteration but enhanced 3-viewport browser #38911716000 found moving fixed WA/TG icons at x32..92, intersecting body text starting x64. This is a visible timing-dependent collision, not a false-positive QA.
- Changed only EN homepage CSS reserved rail to 120px for widths >=768, with at least 28px clearance from measured icon bound. Footer icons, animation, other pages and locales remain unchanged.
- New strict/Pages/browser/screenshot QA must pass. Old success does not prove this new layout.

## 2026-10-16 — Final acceptance evidence of exact keyword routes
- Final source commit 833cb99. EN /technical-seo-audit/, /keyword-research/, /seo-consultation/ are built with exact slug ↔ Title ↔ H1; homepage /#services contains 3 direct linked service cards. Old EN hub and service URLs omitted, corrected RU/ES href/hreflang, accurate WebPage schema. NO changes to production.
- Strict #38912159752 PASS; Pages Preview #38912159880 PASS, context guard #38912159761 PASS, direct services Chromium #38912159784 PASS 390/768/1280; broader home visual #38912159853 PASS; axe-core WCAG automated #38912159768 PASS.
- Browser reports 0 old intermediate URLs, 0 broken local routes, JS/network errors, 0 horizontal overflow. Floating Telegram/WhatsApp collision bounds tested against entire homepage text: 0 on all tested widths. Services anchor not covered by header. Screenshots #12050378578 downloaded and reviewed at 390,768,1280; accepted appearance with 120px EN rail on >=768px only.
- These checks do not establish keyword volumes, rankings, live CrUX or full manual WCAG conformance. Site release and new pages require separate owner instruction. Keep no automatic migration or server changes.

## 2026-10-16 — Owner image directive and lightweight responsive layout
- The three EN homepage service cards must not display older SVG/raster illustrations. Their existing source assets remain preserved for future explicit owner decisions; the site's brand logo and unrelated images remain unchanged.
- Created custom CSS-only 01/02/03 indicators in the cards, with responsive sizes, tasteful borders and gradients, accessible decorative markup and reduced-motion support. No new graphical dependencies or network requests.
- No changes to keywords, exact EN service slugs, Title/H1, canonical/hreflang, three card links, or established 120px left rail reserved for fixed WhatsApp/Telegram controls.
- EN-only source `layouts/index.html` and focused checks `scripts/verify_en_services_route.py`/`scripts/audit_en_services_browser.cjs`; same-commit documentation. RU/ES icon rendering remains as before.
- New static and browser checks require exactly three CSS marks, zero `img` inside EN service cards, size and shape checks, no broken links/overflow or contact overlap. QA pending: Hugo strict + preview + Playwright 390/768/1280 screenshots. Old green runs are historical.
- No automatic work on any other page or production without a separate direct instruction.

## 2026-10-16 — First responsive mark QA failure and correction
- Source 5d5c281 full Hugo #38913678211, Pages #38913678395, general homepage visual #38913678362, axe #38913678269 and context #38913678442 passed. Dedicated CSS-card Chrome #38913678415 exposed marker width collapse at all widths (390=20.8x38; 768=18.4x38; 1280=22.3x46). All card image requests zero, routes/floating contacts had no failures.
- Corrected only EN CSS grid child dimensions to fixed responsive `clamp(38px,4vw,46px)` width and height. This new commit requires a fresh dedicated Chrome PASS and screenshot inspection before acceptance.

## 2026-10-16 — Acceptance of final image-free EN homepage service cards
- Source `00881d5`; strict #38914027341 PASS, preview #38914027471 PASS, context #38914027698 PASS, general home visual #38914027575 PASS, automated axe WCAG check #38914027393 PASS, dedicated Chrome three widths #38914027320 PASS.
- Measured 390/768/1280 CSS-only markers exactly 38×38, 38×38, 46×46px. Card images zero; original icon files remain in Git unchanged. No broken service URLs, fixed contact overlap, scripts/network errors, overflow or hidden anchor.
- Screenshots from artifact #12052215561 manually inspected for all three widths; visual acceptance limited to these screenshots and browser automation, not formal accessibility certification.
- Owner still needs to approve page and future image use. Do not deploy production or pivot to another page automatically.

## 2026-10-16 — EN homepage eight supplementary work tiles simplified per owner
- Immediate owner priority: remove eight competing-looking work tiles and rewrite client text for non-SEO business owners, including businesses without a website.
- Three direct service offers stay /technical-seo-audit/, /keyword-research/, /seo-consultation/. All existing CSS-only numbered service cards intact.
- EN scope title `Other SEO Work We Can Discuss` with exactly 3 plain brief lines (competitor research; page/content improvements; agreed fixes and follow-up). These are examples, NOT 3 more purchasable products. The old decorative SVG disappears from EN markup only; original asset remains and RU/ES retain all legacy-scope rows.
- Home description, definition, deliverables, FAQ/pricing, contact CTA revised; audit only for existing websites, keyword collection even with no site, consultation spoken advice doesn't automatically include a written action plan. No invented guarantee or testimonial.
- EN-only compact scope list CSS; URL, H1, Title, canonical/schema/hreflang and global footer unchanged. All new content locked by static/browser/sitewide CI.
- QA PENDING on this source. Perform strict Hugo, Pages/noindex, Chrome 390/768/1280, visual and automated accessibility; inspect screenshots. No other page or production changes.

## 2026-10-16 — Correct static count after Hugo minification
- Source content commit 755e52d compiled, browser/visual/a11y passed (#38918077643/#38918077646/#38918077640) but strict #38918077584 and preview #38918077632 failed at *test-only* counting of quoted `data-home-field="offerItem..."` attributes in minified HTML.
- The correct business contract is unchanged: 3 and only 3 supporting-work items. Static and CI counters now inspect real parsed LI attributes via HTMLParser, independent of whether Hugo includes quote characters.
- No change to actual site source in this commit; fresh strict/preview green and manual screenshots required for validation.

## 2026-10-16 — Downstream full-site copy assertion
- Strict run #38918491957 passed new HTMLParser scope validation, then detected stale expected literal phrase from old homepage definition, while new source retains stronger explicit buyer benefits. Adjusted two expected strings, still require SEO service definition, no-site keyword research and separate website implementation. Site source unchanged from 755e52d; re-run strict and preview.

## 2026-10-16 — Acceptance: eight supporting tiles condensed to three and business-facing copy
- **Source** `755e52d`: replaced eight 'What Our SEO Services Cover' near-products with 3 compact optional, descriptive lines: competitor research; page/content improvements; fixes/follow-up. Extra work clearly optional and agreed separately. Exactly 3 main service cards/URLs continue; no new service URL or image dependency.
- Rewritten SEO description, result definitions, standalone keyword research spreadsheet/no-website entry path, price/timing FAQ and business-project CTA. Consultation explicitly doesn't promise written plan without separate agreement. No false case studies, prices or ranking guarantees.
- Strict+preview+context `50965ff`: #38918895547/#38918895213/#38918895395 all PASS (no site source change in two intervening CI-only commits). Chromium source #38918077643 on 390/768/1280 PASS, #38918077646 home visual PASS and #38918077640 axe automation PASS.
- Screenshot artifact #12054026326 downloaded and manually reviewed: 390/768/1280 layout of 3 secondary explanatory lines and service cards is legible, no new breakage observed. No field CWV, no guaranteed rankings, no full manual WCAG certification; 2 ARIA and 62 contrast incomplete axe nodes at each 390/1280 size.
- **Scope complete for this explicit owner task**, but full homepage remains OWNER_REVIEW_PENDING and prior P2/P3 findings stay active. Never auto-advance or deploy production.
