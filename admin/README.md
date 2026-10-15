# Seoimpuls Admin

Локальная админка для Hugo-проекта Seoimpuls.

## Запуск

Откройте:

```bat
run_admin.bat
```

Или из консоли:

```bat
python server.py
```

Админка откроется на `http://127.0.0.1:8787/`.

## Что уже умеет

- список Markdown-страниц из `content`;
- редактирование `title`, `description`, `slug`, `translationKey`, `date`, `draft`;
- редактирование тела Markdown;
- JSON-редактор front matter;
- бэкап файла перед каждым сохранением в `admin/backups`;
- создание новых bundle-страниц сразу на EN/RU/ES;
- просмотр и загрузка медиа в `static/uploads`;
- запуск `hugo server` для предпросмотра;
- запуск `hugo` для сборки сайта.
- раздел `Хедер/Футер` для контактов, соцсетей, дополнительных ссылок хедера
  и кликабельных слов футера через `data/chrome.json`;
- validation и индикатор несохраненных изменений для `Хедер/Футер`.
- раздел `Бэкапы` для просмотра и восстановления файлов из `admin/backups`.
- удаление страниц из левого списка через мягкую корзину `admin/trash`;
- восстановление удаленных страниц из блока `Бэкапы` → `Удаленные страницы`;
- главные `_index` страницы защищены от случайного удаления.
- при открытии страницы сразу включается вкладка `Страница`, а не сырой Markdown;
- главный заголовок и SEO-описание подписаны человеческими подсказками;
- адрес и технические поля спрятаны в раскрываемые блоки;
- заголовок и описание можно править прямо в предпросмотре страницы.

## Следующий слой

Главная страница и конструктор SEO-стратегии пока частично зашиты в Hugo-шаблоны.
Чтобы управлять ими как блоками, нужно вынести тексты и настройки в `data/*.yaml`,
а затем добавить отдельные экраны админки.

## Контекст проекта

Рабочий контекст для продолжения в новом чате хранится в:

`CONTEXT_SEOIMPULS_ADMIN.txt`

Его нужно обновлять после важных архитектурных решений и крупных изменений.

## Update 2026-06-07

- Added main menu editor in Header/Footer section.
- Menu is loaded from and saved to `hugo.toml` language blocks.
- Added `GET /api/menu` and `POST /api/menu/save`.
- Menu save creates backup of `hugo.toml` in `admin/backups`.
- Added build status in topbar: site actual / need build.
- Page save/create, chrome/menu save, and backup restore mark site as needing build.
- Successful Hugo build marks site as actual again.
- Local URLs:
  - admin: `http://127.0.0.1:8787/`
  - site: `http://127.0.0.1:1314/ru/`

## Page Builder Format

- Editor has a `Constructor` tab for visual page blocks.
- Blocks are saved into front matter as `builderJson`.
- Supported block types:
  - `text`: heading and text.
  - `image`: image URL, alt, caption.
  - `split`: text plus image on left/right.
  - `buttons`: CTA button group.
  - `grid`: free card grid for mixed text/images.
- Each block supports `full`, `half`, or `third` width.
- Blocks can be moved up/down and disabled without deleting.
- Existing Markdown pages still work; if `builderJson` is empty, Hugo renders normal `.Content`.

## QA 2026-06-07

- Tested all builder modes: text, image, split, buttons, grid, disabled blocks, widths, move up/down, Markdown fallback, preview.
- Fixed disabled blocks rendering on site.
- Fixed adding empty nested buttons/grid cards in builder UI.
- Fixed mobile horizontal overflow in admin sidebar and editor tabs.
- Fixed admin static fallback so media/site images load from project `static/`.
- Final checks passed: JS syntax, Python compile, Hugo build, browser UI smoke test.

## Placement And Banner UX

- Page editor shows section/folder, local URL, and real file path.
- Page can be moved to another section with `Move`, for example from `pbn-sites` folder to `services`.
- Constructor has a `Banner` block with image, text, and CTA buttons.
- New pages start with a banner block by default.
- Internal CTA URLs like `/services/` are rendered language-aware, for example `/ru/services/`.
- Copy URL uses the visible page URL field.
- Added real parent `services` pages for EN/RU/ES so child service pages have a working section URL.
- Page list now shows page URLs and marks `_index` pages as section pages.

## Language URL Update 2026-06-07

