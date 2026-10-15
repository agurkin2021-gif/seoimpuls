# SEOImpuls — основной контекст проекта (читать первым)

КРИТИЧЕСКОЕ ПРАВИЛО ПОЛЬЗОВАТЕЛЯ: ПОСЛЕ КАЖДОГО ИЗМЕНЕНИЯ ПРОЕКТА обновлять ЭТОТ ФАЙЛ в том же Git-коммите, что и изменение. Никаких коммитов с правкой сайта без обновления контекста. Если изменения внесены через несколько технических коммитов, каждый такой коммит обязан содержать актуализацию этого файла. Журнал должен позволять начать работу в другом чате без восстановления истории переписки.

## 1. Проект, доступ и границы

- Название: SEOImpuls.
- Производственный сайт: https://seoimpuls.com/.
- Приватный GitHub-репозиторий: https://github.com/agurkin2021-gif/seoimpuls.
- Система: Hugo Extended, языки английский в корне, русский /ru/, испанский /es/.
- main — архив исходной версии; white-seo-rebuild — ветка для переделки.
- Ни в коем случае не изменять производственный сервер, DNS, CDN и Search Console без отдельного прямого разрешения пользователя.
- Никакой публикации исходного сайта через GitHub Pages. Никаких auto-deploy на сервер.
- Прежние SEO-материалы содержат предложения из области манипулятивного линкбилдинга. Сохранённый исходник НЕ является новой одобренной редакцией сайта.
- Секреты, данные доступа, SSH, .env, персональные данные и служебные дампы не включать в Git. Репозиторий приватный, но это не заменяет санитарную проверку.

## 2. Бизнес-цель и критерии

Полная постраничная пересборка сайта под настоящее, полностью белое SEO — не словесная маскировка серых методов. Исключить коммерческие предложения массовых обратных ссылок, автоматического размещения (XRumer, GSA, XEvil), PBN и сателлитов, Tier-каскадов, искусственного DR, ссылочного спама и обещаний гарантированного топа. Услуги предлагать только такие, которые команда реально оказывает. Реальные направления: technical SEO, on-page SEO, диагностика индексации, семантика и исследование интентов, информационная архитектура и перелинковка, стратегия контента, international SEO, SEO-консультации. Не придумывать кейсы, достижения или клиентов.

Каждая страница:
1. Инвентаризация исходного URL, текущего содержимого, Title, H1, canonical, hreflang, внутренних ссылок.
2. Актуальный SERP top-10 без рекламы по целевому языку/гео; intent map, конкуренты, gaps; отделять проверенные данные от гипотез.
3. Новый уникальный запрос/интент, Title, H1, URL, meta, контент. Не каннибализировать соседние страницы.
4. Сохранение дизайна/структуры и работоспособности, проверка мобильной версии, ссылок, structured data, alt, доступности.
5. Обоснованная миграция старых URL: 301 только к семантически соответствующему преемнику; иначе 404/410 и убрать из sitemap и внутренних ссылок.
6. Сборка Hugo, проверка английского, русского, испанского адресов; контроль отсутствия серых услуг и вводящих в заблуждение обещаний.
7. Обязательно в ТОМ ЖЕ КОММИТЕ обновить этот файл с тем, что сделано и проверено, нерешёнными вопросами и следующим действием.

## 3. Исходники / импорт — состояние на 2026-10-15

- Пользователь загрузил полный архив с сервера: Seoimpuls-all-sources-2026-10-15.zip (92 745 534 байта).
- В рабочей среде подготовлена очищенная копия: SeoImpuls_GitHub_ready.zip, 20 920 516 байт, 2886 файлов, суммарно 35 713 843 байта без сжатия.
- SHA-256 подготовленного ZIP: 764e5fc804588a7877b78143047d0e8fe823d85866b4e14139fd3525c55dc70a.
- В подготовленной копии Hugo source, контент, шаблоны, CSS/JS, статические файлы, админка, _vendor, правила сборки, docs/IMPORT_AUDIT.md, docs/REBUILD_PLAN.md, docs/URL_INVENTORY_BASELINE.csv.
- Из проекта исключены публикация server-current/public, конфигурация сервера и доступа, старые backup, node_modules, временные и посторонние файлы.
- Исходная копия для работы не равна гарантированно побайтово опубликованному состоянию: публикация VPS в архиве может отличаться.
- Подготовленный ZIP находится в беседе ChatGPT и требуется для первичной загрузки. После успешного импорта оставлять ZIP в репозитории не нужно.
- В среде ChatGPT исходники не удалось отправить прямым git push (сетевая среда не разрешает доступ к github.com). Через подключённый GitHub доступно редактирование текстовых файлов, но не прямая загрузка ZIP как двоичного Git-объекта.

IMPORT_STATUS: completed

## 4. Порядок ввода репозитория

1. Репозиторий приватный, уже создан пользователем с README.md на main.
2. В main добавляются этот контекст, AGENTS.md, документация и безопасный импортный GitHub Actions workflow в одном коммите. GitHub Pages не включать.
3. Нужно загрузить SeoImpuls_GitHub_ready.zip в корень main через Add file > Upload files. Архив меньше лимита веб-загрузки GitHub.
4. Workflow import-source.yml проверяет контрольную сумму, структуру и содержимое ZIP, собирает Hugo, удаляет ZIP из отслеживаемого Git, коммитит исходники + актуализирует данный контекст и создаёт white-seo-rebuild.
5. Проверить вкладку Actions и наличие content/, layouts/, hugo.toml в main, а также рабочей ветки. При неудаче импортного job смотреть журнал; не утверждать, что источники в GitHub, пока этого не видно.
6. После успешного импорта выполнять исправления только в white-seo-rebuild с синхронным контекст-логом. Не менять main, не включать Pages и не развёртывать в продакшн.
7. Перед новым чатом прочитать AGENTS.md и этот файл прямо из репозитория, проверить фактическое состояние GitHub/Actions и продолжить с секции 6 «Следующее действие».

## 5. Журнал изменений (новые записи сверху; обновлять в каждом коммите)

### 2026-10-15 — RU/ES catalogs include independent website development service
- Previous ES dev commit 4cbbe2d1: Hugo #38796764348 PASS, context #38796764349 PASS, 29 retired routes, 45 generated HTML, 15 diagnostics/11 files; RU/ES H1, canonical, mutual hreflang, relevant links and sponsored affiliate labels passed. No live deploy; new site-dev offer needs current business/pricing confirmation before production.
- Added a fourth honest card to content/services/_index.ru.md at /ru/uslugi/razrabotka-saitov/ and content/services/_index.es.md at /es/servicios/desarrollo-web/. Source images reused; old 3 SEO service cards not moved. Added content explanation distinguishing site development from audits, keyword research and consultation. EN catalog remains 3 while EN web dev translation is draft.
- Updated .github/workflows/rebuild-qa.yml strict RU and ES service-catalog checks to 4 exact expected cards and continued reciprocal EN/RU/ES hreflang for existing translated SEO services. Rationale docs/research/2026-10-15-ru-es-catalog-website-development.md.
- CI for current commit PENDING; correct any card pairing or link issues before moving on. Old web-development pages remain retired only in rebuilt Hugo, not live; all 301/410 decisions pending GSC. Full release remains BLOCKED.
- Next: remove /es/soft/ empty service from candidate and check no incoming links; then clean RU/ES About and SEO overview/Home and FAQ. Preserve explicit /go/vdsina/ affiliate redirect without misleading automatic /soft/ rewrites.

### 2026-10-15 — ES website development migrated from satellite mixed offer
- Previous RU website-development commit e82b4843: Hugo build #38796288559 PASS and context guard #38796289464 PASS. Retired routes 28, 45 generated HTML, 17 diagnostic findings in 11 pages, RELEASE BLOCKED. New RU /ru/uslugi/razrabotka-saitov/ canonical, related SEO links and properly disclosed optional VPS affiliate checked.
- Replaced content/services/website-creation/index.es.md with legitimate scoped web-development page at /es/servicios/desarrollo-web/ (H1 «Desarrollo web a medida para empresas»). Removed satellite/ranking claims and made pricing of US$75/$16 historical and subject to confirmation. Existing translationKey services-website-creation retained, with ES and RU as available variants; EN version remains draft.
- Old /servicios-de-link-building/creacion-de-sitios-web/ added to docs/retired-routes-en.txt. SEO intent, public competitor examples and migration caveats in docs/research/2026-10-15-es-web-development-migration.md. Real exact Google top-10 SERP, GSC/live HTTP/referring links, and actual current business rates still UNVERIFIED. No production 301/410.
- .github/workflows/rebuild-qa.yml now checks generated RU/ES mutual hreflang, titles, canonical, local related links and clearly labeled sponsored/nofollow VPS referral. CI result for this commit PENDING.
- The new website development page is not yet a fourth card in the RU/ES SEO services catalog: expand catalogs after checking pages and confirming product terms; do not disturb three existing SEO intents or fake an EN page.
- Main, live server, DNS, GitHub Pages and partner endpoint unchanged. Next: CI; decide whether to add RU/ES website development as complementary cards; then remove /es/soft/ empty archive and rewrite RU/ES SEO/About/home copy.

