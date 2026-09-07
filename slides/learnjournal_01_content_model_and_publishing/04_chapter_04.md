---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnJournal 01｜內容模型與發佈"
footer: "初學者教材｜觀念 → 語法 → LearnJournal 實作"
---

# 第 4 章
## Slug、日期網址與日期型 View

**本章成果：**能設計 `/2026/08/29/<slug>/` 這種網址、用日期型 generic view 做年／月彙整，並解釋時區如何影響「哪一天」。

<!--
授課提示：時區那幾頁最容易卡。準備一個 UTC 晚上、台北已隔天的例子現場示範。
-->

---

## 4-1 為什麼文章網址要含日期？

```text
/articles/42/                    ← 能用，但看不出是什麼、什麼時候
/2026/08/29/從-learnmart-到-learnjournal/   ← 人看得懂、搜尋引擎友善、可分享
```

- slug 讓網址帶語意
- 日期讓「同名標題」在不同時間各有一個網址（`unique_for_date`，第 3 章）
- 這是內容網站的慣例（多數新聞／部落格都這樣）

---

## 4-2 URLconf：把日期切成參數

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/urls.py`**

```python
urlpatterns = [
    path("<int:year>/", views.ArticleYearArchiveView.as_view(), name="archive-year"),
    path("<int:year>/<int:month>/", views.ArticleMonthArchiveView.as_view(), name="archive-month"),
    path("<int:year>/<int:month>/<int:day>/<uslug:slug>/",
         views.ArticleDetailView.as_view(), name="article-detail"),
]
```

- `<int:year>` 等：path converter，自動轉成 `int` 傳進 view 的 `self.kwargs`
- 三條路徑由短到長：站台根下的 `/2026/`、`/2026/08/`、`/2026/08/29/<slug>/`

---

## 4-3 <span class="label warning">常見錯誤</span> 內建 `slug` converter 不收中文

```python
path(".../<slug:slug>/", ...)      # slug converter 的 regex：[-a-zA-Z0-9_]+
```

中文標題產生的 slug（`從-learnmart-到-learnjournal`）會**比對失敗 → 404**。

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/urls.py` 自訂 converter**

```python
from django.urls import register_converter

class UnicodeSlugConverter:
    regex = r"[-\w]+"          # \w 在 Python 3 預設含中日韓文字
    def to_python(self, value): return value
    def to_url(self, value): return value

register_converter(UnicodeSlugConverter, "uslug")
```

之後路徑用 `<uslug:slug>`。

---

## 4-4 path converter 的四個部分

```python
class UnicodeSlugConverter:
    regex = r"[-\w]+"                       # 1. 這段網址長什麼樣
    def to_python(self, value):             # 2. 比對成功後，轉成給 view 的值
        return value
    def to_url(self, value):                # 3. reverse() 時，把值變回網址片段
        return value

register_converter(UnicodeSlugConverter, "uslug")   # 4. 註冊一個名字
```

Django 內建的 `int`、`str`、`slug`、`uuid`、`path` 就是同樣結構的現成品。

---

## 4-5 文章頁 View：用日期 + slug 精準定位

**<span class="label current">目前 LearnJournal｜節錄</span>｜`journal/views.py` 的 `ArticleDetailView`**

```python
def get_object(self, queryset=None):
    queryset = queryset or self.get_queryset()          # Article.published...
    return get_object_or_404(
        queryset,
        slug=self.kwargs["slug"],
        published_at__year=self.kwargs["year"],
        published_at__month=self.kwargs["month"],
        published_at__day=self.kwargs["day"],
    )
```

- 從 `Article.published` 出發：草稿／未到時間的文章自動查不到
- 四個條件一起比對：日期不符就 404

---

## 4-6 時區：`__year` / `__month` / `__day` 是「哪個時區的」？

專案設定 `USE_TZ=True`、`TIME_ZONE="Asia/Taipei"`：

- 資料庫存的 `published_at` 是 **UTC**
- ORM 的 `published_at__day=29` 會先**換算成 `TIME_ZONE`** 再取「日」

```text
published_at = 2026-08-28 16:30 UTC
              = 2026-08-29 00:30 台北時間
__day 比對用的是 29（台北），不是 28（UTC）
```

---

## 4-7 所以 `get_absolute_url()` 也要用當地時間

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/models.py`**

```python
def get_absolute_url(self):
    if self.published_at:
        local = timezone.localtime(self.published_at)     # UTC → Asia/Taipei
        return reverse("journal:article-detail", kwargs={
            "year": local.year, "month": local.month, "day": local.day, "slug": self.slug,
        })
    return reverse("journal:article-preview", kwargs={"pk": self.pk})
```

**如果這裡用 `self.published_at.year`（UTC）**，產生的網址是 8/28，但 View 的 `__day` 比對是 29 → 點自己的連結會 404。當地時間兩邊要一致。

<!--
授課提示：這是「USE_TZ 的實際後果」最具體的例子。LearnMart 開了 USE_TZ 但沒真的踩過這個坑。
-->

---

## 4-8 草稿沒有 `published_at`：另一條網址

```python
return reverse("journal:article-preview", kwargs={"pk": self.pk})
```

- 已發佈：日期網址 `/2026/08/29/<slug>/`
- 草稿／排程：預覽網址 `/articles/<pk>/preview/`，且**只有作者本人**看得到

`get_absolute_url()` 依狀態回傳不同網址——`get_absolute_url` 不一定只有一種結果。

---

## 4-9 日期型 generic view：Django 內建

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/views.py`**

