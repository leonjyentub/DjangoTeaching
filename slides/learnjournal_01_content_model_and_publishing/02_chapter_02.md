---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnJournal 01｜內容模型與發佈"
footer: "初學者教材｜觀念 → 語法 → LearnJournal 實作"
---

# 第 2 章
## 多對多、中介模型與 data migration

**本章成果：**能設計多對多關聯、判斷何時需要中介模型、用自我關聯做樹狀結構，並寫一支把舊資料轉成新關聯的 migration。

<!--
授課提示：本章資訊量大，建議拆兩次課：2-1～2-9（M2M 與 through）一次、2-10～2-15（自我關聯與 data migration）一次。
-->

---

## 2-1 為什麼 ForeignKey 不夠？

LearnBoard／LearnMart 的關聯都是「一對多」：

```text
Category 1 ── * Product          一個分類有多個商品，一個商品一個分類
User 1 ── * Message              一個作者有多則留言，一則留言一個作者
```

但「文章與標籤」是**兩邊都是多**：

```text
Article * ── * Tag               一篇文章多個標籤，一個標籤多篇文章
```

ForeignKey 只能放在「多」的那一邊指向「一」。兩邊都多，就需要 `ManyToManyField`。

---

## 2-2 多對多的實體：其實是第三張表

```text
Article            ArticleTag（連結表）         Tag
+----+          +---------+--------+          +----+
| id |◄─────────| article | tag_id |─────────►| id |
+----+          +---------+--------+          +----+
                  每一列 = 一組「文章↔標籤」配對
```

- 資料庫沒有「多對多欄位」這種東西——它是**一張只放兩個 ForeignKey 的中介表**
- Django 的 `ManyToManyField` 預設會**自動**幫你建這張表
- 你在 Python 端看到的是 `article.tags`，不用直接碰中介表

---

## 2-3 `ManyToManyField`：最小形式

**<span class="label">教學用最小範例</span>**

```python
class Tag(models.Model):
    name = models.CharField(max_length=40, unique=True)

class Article(models.Model):
    title = models.CharField(max_length=160)
    tags = models.ManyToManyField(Tag, related_name="articles", blank=True)
```

- `ManyToManyField(目標 model, ...)`
- `related_name="articles"`：反向查詢入口 `tag.articles.all()`
- `blank=True`：表單層允許「一個標籤都不選」（M2M 不需要也不能有 `null`）

---

## 2-4 操作 M2M：`add` / `remove` / `set` / `clear`

```python
article = Article.objects.get(pk=1)
orm = Tag.objects.get(name="ORM")

article.tags.add(orm)            # 加一個配對（重複 add 不會出錯）
article.tags.remove(orm)         # 移除這個配對（不會刪 Tag 本身）
article.tags.set([tag_a, tag_b]) # 替換成剛好這些
article.tags.clear()             # 清空所有配對

article.tags.all()               # QuerySet[Tag]
orm.articles.all()               # 反向 QuerySet[Article]
```

> `.add()`／`.remove()` 動的是**中介表的列**，不是 `Tag` 或 `Article` 本身。

---

## 2-5 <span class="label warning">常見錯誤</span> 新物件還不能加 M2M

```python
article = Article(title="新文章")
article.tags.add(orm)            # ✗ ValueError：instance 還沒有 pk

article.save()                   # 先存，拿到 pk
article.tags.add(orm)            # ✓
```

中介表需要 `article_id`；物件還沒 `save()` 就沒有 id。

**在 `ModelForm` 用 CBV 存 M2M**：`CreateView` 會先 `form.save()`（存本體），再 `form.save_m2m()`（存關聯）。若你自己 override `form_valid` 且用了 `commit=False`，要記得手動呼叫 `save_m2m()`。

---

## 2-6 何時需要「中介模型」？關聯本身要帶資料時

預設 M2M 表只有兩個 ID。但如果「這組配對」本身有屬性——例如**精選排序**：