### 2026-10-15 — RU website creation migrated out of old link-selling namespace
- Baseline commit c07b0c29: Hugo #38794930874 PASS and context guard #38794930526 PASS; 27 retired routes and 20 informational audit findings in 11 HTML; release BLOCKED.
- Inspected content/services/website-creation/index.ru.md: legacy product combines honest responsive website development with a satellite package and other questionable claims. Replaced with a practical, bounded website-development offer using real source capabilities: small landing/multipage sites, semantic markup, mobile layout, basic technical SEO, conditional DNS/HTTPS and handover; NO satellite packages or ranking guarantees.
- New clean candidate URL /ru/uslugi/razrabotka-saitov/, Title/H1 «Разработка сайтов на чистом коде», preserved translationKey=services-website-creation and relevant image. Historical $75/$16 is labeled not an approved present tariff; confirm current business offering and terms before release. Clearly labeled optional VPS referral /go/vdsina/ with sponsored/nofollow must be checked in generated HTML.
- Old /uslugi-linkbildinga/sozdanie-saitov/ appended to docs/retired-routes-en.txt; no live redirect/410. docs/research/2026-10-15-ru-web-development-migration.md documents a publicly sampled competitor comparison (NOT exact Google top 10), intent, gaps, URL migration and unknown GSC. Updated blocking QA to verify H1, canonical, internal links, old URL absence, and single explicitly disclosed affiliate.
- Current commit CI pending. Full original kept in main. RU/ES catalogs still show exactly three already-reviewed SEO offers; development service is not added as a fourth card until both locales and offering scope are checked. Existing EN translation remains draft.
- Next: check current CI; separately rebuild ES /servicios-de-link-building/creacion-de-sitios-web/ at /es/servicios/desarrollo-web/, preserving translationKey and reviewing pricing. Then consider RU/ES catalog cards together and move to /es/soft/. No live server, DNS, Pages or main changes.

### 2026-10-15 — RU/ES architecture quality gate confirmed; remaining issues inventoried
- Previous ES catalog commit 91a86bf5: GitHub Actions #38794561199 PASS (Hugo, 27 retired routes over 45 HTML, 3-page RU/ES/EN catalog + keyword + consultation reciprocal hreflang, canonical and cards), context #38794561487 PASS. Whole-site diagnostic 21 findings in 12 HTML; site release BLOCKED.
- Fixed content/services/_index.ru.md: removed the leftover negative advertising reference to artificial Domain Rating and link networks; instead clarified verification criteria. This is only a local copy correction; 3 RU cards and all paths unchanged.
- Added docs/research/2026-10-15-remaining-sitewide-issues.md with exact affected page groups, planned remediation order and clear separation between gray offers and permitted explicitly labelled /go/vdsina/ affiliate.
- Complete RU/ES canonical and translation architecture is verified in static CI; not a claim that all RU/ES copy, SERP or visual QA is finished. No server, DNS, GitHub Pages, production redirects or main changes.
- New context-only/copy commit needs its own CI confirmation; target is <=20 remaining scanner findings (no broad unjustified suppression). Next step: audit/rebuild RU/ES website-creation old pages under independent genuine intent or retire them safely, preserving historical signals after GSC.

### 2026-10-15 — ES clean SEO catalog replaces link-selling hub
- Previous ES consultation commit fc75fac8: Hugo #38794106882 PASS, context #38794106978 PASS, ES consultation new H1/canonical/EN-RU alternates and old URL retirement; 26 retired routes, 38 diagnostics in 16 HTML, RELEASE BLOCKED.
- content/services/_index.es.md rebuilt as /es/servicios/ with H1/Title «Servicios SEO para sitios web», 3 honest cards linking /es/seo/, /es/servicios/investigacion-palabras-clave/, /es/servicios/consultoria-seo/; translationKey services retained.
- content/_index.es.md: homepage brand SEO title/description, first service card and link corrected (VPS affiliate block retained). content/seo/index.es.md catalog CTA corrected; layouts/index.html ES fallback labels, URLs, SEO icon corrected; hugo.toml ES menu now has Servicios SEO catalog and SEO técnico detail.
- Old /servicios-de-link-building/ added to docs/retired-routes-en.txt for build/link/sitemap gate. docs/research/2026-10-15-es-services-architecture.md maps unique intents and notes SERP_UNVERIFIED. NOT a same-intent redirect to the new clean catalog.
- QA extended for ES hub 3 cards, title/canonical, menu, homepage, three-way EN/RU/ES canonical/hreflang for hub/keyword/consult. New Actions for current commit PENDING; strict release remains BLOCKED by other gray RU/ES and sitewide QA. Main, DNS, server, Pages unchanged.
- Next: inspect all latest Actions, verify no broken links and hreflang, inventory remaining legacy gray active pages and review website creation. Then full post-page SERP/on-page audit RU/ES and final release test; live migration requires separate owner authorization.

### 2026-10-15 — ES SEO consultation migrated to clean service URL
- Previous ES keyword migration commit 47926dc5: Hugo CI #38793772992 PASS and context guard #38793772952 PASS. New /es/servicios/investigacion-palabras-clave/ H1/canonical/EN-RU alternates passed; 25 retired URLs, site scanner 44 findings/18 affected pages. RELEASE BLOCKED.
- Rebuilt content/services/seo-consultation/index.es.md at /es/servicios/consultoria-seo/ with H1 «Consultoría SEO para sitios web», advisory search intent and distinct content from ES keyword/technical pages. Replaced corrupt legacy description, unlimited lifetime support and link-selling offers; old US$350/three hours explicitly historical pending confirmation.
- Updated two old-link references in ES catalog from /servicios-de-link-building/consultoria-seo/ to new /es/servicios/consultoria-seo/. Retired former URL in docs/retired-routes-en.txt. Same-intent 301 only PROPOSED at future production migration; main and live site unchanged.
- docs/research/2026-10-15-es-consultation-migration.md documents competitor comparisons (SERP_UNVERIFIED, no exact geo-fixed top-10) and intent/limitations. New QA checks built ES canonical/H1 and EN-RU hreflang, new keyword link and absence of old URL; CI pending.
- Next: after PASS build ES /es/servicios/ clean catalog, update ES menu/home/SEO CTA, verify old hub absence, reciprocal hreflang and all three service destinations. Then cross-locale SEO QA, remaining legacy pages still BLOCKED.

### 2026-10-15 — ES keyword research migrated to clean commercial URL
- Previous RU services hub commit 5a9543f8: Hugo #38793415941 PASS, context #38793416117 PASS; /ru/uslugi/ self canonical, EN hreflang, three live SEO service cards, new menu/home link, 24 retired URLs and 50 whole-site diagnostic findings; RELEASE BLOCKED.
- Rebuilt content/services/keyword-research/index.es.md under /es/servicios/investigacion-palabras-clave/ with Title/H1 «Investigación de palabras clave para SEO»; own commercial intent, eight detailed content sections, historical US$90 conditional on scope and no ranking guarantees. translationKey remains services-keyword-research, enabling EN and RU hreflang.
- Updated exact two ES old inbound references from /servicios-de-link-building/palabras-clave/ in old ES catalog and ES website-creation source, registered old URL in docs/retired-routes-en.txt. Same-intent 301 only proposed for future live migration.
- Search-intent evidence in docs/research/2026-10-15-es-keyword-migration.md, SERP_UNVERIFIED (not exact Google top 10/geo). QA checks ES H1/canonical/RU/EN alternates and absence of old route. New CI pending; ES hub still old until consultation and then parent migration. No server/main changes, visual QA and GSC pending.
- Next: verify this CI, then ES consultation /es/servicios/consultoria-seo/ with old-hub inbound link update, then clean ES catalog /es/servicios/.

### 2026-10-15 — RU clean SEO catalog and primary navigation rebuilt
- Previous RU consultation commit f956fcbc passed Hugo #38792517329 and context guard #38792517336. True RU keyword and consultation pages now exist independently of the old link-building namespace.
- content/services/_index.ru.md: new canonical /ru/uslugi/, H1 «SEO-услуги для сайта», only 3 truthful cards for /ru/seo/, /ru/uslugi/semanticheskoe-yadro/ and /ru/uslugi/seo-konsultaciya/; translationKey services retained for EN/RU/ES alternates. No old link-selling/satellite offer in this new catalog.
- Updated RU main in content/_index.ru.md, CTA inside content/seo/index.ru.md, RU navigation in hugo.toml (catalog plus separate technical SEO), RU homepage template fallback/card copy and icon in layouts/index.html. Old /uslugi-linkbildinga/ added to docs/retired-routes-en.txt for build and link checking.
- Report docs/research/2026-10-15-ru-services-architecture.md records intent ownership, sample evidence and SERP_UNVERIFIED; no unverified rank proof claimed. The other languages and shared EN services source unchanged.
- CI of this commit pending: generated RU catalog with exactly 3 correct card hrefs, self canonical, EN hreflang, RU homepage link, menu and old retired route absence must pass. Main, server, DNS, Pages untouched. No final 301/410 decisions; full release still BLOCKED (other RU and ES legacy pages, GSC, visual QA).
- Next after CI: ES keyword /es/servicios/investigacion-palabras-clave/ and consultation /es/servicios/consultoria-seo/, then /es/servicios/ catalog with homepage, menu and hreflang. Maintain per-commit context.