- English is now the root language: `/`, `/services/`, `/about/`.
- RU and ES keep language prefixes: `/ru/`, `/ru/services/`, `/es/`, `/es/services/`.
- `hugo.toml` uses `defaultContentLanguageInSubdir = false`.
- Admin page URL calculation was updated, so EN pages no longer show `/en/...`.
- Header language switcher fallback was updated, and language flag styling now uses language classes instead of only URL prefixes.
- Checked URLs:
  - `http://127.0.0.1:1314/services/` -> 200
  - `http://127.0.0.1:1314/en/services/` -> 404
  - `http://127.0.0.1:1314/ru/services/` -> 200
  - `http://127.0.0.1:1314/es/services/` -> 200

## Section Page URL Fix 2026-06-07

- `_index` pages are section pages, so their URL is built from the section folder only.
- Example: editing the RU services section and typing `ser` now previews `http://127.0.0.1:1314/ru/ser/`, not `http://127.0.0.1:1314/ru/ser/services/`.
- Moving a section page keeps the target file as `_index.{lang}.md` inside the new section folder.
- Normal child pages still use `section + slug`, for example `/ru/services/pbn-sites/`.

## Builder Image Picker 2026-06-07

- Builder image fields now have a `Выбрать` button.
- Builder image fields also have a direct `Загрузить` button for picking a file from the computer.
- The picker shows images from public static media and can upload a new image.
- Uploaded files go to `static/uploads` and are inserted as `/uploads/...`.
- Works for `Banner`, `Картинка`, `Текст + картинка`, and image fields inside `Свободная сетка`.
- The image field expects an image URL/path, not a page URL.

## Page Visibility Badges 2026-06-07

- The page list now labels why a page exists in admin:
  - `МЕНЮ`: visible from main navigation.
  - `ФУТЕР`: legal/footer page, for example privacy, cookie, terms.
  - `НА САЙТЕ`: published page that is reachable but not in main menu/footer legal strip.
  - `ЧЕРНОВИК`: content file exists, but Hugo does not publish it normally.
- This keeps service/legal/draft pages editable without making them look like the same kind of page.

## Builder Field Hints 2026-06-07

- Added Russian hints in the page builder so fields are easier to remember:
  - `Тип`: what kind of block this is.
  - `Ширина`: how much row space the block takes.

## Page Delete Trash 2026-06-07

- Left page list now has a delete button for every removable page.
- Delete is soft: markdown files move from `content/...` to `admin/trash/{stamp}/content/...`.
- Home/root `_index` pages are protected from deletion.
- Deleted pages are listed in `Бэкапы` → `Удаленные страницы`.
- Restore moves the file back to its original `content/...` path.
- Restore refuses to overwrite an existing page at the same path.
- API added:
  - `POST /api/page/delete`
  - `GET /api/trash`
  - `POST /api/trash/restore`

## Cleaner Page Editing UX 2026-06-07

- Selecting a page now opens the `Страница` tab by default.
- The first visible fields are editor-friendly:
  - `Основной заголовок страницы`;
  - `Описание для Google`.
- URL/slug/section controls moved into a collapsible `Адрес страницы` section.
- `translationKey`, date, draft, and file path moved into a collapsible `Техническое` section.
- Tabs were renamed:
  - `Страница`;
  - `Markdown`;
  - `Технический JSON`;
  - `Черновой просмотр`.
- In the page preview, H1 and description are contenteditable and sync back to the real fields before save.

## Page Canvas Inspector 2026-06-07

- The `Страница` tab now works as a page canvas plus a right inspector.
- The page canvas is the main area; the selected block settings are shown on the right.
- Clicking a text/image/button/grid block on the canvas selects it and highlights it.
- The inspector shows only the selected block, not all blocks at once.
- Text, block titles, image captions, grid card text, and button labels can be edited directly on the canvas.
- Direct canvas edits sync back into `builderJson`; the live site still changes only after `Сохранить`.
- Existing add block buttons remain at the top: banner, text, image, split, buttons, grid.

## Simple Page Canvas 2026-06-07

- The main editing screen is now the page itself inside admin.
- Technical panels for SEO fields, URL, file path, Markdown, and JSON are hidden from the working view.
- The existing page URL is not edited during normal page work; placement is handled during page creation or hidden technical maintenance.
- The visible work area is header + page body + footer, with add buttons above the page.
- Empty pages show only header, footer, H1/description area, and an empty body drop zone.
- The inspector is hidden from the normal flow; blocks are edited directly on the canvas.
- Clicking an image/empty image area opens image selection/upload.
- Double-clicking a button label asks for the button URL.
- `Ctrl +` / `Ctrl -` changes the selected block width when focus is not inside text.

## Critic Simplicity Pass 2026-06-07

- Main target: a non-technical user should create a page in about five minutes.
- New page dialog was simplified:
  - title;
  - human section selector;
  - one language by default.