```text
文章 A 的標籤頁，想讓「ORM」排在「教學筆記」前面
→ 排序是「A↔ORM 這組配對」的屬性，不是 Tag 的、也不是 Article 的
```

這時用 `through=` 指定一個你自己寫的中介模型，把欄位加上去。

> 回扣 LearnMart：`OrderItem` 就是 Order 與 Product 之間的中介模型，
> 帶著 `unit_price`、`quantity`、`product_name` 快照——同一個道理。

---

## 2-7 `through`：LearnJournal 的實際做法

**<span class="label current">目前 LearnJournal｜節錄</span>｜`journal/models.py`**

```python
class Article(models.Model):
    tags = models.ManyToManyField(
        Tag, through="ArticleTag", related_name="articles", blank=True,
    )

class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    featured_order = models.PositiveSmallIntegerField("精選排序", default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["article", "tag"], name="unique_article_tag")]
        ordering = ["featured_order"]
```

`UniqueConstraint`：同一篇文章不能重複掛同一個標籤（預設 M2M 表自動有這限制，`through` 要自己加）。

---

## 2-8 用了 `through` 就不能直接 `add()`

```python
# 預設 M2M：article.tags.add(tag)          ← through 之後這行會報錯

# through 模型：直接建立中介列
ArticleTag.objects.create(article=article, tag=orm, featured_order=1)

# 讀取仍然一樣方便
article.tags.all()                          # QuerySet[Tag]，依 featured_order 排序
article.tags.through.objects.filter(article=article)   # 拿中介列（含 featured_order）
```

**取捨：**`through` 換來「關聯帶資料」，代價是新增配對要多寫一行。
只有真的需要配對屬性時才用 `through`。

---

## 2-9 同一個模型的第二個 M2M：共同作者

**<span class="label current">目前 LearnJournal｜節錄</span>｜`journal/models.py`**

```python
class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT, related_name="articles")
    coauthors = models.ManyToManyField(
        User, related_name="coauthored_articles", blank=True,
    )
```

- `author`（FK，一位）與 `coauthors`（M2M，多位）指向**同一個 `User`**
- `related_name` 一定要不同：`user.articles`（主要作者）vs `user.coauthored_articles`（掛名）
- 這個 M2M 沒有配對屬性，所以用預設形式（不加 `through`）

<!--
授課提示：問學生：如果兩個 related_name 都用預設會怎樣？（reverse accessor 衝突，makemigrations 直接報錯）
-->

---

## 2-10 自我關聯：一則留言可以回覆另一則

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/models.py` 的 `Comment`**

```python
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies",
    )
    body = models.TextField(max_length=1000)
    is_approved = models.BooleanField(default=True)
```

- `ForeignKey("self")`：指向同一個 model
- `parent=None` → 這是頂層留言；`parent=某留言` → 這是它的回覆
- `comment.replies.all()`：這則留言的所有直接回覆

---

## 2-11 自我關聯畫成樹

```text
Comment(id=1, parent=None)          頂層留言
├── Comment(id=2, parent=1)         回覆 1
│   └── Comment(id=4, parent=2)     回覆 2（第二層）
└── Comment(id=3, parent=1)         回覆 1
```

```python
top = article.comments.filter(parent__isnull=True, is_approved=True)
for comment in top:
    for reply in comment.replies.all():
        ...
