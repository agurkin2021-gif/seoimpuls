# SEOImpuls — customer-first EN /seo-services/ simplification

> HISTORICAL/SUPERSEDED: English intermediate services hub removed from new architecture. Active owner plan: EN_DIRECT_SERVICES_ARCHITECTURE.md. Do not recreate hub automatically.
Date: 2026-10-16. Status: **CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / OWNER_REVIEW_PENDING — owner approval still required**. Authorized scope: **ONLY /seo-services/**. Owner explicitly prohibits any assistant-initiated transition to another page.

## Problem (verified in source, not presumed Google traffic data)
- 23 equal-weight workstream cards: 3 established commercial pages, 14 constituent tasks, 6 specialist areas without confirmed standalone offer.
- 20 nearly interchangeable topic-specific mailto CTAs create false choice and visual overload.
- Overlap is primarily **offer and buyer-task overlap**, not 23 indexed URL duplicates (all cards live on /seo-services/).
- Actual commercial menu: Technical SEO audit (/seo/), Keyword research (/services/keyword-research/), SEO consultation (/services/seo-consultation/).

## UX acceptance contract
- Keep /seo-services/, existing HTML Title, self canonical, breadcrumbs, 3 relevant linked destinations, noindex Pages preview and honest limits. The H1 is updated under the owner's newer requirement for buyer-friendly wording.
- Exactly 3 primary entry service cards. An existing choice-by-problem selector may remain only if it adds useful problem/outcome clarity; it must not create 23 competing offers.
- Replace the 23 visually equal cards with a **short 4-area scope overview**, e.g. technical diagnostics; keywords/pages/content; platform/market specializations; research, implementation and measurement. Maximum 4 visible work-area blocks, each with one concise description and simple examples. Treat these as examples of possible scope, not standalone promised packages or separate destinations.
- Limit granular links to the 3 genuine service landing pages plus one unambiguous consultation/contact CTA. Do not fake authority, expertise, quotes, testimonials, rankings, package prices or client results. Specialist fit requires confirmation rather than a claim of established capability.
- Preserve sample report (clearly hypothetical) and verifiable internal QA report; keep concise buying process and FAQ. Remove all prominent "23 services" and 3/14/6 bookkeeping from customer-facing copy.
- Protect the 768px floating contact non-overlap correction; adaptive mobile/tablet/desktop, focus, links, JSON-LD, language and canonical must keep working.

## Execution gates
| Gate | Scope | Acceptance | Status |
|---|---|---|---|
| S0 | Inspect source + accessibility page | 23-card overload and overlap documented; freeze other pages | DONE |
| S1 | EN-only UX/content simplification | Four concise groups, no 23 workstream tiles or 20 mailto CTAs, three service pathways preserved | DONE — code + browser checked |
| S2 | Tighten EN-only static/browser tests | Assert new block counts/semantics without weakening strict SEO, navigation, page proof, 390/768/1280 overlap checks | DONE — accepted checks pass |
| S3 | Full automated/browser evidence | Hugo + strict whitehat + Pages preview + Playwright 390/768/1280 all green, screenshots actually reviewed | DONE — runs #38899685820/#38899685817/#38899499592; screenshots inspected |
| S4 | Owner-facing acceptance/status | Document completed test IDs and known limitations; remain on /seo-services/ even if approved | OWNER_REVIEW_PENDING; do not switch automatically |

## Exact working paths
- Source data: `data/en_seo_catalog.json` (23 legacy entries may be retained as research; do not render as 23 equal services).
- EN template: `layouts/partials/en-services-catalog.html`.
- EN page metadata: `content/services/_index.md` (only if truly necessary; URL/Title/H1 preferably unchanged).
- Tests: `scripts/verify_en_services_route.py`, `scripts/audit_en_services_browser.cjs` and page-specific expected output in CI (if any).
- Every individual code/docs change must update `CHATGPT_PROJECT_CONTEXT.md` in the same Git commit.
- No edits to homepage, technical SEO service, RU/ES, global header/footer, main branch, production or DNS/GSC.

## Invariant
**NEVER AUTO-PIVOT.** When S0–S4 are DONE, stop on this page and wait for a new explicit owner instruction before beginning any other URL.

## 2026-10-16 — EN-only UX redesign source commit
- Customer view: 3 real service entries + 3 concise decision routes + 4 non-commercial scope cards with 12 examples, not 23 separately marketed tasks and 20 extra email buttons.
- Specialist scope and fixed-package caveats preserved; 5 FAQ entries retained. Exact H1/Title/url and case-example proof unchanged.
- Updated static and browser tests require new work-area DOM with 0 workstream tiles; previous CI PASS no longer applies to this edited version.
- Status EDITED_QA_PENDING. Next: inspect strict Hugo, preview noindex and Chrome 390/768/1280 evidence. Remain on this page regardless of result.

## 2026-10-16 — First full gate feedback
- Source commit 46bc35e builds under Hugo but strict/Pages jobs #38899499369 and #38899499275 stopped at stale assertion expecting previous heading "SEO Work We Can Scope". EN static assertion corrected with this documentation/context commit; no page source changed.
- Browser run #38899499592 was still in progress when correction was prepared; no claim of browser PASS. S3 remains PENDING.

## 2026-10-16 — Recorded QA evidence after fix
- Updated EN-only static assertion (same source HTML) in commit `462aa03`; full strict Hugo gate #38899685820 PASS, Pages Preview #38899685817 PASS, context guard #38899685925 PASS.
- Responsive Chromium #38899499592 PASS for source `46bc35e` which is unchanged by later test-only fix. 390/768/1280 browser `fail:[]`; 3 service cards, 3 buyer decisions, 4 informative scope cards/12 examples, 0 old 23 tiles, 0 per-task email CTAs; broken links, overflow and runtime/network failures zero. Tablet and desktop floating shortcuts 2, overlapping category text 0.
- Screenshot artifact #12044858940 downloaded and inspected: desktop full page, mobile full page, tablet category and viewport captures. Four area grid is 2 columns on desktop/tablet and one on mobile; no observed clipping or contact overlap. This is manual screenshot review, not formal WCAG certification.
- Page status **CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / OWNER_REVIEW_PENDING**. Do not mark the second page closed or begin any other page without an explicit user instruction.

## 2026-10-16 — Plain service descriptions with search terms (ACTIVE UPDATE)
- Owner wants a catalogue readable by non-SEO business owners but containing phrases people actually search. Peer examples use SEO Audit, Keyword Research, SEO Consultation, SEO Competitor Analysis and On-Page SEO; **no verified search volume or exact localized SERP positions** were established. No keyword ranking guarantees.
- Existing three commercial pages/links remain: /seo/, /services/keyword-research/, /services/seo-consultation/. Cards now display SEO Audit / Keyword Research / SEO Consultation with everyday explanations of what problem each solves and what result is delivered. All three existing service images stay, especially /uploads/semantika-1788907052-q46-1788907068324.webp for semantic keyword research.
- Keyword research is explicitly a standalone deliverable before a website exists; search phrases are cleaned and grouped by topic (clustering) into a spreadsheet.
- The four information cards use clear searchable terms (SEO Audit, Keyword Research, SEO Competitor Analysis, On-Page SEO) with business-first explanations. The last two are possible additionally agreed work, NOT independent confirmed service packages or new URLs.
- H1 was deliberately changed to "Find the Right SEO Service for Your Business" to remove the misleading requirement of a website, retaining original Title/URL/canonical. Page benefits, process, CTA, FAQ and sample audit wording simplified. Historical technical self-QA disclosure retained but initially collapsed.
- Changed only EN /seo-services/ source, EN-guarded shared presentation, dedicated SEO QA and that page's H1 assertion in sitewide CI, with the required context. No edits to the homepage, other service pages, RU/ES, main or production.
- Status **EDITED_QA_PENDING**, dependent on fresh Hugo/strict, Pages noindex preview, browser 390/768/1280 and inspected screenshots. Older PASS runs applied to different source.
- NEVER switch to other pages without explicit new owner command.

## 2026-10-16 — Follow-up UX cleanup after reviewing fresh screenshots
- Browser checks of commit e7f9188 passed (strict #38904642890, preview #38904642446, Chromium #38904642723, context #38904642597); artifact #12048005196 viewed on 390, 768 and 1280 screenshots.
- Screenshot review revealed remaining commercial duplication: the 3 image-bearing linked service cards were repeated in a second 3-choice block, then two of the same services appeared among four work-area cards. This violates the owner's preference for a simple service selector.
- Next source revision removes the duplicate 3-choice block completely, preserves all 3 primary card destinations + images + explanatory benefit, and limits the *additional* informational work areas to SEO Competitor Analysis and On-Page SEO (2 cards, 3 examples each). No new commercial child pages or promises. Existing FAQ, proof, audit example and contact methods remain.
- Static and browser regression tests updated to require 3 primary service cards, 0 repeated choice cards, 2 supplemental areas / 6 examples. All other site SEO, images, contacts, floating icons and breakpoint checks continue.
- Current source QA **PENDING**; previous e7f9188 PASS cannot be assigned to the newly edited source. Final owner acceptance still pending. NO AUTO-PIVOT.

## 2026-10-16 — Final QA for no-duplicate business-friendly EN /seo-services/
- Final source commit: `9266336`. The exact code was checked in GitHub Actions: full Hugo + strict QA [#38905365028](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38905365028) **PASS**; GitHub Pages nonindexed preview [#38905365102](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38905365102) **PASS**; context guard [#38905364899](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38905364899) **PASS**; browser 390/768/1280 [#38905365160](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38905365160) **PASS**.
- Browser logs: HTTP 200, 1 expected H1, 3 service cards, 0 duplicate 3-choice cards, 2 supplemental areas (SEO Competitor Analysis, On-Page SEO), 6 examples, 0 legacy 23-card workstreams, no broken internal routes, JavaScript errors, network failures, horizontal scrolling, keyboard/FAQ faults or head/schema discrepancies. WA/TG shortcut overlap with text: zero on both 768 and 1280.
- Screenshot artifact [#12048086527](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38905365160/artifacts/12048086527) downloaded and manually examined: 390/768/1280 first and category screenshots, desktop full page. No visible clipped text/primary links or floating icon overlap. Long website content and ranking claims were not empirically measured; not a WCAG conformance certification.
- **Acceptance:** technically QA passed, but the second page is not owner-closed. Keep only `/seo-services/` active; no move to homepage, `/seo/` or other pages without new direct owner instruction. Never publish production without separate approval.
