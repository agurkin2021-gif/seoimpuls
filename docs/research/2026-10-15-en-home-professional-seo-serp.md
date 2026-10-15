# SEOImpuls — EN homepage SERP-first and intent gap audit (2026-10-15)

## Reproducible snapshot, restrictions
- **Primary query:** `professional seo services` (owner-selected H1). Keyword Planner screenshot from owner: 1k–10k estimated monthly searches, **all locations** / English, advertising competition low. This is not organic keyword difficulty or US-only demand.
- **Google snapshot captured in Opera:** https://www.google.com/search?q=professional+seo+services&hl=en&gl=us&pws=0&udm=14&num=10
- **Date:** 2026-10-15, desktop Opera, English `hl=en`, US localization requested via `gl=us`, `pws=0`, Web `udm=14`; ordinary organic results only, excluding sponsored results and Google AI Overview. Google said **"Can't determine location"**, so US physical geolocation and IP independence are not established. Results can change by user/session/time. This is a **VERIFIED PARAMETERIZED SERP SNAPSHOT, not a strictly US-geolocated reproducible top10**.
- The default All tab also presented AI Overview, People Also Ask, local businesses and sponsored placements. Those features are excluded from the Web rank table. Sponsored SearchBerg result appeared after organic top 10 in Web results.
- Each of the first 10 listed links was followed via Google in Opera to resolve its actual final URL; their pages were inspected for headings and intent, not merely inferred from names. No search volumes, organic KD, link authority, ranking stability or conversions are implied.

## Exact first ten organic Web results
| Rank | Actual URL | Visible result title / entity | URL intent | Key buyer-facing coverage observed |
|---:|---|---|---|---|
| 1 | https://coalitiontechnologies.com/seo-search-engine-optimization | The #1 SEO Services Company with 860+ Case Studies — Coalition Technologies | Commercial service | What SEO services mean, coverage, implementation, case studies/reviews, proof claims, pricing link, method, conversion, FAQ |
| 2 | https://clutch.co/seo-firms | Top SEO Companies & Services — Clutch | Directory/comparison | Multiple providers, vetting, price/timeline questions, profiles and reviews |
| 3 | https://netlynxinc.com/seo-services/ | Professional SEO Company, Best SEO Agency — Netlynx | Commercial service | SEO service types, audit, technical/on-page, consultation, testimonials and local positioning |
| 4 | https://agencies.semrush.com/list/seo/united-states/ | Best SEO Companies in United States 2026 — Semrush | Directory/comparison | Filters by location/service/budget, buyer vetting questions, expertise, proof and cost expectations |
| 5 | https://coalitiontechnologies.com/ | Coalition Technologies: SEO Company | Company homepage | Organization identity, cases/reviews, service choices, pricing estimator, free assessment CTA |
| 6 | https://www.gobluemedia.com/areas/seo-company-california/ | SEO Agency in California — Blue Media | Regional commercial service | Local commercial targeting, specializations, verified cases claimed, contact and FAQs |
| 7 | https://thriveagency.com/digital-marketing-services/search-engine-optimization-seo/ | Search Engine Optimization – SEO Company — Thrive | Commercial service | On-page/technical services, process, timelines, costs, proof and industry fit |
| 8 | https://revenuebase.ai/companies/seo-agencies-for-professional-services/united-states | Top 25 SEO agencies for professional services — RevenueBase | Database/directory | Lists and company data, industry/geo segmentation, directory methodology |
| 9 | https://www.bark.com/en/us/search-engine-optimization/california/los-angeles/ | Find a SEO Specialist in Los Angeles — Bark | Local specialist marketplace | Quotes, selection of professionals, price and process questions |
| 10 | https://www.americaneagle.com/expertise/digital-marketing/search-engine-optimization | SEO Services — Americaneagle.com | Commercial SEO service | Services by industry, expertise, site audit, case studies, FAQ, conversions and consultation |

**Interpretation:** six direct-provider listings (including Coalition twice), three directories (Clutch, Semrush, RevenueBase), one marketplace (Bark). User intent is predominantly COMMERCIAL / PROVIDER-SELECTION, partially LOCAL, not merely a definition of SEO. This snapshot alone DOES NOT prove low organic competition. Agencies and directories have broad web footprints and proof mechanisms; our positioning as **SEO specialists, not an agency** should remain factually accurate.

