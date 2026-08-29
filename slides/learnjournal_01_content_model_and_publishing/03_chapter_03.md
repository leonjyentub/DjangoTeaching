---
marp: true
theme: default
size: 16:9
paginate: true
header: "LearnJournal 01｜內容模型與發佈"
footer: "初學者教材｜觀念 → 語法 → LearnJournal 實作"
style: |
  section {
    font-family: 'Noto Sans CJK TC', 'Noto Serif CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', 'Heiti TC', sans-serif;
    font-size: 28px;
    line-height: 1.35;
    padding: 58px 70px;
  }
  h1, h2 {
    font-family: 'Noto Sans CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', sans-serif;
  }
  h1 { color: #1f5c3d; }
  h2 { color: #2e7d51; }
  blockquote {
    border-left: 6px solid #9ccbb3; padding-left: 18px; color: #2f4038;
    font-family: 'Noto Serif CJK TC', 'Noto Sans CJK TC', 'WenQuanYi Zen Hei', serif;
  }
  code, kbd {
    font-family: 'Noto Sans Mono CJK TC', 'SF Mono', Consolas,
                 'WenQuanYi Zen Hei Mono', 'Courier New', monospace;
    font-size: 0.92em;
  }
  pre { font-size: 0.72em; line-height: 1.28; }
  table { font-size: 0.78em; }
  strong { color: #17633a; }
  .label { display: inline-block; padding: 0.15em 0.55em; border-radius: 999px; font-size: 0.72em; font-weight: 700; background: #e6efe9; color: #1f5c3d; }
  .current { background: #e5f4ea; color: #17633a; }
  .warning { background: #fff0d9; color: #8a4b08; }
  .check { background: #f3e8ff; color: #6b21a8; }
  .small { font-size: 0.78em; }
---

# 第 3 章
## 自訂 Manager、`F()` 與資料庫約束

**本章成果：**能把重複的查詢條件收斂成具名 QuerySet 方法，用 `F()` 做原子更新，並用 `CheckConstraint` 把規則放到資料庫層。

<!--
授課提示：先複習 LearnMart 第 5 章 QuerySet lazy 與 N+1；本章的 Manager 全建立在那之上。
-->

---

## 3-1 問題：同一個條件寫了很多次

**<span class="label current">目前 LearnMart｜節錄</span>——同樣的 filter 散在多個 view**

```python
Product.objects.filter(is_active=True).select_related("category", "seller")   # ProductListView
Product.objects.filter(is_active=True).select_related("seller", "category")   # ProductDetailView
```

LearnJournal 的「已發佈」比這更麻煩——**兩個條件**：

```python
status == "published"  且  published_at <= 現在
```

如果每個 view 都自己寫，總有一天有人漏掉「時間到了沒」，草稿或排程文章就外洩。

---

## 3-2 心智模型：三種物件（回扣 LearnMart 5-1）

```python
Article.objects                       # Manager：查詢的入口
Article.objects.filter(status="published")   # QuerySet：0 到多筆，lazy
Article.objects.get(pk=1)             # 一個 Article instance
```

- **Manager** 掛在 class 上（`Article.objects`），負責「開始一個查詢」
- **QuerySet** 是查詢本身，可以再串 `.filter()`、`.order_by()`
- 我們要做的是：**給 QuerySet 加一個叫 `published()` 的方法**

---

## 3-3 自訂 QuerySet：把條件變成方法

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/managers.py`**

```python
from django.db import models
from django.utils import timezone

class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="published", published_at__lte=timezone.now())

    def by_tag(self, slug):
        return self.filter(tags__slug=slug)

    def with_feed_fields(self):
        return self.select_related("author", "category").prefetch_related("tags")
```

每個方法回傳 `self.filter(...)`——也就是**還是一個 QuerySet**，所以可以串起來。

---

## 3-4 可鏈式：這就是重點

```python
Article.objects.published().by_tag("orm").with_feed_fields()
Article.objects.by_tag("orm").published()           # 順序不拘，結果一樣
```

因為每個方法都回傳 QuerySet，可以像 Django 內建的 `.filter().exclude().order_by()` 一樣接下去。

- 呼叫端只說「我要什麼」（已發佈、某標籤、附帶關聯欄位）
- 「怎麼查」的細節收在 `managers.py` 一處
- 未來規則改變（例如加上 `is_deleted=False`），只改一個地方

---

## 3-5 把 QuerySet 掛成 Manager

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/models.py`**

```python
class Article(models.Model):
    ...
    objects = ArticleQuerySet.as_manager()   # 全部文章，含草稿
    published = PublishedManager()            # 只有公開文章
```

- `ArticleQuerySet.as_manager()`：把 QuerySet 的方法「借」給 Manager，`Article.objects.published()` 就能用
- `published` 是第二個 Manager，預設就只回傳公開文章（下一頁）

> 第一個定義的 Manager 是 `_default_manager`。這裡 `objects` 先定義，所以 admin、關聯查詢預設看得到草稿。

---

## 3-6 `PublishedManager`：預設就過濾好

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/managers.py`**

```python
class PublishedManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db).published().with_feed_fields()
```

```python
Article.objects.all()       # 3 筆（含草稿）
Article.published.all()      # 只有已發佈，且已 select_related / prefetch_related
Article.published.by_tag("orm")   # 也能繼續串 QuerySet 方法
```

view 裡直接寫 `Article.published.all()`，不可能忘記過濾條件。

---

## 3-7 問題：瀏覽數 +1 的 race condition

**<span class="label current">目前 LearnMart｜節錄</span>——checkout 扣庫存的寫法**

```python
item.product.stock -= item.quantity
item.product.save(update_fields=["stock"])
```

這是「讀進 Python → 改 → 寫回」。兩個請求同時進來：

```text
請求 A 讀到 stock=10        請求 B 讀到 stock=10
A 算 10-1=9，寫回 9          B 算 10-1=9，寫回 9
結果：賣了兩件，庫存只少 1
```

LearnJournal 的 `view_count += 1` 有一模一樣的問題。

---

## 3-8 `F()`：讓資料庫自己算

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/models.py`**

```python
from django.db.models import F

class Article(models.Model):
    def register_view(self):
        Article.objects.filter(pk=self.pk).update(view_count=F("view_count") + 1)
```

- `F("view_count")` 代表「資料庫裡那一欄目前的值」，不是 Python 讀到的舊值
- 產生的 SQL 是 `UPDATE ... SET view_count = view_count + 1 WHERE id = ?`
- 加法在**資料庫內**完成，中間沒有「讀回 Python」的空窗，不會互相蓋掉

---

## 3-9 `F()` 的其他用途

```python
from django.db.models import F

# 找出「回覆數 > 讚數」的文章（欄位對欄位比較）
Article.objects.filter(reply_count__gt=F("like_count"))

# 批次調整：所有精選排序 +1
ArticleTag.objects.update(featured_order=F("featured_order") + 1)
```

- `F()` 可用在 `filter()`（欄位互比）與 `update()`／`annotate()`（欄位運算）
- 用 `F()` 的 `update()` **不會**觸發 `save()`、`auto_now`、signal——它是直接一句 SQL

<!--
授課提示：現場開兩個 shell 同時對同一篇文章 register_view()，再比對「Python 讀改寫」版本，眼見為憑。
-->

---

## 3-10 <span class="label warning">常見錯誤</span> `F()` 之後 instance 是舊的

```python
article.register_view()
article.view_count           # 還是舊值！Python 端的 instance 沒被更新

article.refresh_from_db()    # 重新從資料庫讀
article.view_count           # 現在對了
```

`update()` 只動資料庫，不動你手上的 Python 物件。要看新值就 `refresh_from_db()`（回扣 LearnMart 第 7 章測試技巧）。

---

## 3-11 SQLite 保證到哪？

- `F("view_count") + 1` 的**單句 UPDATE 是原子的**——即使 SQLite 也一樣，因為它整個資料庫一次只有一個寫入者
- 但「先 SELECT 檢查、再 UPDATE」這種**跨句**邏輯，SQLite 沒有 row-level lock（LearnMart 第 5 章 `select_for_update()` 已提過）
- 本冊只需要「單句原子遞增」這一層，`F()` 就夠

> 結論：計數器、按讚數、庫存這種「加減既有值」的操作，一律用 `F()`，不要讀進 Python。

---

## 3-12 `CheckConstraint`：把規則放進資料庫

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/models.py` 的 `Article.Meta`**

```python
from django.db.models import Q

class Meta:
    constraints = [
        models.CheckConstraint(
            name="published_article_has_timestamp",
            condition=~Q(status="published") | Q(published_at__isnull=False),
        ),
    ]
```

讀法：「**不是** published，**或者** `published_at` 有值」——也就是「published 就必須有時間」。

- 表單驗證會擋，但表單不是唯一入口（shell、admin、data migration、其他程式）
- `CheckConstraint` 是資料庫層的最後防線

---

## 3-13 三種「防線」不能互相取代

| 防線 | 寫在哪 | 擋得住 |
|---|---|---|
| Form `clean()` | `forms.py` | 使用者透過表單送的錯資料 |
| Model `save()` 邏輯 | `models.py` | 程式碼路徑（含 shell、指令） |
| `CheckConstraint` / `UniqueConstraint` | `Meta.constraints` | **所有**寫入，包含繞過 ORM 的 |

LearnMart 只用過 `UniqueConstraint`（購物車、評價）。LearnJournal 加上 `CheckConstraint`。

> 回扣 LearnMart 第 5 章：validator 與 database constraint 是不同防線。

---

## 3-14 `save()` 裡的便利邏輯

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/models.py`**

```python
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.title, allow_unicode=True) or "article"
    if self.status == self.Status.PUBLISHED and self.published_at is None:
        self.published_at = timezone.now()
    super().save(*args, **kwargs)
```

- 沒填 slug 就從標題自動產生
- 狀態設成 published 但沒給時間，就用「現在」
- **一定要呼叫 `super().save()`**，否則根本沒寫進資料庫

> `CheckConstraint` 與這段 `save()` 邏輯是搭配的：`save()` 讓正常流程方便，Constraint 擋住異常流程。

---

## 3-15 索引：讓常用查詢更快

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/models.py` 的 `Article.Meta`**

```python
class Meta:
    ordering = ["-published_at", "-created_at"]
    indexes = [
        models.Index(fields=["status", "published_at"]),
        models.Index(fields=["slug"]),
    ]
```

- 首頁幾乎每次都查 `status="published"` 且依 `published_at` 排序 → 建一個複合索引
- 文章頁用 slug 找 → slug 索引
- 索引加速讀取，但**每次寫入要多維護一份**——不是欄位越多索引越好

---

## 3-16 `unique_for_date`：slug 只要「當天」唯一

**<span class="label current">目前 LearnJournal｜節錄</span>**

```python
slug = models.SlugField(max_length=160, unique_for_date="published_at", allow_unicode=True)
```

- 不是全站唯一，而是「同一個發佈日期內」不重複
- 搭配第 4 章的日期網址 `/2026/08/29/<slug>/`——只要那一天沒有同名 slug 就能定位
- 這是 **ModelForm 驗證層**的檢查（不是資料庫 constraint），shell 直接建立不會被擋

---

## 3-17 `allow_unicode=True`：中文 slug

```python
slugify("從 LearnMart 到 LearnJournal", allow_unicode=True)
# '從-learnmart-到-learnjournal'
```

- Django 內建的 `slug` 只接受 ASCII；中文標題產生的 slug 會被清成空字串
- `SlugField(allow_unicode=True)` 讓欄位驗證接受中文
- URL 端還需要一個自訂 path converter（第 4 章）

---

## 第 3 章｜觀念檢核與實作

1. 「自訂 QuerySet 方法要回傳 `self.filter(...)`」為什麼重要？
2. `Article.objects` 和 `Article.published` 差在哪？哪個看得到草稿？
3. `F("view_count") + 1` 為什麼能避免 race condition？SQLite 保證到哪一層？
4. `article.register_view()` 之後 `article.view_count` 為什麼還是舊的？
5. Form `clean()`、Model `save()`、`CheckConstraint` 三者各擋住什麼入口？

**實作任務：**為 `ArticleQuerySet` 加一個 `popular(days=7)` 方法，回傳「近 `days` 天內發佈、依 `view_count` 由高到低」的已發佈文章；在 shell 驗證它能和 `by_tag()` 串接。

**<span class="label check">配套實作手冊</span>：**[第 3 章答案與步驟](../workbooks/learnjournal_01_content_model_and_publishing_workbook.md#chapter-3)
