# SEOImpuls — EN homepage JSON-LD audit and minimal schema correction

Date 2026-10-15. Scope: **English homepage only**, Hugo `white-seo-rebuild`; production `seoimpuls.com`, main, RU/ES and other EN pages untouched.

## Source-confirmed before-state
1. `layouts/partials/head/seo.html` emitted one `WebSite` on each homepage with `author: {\"@type\":\"Person\",\"name\":\"SeoImpuls Team\"}`, from global `hugo.toml` author setting. A collective business brand is not a particular Person. No genuine personal identity supplied.
2. On all locales, even the homepage `/`, the shared template emitted `BreadcrumbList` with exactly **one** `ListItem` (Home). Google Breadcrumb rich-result rules specify at least two items. EN homepage has no actual second breadcrumb level, so suppress it there.
3. No explicit `Organization` entity on EN homepage; the English `WebSite.description` came from generic `Site.Params.description`, not the selected page `description`.
4. Verified existing files `static/SEOIMPULS_logo.webp` (487 × 229 pixels, WebP) and `static/SEOIMPULS_logo_tight.webp` (400 × 132). The main logo configured in `hugo.toml` is used for schema. Both are over Google's 112×112-pixel minimum.
5. Chromium HTML audit previously found the JSON-LD syntax parseable, but that did **not** check semantic correctness or Google rich-result eligibility.

## Corrected EN-home-only output
- `Organization`: `@id=#organization`, name **SeoImpuls**, homepage URL, real existing brand logo WebP URL. No office address, legal name, business registration, employee count, false reviews/ratings, claimed awards or unverifiable social identities.
- `WebSite`: `@id=#website`, homepage URL, site name, EN `inLanguage`, approved homepage meta description, `publisher` linking by `@id` to Organization.
- Remove misleading team-as-Person `author` on EN homepage.
- Remove EN homepage one-item `BreadcrumbList`; do not append fake second breadcrumb.
- Do **not** add `Service`, `FAQPage`, `AggregateRating`, `Review` or other rich-result bait to this general buyer-oriented homepage.
- Restore existing legacy output in Hugo's non-EN `else` branch *unchanged*: RU/ES WebSite and single breadcrumb remain to be addressed in later language migration. The `BlogPosting` markup on English service pages was not edited.

## Guards and deployment
- Added `scripts/verify_en_home_schema.py` with strict parsing of generated EN homepage JSON-LD and exact two types, matching production canonical, `@id` relation, logo, meta description; negative checks for `Person`/`BreadcrumbList`. Checks RU/ES page schemas still generated as prior to this scoped change.
- Ran same guard after Hugo build in **both** rebuild QA (production-base URL) and Pages Preview build (subdirectory baseURL). Playwright EN-home 390/1280 browser audit also auto-triggers on edits to the shared schema partial.
- Google documentation: https://developers.google.com/search/docs/appearance/structured-data/organization and https://developers.google.com/search/docs/appearance/structured-data/breadcrumb .
- Pages Preview is **intentionally noindex** and canonical points to production; its rich-result testing is not proof of eligibility in Google Search. Verify generated markup independently and do not promise knowledge panel/logo display.

## Open evidence limitations
- Google Search Console `/` vs `/services/` query overlap unavailable, GSC_PENDING.
- No proven legal registration or specialist biography supplied, so no additional Organization/Person claims.
- No result placement/ranking eligibility guarantee. RU/ES and English service BlogPosting issues deferred until user re-scopes.
- Hugo/Pages/Chromium QA and external Rich Results test **pending at time this change was written**; update status only after seeing actual run results.
