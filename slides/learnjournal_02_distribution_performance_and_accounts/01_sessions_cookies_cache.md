---
marp: true
theme: default
paginate: true
---

# 03B-1 Sessions / Cookies / Cache

三個都在「記住資料」，但資料的擁有者、位置與風險不同。

---

# Cookie：瀏覽器幫你帶回來

本專案用 cookie 記「閱讀密度」：

```python
response.set_cookie(
    "reading_mode",
    mode,
    max_age=60 * 60 * 24 * 365,
    samesite="Lax",
    secure=not settings.DEBUG,
)
```

重點：cookie 來自 client，**不能把它當可信權限資料**。

---

# 實際觀察 cookie

1. 啟動 server。
2. 在側欄切換「舒適 / 緊湊」。
3. 開 DevTools → Application/Storage → Cookies。
4. 找 `reading_mode`。
5. 重新整理頁面，確認 class 仍是 `reading-compact` 或 `reading-comfortable`。

可手動改 cookie，這正好證明它不可信。

---

# Session：server 端保存的 per-browser 狀態

文章頁把最近看過的 article id 放進 session：

```python
previous = request.session.get("recent_article_ids", [])
request.session["recent_article_ids"] = [article.pk] + [
    pk for pk in previous if pk != article.pk
][:4]
```

瀏覽器通常只保存 session key；真正資料由 Django session backend 管理。

---

# 為什麼 session 只存 ID？

不要把整個 model object 塞進 session。

存 ID 的好處：

- session 小很多
- 文章改標題後不會顯示舊資料
- 每次顯示時仍經過 `Article.published` 規則
- 容易設定最多 5 筆

---

# 用 shell 看 session 的心智模型

```bash
uv run python manage.py shell
```

你不必手動操作 session table 才算理解；先記住：

```text
browser cookie
   ↓ session key
SessionMiddleware
   ↓
request.session  ←→ session backend
```

---

# Cache：不同 request 共用結果

`site_nav` 不是每次都打 DB：

```python
categories = cache.get(NAV_CACHE_KEY)
if categories is None:
    categories = tuple(Category.objects.values("name", "slug"))
    cache.set(NAV_CACHE_KEY, categories, timeout=300)
```

這就是最基本的 **cache-aside** 模式。

---

# Hit / Miss / Expire / Invalidate

四個字一定要分清楚：

- miss：cache 沒有 → 去 DB 算
- hit：cache 有 → 直接拿
- expire：TTL 到期自動失效
- invalidate：資料變更時主動刪 cache

本專案用 signal 在 Category 變更後 `cache.delete()`。

---

# Template fragment cache

側欄示範：

```django
{% load cache %}
{% cache 300 sidebar_latest %}
  {% latest_articles 5 %}
{% endcache %}
```

適合「頁面只有一小塊昂貴，但整頁不能共用」的情境。

---

# 為什麼不 cache 整個首頁？

首頁包含：

- `request.GET.q`
- 分頁
- session 的最近文章
- cookie 的閱讀模式
- 登入狀態

整頁 cache 若 key 設計不完整，很容易把 A 使用者的內容送給 B。

---

# 測試

```bash
uv run python manage.py test journal.tests.SessionCookieMiddlewareTests
```

你應該看到測試涵蓋：

- 文章 id 寫入 session
- cookie value 被設成 `compact`
- middleware 加上 response header

---

# 常見錯誤

- `request.session` 不存在：檢查 `SessionMiddleware`
- cookie 設了但瀏覽器沒送回：檢查 domain/path/secure
- cache 改資料後仍舊：你遇到 stale cache，思考 invalidation
- LocMemCache 在多 process 不共享：production 要用共用 backend

---

# 本章檢核

1. 權限角色可以存在 cookie 嗎？為什麼？
2. session 適合存 model instance 嗎？
3. cache timeout 與 invalidation 有何差別？
4. 為什麼 production 多 process 不適合 LocMemCache？
