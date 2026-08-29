# 第三個教學專案規劃：LearnJournal（學誌）與語法／特性缺口補完

**用途：** 規劃 LearnBoard → LearnMart 之後的下一個教學專案，盤點兩個現有專案沒教到的 Python 語法與 Django 特性，並給出 Deck 03／04 的章節地圖。
**性質：** 一般 Markdown 規劃文件（非 Marp），供授課者與投影片拆分 agent 共用。
**基準：** 目前 repository 的 `learnboard/`、`learnmart/` 與 `slides/00a–02`。

---

## 0. 實作進度（2026-08-29）

已建立 `learnjournal/` 骨架 ＋ Deck 03A（第 1–6 章）對應的可跑實作：

- uv 環境（Django 5.2 ＋ `markdown`）、`journal` app、`config` settings（含 email console backend、locmem cache、`sitemaps`／`humanize`）
- Models：`User`／`Category`／`Tag`／`Article`／`ArticleTag`(through)／`Comment`(self-FK)／`Reaction`／`Subscription`；`F()` 原子遞增、`CheckConstraint`、`Meta.indexes`、`unique_for_date`、`allow_unicode` slug
- `journal/managers.py`：`ArticleQuerySet` ＋ `PublishedManager`
- Views：`HomeView`／分類／標籤／作者、`ArticleDetailView`（`FormMixin` ＋日期網址 ＋`F()` 遞增）、`YearArchiveView`／`MonthArchiveView`、草稿預覽、寫作 CRUD、訂閱
- `journal/urls.py`：自訂 `uslug` unicode path converter；`/YYYY/MM/DD/<slug>/`
- `journal/templatetags/journal_extras.py`：`markdownify` filter、`reading_time` simple_tag、`tag_cloud`／`latest_articles` inclusion_tag（`values().annotate()` GROUP BY）
- `journal/signals.py`：`post_save` 渲染 Markdown（其餘副作用留掛鉤）
- `journal/admin.py`：inline、admin action、`prepopulated_fields`、`date_hierarchy`、`autocomplete_fields`
- `journal/migrations/0003_backfill_excerpt.py`：教學用 `RunPython` data migration
- `seed_demo`、11 支 `TestCase`（published manager／`F()`／時區日期網址／M2M 正反向／巢狀留言權限／文章擁有權）全綠

尚未做（Deck 03B／04 的目標，程式碼中以 `# Deck 03B …`／`# Deck 04 …` 標註掛鉤點）：
sessions／cookies、快取框架、signal 深入、自訂 middleware、email／密碼重設、全文檢索（PostgreSQL）、
RSS／sitemap 內容、Django 權限框架、帶參數的 management command ＋ cron、`inlineformset_factory`、部署。

詳見 [`../learnjournal/README.md`](../learnjournal/README.md)。

---

## 1. 建議專案：LearnJournal 學誌（多作者發佈平台 / 部落格 CMS）

### 1-1 為什麼是「發佈型」網站

課程到目前為止建立了兩根支柱，第三個專案應該補上第三根：

| 專案 | 領域主軸 | 核心心智模型 |
|---|---|---|
| LearnBoard 學言板 | 社群 CRUD ＋擁有權 | 誰可以改哪一筆資料（authentication / authorization） |
| LearnMart 學購商城 | 商業交易 ＋資料完整性 | 多筆寫入一起成功或一起失敗（transaction / locking） |
| **LearnJournal 學誌** | **內容發佈與傳播 ＋效能** | **把內容做出來 → 被找到 → 被訂閱 → 扛得住流量** |

發佈型網站會「自然逼出」兩個現有專案完全沒碰到的東西，不需要為了教語法而硬湊情境：

- 多對多關聯（標籤、共同作者）— **兩個專案都只有 ForeignKey，這是最大的結構缺口**
- 自我關聯 ForeignKey（巢狀留言）
- 自訂 Manager／QuerySet（`Article.objects.published()`）
- slug 與日期網址、日期型 generic view、月份彙整（GROUP BY）
- 自訂 template tag／filter（Markdown、閱讀時間、標籤雲）
- RSS feed、sitemap、full-text search（正好帶出換 PostgreSQL）
- 快取框架、signal、自訂 middleware
- Email 與內建密碼重設流程
- 帶參數的 management command ＋ 排程（cron）
- 部署與營運（兩個 README 結尾「不應上線」清單的逐項實作）

