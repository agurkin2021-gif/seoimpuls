# Global menu audit and staged cleanup, 2026-10-15

## Why
The site-wide white-hat scanner found 300 findings across 55 of 66 generated HTML files (195 legacy navigation references, 29 public legacy URL route hits, 75 legacy visible copy matches, one unrelated affiliate endpoint). These are mostly concentrated in outdated RU/ES catalog menus and pre-rebuild content. This total is a baseline from the scanner run at GitHub Actions #38774047519, not a count of Google penalties.

## This change
- ES top-level menu: replaced **Servicios de link building** and empty **Software** with **Servicios SEO** → /es/seo/.
- RU top-level menu: replaced **Услуги линкбилдинга** and **Софт** with **SEO-услуги** → /ru/seo/.
- Removed special header URL exceptions that bypass Hugo language prefixing for old services and software.
- Removed obsolete language-switcher fallback that forcibly points visitors to link-building catalogs. Untranslated pages now fall back to the correct locale homepage unless a Hugo translation exists.
- Added automated QA for EN/RU/ES HTML main navigation, verifying localized /seo/ link and no old link-building or soft path.
- No changes to production, no live redirects, no accidental publication.

## Remaining blockers
RU/ES actual /seo/ pages and homepages still contain old gray promotional content; navigation now exposes generic SEO label but full new content must follow. All other generated old service pages, /soft/, /seo-strategy-builder/, global dynamic components and /go/vdsina/ still require separate retirement or rewrite. New menus alone do not qualify any page for production.
