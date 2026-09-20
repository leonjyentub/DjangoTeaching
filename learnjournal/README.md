# 學誌 LearnJournal

課程**第三階段**的 Django 教學專案：一個多作者的發佈平台（部落格 / CMS）。前兩階段的
[學言 LearnBoard](../learnboard/)（社群 CRUD 與擁有權）與 [學購 LearnMart](../learnmart/)
（交易與資料完整性）之後，這個專案的主題是**內容的發佈與傳播，以及效能**。

03A 與 03B 都已有對應可執行實作與教材；後續延伸候選見[教材維護摘要](../docs/MAINTENANCE.md)。

## 技術選擇

- Python 3.14.7，由 uv 管理 `.venv`、依賴與 `uv.lock`
- Django 6.1.1
- SQLite（零設定課堂預設）
- PostgreSQL（03B optional 路線，用 `SearchVector` / `SearchRank`）
- `markdown`（內文渲染）
- Bootstrap 5.3 CDN + 少量自訂 CSS，mobile-first RWD
- LocMemCache（課堂）／可替換共用 cache backend（production）
- console email backend（課堂）／可由環境變數替換

## 快速開始

```bash
cd /path/to/learnjournal
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver
```

瀏覽 `http://127.0.0.1:8000/`。示範帳號（僅供本機教學）：

- `editor` / `editor12345`：屬於 `Editors` 群組，可排程／發佈文章
- `amy` / `amy12345`：一般作者，可寫草稿
- `ben` / `ben12345`：一般作者，可寫草稿

`seed_demo` 可重複執行；若同名帳號已存在，不會重設密碼。建立後台帳號：

```bash
uv run python manage.py createsuperuser
```

## 03A：內容模型與發佈基礎

- ManyToManyField、through model、self-FK
- custom Manager / QuerySet
- `F()` 原子遞增
- `CheckConstraint` / indexes
- slug + 日期網址、date-based generic views
- `values().annotate()` 分組統計
- custom template tags / filters
- `FormMixin + DetailView`
- signals、`RunPython` data migration、時區

教材：[`../slides/learnjournal_01_content_model_and_publishing/`](../slides/learnjournal_01_content_model_and_publishing/)

## 03B：已完成的傳播、效能與帳號功能

- Sessions：匿名最近瀏覽文章
- Cookies：閱讀密度偏好
- Low-level cache + template fragment cache + invalidation
- 自訂 middleware：`X-Response-Time`、維護模式 503
- Email：留言通知、console/locmem backend 教學
- Django 內建 password reset 四步流程
- 電子報 double opt-in token / confirmation
- Django Group / Permission：`Editors` + `journal.publish_article`
- RSS feed + sitemap
- `publish_scheduled --dry-run` / `send_weekly_digest --dry-run`
- 環境變數切換 PostgreSQL，全文搜尋使用 `SearchVector` / `SearchQuery` / `SearchRank`
- SQLite 保留 `icontains` fallback，讓第一次操作不需要先安裝 PostgreSQL

教材：[`../slides/learnjournal_02_distribution_performance_and_accounts/`](../slides/learnjournal_02_distribution_performance_and_accounts/)

Workbook：[`../slides/workbooks/learnjournal_02_distribution_performance_and_accounts_workbook.md`](../slides/workbooks/learnjournal_02_distribution_performance_and_accounts_workbook.md)

## PostgreSQL / 全文搜尋（optional）

安裝 optional driver：

```bash
uv sync --extra postgres
```

設定 `DJANGO_DB_ENGINE=postgresql` 與 `DJANGO_DB_NAME`、`DJANGO_DB_USER`、`DJANGO_DB_PASSWORD`、`DJANGO_DB_HOST`、`DJANGO_DB_PORT` 後：

```bash
uv run python manage.py shell -c "from django.db import connection; print(connection.vendor)"
uv run python manage.py migrate
uv run python manage.py seed_demo
```

應先確認輸出是 `postgresql`。`config="simple"` 的 FTS 用於教學 PostgreSQL search API；完整中文斷詞仍應另外評估 `pg_trgm`、tokenizer extension 或專用搜尋服務。