### 1-2 領域模型草案（app：`journal`）

```text
User(AbstractUser)          # 沿用 LearnMart 的自訂 User 時機課；
                            # 但角色改用 Django 內建 Group / Permission，補上權限框架
Category    FK 目標          # 一篇文章一個分類
Tag         M2M ↔ Article   # 第一次教 ManyToManyField
Article
  author        FK   → User
  coauthors     M2M  → User (related_name="coauthored")   # 同一模型第二個 M2M
  category      FK   → Category (on_delete=PROTECT)
  slug         SlugField(unique_for_date="published_at")
  status       draft / scheduled / published   # TextChoices，回扣 Order.Status
  published_at DateTimeField(null=True)
  body         TextField   # Markdown 原文
  body_html    TextField   # 快取渲染結果，透過 signal 更新
  view_count   PositiveIntegerField   # 用 F() 原子遞增（回扣扣庫存 race）
  Meta: CheckConstraint(status=published → published_at 必填)、indexes
ArticleTag  through model   # 給「精選排序」欄位，教 through=
Comment
  article  FK → Article
  parent   FK → self (null=True)   # 自我關聯：巢狀留言
  is_approved  BooleanField        # 審核
Reaction    (user, article, kind)  # M2M through
Subscription  email + confirm_token # 電子報 double opt-in
Follow      M2M(User ↔ User, self) # 追蹤作者
Bookmark    M2M(User ↔ Article)    # 收藏
```

頁面／流程：首頁分頁清單、分類頁、標籤頁（標籤雲用 `annotate(Count)`）、文章頁（`/2026/08/29/<slug>/`、巢狀留言、reaction、閱讀時間、目次）、月份彙整（`/2026/08/`）、全文檢索、作者頁 ＋ RSS、sitemap.xml、編輯後台（草稿／排程／Markdown 預覽／formset 多圖）、電子報訂閱 ＋ 確認信 ＋ 每週摘要、密碼重設。

### 1-3 為什麼不是其他選擇

| 候選 | 補得到的缺口 | 為何較不推薦作為「下一步」 |
|---|---|---|
| LMS／課程平台（LearnCourse） | M2M 報名、容量 race、行事曆、進度 | template tag／feed／全文檢索／發佈流程的教學動機弱；跟商城的「交易」概念重疊度高 |
| Helpdesk／工單（LearnDesk） | 狀態機、指派、SLA、權限框架、signal、middleware | 新手覺得像「內部系統」，缺乏直覺的公開頁面；M2M 以外的畫面偏少 |
| **部落格／發佈平台（LearnJournal）** | **見 §4 全表，覆蓋最完整** | — 官方文件與教材資源最多，學生腦中最容易有成品畫面 |

> LMS 可作為「學有餘力的第二選擇」；工單系統適合作為權限框架的補充案例，但不必整個做。

---

## 2. 現有教材已涵蓋的範圍（盤點基準）

