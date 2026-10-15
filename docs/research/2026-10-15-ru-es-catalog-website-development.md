# RU/ES website development as a separate fourth catalog service — 2026-10-15

Scope: two localized service-catalog pages and one CI update only. No changes to the English catalog while its website-development translation remains an unpublished draft.

RU /ru/uslugi/: add a fourth card "Разработка сайтов на чистом коде", target /ru/uslugi/razrabotka-saitov/.
ES /es/servicios/: add a fourth card "Desarrollo web a medida", target /es/servicios/desarrollo-web/.

The existing three service-card intents remain distinct:
1. Technical SEO (audit and fixes).
2. Keyword research, clusters and URL mapping.
3. Consultation, diagnostics and priorities.
4. Website development, landing pages and small multi-page websites with independently agreed implementation scope.

Both new pages already passed static CI (Hugo, canonical, RU↔ES alternate, no old legacy source pages, visible and sponsored hosting referral). Catalog references now point to the verified new canonical URLs. The catalog descriptions make clear that website creation is not automatically included in technical SEO or keyword research.

Source images are reused from the project's existing website-development pages; no invented portfolio images or fabricated customer metrics. Prices on the service detail pages remain explicitly historical/unconfirmed. Current commercial availability, scope and GSC migrations must still be confirmed before publication.

Release gate is still blocked: /es/soft/ and additional RU/ES homepage, about, SEO overview and FAQ legacy copy remain. This commit updates generated catalog-card tests from exactly 3 to exactly 4 in RU and ES. EN remains 3 until its own service is independently rebuilt.