### 2026-10-15 — RU SEO consultation migrated to independent white SEO URL
- Previous RU keyword commit 516da541 CI #38792210897 PASS, context guard #38792210910 PASS: /ru/uslugi/semanticheskoe-yadro/ H1/canonical/en-us alternate, old URL retired and no stale links, 68 diagnostic findings in 20 HTML. Release BLOCKED.
- Replaced content/services/seo-consultation/index.ru.md with substantive white SEO advisory content at /ru/uslugi/seo-konsultaciya/; retained translationKey for EN/ES matching, clear advisory vs technical-audit vs semantic clustering intent. Removed corrupt source meta and claims of perpetual support, mass link-selling topics, ranking guarantees. Prior $350/three hours explicitly marked historical pending confirmation.
- Updated exact referring RU hub links /uslugi-linkbildinga/seo-konsultaciya/ → /ru/uslugi/seo-konsultaciya/; registered old route as candidate withdrawn in docs/retired-routes-en.txt (only proposed future relevant 301, NOT live). New source evidence doc docs/research/2026-10-15-ru-consultation-migration.md with SERP_UNVERIFIED sample competitive pages.
- New QA validates generated H1, canonical, hreflang EN, real RU keyword internal link and old route absence. CI for THIS commit pending. RU hub still displays old category/name and is next. Main/production untouched, visual QA and GSC pending.
- Next: rebuild RU /ru/uslugi/ as the legitimate non-gray catalog, change homepage card and RU primary navigation; inspect cross-language and legacy hub links. Then ES analogues.

### 2026-10-15 — RU keyword research migrated to independent white SEO URL
- Previous commit f312bb56: Hugo build #38791068670 PASS and context #38791068844 PASS; old sales 21 routes removed, 45 HTML; sitewide scanner 74 findings in 20 HTML, RELEASE BLOCKED.
- Rewritten content/services/keyword-research/index.ru.md: new canonical /ru/uslugi/semanticheskoe-yadro/; H1/Title «Сбор семантического ядра и кластеризация запросов», commercial intent distinct from /ru/seo/, original translationKey preserved. Eight meaningful sections: input, formats, intent clustering, methodology, deliverables, pricing caveat, FAQ, contact. Historical $90 is explicitly pending confirmation; no false guarantees.
- Updated RU catalog inbound links and old website-creation embedded keyword-service link from /uslugi-linkbildinga/sbor-semanticheskogo-yadra/ to /ru/uslugi/semanticheskoe-yadro/. Registered withdrawn candidate old URL in retired-route manifest to fail on remaining links/HTML/sitemap. New research docs/research/2026-10-15-ru-keyword-migration.md with competitor URLs and explicit SERP_UNVERIFIED: search examples are NOT exact verified Google top-10.
- Tests for this commit require Hugo build, new page canonical/H1 and absence of old URL, link audit, context guard; live 301 has NOT been applied and must await GSC and live traffic/referrers, no server or main changes. Existing RU catalog still has old parent namespace until its own migration and is not release-ready.
- Next: after CI, rebuild RU consultation with independent /ru/uslugi/seo-konsultaciya/, then replace RU catalog and homepage/menu references, and finish ES equivalents. Visual QA still pending.

### 2026-10-15 — ES artificial Domain Rating offer and misleading catalog links retired
- Previous ES Backlinks commit bda3c0d3: Hugo + retired URL check #38790748502 PASS; context #38790748461 PASS. Candidate: 46 HTML, 20 retired URLs, 80 diagnostics in 21 pages, RELEASE READINESS BLOCKED.
- content/services/domain-rating/index.es.md now contains only a draft archival stub under /servicios-de-link-building/domain-rating/; full historical page remains in main. Old artificially elevated third-party metric service is no longer offered in rebuilt site.
- In content/services/_index.es.md removed exactly two old cards: «Domain Rating» button misleadingly linking to '/' and matching unl inked image. Existing genuine consulting/semantics/site-creation elements unchanged; no claims of their full quality readiness.
- docs/retired-routes-en.txt adds /servicios-de-link-building/domain-rating/ and docs/research/2026-10-15-es-dr-retirement.md records migration decision. This commit must pass Hugo, retired-route and context guard QA.
- All six direct old RU/ES gray service page candidates (RU link strategy, backlinks, DR; ES link strategy, backlinks, DR) are retired. But two parent catalogs still have legacy URL/name/content, and RU/ES homepage/SEO/service content needs further work. Full strict release gate BLOCKED.
- No production HTTP changes, 301/410, Page publication, GSC export, browser/visual QA, or new affiliate removal. Main and server unchanged.
- Next after CI: inspect residual whole-site scanner and plan clean /ru/uslugi/ and /es/servicios/ with same-intent migration of genuine keyword research/consultation before retiring parent legacy hubs. Do not auto-redirect gray hubs to generic pages.

### 2026-10-15 — ES Backlinks discontinued page and fake catalog CTA withdrawn
- Previous ES link-strategy commit 29e6cb9c: CI #38790360032 Hugo+retired-routes PASS; context guard #38790360037 PASS; 19 retired URLs across 47 HTML, 85 diagnostic findings/22 affected pages, release BLOCKED.
- content/services/backlinks/index.es.md replaced in white-seo-rebuild with a small draft-only stub; full original saved in main. Old URL /servicios-de-link-building/backlinks/.
- content/services/_index.es.md: removed exactly two obsolete blocks, including a fake «Backlinks» button formerly pointing to homepage '/' and a matching image without a destination. True commercial SEO services kept intact.
- Added URL to docs/retired-routes-en.txt, report docs/research/2026-10-15-es-backlinks-retirement.md. New CI must confirm output and links; GSC, 301/410, external links and live audit still missing. Main, production and /go/vdsina/ unchanged.
- Next: when CI PASS, ES artificial Domain Rating page and misleading button/image; then review remaining old RU/ES hubs and legitimate service migration. Strict release gate BLOCKED.

### 2026-10-15 — ES paid tier link strategy retired and homepage link corrected
- Previous RU DR commit d26527d7: Hugo and retired URL CI #38790050825 PASS; context guard #38790050904 PASS. Retired URL count 18 over 48 HTML; diagnostic findings 93 in 23 files; RELEASE READINESS BLOCKED.
- /servicios-de-link-building/estrategia-de-link-building/: old multi-level link sales removed from the white-seo-rebuild candidate by replacing content/services/estrategia-de-link-building/index.es.md with an unpublished draft stub; full original remains in main.
- Two matching blocks (catalog image and button) removed in content/services/_index.es.md. content/_index.es.md newsUrl changed from retired page to /es/news/. In docs/retired-routes-en.txt added old URL; docs/research/2026-10-15-es-linkstrategy-retirement.md records scope/URL migration.
- CI for this commit is still pending; check generated HTML and sitemap, incoming links and missing target /es/news/. No live 301/410, GSC, browser or PageSpeed verification done. Other genuine services and VDSina affiliate endpoint untouched. Source main and production not modified.
- Next after CI: retire ES Backlinks and artificial DR cards; then replace old catalog hubs with new legitimate taxonomy and migrate keyword research/consultation after SERP/GSC.

### 2026-10-15 — RU artificial DR service withdrawn from candidate
- RU Backlinks commit 0aca4373: Hugo / retired-route check #38789774355 PASS; context guard #38789774377 PASS. Candidate: 49 HTML, 17 retired URLs, 101 scan findings in 24 files; release BLOCKED.
- /uslugi-linkbildinga/uvelechenie-domen-reytinga/ has been replaced in the working branch by a minimal draft stub; full original remains in main. The previous offering sold artificial growth of Ahrefs Domain Rating rather than a legitimate Google SEO deliverable.
- content/services/_index.ru.md: removed exactly two matching image/button blocks, preserving the genuine keyword research, consultation and website creation cards. Added route to docs/retired-routes-en.txt. See docs/research/2026-10-15-ru-domain-rating-retirement.md.
- Upcoming CI must verify Hugo build, absence of retired URL and incoming links, and updated context. No server 301/410, GSC/referring links not reviewed, original main and /go/vdsina/ unchanged.
- RU direct gray-service page pass is complete, but RU legacy hub, homepage and legal service pages still require substantial SEO/URL work. Next: ES estrategia, backlinks and DR in independent commits, then migrate legitimate services and hub.