- **Python 00a：** 變數／型別／None、f-string ＋字串方法、list/tuple/dict/set、comprehension（list）、if/truthy、for/range/enumerate、while/break/continue、`def`／預設值／`*args`／`**kwargs`／作用域、try/except/raise、import、Decimal／timezone、class／self／`__init__`／`__str__`／`Meta`／`TextChoices`／`@property`、繼承／override／`super()`／mixin／abstract、decorator、型別標註基礎。
- **HTML/CSS 00b：** 文件結構、常用與語意標籤、表單標籤、CSS 選擇器／優先權／box model／display、RWD／media query／mobile-first、Bootstrap grid。
- **Django 01：** uv／venv／pyproject、project/app／settings／manage.py、HTTP／URL／converter／命名 URL／`reverse`、function view、template（繼承／include／filter／if／for／autoescape）、static／media、Bootstrap grid、Model（欄位／`blank`／`null`／`DecimalField`／`ImageField`／FK／`on_delete`／`related_name`／`TextChoices`／`Meta`／`__str__`／property）、migration（含 schema 演進、自訂 User 時機）、ORM（`get`／`filter`／lookup／`Q`／lazy／`count`／`exists`／N+1／`select_related`／`prefetch_related`／`aggregate`／`annotate`／validator／`UniqueConstraint`／`get_or_create`／`update_or_create`）、admin 基礎、pagination。
- **Django 02：** Form／ModelForm／`is_valid`／欄位驗證／`clean()`／`save(commit=False)`、CSRF／PRG／messages／檔案上傳、自訂 User／`AbstractUser`／`create_user`／密碼雜湊／`UserCreationForm`、session／`request.user`／`LoginView`／`next`／POST logout／`LOGIN_REDIRECT_URL`、CBV（`ListView`／`DetailView`／`CreateView`／`UpdateView`／`DeleteView`／`get_queryset`／`get_context_data`／`form_valid`／`as_view`）、`LoginRequiredMixin`／`UserPassesTestMixin`／自訂 mixin、三層授權／IDOR／403·404·405、context processor、`transaction.atomic`／`select_for_update`／rollback、`TestCase`／`Client`／`setUp`／`force_login`／`assertContains`／`assertRedirects`／`refresh_from_db`、XSS／CSRF／SQL injection／upload／`check --deploy`（僅預告）。

---

## 3. 未涵蓋的 Python 語法（補充清單）

建議整理成輕薄的「**00c Python 補充**」（約 3 章），或沿用 Deck 02 第 3 章的做法，散入 Deck 03 各章開頭的「先補語法」頁。

| 語法 | 為什麼需要 | 在 LearnJournal 的落點 |
|---|---|---|
| `lambda` ＋ `sorted`／`min`／`max(key=)` | template tag 排序、標籤雲 | `sorted(tags, key=lambda t: -t.count)` |
| f-string 格式規格 `:,` `:.1f` `:.0%` | 閱讀時間、瀏覽數、比例 | `f"{count:,}"`、`f"{ratio:.0%}"` |
| 三元運算 `a if cond else b` | 狀態標籤、預設值 | `"已發佈" if a.is_live else "草稿"` |
| `with` 區塊型 context manager | `with transaction.atomic():`（非 decorator 形式）、`with open()` 讀 Markdown | 匯入命令 |
| `datetime` / `timedelta` 運算 | 排程發佈、「3 天前」、每週摘要區間 | `timezone.now() - timedelta(days=7)` |
| generator / `yield` | management command 逐筆 yield、串流大量資料 | `import_markdown`、`send_weekly_digest` |
| dict／set comprehension | 建索引表、去重 | `{t.slug: t for t in tags}` |
| 序列解包 `*rest`、字典合併 `{**a, **b}` | context 合併、`Article.objects.create(**data)` | view／測試工廠 |
| `collections.Counter`／`defaultdict` | 純 Python 版標籤統計、月份分組（對照 ORM 的 GROUP BY） | 彙整頁 |
| `functools`：`wraps`／`cached_property`／`lru_cache` | 寫自訂 decorator、`@cached_property def reading_time` | model／decorator |
| 自訂 exception class ＋ `finally`／`else`／`raise ... from` | 匯入失敗、訂閱 token 驗證 | 匯入命令、訂閱流程 |
| dunder：`__repr__`／`__eq__`／`__lt__` ＋ `functools.total_ordering` | 值物件（目次節點）排序與除錯 | template tag |
| 型別標註進階 `X | None`、`list[X]`、`dict[str, X]`、`TYPE_CHECKING` | 函式簽章、避免循環 import | 全專案 |
| 正規表示式 `re` 入門 | slug 驗證、從 Markdown 抓 heading 做目次 | template tag／model |
| `enum.Enum` 對照 `models.TextChoices` | 觀念釐清（為何 Django 用 TextChoices） | 00c |
| `pathlib` 操作（settings 已用未教） | `Path.glob` 掃 Markdown 目錄 | 匯入命令 |

