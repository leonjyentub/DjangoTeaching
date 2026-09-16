---
marp: true
theme: default
paginate: true
---

# 03B-5 RSS / Sitemap

同一批公開文章，可以給人看，也可以給 feed reader / crawler 看。

---

# RSS 解決什麼？

RSS 是「機器可讀的更新清單」。

本專案：

```text
/feed/
```

用 Django `contrib.syndication` 產生 XML。

---

# Feed class

```python
class LatestArticlesFeed(Feed):
    def items(self):
        return Article.published.all()[:20]

    def item_pubdate(self, item):
        return item.published_at
```

同一個 `Article.published` 規則被 HTML、RSS、sitemap 重用。

---

# 瀏覽 XML

```bash
curl http://127.0.0.1:8000/feed/
```

或直接開瀏覽器。

觀察：

- `<title>`
- `<link>`
- `<description>`
- `<pubDate>`
- 每篇 `<item>`

---

# Sitemap 解決什麼？

`sitemap.xml` 告訴 crawler：

- 哪些 URL 值得抓
- 最後更新時間
- 大致更新頻率 / priority

本專案：

```text
/sitemap.xml
```

---

# Sitemap class

```python
class ArticleSitemap(Sitemap):
    def items(self):
        return Article.published.all()

    def lastmod(self, obj):
        return obj.updated_at
```

草稿與未到期文章不該出現在 sitemap。

---

# Feed / Sitemap 不是 SEO 魔法

它們只是結構化入口。

還要考慮：

- canonical URL
- robots policy
- status code
- 內容品質
- page speed
- 公開／私人資料邊界

---

# `get_absolute_url()` 的價值

Feed、sitemap、redirect、template 都需要 article URL。

把 URL 規則集中：

```python
article.get_absolute_url()
```

比每個地方手動拼 `/2026/09/...` 更安全。

---

# 測試

```python
self.assertContains(
    self.client.get(reverse("feed")),
    "Feed 測試",
)

self.assertContains(
    self.client.get(reverse("sitemap")),
    article.get_absolute_url(),
)
```

測公開內容有出現，而不是只測 200。

---

# 本章檢核

1. RSS 與 sitemap 的消費者有何不同？
2. 為什麼兩者都應重用 published QuerySet？
3. 草稿出現在 sitemap 有什麼問題？
4. `get_absolute_url()` 幫你消除哪種重複？
