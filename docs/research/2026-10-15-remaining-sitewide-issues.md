# SEOImpuls sitewide follow-up after RU/ES architecture — 2026-10-15

CI baseline: GitHub Actions 38794561199 PASS, context guard 38794561487 PASS, 27 retired URL checks PASS, 45 generated HTML files. White-hat informational scanner: 21 findings on 12 HTML files. This is a deterministic content/navigation test, NOT a Google penalty severity score. Release readiness: BLOCKED.

All three active language versions for these sets are reciprocal and canonical-correct in CI:
- EN /services/ · RU /ru/uslugi/ · ES /es/servicios/
- EN /services/keyword-research/ · RU /ru/uslugi/semanticheskoe-yadro/ · ES /es/servicios/investigacion-palabras-clave/
- EN /services/seo-consultation/ · RU /ru/uslugi/seo-konsultaciya/ · ES /es/servicios/consultoria-seo/

Remaining scanner findings (prioritized; individual entry may have multiple issues):
1. /uslugi-linkbildinga/sozdanie-saitov/ and /servicios-de-link-building/creacion-de-sitios-web/ : legacy website-creation pages, satellite offer and hreflang in old namespace. Decide genuine web-development deliverable, rewrite or draft; old paths require migration mapping. Do not mass-301 to SEO catalog.
2. /es/soft/ : empty legacy software section and internal self-link; remove or create a truly useful independently scoped resource.
3. /ru/index.html : old discussion of behavioral manipulation; /es/index.html : backlinks references. Requires full page-specific rewrite, not just navigational fixes.
4. /ru/seo/ and /es/seo/ : leftover old external-link descriptions. Rewrite on-page content under focused technical SEO intent; retain /ru/seo/ and /es/seo/.
5. /ru/about/ and /es/about/ : descriptions of old link-selling services. Replace with verifiable company approach; never invent staff, years or case studies.
6. /faq/ : English FAQ has backlink-language detection; inspect context and only remove irrelevant promotional content without deleting useful explanations.
7. /go/vdsina/ : the existing explicit noindex affiliate redirect is deliberately retained at owner's direction. It is NOT intrinsically forbidden; build a context-aware audit of referring pages, visible disclosure and rel=sponsored nofollow before exempting it from release scanner. RU and ES home VPS links already visibly disclosed; no software-link hijacking allowed.
8. /ru/uslugi/ : scanner flagged a negative mention of Domain Rating, removed in the corrective commit accompanying this audit. Do not include disallowed service names even in marketing disclaimers.

Technical limitations: No verified geo-specific exact top-10 Google SERP, no Search Console 3–6 month page/query exports, no migration redirects, no live HTTP/crawl, no 390/1280px browser screenshots or Core Web Vitals. None of those are considered PASS.

Next work order: first website creation RU and ES one-by-one (business scope and keyword intent review); then ES soft, RU/ES technical SEO, About, home and FAQ; validate new URL mapping and strict sitewide content gate; then visual/performance/live migration planning. Every change includes the context file in the same Git commit.
