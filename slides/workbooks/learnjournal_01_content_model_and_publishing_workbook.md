# LearnJournal 01 配套實作手冊

本手冊對應 [內容模型與發佈](../learnjournal_01_content_model_and_publishing/00_overview.md)。投影片保留問題與任務；本手冊提供答案、推理、實作步驟與驗收方式。

> 建議先獨立回答，再看解答。涉及 source code 的練習請在個人練習 branch 進行，不要把所有答案貼進正式專案。每段「修改後」只顯示焦點 excerpt，不代表整個檔案。`...` 代表保留原碼，不可貼進可執行檔。

**基準：** 目前 repository 的 `learnjournal/`（app 名 `journal`）。前置：已完成 LearnBoard／LearnMart 兩冊，且 `learnjournal/` 的 `uv run python manage.py test` 在你的環境為 11 passed。

## 目錄

1. [第 1 章｜專案骨架與 Python 語法補充](#chapter-1)
2. [第 2 章｜多對多、中介模型與 data migration](#chapter-2)
3. [第 3 章｜自訂 Manager、`F()` 與資料庫約束](#chapter-3)
4. [第 4 章｜Slug、日期網址與日期型 View](#chapter-4)
5. [第 5 章｜自訂 template tag、filter 與輸出安全](#chapter-5)
6. [第 6 章｜巢狀留言、`FormMixin` 與 signal 入門](#chapter-6)

---

<a id="chapter-1"></a>
# 第 1 章｜專案骨架與 Python 語法補充

## 觀念檢核答案

### 1. `managers.py` 與 `signals.py` 的責任？

- `journal/managers.py`：定義 `ArticleQuerySet`（具名、可鏈式的查詢方法，如 `published()`）與 `PublishedManager`。把「什麼叫已發佈」這種規則收在一處。
- `journal/signals.py`：定義 `@receiver` 函式，處理模型事件的副作用（目前是 `post_save` 把 Markdown 渲染成 `body_html`）。必須在 `apps.py` 的 `ready()` 被 import 才會生效。

### 2. 為什麼沒有 `Pillow`？

`Pillow` 是 `ImageField` 的相依套件。LearnJournal Deck 03A 不做圖片上傳（文章配圖留給 Deck 03B 的 `inlineformset_factory` 章）。刻意不裝，讓依賴集合維持最小。

### 3. `lambda p: -p.count` vs `lambda p: p.count`

`sorted()` 依 `key` 回傳值**升冪**排列。`p.count` 是「數量小的在前」；`-p.count` 把符號反過來，等於「數量大的在前」。也可以寫 `sorted(..., key=lambda p: p.count, reverse=True)`。

### 4. `with transaction.atomic():` vs `@transaction.atomic`

兩者都建立一個資料庫交易區塊（一起 COMMIT 或一起 ROLLBACK）。裝飾器包住**整個 view 函式**；`with` 區塊只包住**你圈起來的幾行**，範圍更精準，其餘程式碼不在交易內。

### 5. `timezone.now()` vs `datetime.now()`

專案 `USE_TZ=True` 時，`timezone.now()` 回傳**帶時區資訊的 aware datetime**（UTC）。`datetime.now()` 回傳沒有時區的 naive datetime，拿去和 aware datetime 比較會拋 `TypeError`，存進 `DateTimeField` 也會有 warning。Django 專案一律用 `django.utils.timezone`。

## 實作任務：草稿與已發佈的可見性

### 目標

用 shell 觀察 `Article.objects` 與 `Article.published` 的差異，並確認 `save()` 會自動補 `published_at`。

### 步驟

1. 進 shell：

   ```bash
   uv run python manage.py shell
   ```

2. 建立一篇草稿：

   ```python
   from journal.models import Article, Category, Tag
   from django.contrib.auth import get_user_model
   User = get_user_model()

   amy = User.objects.get(username="amy")
   cat = Category.objects.first()
   draft = Article.objects.create(author=amy, category=cat, title="我的草稿", body="草稿內容", status="draft")
   ```

3. 觀察兩個 manager：

   ```python
   Article.objects.filter(pk=draft.pk).exists()     # True
   Article.published.filter(pk=draft.pk).exists()    # False（狀態不對）
   print(draft.published_at)                          # None
   ```

4. 改成已發佈並存檔：

   ```python
   draft.status = "published"
   draft.save()
   draft.refresh_from_db()
   print(draft.published_at)                          # 有值了（save() 自動補）
   Article.published.filter(pk=draft.pk).exists()     # True
   ```

5. 收尾：

   ```python
   draft.delete()
   exit()
   ```

### 驗收

- `Article.objects` 看得到草稿，`Article.published` 看不到。
- `status` 改成 `published` 後 `published_at` 由 `Article.save()` 自動填入。

---

<a id="chapter-2"></a>
# 第 2 章｜多對多、中介模型與 data migration

## 觀念檢核答案

### 1. 為什麼「文章 ↔ 標籤」不能只用 ForeignKey？

ForeignKey 表達「多對一」：放在「多」的一邊指向「一」的一邊。文章與標籤是**兩邊都多**（一篇多標籤、一標籤多文章）。資料庫的做法是多一張**中介（連結）表**，每一列是一組「文章 id ↔ 標籤 id」配對。`ManyToManyField` 預設會自動建這張表。

### 2. `through` 換來什麼、代價是什麼？

換來「關聯本身可以帶欄位」——LearnJournal 的 `ArticleTag.featured_order`（某文章的標籤頁排序）。代價是不能再用 `article.tags.add(tag)`，新增配對要 `ArticleTag.objects.create(article=..., tag=..., featured_order=...)`。只有真的需要配對屬性才用 `through`。（對照 LearnMart 的 `OrderItem`：Order↔Product 之間帶單價與數量快照。）

### 3. `author` 和 `coauthors` 的 `related_name` 為何必須不同？

兩者都指向 `User`。反向 accessor 預設是 `<model>_set`（這裡會是 `article_set`），兩個關聯會產生同名 accessor → `makemigrations` 直接報 `fields.E304`。分別給 `related_name="articles"` 與 `"coauthored_articles"`，`user.articles`（我主筆的）與 `user.coauthored_articles`（我掛名的）才分得開。

### 4. data migration 為何用 `apps.get_model()`？

migration 檔是**歷史紀錄**，未來可能在 model 已經改了好幾版之後才被套用（例如同事 clone 舊 commit）。`apps.get_model("journal", "Article")` 拿到的是「這支 migration 當下」的 model 版本；`from journal.models import Article` 拿到的是「現在」的版本，欄位對不上就會壞。

### 5. `Comment.parent` 的 `null=True`、`is_approved`？

- `parent = ForeignKey("self", null=True)`：`null=True` 讓「頂層留言」的 `parent` 可以是資料庫 NULL；有值代表它是某留言的回覆。
- `is_approved`：審核旗標。模板只顯示 `is_approved=True` 的留言；灌水留言可在 admin 設成 `False` 隱藏。

## 實作任務：為 `Tag` 加 `description` 並用 data migration 回填

### 影響檔案

- `journal/models.py`（`Tag`）
- 新增兩支 migration

### 步驟

1. 改 model（練習 branch）：

   ```python
   class Tag(models.Model):
       name = models.CharField("標籤", max_length=40, unique=True)
       slug = models.SlugField("網址代稱", max_length=40, unique=True, allow_unicode=True)
       description = models.CharField("說明", max_length=200, blank=True)   # 新增
   ```

2. 產生 schema migration 並閱讀：

   ```bash
   uv run python manage.py makemigrations journal
   # 應該看到 AddField: description
   ```

3. 建立空的 data migration：

   ```bash
   uv run python manage.py makemigrations journal --empty --name backfill_tag_description
   ```

4. 填入 `RunPython`：

   ```python
   from django.db import migrations

   def fill(apps, schema_editor):
       Tag = apps.get_model("journal", "Tag")
       for tag in Tag.objects.filter(description=""):
           tag.description = f"關於 {tag.name} 的文章"
           tag.save(update_fields=["description"])

   def undo(apps, schema_editor):
       Tag = apps.get_model("journal", "Tag")
       Tag.objects.update(description="")

   class Migration(migrations.Migration):
       dependencies = [("journal", "<上一支 migration 名>")]
       operations = [migrations.RunPython(fill, undo)]
   ```

5. 套用、確認、回退再前進：

   ```bash
   uv run python manage.py migrate
   uv run python manage.py shell -c "from journal.models import Tag; print(Tag.objects.first().description)"
   uv run python manage.py migrate journal <schema migration 前一號>   # 回退
   uv run python manage.py migrate                                      # 再前進
   ```

### 驗收

- `Tag.description` 全部非空。
- `migrate` 可往回也可往前，沒有 `IrreversibleError`。

---

<a id="chapter-3"></a>
# 第 3 章｜自訂 Manager、`F()` 與資料庫約束

## 觀念檢核答案

### 1. 自訂 QuerySet 方法為何要回傳 `self.filter(...)`？

回傳 QuerySet 才能**繼續串接**：`Article.objects.published().by_tag("orm").order_by(...)`。若某個方法回傳 list 或單一物件，鏈就斷了，也失去 lazy 特性。

### 2. `Article.objects` vs `Article.published`

- `objects = ArticleQuerySet.as_manager()`：預設 manager，回傳**全部**文章（含草稿、排程），供 admin、關聯查詢、寫作後台使用。
- `published = PublishedManager()`：`get_queryset()` 已套上 `.published().with_feed_fields()`，只回傳「狀態 published 且時間已到」的文章，並預先 `select_related`／`prefetch_related`。公開頁面一律用它。

### 3. `F("view_count") + 1` 為何避免 race？SQLite 保證到哪？

`F()` 產生的 SQL 是 `UPDATE ... SET view_count = view_count + 1 WHERE id = ?`，加法在資料庫內完成，沒有「讀到 Python → 改 → 寫回」的空窗，兩個並行請求不會互相覆蓋。SQLite 保證**單句 UPDATE 是原子的**（它整個 DB 同時只有一個寫入者）；但「先 SELECT 再 UPDATE」這種跨句邏輯 SQLite 沒有 row lock（見 LearnMart 第 5 章 `select_for_update()`）。本章只需要單句原子遞增這一層。

### 4. `register_view()` 後 `article.view_count` 為何是舊的？

`Article.objects.filter(pk=...).update(...)` 只改資料庫，不動你手上的 Python instance。要看新值需 `article.refresh_from_db()`。

### 5. 三種防線各擋什麼入口？

- Form `clean()`：擋透過該表單送來的錯資料。其他入口（shell、admin、指令、其他 view）繞過它。
- Model `save()` 邏輯：擋所有走 `.save()` 的程式碼路徑；但 `QuerySet.update()`、`bulk_create` 不呼叫 `save()`。
- `CheckConstraint` / `UniqueConstraint`：資料庫層，擋**所有**寫入，含繞過 ORM 的。三者是層層防線，不互相取代。

## 實作任務：`popular(days=7)` QuerySet 方法

### 影響檔案

- `journal/managers.py`

### 修改後（焦點 excerpt）

```python
from datetime import timedelta

class ArticleQuerySet(models.QuerySet):
    ...
    def popular(self, days=7):
        since = timezone.now() - timedelta(days=days)
        return self.filter(published_at__gte=since).order_by("-view_count")
```

### 驗證

```bash
uv run python manage.py shell
```

```python
from journal.models import Article
Article.objects.published().popular(30)              # 可串接
Article.objects.published().by_tag("orm").popular()  # 順序不拘
list(Article.objects.published().popular(days=1).values_list("title", "view_count"))
```

### 驗收

- `popular()` 回傳 QuerySet，可與 `published()`、`by_tag()` 任意順序串接。
- 結果依 `view_count` 由高到低，且只含近 `days` 天發佈的文章。

---

<a id="chapter-4"></a>
# 第 4 章｜Slug、日期網址與日期型 View

## 觀念檢核答案

### 1. 內建 `slug` converter 為何不收中文？自訂要實作什麼？

內建 `slug` 的 regex 是 `[-a-zA-Z0-9_]+`，中文字元不在範圍內，比對失敗 → 404。自訂 converter 要有：`regex`（字串屬性）、`to_python(self, value)`（比對成功後轉給 view）、`to_url(self, value)`（`reverse()` 時轉回網址片段），再用 `register_converter(類別, "名字")` 註冊。

### 2. `published_at__day=29` 是哪個時區的日？

`USE_TZ=True` 時 ORM 會把資料庫的 UTC 時間先換算成 `settings.TIME_ZONE`（`Asia/Taipei`）再取「日」。所以 `get_absolute_url()` 必須用 `timezone.localtime(self.published_at)` 的年月日，才和 View 的 `__year/__month/__day` 一致；否則跨日時（UTC 還是 28 號、台北已是 29 號）會產生指向不存在日期的網址 → 點連結 404。

### 3. `MonthArchiveView` 要你提供什麼？自動給什麼？

你提供：`date_field`、`month_format`、`allow_empty`、`template_name`、`get_queryset()`（或 `queryset`/`model`）。它自動放進 context：`month`（該月第一天）、`next_month`、`previous_month`、以及該月物件清單（依 `context_object_name`）。

### 4. `{% regroup %}` vs `values().annotate(Count())`

- `{% regroup %}`：已經把**全部**文章查出來了，再在模板/Python 端依屬性切組。適合「本來就要顯示每一篇」。
- `values("m").annotate(n=Count("id"))`：在資料庫做 `GROUP BY`，只回傳每組的**數字**，不載入每一列。適合「只要計數」（側欄的每月文章數、標籤雲）。

### 5. `ArticleDetailView.get_object()` 為何從 `Article.published`？

從 `Article.published` 出發，草稿與「排程但時間未到」的文章自然查不到 → 對匿名訪客回 404，不會外洩未公開內容。草稿要預覽走另一條 `article-preview` 路徑（限作者本人）。

## 實作任務：加入 `DayArchiveView`

### 影響檔案

- `journal/views.py`、`journal/urls.py`、新增 `templates/journal/archive_day.html`

### 修改後（焦點 excerpt）

`views.py`：

```python
from django.views.generic.dates import DayArchiveView

class ArticleDayArchiveView(DayArchiveView):
    date_field = "published_at"
    month_format = "%m"
    allow_empty = True
    template_name = "journal/archive_day.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.published.all()
```

`urls.py`（放在 `article-detail` 之前，避免被吃掉）：

```python
path("<int:year>/<int:month>/<int:day>/", views.ArticleDayArchiveView.as_view(), name="archive-day"),
```

`archive_day.html`：

```django
{% extends "base.html" %}
{% block content %}
  <h1>{{ day|date:"Y 年 n 月 j 日" }}</h1>
  {% for article in articles %}{% include "journal/_article_card.html" %}{% empty %}<p>這天沒有文章。</p>{% endfor %}
{% endblock %}
```

### 驗證

```python
from django.urls import reverse
from django.test import Client
from django.utils import timezone
from journal.models import Article

a = Article.published.first()
local = timezone.localtime(a.published_at)
url = reverse("journal:archive-day", args=[local.year, local.month, local.day])
print(Client().get(url).status_code)          # 200
```

### 驗收

- `/2026/8/29/` 回 200 並列出當天文章。
- `/2026/8/29/<slug>/`（文章頁）仍正常——URL 順序沒被 day archive 蓋掉。

---

<a id="chapter-5"></a>
# 第 5 章｜自訂 template tag、filter 與輸出安全

## 觀念檢核答案

### 1. 三種形式的輸入與輸出

- **filter**：輸入「被 filter 的值」（可再帶一個參數），輸出一個值。`{{ x|f }}` 或 `{{ x|f:arg }}`。
- **simple_tag**：輸入任意參數，輸出一個值（可 `as var` 存起來）。`{% t a b %}`。
- **inclusion_tag**：輸入任意參數，輸出「用回傳的 dict 去渲染指定小模板」的結果。`{% t n %}`。

### 2. `markdownify` 為何要 `mark_safe`？何時是漏洞？

`md.markdown()` 產生的是 HTML 字串（`<h2>`、`<pre>`…）。模板預設 autoescape 會把它們變成文字。`mark_safe` 告訴模板「這段別跳脫」。**當被渲染的字串來自不受信任來源**（匿名留言、URL 參數、外部匯入而未清洗的內容）時，`mark_safe` 就等於開了 stored/reflected XSS 的門。

### 3. 文章內文 `|safe`、留言不 `|safe` 的依據？

作者是「受信任的登入使用者」，允許他用 Markdown 排版是刻意的功能；留言可由任何登入者輸入，屬不受信任內容，必須保持 autoescape（只用 `|linebreaksbr` 之類不引入 HTML 的 filter）。判準是**內容作者的信任層級**，不是欄位型別。

### 4. `annotate(count=Count("articles"))` 的 SQL？

對 `Tag` 反向關聯 `articles` 做計數，產生 `... JOIN article_tag JOIN article WHERE article.status='published' GROUP BY tag.id`，每個 Tag 多一個 `count` 欄位。配合 `filter()` + `order_by("-count")` 就是「熱門標籤」。

### 5. `templatetags/__init__.py` 少了會怎樣？

`templatetags` 不被視為 package，Django 掃不到裡面的模組，`{% load journal_extras %}` 報 `'journal_extras' is not a registered tag library`。

## 實作任務：`{% comment_count %}` 與 `excerptify`

### 修改後（焦點 excerpt）｜`journal/templatetags/journal_extras.py`

```python
@register.simple_tag
def comment_count(article):
    return article.comments.filter(is_approved=True).count()


@register.filter
def excerptify(text, length=60):
    text = (text or "").strip()
    return text if len(text) <= length else text[:length].rstrip() + "…"
```

### 測試｜新增到 `journal/tests.py`

```python
from django.template import Context, Template

class TemplateTagTests(BaseData):
    def test_comment_count_counts_approved_only(self):
        article = self.make_article()
        from journal.models import Comment
        Comment.objects.create(article=article, author=self.amy, body="a")
        Comment.objects.create(article=article, author=self.ben, body="b", is_approved=False)
        rendered = Template("{% load journal_extras %}{% comment_count a %}").render(Context({"a": article}))
        self.assertEqual(rendered.strip(), "1")

    def test_excerptify_truncates(self):
        out = Template("{% load journal_extras %}{{ s|excerptify:5 }}").render(Context({"s": "一二三四五六七"}))
        self.assertEqual(out, "一二三四五…")
```

### 驗收

```bash
uv run python manage.py test journal.tests.TemplateTagTests
```

兩個測試通過；`comment_count` 不計未核准留言；`excerptify` 在超長時補「…」。

---

<a id="chapter-6"></a>
# 第 6 章｜巢狀留言、`FormMixin` 與 signal 入門

## 觀念檢核答案

### 1. `DetailView` 少了什麼？`FormMixin` 為何寫前面？

`DetailView` 只有 `get()`（查物件、渲染），沒有 `form_class`／`get_form()`／`get_form_kwargs()`／`post()`。`FormMixin` 補這些。寫在 `DetailView` 前面，是因為 Python MRO 由左到右解析——同名方法（如 `get_context_data`、`get_form_kwargs`）以左邊的 mixin 為優先，才不會被 `DetailView` 的版本蓋掉。

### 2. `comment.author = request.user` 為何不進 `fields`？

它是 server-owned 欄位：由伺服器從 session 決定，不能讓使用者在表單裡指定（否則可冒名）。同理 `article`、`parent` 也由 view 設定。這是 LearnBoard／LearnMart「`author` / `seller` 不在 fields」的同一原則。

### 3. 取 parent 為何用 `self.object.comments.filter(pk=...)`？

`Comment.objects.get(pk=parent_id)` 會接受**任何** id，攻擊者可把回覆掛到別篇文章的留言下（IDOR）。`self.object.comments.filter(pk=parent_id).first()` 限制 parent 必須屬於「當前這篇文章」，越權的 id 得到 `None`（視為頂層留言）。

### 4. `render_markdown` 為何用 `update()` 不用 `instance.save()`？

handler 是掛在 `post_save(Article)` 上的。若在裡面呼叫 `instance.save()`，會再次觸發 `post_save` → 無限遞迴。`Article.objects.filter(pk=...).update(body_html=...)` 只發一句 UPDATE，不觸發 signal。

### 5. 什麼副作用適合 signal？

跨 app、或「原本的程式碼不該知道」的鬆耦合副作用（例：稽核記錄、快取失效、寄通知）適合 signal。屬於存檔本質、同一 app 內的邏輯（例：從標題產生 slug、發佈時補時間）直接寫在 `save()` 更好讀、更好測。

## 實作任務：留言預設待審核

### 影響檔案

- `journal/models.py`（`Comment.is_approved` 預設）
- `journal/views.py`（`ArticleDetailView.post()` 的成功訊息）
- `journal/tests.py`（新增測試）

### 修改後（焦點 excerpt）

`models.py`：

```python
is_approved = models.BooleanField("已核准", default=False)   # 由 True 改為 False
```

`views.py`（`post()` 成功分支）：

```python
    comment.save()
    if comment.is_approved:
        messages.success(request, "留言已送出。")
    else:
        messages.info(request, "留言已送出，待編輯核准後顯示。")
    return redirect(self.object.get_absolute_url() + "#comments")
```

模板：頂層留言迴圈加上「作者本人可見自己未核准留言」：

```django
{% for comment in article.comments.all %}
  {% if comment.is_approved or comment.author == user %}
    ... 顯示 ...
    {% if not comment.is_approved %}<span class="badge text-bg-warning">待審核</span>{% endif %}
  {% endif %}
{% endfor %}
```

### 測試

```python
def test_new_comment_is_pending_and_hidden_from_others(self):
    article = self.make_article()
    self.client.login(username="ben", password="pw-ben-12345")
    self.client.post(article.get_absolute_url(), {"body": "待審留言"})
    # 換一個未登入 client 看不到
    from django.test import Client
    self.assertNotContains(Client().get(article.get_absolute_url()), "待審留言")
    # 作者本人看得到
    self.assertContains(self.client.get(article.get_absolute_url()), "待審留言")
```

### 驗收

- 匿名／他人看不到未核准留言；作者本人看得到並有「待審核」標記。
- admin 把 `is_approved` 打勾後，所有人可見。
- `seed_demo` 若依賴留言可見，記得同步調整（或在 seed 裡直接建立 `is_approved=True`）。

---

## 完成 Deck 03A 後

累積的 `journal/tests.py` 應該仍是綠的，加上你在各章新增的測試：

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

接著進入 Deck 03B（傳播、效能與帳號）：sessions/cookies、快取、signal 深入、middleware、email、全文檢索、RSS/sitemap、權限框架、排程指令。
