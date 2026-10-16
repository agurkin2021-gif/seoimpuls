# SEOImpuls — customer-first EN /seo-services/ simplification
Date: 2026-10-16. Status: **EDITED_QA_PENDING**. Authorized scope: **ONLY /seo-services/**. Owner explicitly prohibits any assistant-initiated transition to another page.

## Problem (verified in source, not presumed Google traffic data)
- 23 equal-weight workstream cards: 3 established commercial pages, 14 constituent tasks, 6 specialist areas without confirmed standalone offer.
- 20 nearly interchangeable topic-specific mailto CTAs create false choice and visual overload.
- Overlap is primarily **offer and buyer-task overlap**, not 23 indexed URL duplicates (all cards live on /seo-services/).
- Actual commercial menu: Technical SEO audit (/seo/), Keyword research (/services/keyword-research/), SEO consultation (/services/seo-consultation/).

## UX acceptance contract
- Keep /seo-services/, approved HTML Title and H1, self canonical, breadcrumbs, 3 relevant linked destination URLs, noindex Pages preview and truthful service limitations.
- Exactly 3 primary entry service cards. An existing choice-by-problem selector may remain only if it adds useful problem/outcome clarity; it must not create 23 competing offers.
- Replace the 23 visually equal cards with a **short 4-area scope overview**, e.g. technical diagnostics; keywords/pages/content; platform/market specializations; research, implementation and measurement. Maximum 4 visible work-area blocks, each with one concise description and simple examples. Treat these as examples of possible scope, not standalone promised packages or separate destinations.
- Limit granular links to the 3 genuine service landing pages plus one unambiguous consultation/contact CTA. Do not fake authority, expertise, quotes, testimonials, rankings, package prices or client results. Specialist fit requires confirmation rather than a claim of established capability.
- Preserve sample report (clearly hypothetical) and verifiable internal QA report; keep concise buying process and FAQ. Remove all prominent "23 services" and 3/14/6 bookkeeping from customer-facing copy.
- Protect the 768px floating contact non-overlap correction; adaptive mobile/tablet/desktop, focus, links, JSON-LD, language and canonical must keep working.

## Execution gates
| Gate | Scope | Acceptance | Status |
|---|---|---|---|
| S0 | Inspect source + accessibility page | 23-card overload and overlap documented; freeze other pages | DONE |
| S1 | EN-only UX/content simplification | Four concise groups, no 23 workstream tiles or 20 mailto CTAs, three service pathways preserved | SOURCE DONE, QA PENDING |
| S2 | Tighten EN-only static/browser tests | Assert new block counts/semantics without weakening strict SEO, navigation, page proof, 390/768/1280 overlap checks | SOURCE DONE, QA PENDING |
| S3 | Full automated/browser evidence | Hugo + strict whitehat + Pages preview + Playwright 390/768/1280 all green, screenshots actually reviewed | PENDING |
| S4 | Owner-facing acceptance/status | Document completed test IDs and known limitations; remain on /seo-services/ even if approved | PENDING |

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