### 2026-10-15 — RU paid backlink package unpublished and catalog links removed
- Previous commit 60c2937b: Hugo build and retired-route check #38789334524 PASS; context guard #38789334373 PASS. Scanner 108 findings / 25 affected files across 50 HTML; 16 retired routes all absent; release still BLOCKED.
- Old route /uslugi-linkbildinga/obratnye-ssylki/ removed from candidate public output. Instead of leaving the large commercial copy in the working branch, content/services/obratnye-ssylki/index.ru.md replaced with a minimal draft-only archival stub; full original remains untouched in main.
- Exactly two catalog entries (button and image) removed from content/services/_index.ru.md, without changing legitimate keyword research, consultation and website creation entries. Added the old URL to docs/retired-routes-en.txt. Assessment: docs/research/2026-10-15-ru-backlinks-retirement.md.
- The draft and generated URL/link checks must pass GitHub Actions for this commit before next page. No actual server 410/301, GSC not exported, canonical/referring links unverified, no action on production or affiliate endpoints.
- Next: after CI PASS, audit/retire RU artificial Domain Rating page, then ES link strategy, backlinks and DR, each separately and with persistent context.

### 2026-10-15 — RU link-building sales page retired
- Previous white-seo-rebuild commit 5fb8666e: GitHub Actions 38788366497 (Hugo and retired route validation) PASS and 38788366136 (context guard) PASS. 15 retired URLs, 51 HTML pages, 117 informational scan findings in 26 files; release blocked.
- content/services/linkbilding/index.ru.md: draft:false → true; old URL /uslugi-linkbildinga/linkbilding/ no longer appropriate (paid tiered links via forums/blogs).
- content/services/_index.ru.md: removed exactly 2 matching image/button blocks. content/_index.ru.md: replaced old home newsUrl with /ru/news/; all other homepage elements retained. Registered the URL in docs/retired-routes-en.txt; details in docs/research/2026-10-15-ru-linkbuilding-retirement.md.
- Test before declaring pass: new Hugo Actions and context guard, no generated former page/inbound links, /ru/news/ destination. No live 301/410 and no production, main, Pages or affiliate endpoint changes.
- Next: after passing CI, retire RU /uslugi-linkbildinga/obratnye-ssylki/, then RU artificial DR, followed by ES equivalents. Preserve genuine keyword research and consulting content.

### 2026-10-15 — ES satellite/microsite sales withdrawn from candidate
- Previous RU satellite commit 1def6013: Hugo build #38788100026 PASS, context guard #38788099520 PASS, retired routes 14 / 52 HTML PASS, diagnostic 123 findings in 27 HTML files, RELEASE READINESS BLOCKED.
- content/services/desarrollo-de-micrositio/index.es.md: draft:false → true for /servicios-de-link-building/desarrollo-de-micrositio/. The source bundled microsites/satellites with guaranteed first-page Google positions and authority placements; this is withdrawn without pretending the same intent is served by honest SEO services.
- Removed exactly two matched ES catalog blocks (image + button) in content/services/_index.es.md and added route to docs/retired-routes-en.txt. Scope/risk documented in docs/research/2026-10-15-es-microsite-retirement.md. No changes to other catalog entries.
- No live HTTP 301/410, no change to main, GitHub Pages or production. GSC/referring links and live URLs are UNKNOWN; future REVIEW_BEFORE_410 decision remains conditional. Contextual affiliate /go/vdsina/ preserved; gray page affiliate link simply no longer generated.
- This commit's Actions still pending. The four requested RU/ES Tier and satellite URLs are now draft in work branch; must verify Actions and check remaining risks before claiming complete sitewide white SEO.
- Next: verify new CI; inspect all remaining legacy RU/ES catalog pages, SEO homepages, sitemap, source and HTML; prioritize disarming both old link-building hubs and sales of backlinks/DR, then verify lawful same-intent service migrations.

### 2026-10-15 — RU satellite promotional page removed from candidate
- Previous ES Tier commit 25051e7c: Hugo #38787834456 PASS and context guard #38787834442 PASS. Retired-route check: 13 URLs over 53 HTML, zero stale links; 131 whole-site diagnostic findings in 28 files, release BLOCKED.
- Source content/services/sozdanie-satellitov/index.ru.md → draft:true for /uslugi-linkbildinga/sozdanie-satellitov/. Current page bundled site creation with satellite ranking schemes, guaranteed Google Top and paid authority placements, hence not a legitimate same-intent white SEO replacement.
- Removed exactly two corresponding RU catalog blocks (image and button) in content/services/_index.ru.md, keeping other services for their own audit. Added route to docs/retired-routes-en.txt for CI; rationale docs/research/2026-10-15-ru-satellites-retirement.md.
- Main/production/Pages untouched; no 301/410 actions on server. GSC/live indexing/backlink analysis still pending. Genuine website development to be evaluated separately under independent legitimate intent. VDSina explicit endpoint unchanged, but affiliate reference inside retired gray content no longer rendered.
- New CI pending; next: verify result, then separately retire ES legacy satellite/microsite page and its 2 catalog cards. Whole site still RELEASE READINESS BLOCKED.

### 2026-10-15 — ES Tier 1–2–3 withheld and removed from ES catalog
- RU Tier commit 603d15b9: Hugo #38787608283 PASS and context guard #38787608200 PASS; retired check 12 URLs/54 HTML, whole-site diagnostic 140 findings/29 affected files, RELEASE READINESS BLOCKED.
- content/services/tier-1-2-3/index.es.md: draft false → true for /servicios-de-link-building/tier-1-2-3/. Removed precisely two blocks referencing this URL (ES catalog image and corresponding button) from content/services/_index.es.md. Other catalog products left for separate passes.
- Registered /servicios-de-link-building/tier-1-2-3/ in docs/retired-routes-en.txt; generated pages, internal links and sitemap are validated by scripts/verify_retired_routes.py in GitHub Actions. Context/evidence: docs/research/2026-10-15-es-tier-retirement.md.
- The old Tier transaction is not equivalent to a legitimate technical SEO service, so no artificial 301 to generic SEO. Future 410 merely proposed pending live/GSC/referring-link audit; production, main and Pages unchanged. The affiliate redirect /go/vdsina/ was not removed.
- New CI pending, then RU satellite /uslugi-linkbildinga/sozdanie-satellitov/ page and exactly matched catalog card, followed by ES microsite/satellite. Strict release gate still BLOCKED.

### 2026-10-15 — RU Tier 1–2–3 removed from Hugo candidate and service cards
- Previous commit f8c1985c: Hugo rebuild + RU/ES CTA and retired URLs #38787065170 PASS; context guard #38787065220 PASS. Baseline diagnostic had 151 issues across 30/55 HTML files, RELEASE READINESS BLOCKED.
- Source content/services/tier-1-2-3/index.ru.md: draft:false → true for /uslugi-linkbildinga/tier-1-2-3/. Removed exactly two referring builder blocks (image + button) from content/services/_index.ru.md, without editing the remaining catalog cards.
- Added /uslugi-linkbildinga/tier-1-2-3/ to docs/retired-routes-en.txt. The blocking verify_retired_routes.py tests generated HTML pages, links and sitemap. Research and migration rationale in docs/research/2026-10-15-ru-tier-retirement.md. Existing pricing or Tier-network SEO copy is not repurposed.
- No new white SEO service pretended to fulfil the old tier package. Future 410 candidate remains only a migration plan pending GSC/live/backlink audit. /go/vdsina/ partner redirect and other related, genuinely contextual placements kept; links inside retired gray page vanish as that page is unpublished.
- This commit's CI is pending; next is confirm both checks and fix any remaining references before proceeding to ES Tier. Main/server/Pages unchanged; strict sitewide gate remains BLOCKED.

### 2026-10-15 — ES legacy SEO Strategy Builder retired; homepage entry points corrected
- Предыдущий RU step commit 0426a46e: GitHub Actions Hugo+retired-route+RU hero validation #38786675935 PASS, project context #38786676085 PASS. Было 152 находки в 31 из 56 HTML; strict release gate BLOCKED.
- content/strategy-builder/index.es.md: draft:true; /es/constructor-estrategias-seo/ перестаёт генерироваться обычным Hugo. Старый контент сочетал link-building tactics и контролируемый рост позиций, поэтому не подходит для новой белой SEO-компании.
- content/_index.es.md: heroBuilderUrl → /es/seo/, heroCasesUrl → /es/about/, offerItem8 убрал ссылку на старый конструктор. layouts/index.html: испанские подписи CTA → «Servicios SEO» / «Sobre nosotros», ES fallback → /es/seo/. EN/RU CTA не менялись.
- docs/retired-routes-en.txt: добавлен /es/constructor-estrategias-seo/. В .github/workflows/rebuild-qa.yml добавлен парсер generated ES HTML, проверяющий реальные URL, подписи и наличие страниц назначения. docs/research/2026-10-15-es-builder-retirement.md описывает SEO-решение и отсутствие live-редиректа.
- Файл контекста обновлён в том же коммите. GitHub Actions данного коммита ещё предстоит проверить; при найденных старых ссылках исправить конкретный источник. Исторический URL не получает 301/410 до live/GSC проверки. Страницы ES SEO/About остаются legacy и требуют последующего SERP/контент-аудита, не считать их готовыми.
- Далее: CI, затем по одной отключать RU/ES услуги Tier/сателлитов с сохранением честной тематической партнёрки на отдельных уместных страницах. Main/production/Pages без изменений. Строгий релизный gate BLOCKED.

