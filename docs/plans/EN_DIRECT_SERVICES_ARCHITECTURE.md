# SEOImpuls: English direct service architecture
Date: 2026-10-16. STATUS: EDITED_QA_PENDING. Branch: white-seo-rebuild.

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
