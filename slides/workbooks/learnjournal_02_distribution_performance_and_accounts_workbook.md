# LearnJournal 03B Workbook：傳播、效能、帳號與排程

這份手冊搭配 `slides/learnjournal_02_distribution_performance_and_accounts/`。每節都包含「操作 → 觀察 → 驗證 → 常見錯誤」。

## 0. 共通準備

```bash
cd learnjournal
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py check
uv run python manage.py test
uv run python manage.py runserver
```

建議保留兩個 terminal：A 跑 `runserver`，B 跑 shell、tests、commands。

如果你看到 `No such file: manage.py`，先用 `pwd`（Windows PowerShell 用 `Get-Location`）確認目前目錄真的是 `learnjournal/`。

---

## 1. Sessions / Cookies / Cache

### 1-1 Session：最近看過

1. 打開兩篇不同文章。
2. 回首頁。
3. 側欄應出現「最近看過（session）」。
4. DevTools → Cookies 可以看到 session key，但不會直接看到文章 id 清單。

測試：

```bash
uv run python manage.py test journal.tests.SessionCookieMiddlewareTests.test_detail_records_recent_article_in_session
```

核心程式：`journal/views.py` 的 `ArticleDetailView.get()` 與 `HomeView.get_context_data()`。

### 1-2 Cookie：閱讀密度

在側欄切換「舒適 / 緊湊」，DevTools 找 `reading_mode`。手動把值改成 `unknown` 再 reload；context processor 會 fallback 成 `comfortable`。

測試：

```bash
uv run python manage.py test journal.tests.SessionCookieMiddlewareTests.test_reading_mode_is_stored_in_cookie
```

### 1-3 Cache：導覽與 sidebar

`journal/context_processors.py` 示範 low-level cache；`templates/journal/_sidebar.html` 示範 template fragment cache。

思考題：為什麼最近看過的文章沒有包進共用 fragment cache？

答案要點：它是 per-session personalized data，若 cache key 沒把使用者/session 納入，會資料串錯。

---

## 2. Middleware

### 2-1 Response header

```bash
curl -I http://127.0.0.1:8000/
```

確認有：

```text
X-Response-Time: ...ms
```

測試：

```bash
uv run python manage.py test journal.tests.SessionCookieMiddlewareTests.test_response_time_middleware_adds_header
```

### 2-2 Maintenance mode

macOS/Linux：

```bash
DJANGO_MAINTENANCE_MODE=1 uv run python manage.py runserver
```

PowerShell：

```powershell
$env:DJANGO_MAINTENANCE_MODE="1"
uv run python manage.py runserver
```

首頁應回 HTTP 503。關掉 terminal 或清掉環境變數後恢復。

觀察 `config/settings.py` 的 middleware 順序：maintenance middleware 在 AuthenticationMiddleware 後，因為它要讀 `request.user`。

---

## 3. Email / Password Reset / Double Opt-in

### 3-1 密碼重設

1. 打開 `/accounts/password-reset/`。
2. 輸入 `amy@example.com`。
3. terminal 會印出 email。
4. 複製 `/accounts/reset/.../.../` URL。
5. 設定新密碼。

驗證：舊密碼不能登入，新密碼可以。

```bash
uv run python manage.py test journal.tests.SubscriptionAndPasswordResetTests
```

### 3-2 電子報 double opt-in

1. 開 `/subscribe/`。
2. 輸入一個新 email。
3. terminal 複製確認 URL。
4. 點擊後再進 shell：

```bash
uv run python manage.py shell
```

```python
from journal.models import Subscription
Subscription.objects.values("email", "is_confirmed")
```

未點確認前 `False`，點完後 `True`。

---

## 4. Group / Permission

`seed_demo` 建立 `Editors` 群組並把 `editor` 放進去。

### 4-1 在 shell 比較

```bash
uv run python manage.py shell
```