### 2026-10-15 — RU legacy SEO Strategy Builder retired; homepage entry points corrected
- Предыдущий коммит e493ca97: GitHub Actions Hugo #38784891265 PASS, project context #38784891338 PASS. ES VPS CTA с корректным affiliate disclosure сохранена. Для всей сборки ранее 154 замечания; strict release gate не пройден.
- content/strategy-builder/index.ru.md для /ru/konstruktor-seo-strategii/: draft=false → true. Устаревший конструктор продвигал линкбилдинг/схемы; не подменяем его новой услугой с тем же URL.
- content/_index.ru.md: heroBuilderUrl → /ru/seo/, heroCasesUrl → /ru/about/, offerItem8 больше не направляет на старый инструмент. Это корректировка навигации, не полный SERP/контент-аудит RU главной; остальные старые коммерческие фрагменты пока остаются.
- layouts/index.html: тексты RU CTA согласованы с целями («SEO-услуги» и «О компании»); fallback для RU и EN уже снятых конструкторов не создаёт ссылки на /ru/konstruktor-seo-strategii/ и /seo-strategy-builder/. ES CTA/fallback на существующий ES конструктор пока не изменён, он следующий по очереди.
- docs/retired-routes-en.txt: добавлен /ru/konstruktor-seo-strategii/. .github/workflows/rebuild-qa.yml проверяет отсутствие HTML и ссылки, наличие целевых RU SEO/About страниц и правильную подпись CTA. docs/research/2026-10-15-ru-builder-retirement.md — миграционная оценка.
- GitHub Actions нового коммита необходимо подтвердить: при остаточной ссылке из шаблона/контента блокирующая проверка должна упасть. Никаких 301/410 на сервере; исходный main сохранён. Strict whitehat gate всё ещё BLOCKED. SERP_VERIFIED/visual QA для RU не проводились.
- Следующее действие: проверить CI и при необходимости устранить конкретные старые ссылки; затем отдельным коммитом отключить ES SEO Strategy Builder и исправить ES главную. После этого пройти RU/ES Tier и сателлиты постранично.

### 2026-10-15 — ES homepage: честная маркировка VPS-партнёрки
- Предыдущий RU homepage commit e8a32067: GitHub Actions Hugo build, RU generated copy guard и context guard PASS.
- В content/_index.es.md (homeJson) старый текст Hosting de red privada заменён на размещение сайтов/приложений, к VPS-карточке добавлено «enlace de afiliado». offerItem6 получил одну тематическую партнёрскую CTA и уточнение, что VPS не гарантирует индексацию/позиции Google.
- URL партнёра и код остались ровно прежними. Добавлен docs/research/2026-10-15-es-home-affiliate-audit.md; в .github/workflows/rebuild-qa.yml проверяется сгенерированный ES HTML.
- Это точечная корректировка старой ES главной, а НЕ полная локализация, не SERP top-10 и не visual QA; релизный gate всё ещё BLOCKED. Новые Actions требуют подтверждения, main/production/Pages не тронуты.
- Следующее: проверить CI и новый affiliate inventory, затем работать с RU/ES strategy-builder (старые серые рекомендации) и Tier/satellite страницами по одной, до постраничного SERP-аудита коммерческих страниц.

### 2026-10-15 — RU homepage: тематическая и прозрачная VPS-партнёрка
- Предыдущий commit cb1e4882: удалён static/ru/soft/index.html с ложным переходом на партнёрский VPS, original /go/vdsina/ сохранён. GitHub Actions build + retired URLs и context guard PASS.
- Правка ТОЛЬКО content/_index.ru.md (homeJson): изменены VPS-карточка и offerItem6. «Хостинг приватных сетей» заменён на обычное размещение сайтов, явно подписано «партнёрская ссылка», без утверждения, что VPS обязательно улучшает индексацию. Точное значение партнёрского URL и код оставлены прежними.
- В docs/research/2026-10-15-ru-home-affiliate-audit.md сохранён scope/evidence. В .github/workflows/rebuild-qa.yml добавлены проверки реально сгенерированной RU главной (текст, маркировка, отсутствие сетей и необоснованного SEO-обещания).
- Текущий коммит требует GitHub Actions проверки; visual QA и SERP RU НЕ проводились, RU homepage ещё содержит другие legacy тексты и не готова к релизу. ES homepage будет отдельным проходом, не подменять перевод автоматикой. Main и продакшен не менялись.
- Следующее: проверить Actions; затем аналогичная локальная правка ES homepage с disclosure и без gray/private-network and ranking claims. После этого разбирать gray strategy pages.

### 2026-10-15 — Удалён обманчивый статический /ru/soft/ redirect из кандидата
- Автоматический inventory #38783627099 PASS и context guard #38783627134 PASS для коммита 34f576b7. Сборка 58 HTML, 14 партнёрских ссылок на 9 страницах; 13 с JS-перехватом, 14 без disclosure непосредственно в тексте ссылки. Это не доказательство отсутствия disclosure в другом месте.
- Файл static/ru/soft/index.html являлся meta refresh + JS переходом /ru/soft/ → /go/vdsina/ с подписью Continue. Это нерелевантная подмена, не программный раздел; удалён ТОЛЬКО из белой рабочей ветки.
- В docs/retired-routes-en.txt добавлен /ru/soft/ (файл исторически назван EN, но CI может проверять любой URL). Добавлено исследование docs/research/2026-10-15-ru-soft-referral-retirement.md. Основной /go/vdsina/ и реферальный код сохранены.
- Нет изменений main, server, GitHub Pages или фактического production redirect. Новый GitHub Actions тест должен подтвердить отсутствие URL и входящих ссылок в generated site; без его результата не считать законченным.
- Другие размещения RU/ES страниц старых ссылочных схем и Tier в очереди; разумные VPS-ссылки будут сохранены с disclosure и rel.
- Следующее: проверить GitHub Actions, затем отдельно исправить раскрытие партнёрства на RU/ES homepage VPS-карточках и VPS-фрагментах; не переписывать остальные страницы без аудита.

### 2026-10-15 — Per-page affiliate link inventory introduced
- Previous commit 58fa3d43: Hugo build #38780153578 PASS and context guard #38780153599 PASS. The /go/vdsina/ affiliate endpoint remains as requested; no automatic /soft/ redirect rewrites remain.
- Discovered VDSina references in RU and ES homepages (card2 VPS and infrastructure text), RU strategy-builder banner, and default VDSina banner in the shared strategy-builder template. These are source-level candidates, NOT automatically approved placements or complete rendered enumeration.
- Added scripts/audit_affiliate_links.py to inspect all generated HTML anchors and report source URL, anchor label, rel sponsored/nofollow, cloaked target and potential misleading labels. Added docs/research/2026-10-15-affiliate-placement-inventory.md and a diagnostic step to .github/workflows/rebuild-qa.yml.
- No existing referral link, partner code or server redirect removed. The full strict sitewide gate still blocks unresolved placements and gray material, and this diagnostic does not change its decision. Main, live server and GitHub Pages untouched.
- This new commit requires its own Actions validation. Next: read exact affiliate report; for each relevant referral add visible disclosure, keep rel; retire misleading placements on gray or unrelated pages. Only then adjust final gate without blanket exemptions.

### 2026-10-15 — Уточнение политики партнёрских переходов: оставлять уместные
- Владелец прямо разрешил сохранять реферальные переходы, если они действительно относятся к содержанию страницы. Это исправляет прежнее чрезмерное правило безусловно удалять /go/vdsina/.
- Подтверждено в источниках: layouts/partials/affiliate-link-cloak.html заменял ссылки /soft/, /ru/soft/, /es/soft/ на партнёрский VPS; layouts/partials/affiliate-link-attrs.html делал те же URL alias к /go/vdsina/. Такие подмены вводят посетителя в заблуждение.
- Убраны только три подмены Soft в affiliate-link-cloak.html и их alias из affiliate-link-attrs.html. **Явный URL /go/vdsina/ и его статический redirect сохранены**, существующие явные партнёрские ссылки не удалялись и исходный партнёрский код не менялся.
- Обновлены docs/SEO_PAGE_WORKFLOW.md, docs/WHITE_HAT_RELEASE_READINESS.md и AGENTS.md: уместность, видимая пометка партнёрства, rel sponsored/nofollow, запрет скрытого hijack навигации. Добавлен проверочный шаг в .github/workflows/rebuild-qa.yml.
- Последний до правки коммит 969f7502: GitHub Actions Hugo/retired-route PASS и context guard PASS. CI текущего коммита предстоит подтвердить. Старый whitehat scanner пока блокирует /go/vdsina/ без контекстной проверки; не ослаблять его до отдельной allowlist/ссылочного аудита. Релиз BLOCKED, RU/ES остаются неочищенными. Main, сервер и Pages не затронуты.
- Следующее действие: проверить CI; затем инвентаризировать размещения /go/vdsina/ в видимых страницах, удалить нерелевантные CTA, подготовить строгую проверку тематических affiliate placements, оставляя сам endpoint.

