# ES /soft/ — blank software section removed, 2026-10-15

Candidate URL: /es/soft/
Source: content/soft/index.es.md
Finding: the source has an empty builder text block with no software, feature, legitimate resource or actionable content. An empty page is not a useful answer to an SEO software query.

Action: mark the ES source as a Hugo draft and add /es/soft/ to the retired-routes manifest. Do NOT redirect this old software page to a VPS provider. A static /ru/soft/ affiliate hijack was already removed; /go/vdsina/ remains as a separate explicit, noindex optional hosting referral when thematically relevant.

The shared homepage template previously provided a /es/soft/ or /soft/ fallback URL for card 2 if an explicit value was not supplied. Now it renders this card only when the language's homeJson includes an actual URL, preventing broken and unrelated fallback links. Current EN/RU/ES home pages all have explicit configured card-2 URLs; no approved actual CTA destinations were changed.

No fake new software product is created. Any future tools/resources section needs a separate, useful intent and actual content.

Live 301/410/404, GSC clicks, crawls and referring links were not checked. No production deployment, Pages, main or source backups changed. The CI sitebuild tests are necessary but not visual QA.