---

## 4. 未涵蓋的 Django 特性（★＝重點缺口）

### 4-1 資料層

| 特性 | 落點／教學動機 |
|---|---|
| ★ `ManyToManyField`（`.add`／`.remove`／`.set`／`.clear`、正反向） | Tag ↔ Article；兩個專案完全沒有 M2M |
| ★ through model（`through=`、`through_fields`） | `ArticleTag` 精選排序、`Reaction`；回扣 `OrderItem` 的「為何要中介模型」 |
| ★ 自我關聯 FK | `Comment.parent` 巢狀留言 |
| ★ 自訂 Manager／`QuerySet`（`models.QuerySet` ＋ `as_manager()`、可鏈式） | `Article.objects.published()`；回扣 `Product.objects.filter(is_active=True)` 到處重複 |
| ★ `F()` 表達式（原子遞增） | `view_count`；回扣 LearnMart checkout `item.product.stock -= x` 的 race，這次做對 |
| `Case`／`When`／`Value`、conditional annotate | 依狀態排序、置頂邏輯 |
| `values()`／`values_list()`／`.only()`／`.defer()` | 清單頁只取需要的欄位 |
| ★ `values().annotate()` = GROUP BY 分組聚合 | 月份彙整、每分類文章數、標籤雲 `annotate(Count)` |
| `Prefetch()` 物件（帶 queryset 的預抓） | 只預抓已核准留言 |
| `CheckConstraint`、`Meta.indexes`、`db_index`、`UniqueConstraint(condition=)` | published 必須有 published_at；LearnMart 只用過 `UniqueConstraint` |
| `unique_for_date` | slug 依發佈日期唯一 |
| 模型 `clean()`／`full_clean()`／`save()` override | slug 自動產生、發佈時間校驗 |
| `bulk_create`／`bulk_update`／`update()` | 匯入、批次改狀態 |
| 日期查詢 `__date`／`__year`／`__range`／`__gte`、`TruncMonth` | 彙整與排程 |
| ★ 資料遷移 `RunPython`（data migration） | 把舊的逗號分隔 tag 字串轉成 M2M 關聯 |
| Fixtures：`dumpdata`／`loaddata` | 種子資料的另一種形式，對照 `seed_demo` |

### 4-2 檢視 / URL 層

| 特性 | 落點 |
|---|---|
| `TemplateView`、`FormView`、`RedirectView` | 關於頁、訂閱表單、舊網址轉址 |
| ★ 日期型 generic view：`YearArchiveView`／`MonthArchiveView`／`DateDetailView` | `/2026/`、`/2026/08/`、`/2026/08/29/<slug>/` |
| `View` 基底類別、`dispatch()` override、`http_method_names` | 自己寫一個最小 CBV，理解 `as_view()` 背後 |
| ★ `FormMixin` 疊在 `DetailView` | 文章頁的留言表單；回扣 LearnMart `add_review` 的手工 function view |
| decorator：`require_http_methods`／`permission_required`／`user_passes_test`／`cache_page`／`vary_on_headers` | 各流程 |
| ★ `PermissionRequiredMixin` ＋ Django 權限框架（Group／Permission／`has_perm`） | editor／author 角色；回扣 LearnMart 自訂 `role` 欄位 ＋ `SellerRequiredMixin` |
| slug ＋ 日期 URL、`get_absolute_url` 用 slug | 文章網址 |
| `redirect()` 永久轉址（301） | slug 變更後的舊網址相容 |

### 4-3 表單層

| 特性 | 落點 |
|---|---|
| `ModelForm` 進階：`exclude`、`__init__` 動態欄位、`ModelChoiceField(queryset=)` | 只能選自己的分類／共同作者 |
| ★ Formset／`inlineformset_factory` | 一篇文章一次編輯多張圖／多個外部連結 |
| `SlugField` 表單、admin `prepopulated_fields` | 編輯後台 |
| widget 客製、表單 `Media` class | Markdown 編輯器掛 CSS/JS |
| `SuccessMessageMixin` | 取代手寫 `messages.success` |