### 2026-10-15 — Blank EN Software page excluded from Hugo
- Previous strategy builder change 113bf180: Hugo/retired routes QA and context guard PASS.
- Source content/soft/index.md: empty content section (one blank builder block, no real utility), draft:false -> true. Existing /soft/ added to docs/retired-routes-en.txt so CI checks it is not published or linked.
- Issue remains: layouts/partials/affiliate-link-attrs.html and affiliate-link-cloak.html can repurpose soft URLs as /go/vdsina/; static/go/vdsina/index.html remains. This is NOT solved by drafting the content page; specific separate template cleanup is next.
- No production redirects/410 done. New CI pending. Main, DNS and site server unchanged. EN/ES/RU tools require distinct legitimate service plans, not placeholder pages.
- Next: confirm CI and eliminate unrelated affiliate-alias behavior in shared templates and static endpoint with links audit.

### 2026-10-15 — Old English SEO Strategy Builder hidden from candidate
- Previous website-creation commit 5806f7de: Hugo/retired-routes #38778332743 PASS, context #38778332779 PASS. Diagnostic scanner: 167 findings in 35 of 60 HTML, versus earlier baseline 300 in 55 of 66. This is internal audit output, not a Google penalty measure.
- content/strategy-builder/index.md /seo-strategy-builder/: added draft: true to prevent the legacy strategy generator from publishing its old page while it remains based on unsuitable SEO practices. Existing script/template source stays available in main.
- Added /seo-strategy-builder/ to docs/retired-routes-en.txt for a blocking generated HTML/sitemap/link test. No live URL/status modification or deployment. RU/ES builder pages remain and need separate work.
- This commit's CI is pending. Future legitimate tool needs independent intent/SERP audit and real white-hat recommendations, not superficial wording changes.
- Next: verify CI then inspect EN /soft/ and legacy affiliate redirect separately; remove them only after route/reference review. Context and production rules unchanged.

### 2026-10-15 — EN website creation page temporarily disabled
- Previous 052a215d: build #38777959133 PASS; context guard #38777959083 PASS.
- Existing content/services/website-creation/index.md mixes ordinary website development with unrelated legacy services under /link-building-services/website-creation/. Changed only draft:false to true.
- Registered the candidate-disabled URL in docs/retired-routes-en.txt and documented the rationale in docs/research/2026-10-15-en-website-creation-review.md.
- Website development itself is not rejected. REVIEW_BUSINESS_OFFER remains; a separate authentic offer and SERP study must precede any new page and redirect. No changes to main or production; CI for new commit pending.
- Next: verify CI; audit old category, software and strategy-builder pages and internal links.

### 2026-10-15 — EN legacy microsite/satellite advertising page withdrawn
- Последний коммит Tier 76a82a6f: rebuild/retired route check и context guard завершились PASS в GitHub Actions. Production и main не тронуты.
- Аудит content/services/microsite-development/index.md: старый URL /link-building-services/microsite-development/ предлагал satellite websites, размещение бренда за ежемесячную оплату, передачу ссылочного авторитета и обещания Google Top. Это не эквивалент реальной заказной веб-разработки, а смешанное предложение, которое нельзя оставлять в white SEO.
- Страница переведена в draft: true, путь добавлен в docs/retired-routes-en.txt, обоснование в docs/research/2026-10-15-en-microsites-retirement.md. Не утверждаем, что самостоятельные microsites запрещены всегда.
- 301/410 на живом сервере НЕ сделаны. Реестр миграции содержит REVIEW_BEFORE_410 до получения GSC/live/backlink evidence. Возможную настоящую услугу website development проверять отдельно и под самостоятельный интент.
- QA этого коммита ещё ожидает GitHub Actions. RU/ES и другие legacy материалы всё ещё публикуются в candidate; strict gate не пройден.
- Следующее: проверить CI; затем раздельно проверить EN website creation (настоящая услуга или PBN) и old link-building section parents/soft/strategy builder, не менять main/production.

### 2026-10-15 — EN Tier 1–2–3 link networks withdrawn from Hugo
- GitHub Actions f2319734: rebuild + retired route check #38777434146 PASS; context guard #38777434159 PASS. Сервер и main неизменны.
- source content/services/tier-1-2-3/index.md for URL /link-building-services/tier-1-2-3/: changed draft: false → true. Карточки и ссылки, встроенные в эту уже закрытую публикацию, перестают генерироваться обычным Hugo.
- Добавлен URL в docs/retired-routes-en.txt для обязательной проверки неприсутствия в sitemap, HTML и внутренних ссылках. В миграционном реестре отмечен RETIRE_410 (только план для релиза, не live response).
- Данный коммит требует собственного Hugo QA + context guard; пока не заявлять полную очистку сайта, ES/RU и другие EN направления всё ещё legacy.
- Дальше: подтвердить Actions; исследовать EN /link-building-services/microsite-development/ на предмет реальной самостоятельной ценности (не автоматически считать все microsites неэтичными), затем принять KEEP/REWRITE/RETIRE с фиксацией.

### 2026-10-15 — EN Domain Rating page set to draft
- После проверки commit b0ca69fb: Hugo/retired URL QA #38777051315 PASS; context guard #38777051329 PASS.
- content/services/domain-rating/index.md: draft=false → true для /link-building-services/domain-rating/. Новое предложение услуг намеренно не включает повышение сторонних SEO-метрик.
- docs/retired-routes-en.txt дополнен старым URL, чтобы тестировать отсутствие HTML, sitemap и внутренних ссылок. Исходный main и действующий сайт не менялись; будущий HTTP 410 лишь предварительное решение, без GSC/live-аудита.
- Проверка этого изменения в Actions ещё не подтверждена; следующий шаг — подтвердить CI, затем по одной разобрать EN Tier 1-2-3 и связанные ссылки.

### 2026-10-15 — EN tiered link-building offer withdrawn from candidate
- Предыдущий коммит c5445d93: GitHub Actions rebuild #38776716307 PASS, context #38776715896 PASS. Автоматические подстановки серых карточек в общем services-hub исправлены, регрессионный retired-route тест подтверждён в CI.
- Обновлён content/services/link-building/index.md для старого URL /link-building-services/link-building/: draft:false → true и showOnHome:true → false. Страница продаёт tiered ссылочное продвижение, а не отдельную легитимную SEO-услугу; корректного same-intent преемника нет.
- Добавлен URL в docs/retired-routes-en.txt; регрессия проверяет отсутствие публикации, ссылок и sitemap. Отчёт docs/research/2026-10-15-en-link-building-retirement.md документирует обоснование и риски.
- Docs/seo-url-migration-register.csv уже содержит RETIRE_410 как ПРЕДЛОЖЕНИЕ; фактические live 404/410/301 НЕ выполнялись. GSC, referring links и визуальная проверка остаются pending.
- Новый Hugo build + retired-route QA и context guard требуют проверки GitHub Actions для этого коммита. Strict whitehat gate всё ещё BLOCKED из-за других старых URL, EN/RU/ES не опубликованы.
- Следующий шаг: проверить CI; затем та же поштучная процедура для EN /link-building-services/domain-rating/ с предотвращением ссылок на draft.

### 2026-10-15 — Защита от автоматически создаваемых ссылок на отключённые услуги
- Шаг текущего плана: проверка входящих ссылок на EN /link-building-services/backlinks/ (страница уже draft: true). В прямых ссылках новых EN content/_index.md, content/seo/index.md, content/services/_index.md, keyword-research, seo-consultation, hugo.toml и header.html точного URL не обнаружено; динамический шаблон services-hub.html формировал URL из текста/типа карточек и дополнительно самостоятельно вставлял Tier 1-2-3. Это системный дефект, независимо от отсутствия прямой строки в EN контенте.
- Изменён layouts/partials/services-hub.html: убраны выдуманные fallback URL backlink/DR/tier/link-building и принудительное добавление Tier/consultation карточек; карточка без явного корректного URL или корректной imageLink не выводится, URL кнопки имеет приоритет над ссылкой картинки. Не изменялись существующие URL реальных услуг. RU/ES устаревшие карточки с прямыми gray ссылками требуют отдельного прохода.
- Созданы scripts/verify_retired_routes.py и docs/retired-routes-en.txt (на данный момент только /link-building-services/backlinks/). Проверка анализирует все сгенерированные HTML, ссылки/динамические data URL, наличие физического HTML и sitemap. Добавлен отдельный блокирующий этап в .github/workflows/rebuild-qa.yml.
- Сборка Hugo и проверка контекста предыдущего коммита 0cb681d7 проверены PASS в Actions #38775570230 и #38775570803. Для текущего коммита новые Actions ещё требуется подтвердить; выполнение CI не гарантирует релизной готовности.
- Оставшиеся риски: другие старые EN страницы всё ещё рендерятся, RU/ES тоже; JS-ссылки вне указанных HTML-атрибутов, реальный browser QA, live статусы и GSC не проверены; strict whitehat gate BLOCKED. main и production не изменены.
- Следующее действие: проверить CI новых тестов, при найденных остатках разобраться с конкретными файлами; затем по одной выводить старые EN услуги /link-building-services/link-building/, domain-rating и tier-1-2-3 с учётом входящих ссылок и миграционного реестра.

