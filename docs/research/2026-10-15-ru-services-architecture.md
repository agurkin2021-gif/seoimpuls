# SEOImpuls RU service taxonomy — localized architecture decision
Date: 2026-10-15.
Status: new candidate URL /ru/uslugi/; source baseline retained in main.

Ownership and intent map:
- /ru/ : branded/general SEO agency value proposition and conversion.
- /ru/uslugi/ : navigational catalog of concrete, truthful services. Query cluster "SEO-услуги".
- /ru/seo/ : technical SEO evaluation, indexation and fixes; NOT the general services catalog.
- /ru/uslugi/semanticheskoe-yadro/ : keyword research, query grouping, intent and URL assignments.
- /ru/uslugi/seo-konsultaciya/ : advisory discussion and prioritization of a defined website problem.

Catalog has exactly three legitimate offers with matching images and buttons. Old website/satellite development cards removed from this new catalog pending a separate deliverability and intent review; legacy source page still requires retirement or clean redesign.

Comparison examples (SERP_UNVERIFIED, not claimed as an exact Google top-10 for a fixed geography):
- https://websniper.ru/seo/semanticheskoe-yadro/
- https://seo-bundle.com/ru/semantic-core/
- https://site-up.ru/seo-konsultacziya
The comparisons support differentiating deliverables, but no SERP rankings/volume or impact claims are asserted.

Changed dependencies: RU homepage SEO service card and meta description, /ru/seo/ catalog CTA, RU Hugo main-menu (catalog + Technical SEO separately), and template fallback for RU homepage.

Translation: shared translationKey=services links RU catalog with EN /services/ and later Spanish /es/servicios/. Canonical is self. HTML build test verifies expected URLs, H1, canonical, en-us hreflang and three cards.

Migration policy: historical /uslugi-linkbildinga/ is a withdrawn link-selling category, not a same-intent equivalent of clean SEO catalog. No blanket production 301. After GSC/traffic/referrers and live verification, choose 404/410 or another justified action. Valid old keyword and consultation services are independently proposed 301 targets and their old page URLs are already in retired test manifest.

Open: exact Google organic top-10 / geo/device/date, GSC impressions and indexation, real redirects, mobile/desktop visual review, CWV, complete RU homepage and SEO overview cleanup. No live server changes.