### 4-4 模板層

| 特性 | 落點 |
|---|---|
| ★ 自訂 template tags／filters：`@register.filter`（markdown、reading_time）、`@register.simple_tag`、`@register.inclusion_tag`（`{% latest_articles %}`、`{% tag_cloud %}`、麵包屑） | 側欄與文章頁 |
| `{% with %}`／`{% cycle %}`／`{% now %}`／`{% regroup %}` | 月份分組顯示 |
| ★ 模板片段快取 `{% load cache %}{% cache 600 sidebar %}` | 側欄 |
| `|linebreaks`／`|truncatewords_html`／`|date:"Y年n月j日"`／`|timesince`／`humanize` 的 `|naturaltime`／`|intcomma` | 顯示格式 |
| `mark_safe`／`format_html` 在 template tag 內的安全邊界 | 回扣 XSS：Markdown 輸出是 stored XSS 觀察點 |

### 4-5 跨領域功能

| 特性 | 落點／教學動機 |
|---|---|
| ★ Sessions API 直接用（`request.session[...]`） | 匿名「最近瀏覽」、未登入的暫存偏好 |
| Cookies（`response.set_cookie`／`request.COOKIES`） | 關閉橫幅的記憶、閱讀進度 |
| ★ 快取框架：`cache.get/set`、`@cache_page`、低階快取、`LocMemCache` vs Redis 概念、快取失效 | 首頁、彙整頁、文章 HTML |
| ★ Signals：`post_save`／`pre_delete`／`m2m_changed`／`@receiver` | 自動產生 slug、留言通知寄信、快取失效、統計；並討論「signal 為何常被濫用、何時該用明確呼叫」 |
| ★ 自訂 middleware | 瀏覽計數、`X-Response-Time` header、維護模式、簡易 rate limit；回扣 Deck 02 第 7 章 trust boundary 的「五層防線」再加一層 |
| ★ Email：`send_mail`／`EmailMultiAlternatives`／console backend／內建密碼重設四件組（`PasswordResetView`／`PasswordResetConfirmView`…）／`PasswordChangeView` | 回扣 Deck 02 第 2 章只做了 login/logout |
| ★ management command 進階：`add_arguments`（argparse）、`--dry-run`、透過 cron 執行 | `publish_scheduled`、`send_weekly_digest`、`import_markdown --dir=...` |
| ★ contrib apps：`django.contrib.sitemaps`、`django.contrib.syndication`（RSS/Atom feed）、`django.contrib.humanize`、`django.contrib.postgres`（`SearchVector`／`SearchRank`／`TrigramSimilarity`） | feed、sitemap、搜尋 |
| ★ 全文檢索演進：`icontains` → `SearchVector`／`SearchQuery`／`SearchRank` → GIN index；SQLite fallback 與限制 | 回扣 Deck 01 第 6 章 `icontains` 搜尋的極限，正式帶出換 PostgreSQL |
| i18n／l10n：`{% translate %}`／`gettext`／`makemessages`／`LocaleMiddleware`／日期在地化 | `USE_I18N` 目前開著但沒教 |
| `JsonResponse` ＋ 輕量 AJAX（選配 HTMX） | 留言即時送出、「載入更多」、reaction 按鈕；課程首次、且刻意少量地引入 JS |
| 檔案／媒體進階：多檔上傳、`FileField` 驗證器、`ImageField` 尺寸限制、`django-storages`／S3 概念 | 文章配圖（部署章收尾） |
| `LOGGING` 設定、`RequestFactory`、`django-debug-toolbar`（看 SQL 數量） | 回扣 N+1 |

### 4-6 部署與營運（建議獨立成 Deck 04）