```python
from journal.models import User
editor = User.objects.get(username="editor")
amy = User.objects.get(username="amy")
editor.has_perm("journal.publish_article")
amy.has_perm("journal.publish_article")
```

預期：`True` / `False`。

### 4-2 UI 比較

- amy 登入：可存草稿；排程／發佈會表單錯誤。
- editor 登入：可排程與發佈。

測試：

```bash
uv run python manage.py test journal.tests.PublishingPermissionTests
```

---

## 5. RSS / Sitemap

```bash
curl http://127.0.0.1:8000/feed/
curl http://127.0.0.1:8000/sitemap.xml
```

檢查 XML 只包含公開文章，不包含 draft/scheduled。

```bash
uv run python manage.py test journal.tests.FeedSitemapAndCommandTests.test_feed_and_sitemap_expose_published_article
```

延伸：新增一篇 draft，重新抓 sitemap，確認 draft title / URL 不存在。

---

## 6. Management Commands / Scheduling

### 6-1 建立一篇已到期的 scheduled article

可用 admin，或 shell：

```python
from datetime import timedelta
from django.utils import timezone
from journal.models import Article, Category, User

Article.objects.create(
    author=User.objects.get(username="editor"),
    category=Category.objects.first(),
    title="排程測試",
    body="scheduled",
    status=Article.Status.SCHEDULED,
    published_at=timezone.now() - timedelta(minutes=1),
)
```

### 6-2 Dry-run

```bash
uv run python manage.py publish_scheduled --dry-run
```

確認 DB 沒變，再執行：

```bash
uv run python manage.py publish_scheduled
```

### 6-3 Digest

```bash
uv run python manage.py send_weekly_digest --dry-run
uv run python manage.py send_weekly_digest --days 14
```

沒有 confirmed subscriber 或期間內沒有文章時，command 應該安全退出而不是報錯。

### 6-4 排程概念

cron 範例（production 請使用絕對路徑與正確環境）：

```cron
*/5 * * * * cd /srv/learnjournal && /usr/local/bin/uv run python manage.py publish_scheduled
0 8 * * 1 cd /srv/learnjournal && /usr/local/bin/uv run python manage.py send_weekly_digest
```

---

## 7. PostgreSQL Full-text Search

SQLite 保持預設，因此第一次學習不需要 PostgreSQL。

### 7-1 安裝 optional extra

```bash
uv sync --extra postgres
```

### 7-2 設定環境變數

macOS/Linux：

```bash
export DJANGO_DB_ENGINE=postgresql
export DJANGO_DB_NAME=learnjournal
export DJANGO_DB_USER=learnjournal
export DJANGO_DB_PASSWORD='your-password'
export DJANGO_DB_HOST=127.0.0.1
export DJANGO_DB_PORT=5432
```

PowerShell：

```powershell
$env:DJANGO_DB_ENGINE="postgresql"
$env:DJANGO_DB_NAME="learnjournal"
$env:DJANGO_DB_USER="learnjournal"
$env:DJANGO_DB_PASSWORD="your-password"
$env:DJANGO_DB_HOST="127.0.0.1"
$env:DJANGO_DB_PORT="5432"
```

### 7-3 驗證 backend

```bash
uv run python manage.py shell -c "from django.db import connection; print(connection.vendor)"
```

必須看到 `postgresql` 才算真的切換。

### 7-4 建 schema 與 demo data

```bash
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver
```

首頁搜尋時，`ArticleQuerySet.search()` 會走 SearchVector / SearchQuery / SearchRank；SQLite 則走 `icontains` fallback。

注意：`config="simple"` 用來清楚展示 PostgreSQL FTS API，不代表已解決完整中文斷詞。中文 production search 應另外評估 pg_trgm、tokenizer extension 或搜尋服務。

---

## 8. 完成檢查

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
python ../scripts/check_material_links.py --root ..
```

你應該能從 test failure 反推是哪一層出問題：URL、middleware、form permission、email backend、session/cookie、command 或 database backend。
