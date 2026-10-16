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


## Validation results — 2026-10-15 (confirmed)
1. GitHub Actions [rebuild #99](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38834500751) — **PASS**. Hugo generated all languages and `Verify EN homepage schema and preserve RU/ES` step passed; log confirmed exactly `Organization` + `WebSite`, correct schema.org context, shared production canonical, verified existing logo file, approved page-level description and linked publisher. No EN `Person`, `BreadcrumbList`, `FAQPage`, `Service`, `Review` or `AggregateRating`. RU/ES homepage legacy types unchanged.
2. GitHub Actions [Pages Preview #40](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38834500755) — **PASS**. The same schema guard also passed after the subdirectory `/seoimpuls/` baseURL build.
3. GitHub Actions [Chromium browser #10](https://github.com/agurkin2021-gif/seoimpuls/actions/runs/38834500854) — **PASS** at 390/1280 CSS px: HTTP 200, one H1 `Professional SEO Services`, valid and parseable JSON-LD, self canonical for production-base build, images/links loaded, zero JS failures/overflow, desktop floating footer preserved and cookie consent actionable.
4. Live Pages Preview image `https://agurkin2021-gif.github.io/seoimpuls/SEOIMPULS_logo.webp` opens directly in connected Opera (image title 487×229); no broken schema logo asset path.
5. External **Google Rich Results Test** at `https://search.google.com/test/rich-results?url=https%3A%2F%2Fagurkin2021-gif.github.io%2Fseoimpuls%2F` returned `URL недоступен Google` / crawling failed. **Not passed and not a JSON-LD invalidity finding**. Pages Preview is purposefully `noindex`, and that URL is not representative of production; Google eligibility and actual crawling must be checked only after authorized production rollout.
6. Google Search Central confirms `Organization` can be used on the homepage for disambiguation and that logo should be crawlable and at least 112px each dimension; source `https://developers.google.com/search/docs/appearance/structured-data/organization`. Breadcrumb rich results require at least two `ListItem` values; `https://developers.google.com/search/docs/appearance/structured-data/breadcrumb`.

**Status:** `EN_SCHEMA_GENERATED_VALIDATED`, `PREVIEW_QA_PASS`, `GOOGLE_RICH_RESULT_EXTERNAL_UNVERIFIED`, `PRODUCTION_NOT_DEPLOYED`, `GSC_PENDING`. Valid JSON-LD and supported Organization fields do not promise a brand Knowledge Panel or ranking improvement. No further content or schema changes required in current scope.

## Open evidence limitations
- Google Search Console `/` vs `/services/` query overlap unavailable, GSC_PENDING.
- No proven legal registration or specialist biography supplied, so no additional Organization/Person claims.
- No result placement/ranking eligibility guarantee. RU/ES and English service BlogPosting issues deferred until user re-scopes.
- Hugo/Pages/Chromium QA and external Rich Results test **pending at time this change was written**; update status only after seeing actual run results.