- `settings` 拆分／環境變數（`django-environ` 或 `os.environ` ＋ `.env`）；`SECRET_KEY`、`DEBUG=False`、`ALLOWED_HOSTS` 的來源
- `collectstatic`／`STATIC_ROOT`／WhiteNoise／`ManifestStaticFilesStorage`
- PostgreSQL 切換、`dj-database-url`、連線設定
- WSGI／ASGI server（gunicorn／uvicorn）、反向代理概念
- `python manage.py check --deploy`（Deck 02 已預告，這裡收尾）、`SECURE_*` settings／HSTS／HTTPS
- migration 在 production 的流程、資料庫備份
- 排程（cron／systemd timer）跑 management command；快取後端（Redis）
- 監控／error tracking（Sentry 概念）、health check endpoint
- （選配、不深入）background task：Celery／django-q 概念

---

## 5. 建議章節地圖

沿用現有每章格式：**核心問題 → 心智模型 → 最小範例 → 語法拆解 → 回扣舊專案 → 可觀察結果 → 檢核 ＋ workbook**。可切成兩冊 Deck 03A／03B，或一冊 14 章。

### Deck 03A｜內容模型與發佈

| 章 | 核心問題 | 新概念 | 可觀察成果 |
|---:|---|---|---|
| 1 | 第三個專案的骨架與 Python 補充 | 專案初始化、`journal` app、00c 語法補充、為何不再雙軌 | 專案可啟動、seed 資料 |
| 2 | 一篇文章多個標籤，怎麼存？ | `ManyToManyField`、through model、正反向查詢、`RunPython` data migration | 標籤頁、共同作者 |
| 3 | 「已發佈」的定義到處重複，怎麼收斂？ | 自訂 Manager／QuerySet、`published()`、`F()` 原子遞增、`CheckConstraint`、索引 | `Article.objects.published()`、瀏覽數不再 race |
| 4 | 文章網址要含日期，彙整頁怎麼做？ | slug ＋ `unique_for_date`、日期型 generic view、`TruncMonth`／`regroup`／GROUP BY | `/2026/08/`、`/2026/08/29/<slug>/` |
| 5 | Markdown、閱讀時間、標籤雲放哪裡？ | 自訂 template tag／filter、`inclusion_tag`、`mark_safe`／`format_html` 安全邊界 | 側欄與文章頁 |
| 6 | 巢狀留言與審核 | 自我關聯 FK、`FormMixin` on `DetailView`、`m2m_changed`／signal 入門 | 可回覆的留言串 |

### Deck 03B｜傳播、效能與帳號

| 章 | 核心問題 | 新概念 | 可觀察成果 |
|---:|---|---|---|
| 7 | 未登入使用者的狀態放哪裡？ | Sessions API、Cookies | 匿名「最近瀏覽」 |
| 8 | 首頁每次都重算，怎麼辦？ | 快取框架、片段快取、debug toolbar 看 SQL | 首頁查詢數下降 |
| 9 | 副作用（寄信、失效快取、統計）放哪裡？ | Signals 深入、自訂 middleware（瀏覽計數／回應時間／維護模式） | header 出現 `X-Response-Time` |
| 10 | 忘記密碼怎麼辦？ | Email、console backend、內建密碼重設流程、電子報 double opt-in | 收到重設信（console） |
| 11 | `icontains` 搜尋不夠好 | PostgreSQL `SearchVector`／`SearchRank`／GIN index、換資料庫 | 相關度排序的搜尋 |
| 12 | 讓內容被訂閱、被搜尋引擎看到 | `contrib.syndication`（RSS）、`contrib.sitemaps`、`humanize`、Django 權限框架取代 role 欄位 | `/feed/`、`/sitemap.xml` |
| 13 | 排程發佈與批次編輯 | management command ＋ `add_arguments` ＋ cron、`inlineformset_factory` | `publish_scheduled` 定時跑 |
| 14 | 安全與測試回歸整合 | Markdown 的 stored XSS、AJAX 的 CSRF、signal 副作用測試、快取污染、測試矩陣 | 回歸測試套件 |

### Deck 04｜部署與營運

6–7 章，內容見 §4-6。以「兩個 README 結尾的『不應上線』清單」為骨架逐項實作。

---

## 6. 與現有教材的回扣點（明確對照，降低認知負荷）

