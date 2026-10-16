# EN homepage balance audit — 2026-10-16

Scope: EN homepage only, working branch white-seo-rebuild. Read-only review of current Hugo source plus live GitHub Pages preview after a fresh navigation; production seoimpuls.com is a different legacy site and was not changed. This document records findings, not owner-approved implementation.

Source checked:
- content/_index.md and layouts/index.html, branch white-seo-rebuild; accepted content/layout source 755e52d; branch docs-only head at audit start 06dac77d.
- Browser: https://agurkin2021-gif.github.io/seoimpuls/?audit=20261016a; Opera accessibility tree and desktop screenshot refreshed on 2026-10-16.
- Prior automated checks: strict Hugo #38918895547, preview #38918895213, direct Chromium 390/768/1280 #38918077643, homepage visual #38918077646, axe diagnostic #38918077640. Their passes refer to unchanged page source, not a new mobile manual audit or field CWV.
- Prior scope review docs/research/2026-10-16-en-home-post-css-audit.md and historical EN SERP/intent documentation. No current GSC performance, verified localized first-ten SERP, conversion data or field Core Web Vitals available.

## Confirmed strengths — preserve
1. Title and H1: Professional SEO Services; three direct EN commercial routes /technical-seo-audit/, /keyword-research/, /seo-consultation/; no separate /services/ or /seo-services/ English catalog needed.
2. The previous eight supplemental card-like service scopes are now exactly THREE short supporting lines labeled Other SEO Work We Can Discuss. No extra service pages or packages implied.
3. Plain buyer copy accepts a business without an existing website for keyword research. Concrete outputs distinguish Website Audit Report, Keyword Research Spreadsheet, and Consultation Priorities.
4. Original EN three numerical CSS marks (01/02/03), no old service images in EN cards; prior no-overflow and social-shortcut geometry automation passed. Existing canonical/JSON-LD/H1 checks passed; preview is intentionally noindex.

## Prioritized balance findings

P1 — Desktop commercial visual hierarchy inverted.
The first sales region uses a very large and wide left panel “From your goal to a clear result” with only one introductory paragraph and three small process steps near its top, leaving extensive unused dark space underneath. The three actual paid services are stacked vertically in a substantially narrower right column. Refreshed desktop screenshot visibly confirms this disproportion. The process dominates available space, while the commercial choices receive less width. Recommendation: give the three service cards the primary full-width or majority-width grid and move the compact process below or use intrinsic rather than stretched panel height. No heavy assets, no new commercial sections.

P1 — Multiple competing sequences of 01/02/03.
Three process steps and three services both present 01/02/03 in the same first commercial area, and the three “What You Receive” cards are numbered as well. This makes independent service choices look like a mandatory sequence and creates visual monotony. Keep distinctive lightweight markers on THREE services; simplify process/deliverable numbering and styling without losing information.

P1 — Header/navigation priority is inconsistent.
Header contains Services (anchor) and separately “Technical SEO Audit”, but does not give Keyword Research or SEO Consultation equivalent prominence. News is top-level, while the buying pathways remain under the hero. Consolidate commercial navigation under a clear Services anchor and avoid privileging one of three equal services. The single-word “Home” breadcrumb on the homepage adds an extra line without real navigational value; consider hiding it ONLY on EN homepage.

P1 — Scope promise inconsistency.
Hero promises “get a practical plan”; process step Deliver says “receive ... a practical plan”. Yet “Consultation Priorities” expressly states a written plan can be agreed separately, and audit / keyword outputs are different products. Avoid suggesting every service includes a written action plan. Clarify verbally delivered consultation priorities versus a separate paid written document. The hero should communicate selection among three services, not the impression all are included.

P1 — Card-label vs landing intent mismatch.
The first commercial card is “SEO Audit” but its linked, dedicated landing page is “Technical SEO Audit”. General SEO audit can imply content, links and strategy as well as technical checks; make the label/scope precise while keeping plain language. “Keyword Research & Clustering” is specialist jargon: use “Keyword Research” as visible buyer label; explain grouping simply in the bullet copy. Keep route /keyword-research/ unchanged.

