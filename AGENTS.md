## NEW OWNER ASSET LOCK — 2026-10-16
Do NOT reuse old service pictures/icons in the three EN homepage service cards until the owner issues a new explicit directive. The current owner-approved direction is a custom lightweight responsive design using CSS-only 01/02/03 marks. Do not delete existing image assets; leave brand logo, RU/ES and unrelated images unchanged. Source `00881d5` passed strict+preview+390/768/1280 browser, screenshots checked, status OWNER_REVIEW_PENDING. Never switch to another page without an explicit owner command; never deploy production automatically.

## CURRENT OWNER DIRECTIVE — 2026-10-16: EN homepage direct SEO services
The owner explicitly superseded the earlier "ONLY EN /seo-services/" lock: the EN homepage must present all actual services directly, without an extra EN services catalogue. They also instructed removing the generic /services/ prefix and naming the old /seo/ technical-audit page by its actual primary query, consistent across URL, HTML Title and H1.

Authorized: EN homepage and header, three existing EN commercial service pages, EN About/FAQ link dependencies, retiring EN-only intermediate URLs, required exact-page schema and QA checks, context and plan. Not authorized: modifying RU/ES source copy, unrelated EN pages, main, actual production, DNS, CDN or Search Console. No automatic next-page progression after this architecture task.

New EN route map:
- Homepage / -> Professional SEO Services
- /technical-seo-audit/ -> Technical SEO Audit | SeoImpuls -> H1 Technical SEO Audit
- /keyword-research/ -> Keyword Research | SeoImpuls -> H1 Keyword Research
- /seo-consultation/ -> SEO Consultation | SeoImpuls -> H1 SEO Consultation

Primary keyword for the former /seo/ is technical seo audit: narrower than technical seo services and matches the actual diagnostic product (technical crawl/index issues, prioritized report). Prior Google SERP snapshot and fresh 2026 service examples support terminology, but search volumes and precise physical-US rankings are UNVERIFIED. Mere keyword placement in URL does not guarantee Google rankings.

The old EN hub is a draft in the rebuilt source; avoid broken cross-language hreflang to it. Keep RU/ES native routes unchanged, keep direct EN hreflang links working. Production redirects remain a separate explicit permission. Mandatory same-commit update of CHATGPT_PROJECT_CONTEXT.md persists.

Current plan is docs/plans/EN_DIRECT_SERVICES_ARCHITECTURE.md. Former EN SEO Services plans are HISTORY only.

## OWNER PAGE LOCK — 2026-10-16 (HIGHEST PRIORITY)
The owner explicitly reopened the **second EN page `/seo-services/`** due to an overloaded 23-workstream service directory and ordered: **NEVER switch to any other page without a new explicit owner command**. This applies even if the page passes all tests, all checklist items are DONE, or the earlier greenfield roadmap names `/seo/` as "next". Do not edit the homepage, `/seo/`, other EN pages, RU/ES or production without separate permission. Only `/seo-services/`, its EN-specific partial/data, directly relevant QA and context/plan documentation are authorized. Read `docs/plans/EN_SEO_SERVICES_SIMPLIFICATION_PLAN.md` as active plan; the older FINISH_PLAN is historical QA evidence. Every repo write must update `CHATGPT_PROJECT_CONTEXT.md` in the same commit. Status: REOPENED / UX_REDESIGN_IN_PROGRESS.

# AGENTS.md — строгие правила работы с SEOImpuls

НОВОЕ РЕШЕНИЕ ВЛАДЕЛЬЦА 2026-10-15 (ПОСЛЕ ЗАВЕРШЕНИЯ EN ГЛАВНОЙ): перейти к английскому каталогу услуг `/services/`, изучить SERP, разделить интенты и рассмотреть описательный URL `/seo-services/`. Английская главная `/` заморожена по контенту; допускаются только необходимые ссылочные зависимости при смене URL каталога. Остальные EN-страницы не переписывать; RU и ES не редактировать/не переводить. GitHub Pages preview разрешён, production `seoimpuls.com` не затрагивать.