- `slug` and three-language checkboxes were removed from the visible creation flow.
- New pages are created empty, without starter banner or placeholder body text.
- Existing Markdown-only pages are shown as a normal text block on the canvas.
- Empty editor now has a clear `Создать страницу` action.
- Block toolbar now prioritizes only:
  - `Текст`;
  - `Картинка`;
  - `Кнопка`.
- Advanced blocks moved under `Еще`.
- Undo is shown as one `Отменить` button; step selector is hidden.
- Save button now says `Сохранить и обновить сайт` and runs Hugo build after saving.
- Technical topbar is hidden in the Pages view.
- Page delete button is less prominent and appears on hover/focus only.

## Button Link Panel 2026-06-07

- Button URL editing no longer depends on hidden double-click knowledge or a browser prompt.
- Clicking a button on the page canvas opens a small `Кнопка` panel.
- The panel has two clear fields:
  - `Текст кнопки`;
  - `Куда ведет`.
- Typing the button label updates the button on the canvas immediately.
- The panel closes with `×` or when another non-button area is selected.

## Real Site Page In Admin 2026-06-07

- The page canvas now loads the real site HTML inside admin through `/site/...`.
- Example: `/ru/services/` is loaded as `http://127.0.0.1:8787/site/ru/services/`.
- This avoids cross-origin iframe limitations from `127.0.0.1:1314` while keeping editing inside admin.
- Header, footer, page CSS, and real Hugo markup come from the site page, not from a mock preview.
- Admin overlays draft builder blocks into the real page iframe.
- Draft edits still save only through the admin `Сохранить и обновить сайт` button.

## Pixel Fine Tune 2026-06-07

- Blocks on the real page iframe can be moved by dragging.
- Dragging changes pixel offsets (`offsetX`, `offsetY`) instead of only changing grid order.
- Arrow keys move the selected block by 1px.
- `Ctrl +` and `Ctrl -` change the selected block width by 1px.
- Existing images on the real page canvas can be dragged directly inside their block.
- Clicking an existing image selects it for moving; clicking an empty image placeholder still opens image upload/selection.
- Image-only blocks are visually rendered as only the image, without the card-like block background, border, or padding.
- Image-only blocks do not reserve a large empty layout area; their technical block is collapsed so the editor shows the image itself.
- In the real admin canvas, selected/hovered images have draggable edge handles.
- Dragging left/right edges changes image width.
- Dragging top/bottom edges changes image height.
- Multiple image blocks remain independently draggable; the visible image, not an invisible technical layer, receives mouse events.
- `Ctrl +` and `Ctrl -` change the clicked/selected image width by 1px.
- If no image is selected, `Ctrl +` and `Ctrl -` change the selected block width by 1px.
- Image pixel resizing keeps `height: auto`, so the image proportions do not stretch.
- Empty captions are not rendered on the real admin canvas, because the public site also does not render empty captions. This keeps admin placement matching the real page.
- Fine-tune values are saved into `builderJson` as:
  - `offsetX`;
  - `offsetY`;
  - `pixelWidth`.
- Image fine-tune values are saved into `builderJson` as:
  - `imageOffsetX`;
  - `imageOffsetY`;
  - `imagePixelWidth`;
  - `imagePixelHeight`.
- Hugo renders those values as inline block style, so saved page keeps the same pixel placement.
- Hugo also renders image fine-tune styles on real image tags, so the saved site matches the admin canvas.
  - `Картинка URL`: image file path, preferably filled through `Загрузить`.
  - `Alt / описание картинки`: short image description for SEO/accessibility.
  - `Подпись`: visible caption under the image.

## Builder Live Preview 2026-06-07

- The `Конструктор` tab now has a live `Предпросмотр страницы` panel rendered as a mini-page, not as an isolated block preview.
- It shows a page-like frame with header, page title, description, content blocks, and footer.
- It updates immediately after adding blocks, typing text, changing title/description, changing widths, selecting images, uploading images, or editing buttons.
- On desktop the preview is shown beside the block editor; on mobile it moves below the editor.
- The separate `Быстрый предпросмотр` tab still exists, but the builder no longer requires switching tabs to see inserted content.

## Admin Visual Page Mode 2026-06-07

- Product direction changed: the site is not edited directly like WordPress.
- The admin has a `Режим страницы` button that opens a fullscreen visual editing mode inside the admin.
- The live site changes only after pressing `Сохранить`.
- The builder now has an undo control:
  - choose 1-10 steps;
  - click `Откатить`;
  - if the rollback looks good, press `Сохранить`.
- The old direct-site edit flow is no longer the main workflow; visual work should happen in the admin page mode.
