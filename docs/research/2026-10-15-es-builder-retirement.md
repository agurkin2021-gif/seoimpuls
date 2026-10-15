# ES Strategy Builder retirement — 2026-10-15

Source `content/strategy-builder/index.es.md`; public candidate route `/es/constructor-estrategias-seo/`. The legacy tool advertises "tácticas de enlaces", "construcción de enlaces adaptativa" and strategy-driven ranking control; the shared builder template contains practices incompatible with the new service scope. Suppressing only these words without modifying the tool would be deceptive.

Decision: remove the ES builder from the rebuilt Hugo output with `draft: true`. This is not a production 410 or 301 and does not decide the treatment of externally indexed URLs without live GSC/crawl evidence. The original is retained on `main`.

Fix incoming primary link: `content/_index.es.md` `heroBuilderUrl` to the existing `/es/seo/`, with button label "Servicios SEO". Secondary hero to `/es/about/`, with "Sobre nosotros". Replace homepage offerItem8 with a description of the audit-to-improvement process instead of recommending the withdrawn builder. Edit fallback in `layouts/index.html` so missing `homeJson` never regenerates a link to the withdrawn Spanish builder. RU/EN homepage navigation is unchanged.

This is an explicit link replacement within the navigation, not a misleading server 301. Both destination pages exist in source but their ES content has not been fully rebuilt under the white-hat SERP process. Avoid claiming final quality, rankings or visual QA.

Release guard: route added to `docs/retired-routes-en.txt`; `scripts/verify_retired_routes.py` must reject published files, sitemap mentions or internal links. Additional `rebuild-qa.yml` checks final link labels and target URLs via HTMLParser plus physical destination files.

No production changes, no Pages, no DNS changes. Next: retire Tier/satellite pages one at a time and then full RU/ES rewrite.