### 2026-10-15 — Зафиксирован регламент постраничной SEO-переработки
- Создан docs/SEO_PAGE_WORKFLOW.md: утверждена последовательность baseline → удаление серых услуг EN → переработка EN → RU → ES → полный QA → отдельное разрешение релиза. В него входят реальная проверка SERP top-10 с гео/датой, межстраничная каннибализация, содержательные требования и stop-gates.
- AGENTS.md дополнен обязательным чтением регламента. Важное разграничение: успешный Hugo/CI не является свидетельством качественного SEO, готовности к релизу или отсутствия старых промо.
- Проверено GitHub Actions по предыдущему коммиту e8d81a0a: rebuild QA #38774652226 PASS; context guard #38774652215 PASS. Полный strict whitehat content gate не пройден.
- Сайт, шаблоны, main и сервер не менялись; добавлена только документация процесса.
- Проверка этого коммита в GitHub Actions будет доступна после push; следующий конкретный шаг — найти/устранить внутренние ссылки EN на уже выключенную /link-building-services/backlinks/, затем другие EN legacy направления.

### 2026-10-15 — EN массовое размещение backlinks исключено из Hugo (первая legacy-страница)
- Предшествующие GitHub Actions: rebuild #38774047519 PASS, context guard #38774047402 PASS. Эти PASS не означают готовности к релизу.
- Файл content/services/backlinks/index.md: исключительно `draft: false` заменено на `draft: true`. Страница /link-building-services/backlinks/ должна перестать генерироваться Hugo и попадать в sitemap; источник остаётся для учёта миграции, main не изменён.
- Причина: продажа массовых ссылок для ранжирования. В реестре миграции кандидат RETIRE_410, НЕ реальная 410 на сервере. Никакого нерелевантного редиректа на /services/ или главную.
- Риски: старые внутренние ссылки на URL могут оставаться; полный strict gate всё ещё заблокирован. Проверки нового коммита Hugo/Actions ещё не подтверждены.
- Следующее: проверить CI, отключать прочие EN серые услуги отдельно с проверкой ссылок; RU/ES потом.

### 2026-10-15 — Global RU/ES menus and language-switcher cleanup
- Whole-site audit GitHub Actions #38774047519: Hugo and individual EN page QA PASS; informational scanner found 300 issues across 55 of 66 HTML (195 legacy nav, 29 old public routes, 75 visible-text flags, 1 affiliate endpoint). RELEASE READINESS BLOCKED; this is baseline, not ranking penalty evidence.
- Edited hugo.toml: removed ES/RU menu items naming link building and empty software, introduced clean localized SEO links /es/seo/, /ru/seo/.
- Edited layouts/partials/header.html: removed hardcoded old-language URL exceptions and forced fallback to legacy link-building hubs; untranslated languages now fall back to respective locale home instead.
- Added docs/research/2026-10-15-global-menu-cleanup.md with evidence and limitations; improved build QA to inspect localized primary navigation.
- Not yet ready: old RU/ES SEO pages and homes are still original, as are gray service pages; scanner will continue BLOCKED. Production and main untouched.
- Next: verify localized nav QA, then retire or rewrite legacy public pages and draft empty software/strategy builder by language; avoid redirecting unrelated content.

### 2026-10-15 — Sitewide release-readiness blocker scanner
- FAQ QA #38773548639 PASS и контекст #38773548616 PASS. Все изменения только white-seo-rebuild.
- Добавлен scripts/whitehat_content_gate.py: сканирует generated HTML EN/RU/ES, sitemap и навигацию на старые ссылки, услуги ссылочного продвижения, PBN, Tier/DR, инструмент-автоматизацию, рефералку VPS. В режиме --strict статус ошибки блокирует релиз.
- Добавлен docs/WHITE_HAT_RELEASE_READINESS.md с обязательными этапами: замена/удаление старых услуг, безопасная миграция URL, локализация, QA.
- Изменён .github/workflows/rebuild-qa.yml: шаг информативного sitewide-сканирования выводит BLOCKED при обнаружении остатков, но НЕ падает специально до завершения процесса. Сам успешный build НЕ ОЗНАЧАЕТ возможность публикации.
- Полный строгий gate и live/GSC/browser QA пока не пройдены; ожидаем старые услуги в EN/RU/ES, /soft/, /seo-strategy-builder/, /go/vdsina/.
- Следующее действие: проверить Actions и его список блокирующих страниц, затем начать обезвреживание старых публичных материалов по отдельным страницам с фиксацией будущего 301/410 и без live-сервера.

### 2026-10-15 — EN FAQ rewritten for buyer questions, trust and accuracy
- Previous About QA #38773315827 PASS, context guard #38773315866 PASS. Server untouched.
- Rewritten content/faq/index.md: preserved /faq/, unique Title/H1 «SEO Services FAQ» and meta; 13 real service questions including audit vs keyword research, GSC, migration, measured outcomes, timelines, scope and languages.
- Removed unsupported expectations for quick rankings; added direct internal links to legitimate white SEO pages and contacts.
- Added docs/research/2026-10-15-en-faq-intent.md: FAQ is a brand/support page, does not cannibalize specific commercial SEO pages, no fake SERP rank claim.
- Extended .github/workflows/rebuild-qa.yml with FAQ content/links/canonical/H1 checks; need confirm new Actions result.
- EN source areas still contain gray legacy pages and strategy builder; RU/ES not rebuilt; working branch not ready to publish.
- Next: sitewide risk inventory of legacy EN/RU/ES URLs, templates and visible navigation; resolve gray service pages as retired or draft in working branch after recording candidate mapping.

### 2026-10-15 — EN About SEOImpuls authenticity and trust rewrite
- Working branch white-seo-rebuild; consultation QA #38772846555 PASS, context guard #38772846622 PASS.
- Reworked content/about/index.md: About SEOImpuls H1, factual methods, boundaries, technical SEO, keyword research, content, consultation, evidence standards and contact.
- Removed unverified current ratings and aggregate Kwork numbers and historical link-service promotion from EN About; avoided inventing cases or generic claims about client results. Kept original /about/ URL and translationKey.
- New docs/research/2026-10-15-en-about-trust-audit.md records prior-claim risk and brand-intent ownership. No fake claim of generic query top-10 relevance.
- Expanded .github/workflows/rebuild-qa.yml H1/canonical/clean content/service links/anchors About checks; verify this commit in Actions.
- RU/ES remain legacy; server, DNS, production and main untouched.
- Next: confirm CI then replace thin EN FAQ and begin global audit for legacy gray URLs across all locales.

### 2026-10-15 — EN SEO consultation rebuilt and added to services catalog
- Working branch white-seo-rebuild; /services/ QA #38772264988 PASS, context guard #38772264795 PASS. Production unchanged.
- Rewritten content/services/seo-consultation/index.md: title/H1 «SEO Consultation & Strategy Review»; unique URL /services/seo-consultation/; prep, diagnostics topics, session boundaries, deliverables/outcomes, FAQ, contacts. Retained legacy published $350 and around three hours as reference terms to confirm; removed unverified lifetime support/case claims and link-building topics.
- Updated content/services/_index.md: third clean commercial card for consultation, new summary and corrected meta description.
- Updated docs/research/2026-10-15-en-services-catalog-intent.md and new docs/research/2026-10-15-en-seo-consultation-intent.md with intent ownership, ten comparison examples (not verified exact Google first-10), migration notes.
- Expanded .github/workflows/rebuild-qa.yml to verify consultation H1/canonical/anchors, no prohibited claims, /services/ directory link. New QA run pending.
- MAIN and production untouched; legacy consultation URL redirect not implemented, old gray pages still exist. Do not publish before full migration and multi-language audit.
- Next: check QA and context Actions; then audit/decommission legacy gray EN pages and all internal links without accidentally redirecting unrelated content.

### 2026-10-15 — Clean EN /services/ catalog and resolve keyword breadcrumb
- Предыдущий QA #38771883235: Hugo build PASS, SEO проверка keyword research FAIL из-за видимой надписи «Link Building Services». Причина: breadcrumb наследовал старый Title раздела services. Контекст guard #38771883177 PASS.
- Переделан content/services/_index.md: URL /services/, Title/H1 «SEO Services & Practical Deliverables», две реально легитимные услуги (technical SEO и keyword research), без backlink/DR/tier/satellites и негативных старых карточек.
- Изменено меню EN в hugo.toml: Services → /services/, Technical SEO → /seo/. Другие языки ещё в оригинальном состоянии.
- Добавлено исследование разделения запросов и архитектуры docs/research/2026-10-15-en-services-catalog-intent.md. Новый каталог намеренно навигационный, не дублирует подробную /seo/.
- QA workflow расширен на /services/ H1/canonical и проверку чистого breadcrumb у keyword research; новый запуск требуется подтвердить.
- Старый /link-building-services/ не перенаправляли: 301 в данном случае может быть нерелевантен, решение после GSC. Production не изменён.
- Следующее: проверить CI, далее SEO Consultation EN /services/seo-consultation/ и после этого добавить её в каталог с контекстом.

