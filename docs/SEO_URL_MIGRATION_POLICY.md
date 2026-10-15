# SEOImpuls commercial URL migration — working decision register (2026-10-15)

**Status: PROPOSED; NOT IMPLEMENTED.** Legacy baselines are preserved in main. No server redirect, no `410`, no changed DNS, no sitemap removal has been done.

## Source
The CSV rows in `docs/seo-url-migration-register.csv` were derived from all 27 source Markdown files under `content/services/` in the 2026-10-15 Hugo export. The destination column is a candidate, not a verified final URL. Some filenames are generated under a language-specific base path; perform a live crawl / 200-status comparison before migration.

## Guardrails
1. Export GSC **Pages + Performance** for at least 3–6 months, filter pages by clicks/impressions/referring links and note indexed canonical before retiring any URLs.
2. Verify live HTTP status, URL actually served, external backlinks and internal reference count. Check translation/hreflang and sitemap.
3. **301 only if the replacement page truly meets substantially the same user need** (keyword research -> keyword research; consultation -> consultation). Do not mass-redirect old backlinks or DR product URLs to a generic SEO page or homepage.
4. For withdrawn services without legitimate equivalents, respond **410 or 404** on production at cutover after removing internal links and sitemap entries; Google does not require a special page to earn “penalty recovery”.
5. For legitimate services check actual deliverability. Website creation must be separated from link satellites; do not assume current price/cases are valid.
6. Create canonical URLs without old `/link-building-services/` / `/uslugi-linkbildinga/` / `/servicios-de-link-building/` path segments.
7. Do not advertise new URLs until they exist as genuine pages in the working branch, pass build and content QA, and are approved for deployment.
8. Always verify 301 chains, loops, 404/410, canonical, sitemap and hreflang across EN/RU/ES before cutover.

## Recommended service taxonomy (still subject to GSC and SERP audit)
- `/` = general SEO agency/organic visibility value proposition (already drafted).
- `/seo/` = focused technical SEO audit and service scope (already drafted).
- `/services/` = navigational catalog for legitimate service offerings; distinct from /seo/ and homepage, not a keyword-stuffed clone.
- `/services/keyword-research/` = keyword research / page mapping.
- `/services/seo-consultation/` = advisory engagement.
- `/services/website-development/` = only if the company actually provides conventional website development.
- RU/ES separate URL taxonomy, native localization and SERP verification.

## Totals
- 27 legacy service content URLs identified: EN 9, ES 9, RU 9.
- `16` candidates for retirement; `6` proposed same-intent migrations; `5` require business/content confirmation.
- Zero production redirect actions performed.
