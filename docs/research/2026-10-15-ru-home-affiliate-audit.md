# RU homepage — targeted affiliate CTA correction (2026-10-15)

Scope: only `content/_index.ru.md` homeJson VPS card and infrastructure paragraph. This is not a complete RU homepage SEO/SERP rewrite and does not approve the remaining old page content.

Source old card2: "Хостинг и VPS для SEO-проектов" / "Хостинг приватных сетей", CTA to VDSina. This offered private network hosting as a core feature, which is inconsistent with a clean SEO-services presentation.
Source old offerItem6: claimed VPS is categorically faster than regular hosting and improves indexing. Those are not guaranteed.

Candidate correction:
- Keep the actual existing VPS affiliate target and partner code unchanged.
- Rename the card "VPS для размещения сайта — партнёрская ссылка" and replace private-network wording with ordinary site/app hosting.
- Replace the infrastructure claim with a limited, conditional explanation of VPS suitability and one CTA explicitly labelled "партнёрская ссылка". State that VPS does not guarantee Google indexation or rank outcomes.
- Preserve `rel="nofollow sponsored"` via the existing link-processing template; GitHub Actions continues testing the rendered result.
- The original source in main and the live seoimpuls.com page remain untouched.

QA: new generated RU HTML checks in rebuild-qa.yml. Browser layout at 390px and 1280px, exact geo SERP, and overall white-hat approval remain pending. ES homepage will be updated in a separate, locale-specific commit.
