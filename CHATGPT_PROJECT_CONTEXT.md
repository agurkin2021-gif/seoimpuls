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

Проверить CI после исключения EN /soft/. Затем отдельно убрать партнёрские подмены ссылок /soft/ и /go/vdsina/ из Hugo-шаблонов и статического endpoint. Проверить полную карту входящих ссылок, не трогать main/production.

## 7. Формат обязательной записи после КАЖДОЙ правки

Дата / ветка / commit SHA (после коммита) / затронутые файлы и URL / причина и SEO-интент / выполненные изменения / проверки и конкретные результаты / известные риски и нерешённые задачи / точный следующий шаг. Каждую новую запись ставить первой в разделе 5; синхронизировать IMPORT_STATUS и «Следующее действие». При незавершённой задаче явно указывать статус, не подменять его словами «готово».