| LearnJournal 新概念 | 回扣 LearnBoard／LearnMart 的哪一處 |
|---|---|
| M2M through model | `OrderItem`（FK ＋快照）「為什麼要中介模型」 |
| `F()` 原子遞增 | LearnMart checkout `item.product.stock -= x` 的 race，這次修對 |
| 自訂 manager `published()` | `Product.objects.filter(is_active=True)` 在多個 view 重複 |
| `CheckConstraint` | LearnMart 只用過 `UniqueConstraint` |
| `FormMixin` on `DetailView` | LearnMart `add_review` 手工 function view |
| Django 權限框架（Group／Permission） | LearnMart 自訂 `role` 欄位 ＋ `SellerRequiredMixin` |
| signal 失效快取 | 全新，無對照 |
| 自訂 middleware | Deck 02 第 7 章 trust boundary「五層防線」再加一層 |
| 內建密碼重設 | Deck 02 第 2 章只做了 login／logout |
| `SearchVector` 全文檢索 | Deck 01 第 6 章 `icontains` 搜尋的極限 |
| 日期型 generic view | Deck 01 的 `ListView`／`DetailView` 之外的第三個 generic view 家族 |
| 部署 Deck 04 | 兩個 README 結尾「這是教學版，不應上線」清單 |

---

## 7. 給投影片拆分 agent 的檔名與資產慣例

依現有 `SOURCE_MAP.md` 慣例：

```text
slides/learnjournal_01_content_model_and_publishing/00_overview.md, 01_chapter_01.md, ...
slides/learnjournal_02_distribution_performance_and_accounts/00_overview.md, ...
slides/03_deployment_and_operations/00_overview.md, ...
slides/workbooks/learnjournal_01_content_model_and_publishing_workbook.md
slides/workbooks/learnjournal_02_distribution_performance_and_accounts_workbook.md
```

- 若最終仍要「共通整合冊」，比照 `01_*_two_projects` 命名為 `03_*` 系列；若第三專案採單軌（建議），直接用 `learnjournal_*`。
- Marp frontmatter 的 `style` 區塊直接沿用 Deck 02（含 `.label`／`.current`／`.warning`／`.check` class）；`header` 改為 `LearnJournal 01｜內容模型與發佈` 等。
- 新圖解建議加入 `slides/assets/`：`m2m_through.svg`、`cache_invalidation_flow.svg`、`signal_fanout.svg`、`fulltext_search_pipeline.svg`、`deployment_topology.svg`；提示詞補進 `slides/diagram_prompts.md`。
- 每章章末一律連到同名 workbook；重點頁保留 `<!-- 授課提示 -->` 講者備註。

---

## 8. 建議的最小 repository 骨架（`learnjournal/`）

```text
learnjournal/
├── config/                 # 目前維持單一 settings.py（比照前兩個專案）；Deck 04 才拆 base/prod
├── journal/
│   ├── models.py           # Article / Tag / Category / Comment / Reaction / Subscription
│   ├── managers.py         # ArticleQuerySet / PublishedManager
│   ├── views.py            # 混用 function view 與 generic view（含日期型）
│   ├── feeds.py            # contrib.syndication
│   ├── sitemaps.py
│   ├── signals.py          # slug、body_html、快取失效、通知
│   ├── middleware.py       # 瀏覽計數 / X-Response-Time
│   ├── templatetags/journal_extras.py
│   ├── forms.py            # ModelForm + inlineformset
│   ├── migrations/         # 含一支 RunPython data migration（tag 字串 → M2M）
│   └── management/commands/
│       ├── seed_demo.py
│       ├── publish_scheduled.py     # 帶 --dry-run
│       └── send_weekly_digest.py
├── templates/
│   ├── base.html
│   └── journal/            # list / detail / archive / author / search / editor
├── static/css/site.css
├── pyproject.toml          # 新增 markdown、psycopg[binary]、（選配）django-debug-toolbar
└── README.md               # 比照現有兩個專案的教學設計說明段落
```

保持「最小但完整」原則：每個特性只留一個最清楚的示範點，其餘變體交給 workbook 練習。