ПЕРВЫМ ДЕЛОМ в каждом новом чате или сеансе открыть CHATGPT_PROJECT_CONTEXT.md в корне репозитория и прочитать всю актуальную запись и следующий шаг. Ничего не начинать на основании памяти чата, если она расходится с содержимым GitHub.

АБСОЛЮТНЫЙ ИНВАРИАНТ: КАЖДАЯ правка проекта включает обновление CHATGPT_PROJECT_CONTEXT.md в ТО ЖЕ Git-коммите. Это относится к HTML, Hugo templates, контенту, SEO, CSS, JS, изображениями, workflow, README и структуре. Если контекст не обновлён — задача не завершена. Отражать факты: файлы, URL, почему, что изменено, конкретно какие проверки прошли и не прошли, следующий шаг. Не писать бездоказательное «идеально» или «опубликовано».

Репозиторий: https://github.com/agurkin2021-gif/seoimpuls (PUBLIC с 2026-10-15; исходники доступны всем; не добавлять секреты).
Production: https://seoimpuls.com/ — НЕ ИЗМЕНЯТЬ, НИЧЕГО НЕ ДЕПЛОИТЬ без отдельного прямого разрешения.
Ветки: main (исходник), white-seo-rebuild (вся переработка).
GitHub Pages Preview для white-seo-rebuild разрешён: https://agurkin2021-gif.github.io/seoimpuls/. Исходник main через Pages не публиковать; production seoimpuls.com не трогать без отдельного указания.
Пользователь требует полностью белое SEO, а не эвфемизмы: убрать массовые ссылки, автоматизацию спама, рост DR, Tier-сети, PBN и гарантию позиций. Не придумывать кейсы и компетенции.
Работа: SERP-first → intent map → архитектура → EN homepage → EN services → RU / ES с учетом локальных запросов → технический аудит → проверка всех URL → отдельное решение о публикации.
Беречь URL-историю и SEO-сигналы. 301 только по релевантности; удалённые услуги не редиректить массово на главную. Удалить остаточные ссылки из навигации, карт и внутренних ссылок.
Строго проверять Hugo build, URL и language locales, canonical/hreflang/sitemap, внутренние ссылки, метаданные и доступность.
Не коммитить секреты, локальные конфиги, .env, данные SSH, персональные данные.

ОБЯЗАТЕЛЬНЫЙ ПОШАГОВЫЙ ПОРЯДОК: перед любым новым SEO-изменением читать docs/SEO_PAGE_WORKFLOW.md и следовать этапам и page-level QA-gates, в особенности SERP_VERIFIED, отсутствие каннибализации, запрет на fake proof и запрет релиза без строгого sitewide gate. Записывать результаты каждой итерации в CHATGPT_PROJECT_CONTEXT.md тем же коммитом.

ПАРТНЁРСКИЕ ССЫЛКИ: владелец разрешил только тематически уместные, прозрачные партнёрские переходы. Не удалять по умолчанию /go/vdsina/ при релевантном использовании; не подменять /soft/, кейсы, меню или другие нерелевантные ссылки; обязательно показывать назначение/партнёрство, rel="sponsored nofollow", отдельный аудит перед релизом. См. docs/SEO_PAGE_WORKFLOW.md.

ПРАВИЛО ДЛЯ ВСЕХ СЛЕДУЮЩИХ СЕССИЙ (2026-10-16): При обсуждении, аудите и работе над переделкой НЕ приводить ссылку на действующий домен SEOImpuls, НЕ открывать его для сравнения и НЕ использовать действующий сайт как предмет аудита. Источник истины — рабочая ветка white-seo-rebuild в GitHub, а для визуальной проверки — её GitHub Pages preview. Ссылки давать только на репозиторий, файлы, коммиты и preview переработки. Действующий сайт не изменять, не деплоить без отдельной команды.