## Management commands

```bash
uv run python manage.py publish_scheduled --dry-run
uv run python manage.py publish_scheduled
uv run python manage.py send_weekly_digest --dry-run
uv run python manage.py send_weekly_digest --days 14
```

Command 定義「做什麼」；cron/systemd timer/container scheduler 定義「什麼時候做」。詳細排程範例在 03B workbook。

## 專案結構

```text
learnjournal/
├── config/                    # settings、根路由、ASGI/WSGI
├── journal/
│   ├── models.py              # User / Category / Tag / Article / ...
│   ├── managers.py            # SQLite fallback + PostgreSQL FTS
│   ├── views.py               # pages、session、cookie、double opt-in
│   ├── forms.py               # ModelForm + publish permission
│   ├── middleware.py          # response time / maintenance mode
│   ├── feeds.py               # RSS
│   ├── sitemaps.py            # sitemap.xml
│   ├── signals.py             # Markdown、cache invalidation、comment email
│   ├── context_processors.py  # cached nav + cookie preference
│   ├── templatetags/journal_extras.py
│   ├── migrations/            # schema/data/permission 演進
│   └── management/commands/   # seed_demo / publish_scheduled / digest
├── templates/                 # base、journal/、registration/password reset
├── static/css/site.css
├── manage.py
└── pyproject.toml
```

## 驗證

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

測試現在除了 03A 的 ORM／日期／M2M／ownership，也覆蓋 03B 的 session/cookie、middleware、publish permission、email/double opt-in、password reset、RSS/sitemap 與 scheduled publishing command。

Repository 教材相對連結另可檢查：

```bash
python ../scripts/check_material_links.py --root ..
```

## 尚未納入本專案 runtime 的延伸題

這些仍適合留作進階作業，而不是阻塞 03B：

- `inlineformset_factory`：一篇文章多張圖
- 更完整中文搜尋 tokenizer / GIN index / materialized search vector
- Redis 等 shared cache backend
- production SMTP / async job queue
- rate limit、spam moderation、監控與 object storage

跨三專案共用的 production 基礎已收進連續教學教材的 [部署設定與正式環境](../slides/courses/16_部署設定與正式環境.md)（第 22～24 章）與 [服務運行與發布維護](../slides/courses/17_服務運行與發布維護.md)（第 25～27 章）。

## 教學設計說明

延續前兩個專案「最小但完整」的原則：每個新特性只留一個清楚、可觀察、可測試的示範點。03B 特別強調同一個功能要能從 browser / response header / terminal email / session-cookie / management command / test assertion 觀察到，不只閱讀 API 名稱。

這仍是教學版，不應直接營運；正式站還需要依實際環境完成 HTTPS/proxy、shared cache、object storage、SMTP/job queue、rate limit、logging/monitoring、backup/restore 與 release process。

## 主要參考資料

- [Django 6.1.1 官方文件](https://docs.djangoproject.com/en/6.1/)
- [Many-to-many relationships](https://docs.djangoproject.com/en/6.1/topics/db/examples/many_to_many/)
- [Managers](https://docs.djangoproject.com/en/6.1/topics/db/managers/)
- [Custom template tags and filters](https://docs.djangoproject.com/en/6.1/howto/custom-template-tags/)
- [Sessions](https://docs.djangoproject.com/en/6.1/topics/http/sessions/)
- [Cache framework](https://docs.djangoproject.com/en/6.1/topics/cache/)
- [Middleware](https://docs.djangoproject.com/en/6.1/topics/http/middleware/)
- [Authentication / permissions](https://docs.djangoproject.com/en/6.1/topics/auth/)
- [Email](https://docs.djangoproject.com/en/6.1/topics/email/)
- [Syndication feed framework](https://docs.djangoproject.com/en/6.1/ref/contrib/syndication/)
- [Sitemap framework](https://docs.djangoproject.com/en/6.1/ref/contrib/sitemaps/)
- [PostgreSQL full text search](https://docs.djangoproject.com/en/6.1/ref/contrib/postgres/search/)