## Adjacent-query intent separation (same Google Web/locale/session parameters)
- `seo services`: broader/localized mix; only Coalition's same specific SEO page overlapped the first 10 of `professional seo services` in this exploratory query (not a stable or universal overlap measure).
- `technical seo services`: predominantly specialized audit/service pages, including Onely and SEO Brand; substantially different topical page type from broad provider selection.
- `keyword research services`: keyword service, tools, freelancers, how-to/comparison mixed; specialized content belongs in dedicated keyword-research page.
- **Owning URLs:** `/` = overall professional specialist offer and buying decision. `/services/` = catalog/comparison of available SEO work; `/seo/` = technical SEO assessment and on-page specifics; `/services/keyword-research/` = keyword clusters and mapping; `/services/seo-consultation/` = advisory session; `/faq/` = detailed service policy explanations; `/about/` = truthfully documented team/about. Risk of overlap between `/` and `/services/` remains `GSC_PENDING`; do not rewrite sibling URLs under current scope.

## EN homepage on-page baseline (checked against source and prior browser QA)
- `/`: title/H1 `Professional SEO Services`; generated `<title>Professional SEO Services | SeoImpuls</title>`; one H1 and descriptive meta, canonical `https://seoimpuls.com/`; EN / RU / ES hreflang emitted, but *reciprocal intent equivalence is pending future RU/ES rebuild*.
- HTML and JSON-LD valid in 390/1280 Chromium audit; technical report `docs/research/2026-10-15-en-home-technical-visual-audit.md` (Hugo/Playwright).
- Above fold: technical/keyword/content intro, services CTA and How We Work anchor; process Diagnose/Prioritize/Validate, two specialized cards to /seo/ and /services/keyword-research/.
- Below: eight service categories with conditional scope; three concrete deliverable types; bottom project enquiry CTA and /services/seo-consultation/; live chat/email in footer. No fabricated cases, prices or team claims.
- SEO images, internal paths, robots/canonical and script checks passed prior testing. Commercial depth remains thinner than large-agency landing pages, but this is not a technical error.

## Content-gap ownership & decisions (prioritized)
| Priority | Gap against observed buyer intent | Status before this study | Honest action on EN homepage only |
|---|---|---|---|
| P1 | Direct answer: what professional SEO services mean and who provides them | Absent as a standalone concise response | Add a short direct explanation, clarify specialist-led scope and no agency claim. Avoid generic textbook SEO essay. |
| P1 | Choice of service / entry path for different buyer needs | Cards cover technical and keyword services; consultation only near bottom | Add a concise buyer-decision row: site technical assessment vs keyword map vs consultation, each to already-published matching page. Do not offer invented retainers. |
| P1 | Cost and timelines / what influences them | No explanation on main page (in FAQ only) | Add short direct answers: price and timeline depend on site size, scope, market and access; no invented fixed prices; search results not guaranteed in a fixed interval; link to existing /faq/ for details. |
| P1 | Accountability: how to measure and review | Generic claims, but deliverables and verification block already exist | Add one concrete sentence about baseline, acceptance criteria, and who applies fixes. Avoid duplicating full technical pages. |
| P2 / BLOCKED by evidence | Trust proof: cases, ratings, years, named specialists | No validated evidence | Do **not** invent; mark PROOF_REQUIRED. Can link to genuine About/Contact. If verified examples later supplied, add separately. |
| P2 | Pricing packages, guarantees, industry badges | No approved prices/industries | Explicitly not add. Any published price/claims require owner confirmation. |
| P2 | Off-page authority building | Existing legacy link-spam offering excluded | Do NOT resurrect bulk links, tier/PBN or artificial DR simply because some competitors advertise off-page SEO. |
| P2 | AI Overview / GEO keyword variants | All tab displayed AI Overview | Do not claim ability to optimize for AI citations or invent standalone services. Existing helpful technical/on-page content supports search comprehensibility. |

## Proposed content structure, minimal change
1. Keep H1 and metadata; no rank-guarantee or experience exaggeration.
2. Keep process/featured cards, add short buyer-intent answer before eight service categories.
3. Keep eight scope cards and three output cards; add short 3-way service selection so buyer can start with the right existing page.
4. Add buyer-level micro FAQ (price factors, timing, scope vs one-time) and relevant link to /faq/. Do not add FAQPage structured data (commercial pages are generally ineligible for Google's FAQ rich results).
5. Retain working EN footer/Telegram CTA, no fake address, no large generic duplicate paragraph. All enhancements EN-only in shared template guards.

## Evidence and status
- Source: direct Google Web view through connected Opera on 2026-10-15; ten destination pages opened and headings inspected; official guidance https://developers.google.com/search/docs/fundamentals/seo-starter-guide and https://developers.google.com/search/docs/fundamentals/creating-helpful-content.
- **SERP_SNAPSHOT_VERIFIED, GEO_PHYSICAL_UNVERIFIED, GSC_PENDING, ORGANIC_KD_UNVERIFIED.** No assertion that this is exact US resident Google ranking or globally stable top10.
- Next: implement EN-only factual gaps with per-commit QA, published Preview review. No production deploy and no other locale changes.
