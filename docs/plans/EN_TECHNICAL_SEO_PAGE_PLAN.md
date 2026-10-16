# SEOImpuls — controlled EN /seo/ technical SEO page plan

**Initiation:** 2026-10-16 after the completed EN /seo-services/ audit, user explicitly instructed to start the next /seo/ stage and, after a connection failure, to retry. Keep homepage, /seo-services/, all sibling specialist URLs, RU/ES, main and production UNCHANGED. Work only in `white-seo-rebuild`.

**Recovery source of truth:** this file, `CHATGPT_PROJECT_CONTEXT.md`, `AGENTS.md`, `docs/SEO_PAGE_WORKFLOW.md`, `docs/research/2026-10-16-en-technical-seo-serp-intent.md`. Preserve `/seo/` route and `seo-overview` design unless verified evidence demands change.

**Process for every change:** inspect branch HEAD; take first unclosed gate; minimal diff; ALWAYS update `CHATGPT_PROJECT_CONTEXT.md` within same commit; run Hugo strict white-hat, route assertions and Pages preview; browser 390/768/1280, screenshots + keyboard and click; CI IDs/conclusions before claiming PASS. No production deploy, redirects or GSC modifications.

## Sequential gates

| ID | Priority | Action | Acceptance evidence | Status |
|---|---|---|---|---|
|0|P0|Restore repository/Opera access and inventory current /seo/ source+SEO workflow|HEAD, source path, Title/H1, basic page content and known release boundaries|**DONE 2026-10-16**|
|1|P0|Google Web SERP for `technical seo services` and `technical seo audit services`, competitor types, gaps and URL ownership|10 observed result title URLs per query, exact query parameters, date, geo caveat and comparisons|**DONE 2026-10-16; parameterized SERP snapshots, US physical geo unverified**|
|2|P0|Complete route-specific rendered HTML baseline for `/seo/`: title, one H1, canonical, robots, hreflang, OG, BreadcrumbList, JSON-LD, internal/external links, images, FAQ anchors and cookie/footer|Recorded evidence and targeted defect list, no unrelated pages altered|**IN_PROGRESS; `BlogPosting` defect confirmed in template; generated HTML assertion and route-specific QA pending**|
|3|P0|Fix false `BlogPosting` structured data with EN /seo/-only template branch and targeted test|Accurate schema rendered; no change to non-/seo/ routes; Hugo/strict/Pages PASS|**NEXT after gate 2**|
|4|P1|Resolve focused commercial intent and information hierarchy; make technical audit dominant without copying keyword/catalogue page|Direct answer, scope/outputs, technical-vs-general distinction, no inaccurate packaged claims; no URL rename|TODO|
|5|P1|Show auditable technical deliverable and diagnosis vs implementation/verification contract|Problem→evidence→affected URLs→owner→fix→retest template, clearly illustrative if no client-approved proof; honest scope/price factors|TODO|
|6|P0|Accessibility/mobile/tablet/desktop, internal links, SEO schema, content and browser visual final QA with screenshots|390/768/1280 no blocking defects; tests actually completed, no fictitious CrUX values|TODO|
|7|P0|Final page decision and recovery context with specific CI ids, open blockers and production restrictions|CODE_QA_PASS/VISUAL_QA_PASS only if proven; otherwise honest pending; external releases blocked|TODO|
|X|External|Actual client-authorized examples, GSC and historic URL/link evidence, US physical localization, RU/ES content parity and owner's separate production approval|Do not invent, do not silently release|BLOCKED_EXTERNAL|

**Scope:** Preserve separate queries owned by `/` (provider selection), `/seo-services/` (choice of work), `/services/keyword-research/` (keywords) and `/services/seo-consultation/` (advisory). This `/seo/` owns **technical SEO services / technical SEO audit** and developer-usable diagnostics, not every SEO service.

**Snapshot findings:** `content/seo/index.md` currently offers a technical audit but gives On-Page, Content/Keyword and International equal top-level weight. EN head schema partial currently sets BlogPosting for all `.IsPage`. Avoid broad template rewrites. No customer results, promised rank gains, prices or delivery commitments may be fabricated.

**Preview:** https://agurkin2021-gif.github.io/seoimpuls/seo/ (preview must stay noindexed). Production https://seoimpuls.com/ untouched. All existing old-URL migration risks retained.

## Work journal

- 2026-10-16 — Restored GitHub read/write and Opera, confirmed branch HEAD `1d5eaf29395b2cc587fb2a415e99c32d64225b9e`. Read AGENTS, workflow, current /seo/ source and prior comparison. Two desktop Google Web SERPs (gl=us/hl=en/pws=0/udm=14/num=10) inspected through Opera, 10 first observed URLs per query recorded in research; actual US physical geo not verified. Confirmed `BlogPosting` source-level schema bug. **This commit is documentation/baseline only**, no HTML/content/code alterations. Next: route-specific generated HTML and schema test before any markup change.