P2 — Duplicate explanations across the page.
Hero, “What Are Professional SEO Services?”, optional three tasks, “What You Receive”, three FAQ cards and bottom “Tell Us About Your SEO Project” repeat the ideas of choosing one service, website optional, agreed scope, rankings not guaranteed. None alone is harmful; together they dilute urgency and create near-identical blocks. Combine repeated qualification where it is closest to a buying decision, keep service specifics in the 3 cards and detailed pages, retain a short FAQ and final contact. Do not recreate an eight-card service menu.

P2 — Section/heading hierarchy and weak differentiation.
The three main paid card titles use H3 within an aside without a local visible H2 “Choose an SEO Service”; the neighboring “From your goal to a clear result” is an H2 in a separate article. Supply a coherent heading for the offer group or promote main service headings consistently. The cards' bullets emphasize report types and search visibility, but they do not immediately say who each service is for in one short contrasting line: existing website with problems vs new business seeking topics vs business owner needing guidance. This is buyer comprehension, not a proven Google heading penalty.

P2 — Weakly differentiated CTAs.
“Explore SEO Services” and “How We Work” scroll to adjacent parts of the same block already close to the fold; they do not represent two clearly different user paths. Keep one direct path to three services; make the second only a genuine alternative such as contact, if approved. Do not imply instant audit/consultation availability.

P2 — Fixed full-width Contacts strip / viewport obstruction risk.
Current desktop Opera screenshot shows a full-width Contacts band at the bottom of the viewport, occupying part of visible content while the last card continues below. Earlier automation checks individual WhatsApp and Telegram ICON rectangles, not every animation state and full-width band. This merits a focused scroll/focus/intersection test before deciding any CSS change. Do not assert unreachable content without reproduction.

P2 — 768px tablet and 390px mobile presentation.
Prior verified screenshot assessment recorded a tall multirow tablet navigation at 768 and a cookie-consent sheet consuming a large part of a 390px viewport. Prior automated 390/768/1280 checks passed code/overflow gates, but these are qualitative UX issues, not proven broken links. Compress without removing legal accept/reject/preferences controls.

P3 — Trust and pricing information.
Main page lacks verifiable project-specific proof or a concrete output specimen; “About” link alone carries trust burden. Do not invent logos, ratings, clients, cases or a fake noindex example (previously rejected by owner). Scope-based pricing is honest but offers no approximate purchase expectation; only add genuine prices/ranges/timelines if owner can verify and honor them. Not a validated ranking defect.

## Recommended lean information architecture — no new URLs
1. Compact header; homepage hero with ONE clear buyer value proposition and primary services anchor.
2. THREE balanced, equal-status service cards linked directly to the three existing commercial URLs; plain outcome and intended buyer per card.
3. Short “how we work” strip with distinct visual treatment and no redundant 01/02/03 repetition.
4. Condensed optional work + deliverables, ideally no extra visually equal-service card grid.
5. Short buyer FAQ (scope/cost/time) and one clear contact CTA; existing legal and contact mechanisms remain.
6. Keep one H1, Title/H1 keyword alignment, canonical, Organization/WebSite schema and noindex-only preview behavior; no production deployment.

## SEO/QA boundaries and next implementation priority
Confirmed source/preview findings are design, offer hierarchy and buyer-copy issues, not evidence of a Google algorithmic penalty or measured traffic loss. Existing source and CI checks remain in place; no live production change was made by this audit. Keep EN-only scope. Suggested fix order after owner direction: (1) desktop layout and repeated numbering, (2) clarify three card labels and written-plan scope, (3) header/CTA/heading hierarchy, (4) compact duplication, (5) contacts/footer scroll geometry, mobile/tablet consent/nav and manual accessibility checks. Re-run Hugo strict, noindex preview, desktop/tablet/mobile browser, and screenshots after any code edits.

STATUS: AUDIT_RECORDED / EN_HOMEPAGE_CODE_UNCHANGED / OWNER_REVIEW_PENDING / PRODUCTION_NOT_DEPLOYED.