### 2026-10-15 — EN keyword research genuine SEO service page
- Ветка white-seo-rebuild. Страницы / и /seo/ ранее успешно прошли GitHub Actions, без деплоя.
- Переработан content/services/keyword-research/index.md: H1/Title Keyword Research & Search Intent Mapping; новый URL /services/keyword-research/, от старого /link-building-services/keyword-research/ нужен будущий релевантный 301 при отдельном разрешении.
- Реальные коммерческие интенты: query research, clustering, intent mapping, URL assignments, content gaps, deliverables, FAQ, условия и контакты. Цена $90 сохранена из существующего исходного предложения, без вымышленных сроков и объемов.
- SERP reference/intent study: docs/research/2026-10-15-en-keyword-research-intent.md, 10 примеров не являются точным Google top-10 по одному региону.
- Дополнены тесты Hugo и SEO в .github/workflows/rebuild-qa.yml; текущая QA требует проверки Actions. Изменения в main, сервере и GitHub Pages отсутствуют.
- ВАЖНО: каталог /services/ ещё не создан, старый /link-building-services/ содержит старые ссылки, ES/RU требуют миграции. Рабочая ветка пока не является готовой публикацией.
- Следующее действие: QA нового URL; создание корректного /services/ каталога и EN SEO консультации, чтобы устранить зависимость от старого линкбилдинг-раздела.

### 2026-10-15 — Inventory of legacy commercial URLs and provisional migration decisions
- /seo/ QA #38771057820 PASS; контекст #38771057945 PASS. Сайт на сервере не изменён.
- Созданы docs/seo-url-migration-register.csv (27 legacy коммерческих URL из Hugo content/services EN/RU/ES) и docs/SEO_URL_MIGRATION_POLICY.md с кандидатами 301, 404/410 или ручной бизнес-проверки.
- Это ПЛАН, а не применённые редиректы. GSC-данных о показах/кликах и реальных внешних ссылках ещё нет; окончательный статус каждого URL не подтверждён.
- Условие: 301 только для реального тематического преемника; серые услуги не маскировать и не вести на главную; при удалении проверять sitemap, canonical, hreflang, внутренние ссылки.
- Следующее действие: работа над законными коммерческими услугами (keyword research, consultation) и выделение чистого каталога /services/ без каннибализации / и /seo/; сначала SERP и проверка функционального предложения.

### 2026-10-15 — EN /seo/ deep rewrite
- Ветка: white-seo-rebuild. Homepage QA #38770565895 PASS; context guard #38770566048 PASS. Сервер не затронут.
- Изменён content/seo/index.md: новый уникальный H1/Title «Technical SEO Services & Audits», meta, сохранён исходный URL /seo/ и responsive template design=seo-overview.
- Удалены из новой EN страницы CTA на link-building, старые недоказанные обещания и расплывчатые тематические блоки. Добавлены технический аудит, on-page SEO, семантика, международное SEO, процесс, результаты работ, FAQ и проверяемые контакты.
- Исследование и разграничение интентов сохранены в docs/research/2026-10-15-en-seo-services-intent.md. Данные конкурентных примеров — не подтверждённый точный Google SERP top-10 одного региона.
- Обновлён .github/workflows/rebuild-qa.yml с проверками /seo/ H1, якорных разделов, устаревших ссылок и терминов. Новый Actions run ещё должен подтвердить build.
- Не публиковать сайт: остальные старые услуги, footer/soft, RU/ES и глобальная архитектура требуют очистки, карта 301/410 не готова.
- Следующий шаг: проверить Actions; затем детально разобрать старые коммерческие услуги и URL-mapping без редиректов на нерелевантную главную.

### 2026-10-15 — QA first run and HTML parser fix
- GitHub Actions #38770346654: Hugo EN/RU/ES/sitemap build PASS, homepage automated text/H1/link assertions reached process-anchor check, which failed with «SEO process anchor missing».
- Причина проверки: тест использовал поиск точной строки id="how-it-works" по минифицированному HTML. Hugo HTML minifier может убирать кавычки в безопасных атрибутах; такая проверка неустойчива.
- В .github/workflows/rebuild-qa.yml id атрибут теперь проверяется через HTMLParser, а не совпадение строки. EN homepage не изменялась; это исправление только QA.
- Context-guard #38770346469 PASS.
- Следующий шаг: дождаться нового rebuild-qa, проверить canonical и фактическое содержание output; если ошибки повторятся, документировать и исправить.

### 2026-10-15 — EN homepage: commercial-intent and white SEO rebuild
- Рабочая ветка: white-seo-rebuild. Main остаётся исходным эталоном.
- Зафиксирован успешный GitHub Actions импорт #38768910498: ZIP SHA проверен, Hugo EN/RU/ES/sitemap PASS, файлы доступны в main, ZIP удалён.
- Документирован конкурентный ориентир из 10 релевантных англоязычных страниц: docs/research/2026-10-15-en-home-serp-intent.md. Это выборка, не подтверждённый точный Google top-10 одного региона.
- Файлы: content/_index.md, layouts/index.html, hugo.toml. EN главная переписана под SEO Services; удалена из видимой EN версии ссылка на VPS и продвижение backlinks/DR, вместо фальшивой новости теперь реальный процесс, исправлены EN услуги меню и CTA.
- Добавлена .github/workflows/rebuild-qa.yml (только проверка, без публикации), проверяющая Hugo, три главные, sitemap и английский H1, canonical, старый контент и CTA.
- ПРОВЕРКИ: до завершения нового Actions workflow не заявлять, что обновлённая главная прошла build и UX-QA; необходимо проверить в Actions.
- НЕ ГОТОВО к публикации: /seo/ и другие EN-услуги, RU/ES, footer, устаревшие URL, реальный SERP geo-specific, responsive/visual проверки.
- Следующий шаг: проверить Actions и HTML EN главной; затем провести аудит и переработку EN /seo/, не трогая продакшн.

### 2026-10-15 16:26 UTC — Verified source import via GitHub Actions
- Uploaded ZIP matched the recorded SHA-256; files extracted into main.
- Hugo --minify build completed with EN/RU/ES homepage and sitemap checks.
- Source archive removed from repository in this commit; no GitHub Pages and no production deployment.
- Working branch white-seo-rebuild will be created from this imported commit.
- Next: check main file tree and working branch; then begin inventory and intent map.

### 2026-10-15 — Исправление импорта после первого запуска Actions
- Первый запуск Actions #38768517453: SHA ZIP OK, распаковка OK, Hugo build (EN/RU/ES/sitemap) OK, Git push FAILED.
- Подтверждённая причина: GITHUB_TOKEN отклонил запись `.github/workflows/build-check.yml` из архива (workflow permission). Ветка white-seo-rebuild ещё не существует; main пока содержит исходный ZIP.
- Изменён .github/workflows/import-source.yml: старые workflow архивируются в docs/legacy-workflows/ (не активируются), триггер расширен на изменение самого импортного workflow, чтобы повторить запуск при этом коммите.
- Обновлена запись контекста в том же коммите. Prod сервер и публикация GitHub Pages не затронуты.
- Дальше: проверить новый Actions run, наличие content/layouts в main и рабочей ветки; только после подтверждения начать white-hat переписывание.

### 2026-10-15 — Добавлена автоматическая проверка журнала изменений
- Создан workflow .github/workflows/context-guard.yml: для каждого нового коммита в white-seo-rebuild проверяется наличие изменения CHATGPT_PROJECT_CONTEXT.md в том же коммите.
- Workflow сигнализирует об ошибке в Actions при нарушении правила; он не заменяет защиту ветки GitHub и сам по себе не блокирует все прямые push.
- Изменения в сайт не вносились; источник всё ещё ожидает импорт.

### 2026-10-15 — Инициализация правил восстановления
- Создан приватный пустой репозиторий agurkin2021-gif/seoimpuls с README.md.
- Зафиксирован обязательный контекст-файл и инструкции для последующих чатов.
- Подготовлен workflow безопасного импорта проекта из ZIP. Сайт на сервере не изменён.
- Проверен локально подготовленный ZIP: 2886 файлов, повреждений ZIP не обнаружено, SHA-256 указан выше.
- На момент этого коммита ИСХОДНИКИ В GITHUB ЕЩЁ НЕ ЗАГРУЖЕНЫ. Не считать проект готовым к редактированию или публикации.
- Следующий этап: загрузка ZIP и успешный импорт GitHub Actions.

## 6. Следующее действие

Проверить GitHub Actions для четвёртой карточки RU/ES веб-разработки: оба каталога ровно 4 карточки с проверенными URL, valid H1/canonical, без серых терминов. Затем отдельно /es/soft/ — пустая страница/legacy anchor. Потом последовательно About RU/ES, SEO RU/ES, homepage RU/ES, EN FAQ. Никогда не удалять /go/vdsina/ автоматически; ссылки должны быть тематическими, обозначенными как sponsored. Main/live server/DNS/Pages без изменений.

## 7. Формат обязательной записи после КАЖДОЙ правки

Дата / ветка / commit SHA (после коммита) / затронутые файлы и URL / причина и SEO-интент / выполненные изменения / проверки и конкретные результаты / известные риски и нерешённые задачи / точный следующий шаг. Каждую новую запись ставить первой в разделе 5; синхронизировать IMPORT_STATUS и «Следующее действие». При незавершённой задаче явно указывать статус, не подменять его словами «готово».
