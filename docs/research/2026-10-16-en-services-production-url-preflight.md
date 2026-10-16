# SEOImpuls — EN /seo-services/ production URL preflight (read-only)

**Date:** 2026-10-16. **Page in scope:** EN catalogue `/seo-services/`, branch `white-seo-rebuild`. **Result:** LIVE_URL_SURFACE_OBSERVED / SEMANTIC_MIGRATION_MAP_DRAFTED / GSC_AND_HTTP_MIGRATION_BLOCKED / PRODUCTION_UNTOUCHED.

This document is a read-only *preflight*, **not** an authorized migration, server instruction, or proof of Google indexing. The accepted catalogue code and its previously passed responsive QA have not been modified. Do **not** expand implementation scope to `/seo/`, other EN service pages, RU/ES, production, or `main`.

## Evidence and collection limits

1. **Connected Opera (live, 2026-10-16):** opened these actual production URLs individually:
   - `https://seoimpuls.com/link-building-services/` — renders active "Link Building Services" page and old service links.
   - `https://seoimpuls.com/services/` — renders nginx "404 Not Found".
   - `https://seoimpuls.com/seo-services/` — renders nginx "404 Not Found".
   - `https://seoimpuls.com/` — renders "SEO Backlink Service" and navigation to the legacy link-building catalogue.
   - `https://seoimpuls.com/link-building-services/keyword-research/` and `.../seo-consultation/` — live pages with their old commercial descriptions.
   - **Caveat:** these are current browser page observations, **not an independently captured HTTP status/redirect-chain log**; no production credentials or edits were used. A prior Opera audit in `docs/research/2026-10-15-en-services-serp-and-architecture.md` also observed both new/generic URLs returning 404.
2. **Production robots/sitemap, Opera 2026-10-16:**
   - `https://seoimpuls.com/robots.txt`: `User-agent: *`, `Allow: /`, `Sitemap: https://seoimpuls.com/sitemap.xml`.
   - `https://seoimpuls.com/sitemap.xml`: sitemap index lists `/en/sitemap.xml`, `/es/sitemap.xml`, `/ru/sitemap.xml`.
   - `https://seoimpuls.com/en/sitemap.xml`: includes `/link-building-services/` and legacy child URLs including `/backlinks/`, `/domain-rating/`, `/link-building/`, `/tier-1-2-3/`, `/keyword-research/`, `/seo-consultation/`, along with `/seo/` and other site routes. No root `/services/` or `/seo-services/` observed there.
3. **Current GitHub Pages preview, Opera 2026-10-16:**
   - `https://agurkin2021-gif.github.io/seoimpuls/seo-services/` — current three-way chooser and 23-workstream catalogue.
   - `https://agurkin2021-gif.github.io/seoimpuls/en/sitemap.xml` — includes new `/seo-services/`, `/seo/`, `/services/keyword-research/`, `/services/seo-consultation/`, not the old `/link-building-services/`. The appearance of `/services/...` **child routes** does **not** mean root `/services/` is listed.
   - Visiting `https://agurkin2021-gif.github.io/seoimpuls/services/` reaches `/seo-services/` in Opera via Hugo's HTML alias. This does not prove a server-side HTTP 301.
4. **Source confirmation:** `content/services/_index.md` in working branch declares `url: "/seo-services/"`, `aliases: ["/services/"]`, `translationKey: services`. Archived `main` version declares `url: "/link-building-services/"` with content oriented to backlinks/Tier/microsites. `content/services/keyword-research/index.md` and `.../seo-consultation/index.md` in working branch retain their own service routes.

## URL-level candidate decisions — all **provisional**, no production action

| Observed live URL | Proposed target / action after future authorization | Reason and gate |
| --- | --- | --- |
| `/seo-services/` (currently displays 404) | Publish new EN catalogue at same self-canonical URL **only as part of coordinated approved release** | New intent: compare white-hat SEO work by problem/deliverable. Check actual production HTTP 200, robots, canonical, sitemap, menus, and QA after release. |
| `/services/` (currently displays 404) | **Possible** true HTTP 301 → `/seo-services/` once launched | Same catalogue-selection intent; first confirm any historical GSC/external-link evidence and validate source URL/redirect chain. Preview HTML alias is not a 301. |
| `/link-building-services/` (currently legacy link-building catalogue) | **NO automatic 301** to `/seo-services/`; decide retain/rewrite, 404/410 or strictly appropriate alternate after sitewide review | Old landing page sells links/Tier and satellite-related areas; new hub does not sell those. Intent and offering mismatch makes a blanket redirect misleading. Collect GSC and backlink data first. |
| `/link-building-services/keyword-research/` | Candidate 301 → `/services/keyword-research/` **only after exact intent and URL signal review** | Both describe keyword discovery and clustering, but old advertised scope/pricing differ from new scoped offer. Not approved yet. |
| `/link-building-services/seo-consultation/` | Candidate 301 → `/services/seo-consultation/` **only after exact intent and URL signal review** | Core consultation overlaps, but terms, scope and claims differ. Preserve relevant legacy URLs until decision. |
| `/link-building-services/backlinks/`, `/domain-rating/`, `/link-building/`, `/tier-1-2-3/`, `/microsite-development/` | **No mass redirect** to new catalogue. Later choose 404/410 or genuine matching successor per URL | Old manipulated-link/DR/Tier/satellite offerings are not what `/seo-services/` offers. Any deprecation is a separate sitewide migration. |
| `/link-building-services/website-creation/` | No guessed EN successor or catalogue redirect | Website-development intent is not one of the three EN specialist offerings. Needs separate URL and locale decision. |
| `/seo/` | Preserve route, no edit or redirected destination change in this preflight | Independent technical SEO intent; earlier attempted pivot to this page is inactive. |
| RU/ES legacy catalogues and `/ru/uslugi/`, `/es/servicios/` | **Read-only; no URLs or hreflang rewritten** | EN has 23 scopes; RU/ES content parity remains partial. Spanish market/language targeting is not confirmed. |

## Release gates and enforceable constraints

- **First obtain URL-level evidence:** GSC indexed URLs, clicks/impressions/queries, valid referring URLs and backlink destinations for a meaningful historical window (project guideline 3–6 months). A sitemap entry or a live 404 does not prove absence of historic ranking/links.
- **Then approve a distinct action for each old URL:** relevant 301; keep indexable with truthful replacement where appropriate; or 404/410 when no semantic successor. Do not forward a whole grey-service URL subtree to the EN clean catalogue or homepage.
- **Only with separate production permission** configure actual nginx/CDN 301s, replace outdated sitemaps/navigation/old commercial claims, validate full EN/RU/ES deployment dependencies, and verify external HTTP response status/Location/canonical/robots with response headers. Perform before/after HTTP/HTML and mobile browser checks.
- Ensure production `/seo-services/` has one production canonical `https://seoimpuls.com/seo-services/` and intended index policy; Pages preview must remain `noindex,nofollow`. The live site currently has link-building focused homepage/navigation; publishing the new catalogue alone would be an inconsistent partial release.
- GSC, real client-authorized proof, RU/ES content equivalence and the final release approval are **still unavailable**. This audit does **not** clear any of those blockers.

## Decision

**No code, sitemap, HTTP redirect, DNS or production change now.** The next decision can be made only on verified Search Console/history and an explicit sitewide production/migration plan. This read-only gate supplies current URL evidence and avoids guessing or silently redirecting unrelated legacy pages. The accepted EN `/seo-services/` catalogue remains `CODE_QA_PASS / RESPONSIVE_VISUAL_QA_PASS / RELEASE_BLOCKED`.