```

**教學版取捨：**LearnJournal 的模板只顯示兩層（留言 + 直接回覆）。
真正的無限層巢狀需要遞迴 template 或 MPTT 類套件——本冊不做。

---

## 2-12 資料模型全貌

```text
User 1 ── * Article(author)        User * ── * Article(coauthors)
Category 1 ── * Article
Article * ──(ArticleTag)── * Tag
Article 1 ── * Comment ── self(parent)
Article 1 ── * Reaction * ── 1 User      （user × article × kind 唯一）
Subscription（獨立：email 訂閱）
```

- `Article.author` 用 `PROTECT`：有文章時不能刪作者（保留內容歸屬）
- `Comment.author` 用 `CASCADE`：刪帳號時他的留言一起走
- `on_delete` 是商業決策——回扣 LearnMart 第 4 章那張表

---

## 2-13 舊資料怎麼搬？先看情境

假設 LearnJournal 早期版本把標籤存成一個文字欄位：

```text
Article.legacy_tags = "orm, 測試, 教學筆記"     ← 逗號分隔字串
```

現在要改成 `Tag` + `ArticleTag` 的關聯。直接改 model 只會產生「加欄位／刪欄位」的 schema migration，**舊資料不會自己搬家**。

需要一支 **data migration**：用程式碼把每篇文章的 `legacy_tags` 拆開，建立對應的 `Tag` 與 `ArticleTag`。

> 回扣 LearnBoard：`0002_message_author` 是 schema 演進化石；data migration 是「schema 沒變，但資料要動」。

---

## 2-14 `RunPython`：data migration 的核心

**<span class="label">教學用最小範例</span>**

```python
from django.db import migrations

def split_legacy_tags(apps, schema_editor):
    Article = apps.get_model("journal", "Article")     # 注意：不是 import 真的 model
    Tag = apps.get_model("journal", "Tag")
    for article in Article.objects.exclude(legacy_tags=""):
        for name in [s.strip() for s in article.legacy_tags.split(",") if s.strip()]:
            tag, _ = Tag.objects.get_or_create(name=name, defaults={"slug": name})
            article.tags.add(tag)

def undo(apps, schema_editor):
    apps.get_model("journal", "ArticleTag").objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [("journal", "0002_...")]
    operations = [migrations.RunPython(split_legacy_tags, undo)]
```

---

## 2-15 data migration 的四條規則

1. **用 `apps.get_model()`**，不要 `from journal.models import Article`——migration 要拿「當時的歷史版本」，不是現在的。
2. **一定要提供反向函式**（第二個參數），否則不能往回 migrate；安全的話用 no-op。
3. **大表要分批**（`iterator()`、切 range），一次載入全部會爆記憶體。
4. **產生後先讀再套用**：`makemigrations --empty journal` 建空殼，自己填 `RunPython`。

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/migrations/0003_backfill_excerpt.py`** 就是一支真的 data migration：把早期沒填 `excerpt` 的文章，從內文前 140 字補一份摘要。

---

## 2-16 <span class="label warning">常見錯誤</span> M2M 與 data migration

- 新 instance 還沒 `save()` 就 `.add()` → `ValueError`
- 用了 `through` 卻呼叫 `.add()` → 直接報錯，要 `ArticleTag.objects.create(...)`
- 兩個指向同一 model 的關聯 `related_name` 沒區分 → `makemigrations` 報 accessor 衝突
- data migration 裡 `import` 真的 model → 未來 model 改欄位時這支 migration 會壞
- 忘記寫反向函式 → `migrate journal 0002` 直接失敗

---

## 第 2 章｜觀念檢核與實作

1. 為什麼「文章 ↔ 標籤」不能只用 ForeignKey？資料庫實際上多了什麼？
2. `through` 換來什麼、代價是什麼？舉一個 LearnJournal 裡的例子。
3. `author` 和 `coauthors` 都指向 `User`，為什麼 `related_name` 必須不同？
4. data migration 為什麼要用 `apps.get_model()` 而不是直接 import？
5. `Comment.parent` 的 `null=True` 代表什麼？`is_approved` 又是做什麼的？

**實作任務：**在練習 branch 為 `Tag` 加一個 `description` 欄位，產生 schema migration；再寫一支 data migration，把所有 `description=""` 的標籤補上 `f"關於 {tag.name} 的文章"`。跑 `migrate` 再 `migrate journal <前一號>` 確認可逆。

**<span class="label check">配套實作手冊</span>：**[第 2 章答案與步驟](../workbooks/learnjournal_01_content_model_and_publishing_workbook.md#chapter-2)
