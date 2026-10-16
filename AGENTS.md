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
