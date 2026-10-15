(function () {
  "use strict";

  var container = document.querySelector(".js-news-strip-single[data-news-feed-url]");
  if (!container) return;

  var feedUrl = container.getAttribute("data-news-feed-url");
  if (!feedUrl) return;

  var loaded = false;
  var loading = false;
  var items = [];
  var cursor = 0;
  var sentinel = document.createElement("div");
  sentinel.className = "seo-news-strip__loader";
  sentinel.setAttribute("aria-hidden", "true");
  container.appendChild(sentinel);

  function text(value) {
    return value == null ? "" : String(value);
  }

  function makeLink(className, href) {
    var link = document.createElement("a");
    link.className = className;
    link.href = href || "#";
    return link;
  }

  function renderItem(item) {
    var article = document.createElement("article");
    article.className = "seo-news-article seo-news-article--loaded";
    article.setAttribute("data-news-url", text(item.url));
    if (item.path) article.setAttribute("data-news-path", text(item.path));
    article.setAttribute("data-news-cluster", text(item.cluster));

    var title = document.createElement("h2");
    title.className = "seo-news-article__title";
    title.setAttribute("data-news-field", "title");
    title.textContent = text(item.title);
    article.appendChild(title);

    var date = document.createElement("time");
    date.className = "seo-news-article__date";
    date.dateTime = text(item.dateISO);
    date.textContent = text(item.dateText);
    article.appendChild(date);

    if (item.image) {
      var imageLink = makeLink("seo-news-article__image-link", item.url);
      imageLink.setAttribute("aria-label", text(item.title));

      var image = document.createElement("img");
      image.className = "seo-news-article__image";
      image.src = item.image;
      image.alt = text(item.title);
      image.setAttribute("data-news-image", "");
      if (Number(item.imageWidth) > 0) {
        image.style.width = Number(item.imageWidth) + "px";
        image.style.maxWidth = "none";
        image.style.float = "none";
      }
      image.loading = "lazy";
      image.decoding = "async";
      imageLink.appendChild(image);
      article.appendChild(imageLink);
    }

    var body = document.createElement("div");
    body.className = "seo-news-article__body";
    body.setAttribute("data-news-field", "description");
    body.innerHTML = text(item.bodyHtml || item.body);
    body.querySelectorAll("a").forEach(function (link) { link.replaceWith.apply(link, Array.from(link.childNodes)); });
    article.appendChild(body);


    return article;
  }

  function appendNext() {
    if (cursor >= items.length) {
      sentinel.remove();
      return;
    }
    container.insertBefore(renderItem(items[cursor]), sentinel);
    cursor += 1;
  }

  function loadFeed() {
    if (loaded || loading) return;
    loading = true;
    fetch(feedUrl, { credentials: "same-origin" })
      .then(function (response) {
        if (!response.ok) throw new Error("News feed failed");
        return response.json();
      })
      .then(function (data) {
        items = Array.isArray(data.items) ? data.items : [];
        loaded = true;
        appendNext();
      })
      .catch(function () {
        sentinel.remove();
      })
      .finally(function () {
        loading = false;
      });
  }

  function nearBottom() {
    return container.scrollTop + container.clientHeight >= container.scrollHeight - 90;
  }

  container.addEventListener("scroll", function () {
    if (!loaded && nearBottom()) {
      loadFeed();
      return;
    }
    if (loaded && nearBottom()) appendNext();
  }, { passive: true });
})();