```python
from django.views.generic.dates import MonthArchiveView, YearArchiveView

class ArticleMonthArchiveView(MonthArchiveView):
    date_field = "published_at"
    month_format = "%m"
    allow_empty = True
    template_name = "journal/archive_month.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.published.all()
```

- `LearnBoard`／`LearnMart` 用過 `ListView`／`DetailView`；這是**第三個** generic view 家族
- `date_field`：依哪個欄位切時間
- `allow_empty=True`：沒文章的月份也顯示頁面（不是 404）

---

## 4-10 `MonthArchiveView` 幫你準備好的 context

模板可直接用：

```django
{{ month }}              {# 這個月的第一天，可 |date:"Y 年 n 月" #}
{{ articles }}           {# 這個月的文章（context_object_name） #}
{{ previous_month }}     {# 上個月的第一天，可能是 None #}
{{ next_month }}         {# 下個月 #}
```

**<span class="label current">目前 LearnJournal｜節錄</span>｜`templates/journal/archive_month.html`**

```django
{% for article in articles %}{% include "journal/_article_card.html" %}{% endfor %}
{% if previous_month %}<a href="{% url 'journal:archive-month' previous_month|date:'Y' previous_month|date:'n' %}">← 上個月</a>{% endif %}
```

---

## 4-11 年彙整：用 `{% regroup %}` 依月份分組

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`templates/journal/archive_year.html`**

```django
{% regroup articles by published_at.month as month_list %}
{% for month in month_list %}
  <h2>{{ month.grouper }} 月</h2>
  <ul>
    {% for article in month.list %}
      <li><a href="{{ article.get_absolute_url }}">{{ article.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}
```

- `{% regroup %}`：把**已排序**的清單依某個屬性切成小組
- `month.grouper` 是分組值（月份），`month.list` 是那組的項目
- 前提：`articles` 已經依 `published_at` 排好（`Article.published` 的 `Meta.ordering` 保證了）

---

## 4-12 GROUP BY：這件事也能讓資料庫做

模板 `regroup` 是「已經查出全部文章，再在 Python 分組」。
如果只想要「每個月幾篇」的數字，讓資料庫算更省：

```python
from django.db.models import Count
from django.db.models.functions import TruncMonth

(Article.published
    .annotate(m=TruncMonth("published_at"))
    .values("m")                     # GROUP BY m
    .annotate(n=Count("id"))         # 每組數量
    .order_by("-m"))
# [{'m': date(2026, 8, 1), 'n': 3}, ...]
```

`values().annotate()` = SQL 的 `GROUP BY`（第 5 章標籤雲會再用一次）。

---

## 4-13 完整 request flow：一次文章頁

```text
GET /2026/8/29/從-learnmart.../  
  → config/urls.py include journal.urls
  → path("<int:year>/<int:month>/<int:day>/<uslug:slug>/")
  → ArticleDetailView.as_view()
  → get_object(): Article.published + 四個日期/slug 條件 → get_object_or_404
  → register_view(): F("view_count") + 1（原子遞增）
  → get_context_data(): 留言、reaction 統計、留言表單
  → render article_detail.html → body_html|safe、標籤、留言串
```

> **你應該看到**：重新整理頁面，「瀏覽」數字每次 +1。

---

## 4-14 <span class="label warning">常見錯誤</span> 日期網址與時區

- URLconf 用 `<slug:slug>` 而非自訂 `uslug` → 中文 slug 404
- `get_absolute_url()` 用 UTC 的年月日 → 點連結 404（跨日時）
- `MonthArchiveView` 忘了設 `allow_empty=True` → 空月份 404
- `get_queryset()` 用 `Article.objects` 而非 `Article.published` → 草稿被彙整頁列出
- `{% regroup %}` 前資料沒排序 → 同一個月被切成好幾組

---

## 第 4 章｜觀念檢核與實作

1. 為什麼內建 `slug` converter 不能用在中文 slug？自訂 converter 要實作哪三樣東西？
2. `published_at__day=29` 的「29」是哪個時區的日？為什麼 `get_absolute_url()` 要 `localtime`？
3. `MonthArchiveView` 需要你提供哪些屬性？它自動放進 context 的有哪些？
4. `{% regroup %}` 和 `values().annotate(Count())` 都能分組，差別在哪？
5. `ArticleDetailView.get_object()` 為什麼從 `Article.published` 出發而不是 `Article.objects`？

**實作任務：**加一條 `path("<int:year>/<int:month>/<int:day>/", ArticleDayArchiveView...)`（`DayArchiveView`），模板重用 `_article_card.html`；在 shell 用 `reverse()` 產生它的網址並用 test client 取得 200。

**<span class="label check">配套實作手冊</span>：**[第 4 章答案與步驟](../workbooks/learnjournal_01_content_model_and_publishing_workbook.md#chapter-4)
