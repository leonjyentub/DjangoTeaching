# 學誌 LearnJournal

課程**第三階段**的 Django 教學專案：一個多作者的發佈平台（部落格 / CMS）。前兩階段的
[學言 LearnBoard](../learnboard/)（社群 CRUD 與擁有權）與 [學購 LearnMart](../learnmart/)
（交易與資料完整性）之後，這個專案的主題是**內容的發佈與傳播，以及效能**。

規劃背景與完整缺口盤點見 [`../slides/03_next_project_plan.md`](../slides/03_next_project_plan.md)。

## 技術選擇

- Python 3.13，由 uv 管理 `.venv`、依賴與 `uv.lock`
- Django 5.2 LTS
- SQLite（Deck 03B 第 11 章會換 PostgreSQL 做全文檢索）
- `markdown`（內文渲染）
- Bootstrap 5.3 CDN + 少量自訂 CSS，mobile-first RWD

## 快速開始

```bash
cd /path/to/learnjournal
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver
```

瀏覽 `http://127.0.0.1:8000/`。示範帳號（僅供本機教學）：

- `editor` / `editor12345`
- `amy` / `amy12345`
- `ben` / `ben12345`

`seed_demo` 可重複執行；若同名帳號已存在，不會重設密碼。建立後台帳號：

```bash
uv run python manage.py createsuperuser
```

## 這個專案「新教」什麼（兩個前專案沒有的）

| 主題 | 落點 | 回扣 |
|---|---|---|
| **多對多關聯** | `Article.tags`（through `ArticleTag`）、`Article.coauthors` | LearnBoard／LearnMart 只有 ForeignKey |
| **through 中介模型** | `ArticleTag.featured_order` | `OrderItem` 的「關聯上帶資料」 |
| **自我關聯 ForeignKey** | `Comment.parent` 巢狀留言 | 全新 |
| **自訂 Manager / QuerySet** | `journal/managers.py`、`Article.published` | `Product.objects.filter(is_active=True)` 到處重複 |
| **`F()` 原子遞增** | `Article.register_view()` | LearnMart 扣庫存的 race condition，這次做對 |
| **`CheckConstraint` / `Meta.indexes`** | `Article.Meta` | LearnMart 只用過 `UniqueConstraint` |
| **slug + 日期網址** | `/2026/08/29/<slug>/`、`unique_for_date`、自訂 unicode slug converter | — |
| **日期型 generic view** | `YearArchiveView` / `MonthArchiveView` | `ListView` / `DetailView` 之外的第三個家族 |
| **`values().annotate()` = GROUP BY** | 標籤雲 `{% tag_cloud %}` | `aggregate` / `annotate` 的延伸 |
| **自訂 template tags / filters** | `journal/templatetags/journal_extras.py`（filter / simple_tag / inclusion_tag） | — |
| **`FormMixin` 疊在 `DetailView`** | `ArticleDetailView`（文章頁 + 留言表單） | LearnMart `add_review` 的手工 function view |
| **Signals** | `journal/signals.py`（存檔渲染 Markdown） | 全新；並討論「何時不該用 signal」 |
| **`RunPython` data migration** | `0003_backfill_excerpt.py` | LearnBoard `0002_message_author` 的 schema 演進化石 |
| **時區與日期網址** | `get_absolute_url()` 用 `localtime` 對齊 `__year/__month/__day` | `USE_TZ` 的實際後果 |

## 尚未實作（後續章節 / Deck 03B、04 的目標）

程式碼裡以 `# Deck 03B ...` / `# Deck 04 ...` 註解標出掛鉤點：

- Sessions / Cookies（匿名最近瀏覽）、快取框架與片段快取
- Signals 深入（留言通知寄信、`m2m_changed` 更新計數、快取失效）
- 自訂 middleware（瀏覽計數 / `X-Response-Time` / 維護模式）
- Email 與內建密碼重設四件組；電子報 double opt-in 寄信與確認
- 全文檢索（PostgreSQL `SearchVector` / `SearchRank`）
- `contrib.syndication`（RSS）、`contrib.sitemaps`
- Django 權限框架（Group / Permission）取代目前「任何登入者都能寫」
- management command 加參數（`publish_scheduled --dry-run`、`send_weekly_digest`）+ cron
- `inlineformset_factory`（一篇文章多張圖）
- settings 拆分、環境變數、`collectstatic`、部署

## 專案結構

```text
learnjournal/
├── config/                    # settings、根路由、ASGI/WSGI
├── journal/
│   ├── models.py              # User / Category / Tag / Article / ArticleTag / Comment / Reaction / Subscription
│   ├── managers.py            # ArticleQuerySet / PublishedManager
│   ├── views.py               # function view + generic view + 日期型 view + FormMixin
│   ├── forms.py               # ModelForm，含動態 queryset
│   ├── signals.py             # post_save：渲染 Markdown（其餘留掛鉤）
│   ├── context_processors.py  # 導覽列分類
│   ├── templatetags/journal_extras.py
│   ├── admin.py               # inline、action、prepopulated_fields、date_hierarchy
│   ├── migrations/            # 0003 是教學用 RunPython data migration
│   └── management/commands/seed_demo.py
├── templates/                 # base、journal/、registration/
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

目前有 11 支 `TestCase`，覆蓋 published manager、`F()` 遞增、日期網址與時區、M2M 正反向、
巢狀留言權限、文章擁有權。

## 教學設計說明

延續前兩個專案「最小但完整」的原則：每個新特性只留一個最清楚的示範點，變體交給
workbook 練習。這是教學版，不應直接營運——正式站還需要環境變數管理、`DEBUG=False`、
HTTPS、物件儲存、快取後端、rate limit、垃圾留言防治與更完整的測試（Deck 04 主題）。

## 主要參考資料

- [Django 5.2 官方文件](https://docs.djangoproject.com/en/5.2/)
- [Many-to-many relationships](https://docs.djangoproject.com/en/5.2/topics/db/examples/many_to_many/)
- [Managers](https://docs.djangoproject.com/en/5.2/topics/db/managers/)
- [Custom template tags and filters](https://docs.djangoproject.com/en/5.2/howto/custom-template-tags/)
- [Class-based views: date-based](https://docs.djangoproject.com/en/5.2/ref/class-based-views/generic-date-based/)
- [Signals](https://docs.djangoproject.com/en/5.2/topics/signals/)
- [Data migrations](https://docs.djangoproject.com/en/5.2/topics/migrations/#data-migrations)
- [Time zones](https://docs.djangoproject.com/en/5.2/topics/i18n/timezones/)
