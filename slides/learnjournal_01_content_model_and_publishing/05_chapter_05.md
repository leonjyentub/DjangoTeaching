---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnJournal 01｜內容模型與發佈"
footer: "初學者教材｜觀念 → 語法 → LearnJournal 實作"
---

<!-- _class: cover -->

# 第 5 章
## 自訂 template tag、filter 與輸出安全

<div class="box">能寫三種形式的自訂 template tag，用 GROUP BY 做標籤雲，並解釋 `mark_safe` 的安全邊界</div>

<!--
授課提示：先複習 LearnBoard/LearnMart Deck 02 第 7 章的 autoescaping 與 XSS；本章的 mark_safe 是那一課的延伸。
-->

---

## 5-1 問題：側欄邏輯不該塞進每個 view

首頁、分類頁、標籤頁、文章頁……**每一頁**的側欄都要顯示「最新文章」「熱門標籤」。

如果放在 view 的 `get_context_data()`：

- 每個 view 都要重複那段查詢
- 換 function view 就整組再抄一次
- context processor 可以，但它對**每一頁**都執行，即使那頁不需要

**自訂 template tag**：模板需要時才呼叫，邏輯集中在一個檔案。

---

## 5-2 三種形式，各有用途

| 形式 | 用來 | 例子 |
|---|---|---|
| **filter** | 把一個值變成另一個值 | `{{ article.body \| markdownify }}` |
| **simple_tag** | 算一個值 / 一段字串 | `{% reading_time article %}` |
| **inclusion_tag** | 算好 context，再渲染一個小模板 | `{% tag_cloud 20 %}` |

全部放在 `app/templatetags/` 底下、有 `__init__.py` 的模組裡。

---

## 5-3 註冊的骨架

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/templatetags/journal_extras.py`（開頭）**

```python
from django import template

register = template.Library()
```

模板裡先 `{% load journal_extras %}`（檔名，不含 `.py`），才能用裡面的 tag。

```text
journal/
└── templatetags/
    ├── __init__.py            ← 一定要有，否則 Django 找不到
    └── journal_extras.py
```

---

## 5-4 filter：`markdownify`

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal_extras.py`**

```python
import markdown as md
from django.utils.safestring import mark_safe

@register.filter
def markdownify(text):
    return mark_safe(md.markdown(text or "", extensions=["fenced_code", "tables"]))
```

- `@register.filter`：函式的第一個參數是「被 filter 的值」（`{{ 值|markdownify }}`）
- 回傳的字串包了 `mark_safe`，模板才不會把 `<h2>` 這些標籤跳脫成文字

---

## 5-5 `mark_safe`：明確的安全邊界

Django 模板預設會 **autoescape**：`<script>` 會變成 `&lt;script&gt;`，這是 XSS 的第一道防線（Deck 02 第 7 章）。

`mark_safe` 是在說：「**這段字串我保證安全，不要跳脫。**」

```python
mark_safe(md.markdown(article.body))       # article.body 是誰寫的？
```

- 文章內文 = **作者**（受信任的登入使用者）寫的 → 允許 HTML 是刻意的功能
- 但如果同一條路徑吃到**匿名留言**或 **URL 參數** → 就是 stored XSS

> 規則：`mark_safe` 只能用在你能保證來源受信任的字串上。

---

## 5-6 對照：留言就**不能**這樣

**<span class="label current">目前 LearnJournal｜節錄</span>｜`templates/journal/article_detail.html`**

```django
{{ article.body_html|safe }}          {# 作者內容：允許 HTML #}
...
<p>{{ comment.body|linebreaksbr }}</p>  {# 留言：只換行，仍然 autoescape #}
```

- 文章 `body_html` 由 signal 用 markdown 產生（第 6 章），作者可控 → `|safe`
- 留言 `comment.body` 是任何登入者輸入 → **不加 `|safe`**，`<script>` 會被跳脫

同一頁，兩種輸出策略，差別就在「誰是作者」。

---

## 5-7 simple_tag：`reading_time`

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal_extras.py`**

```python
@register.simple_tag
def reading_time(article):
    return f"閱讀時間約 {article.reading_minutes} 分鐘"
```

```django
{% load journal_extras %}
{% reading_time article %}              {# → 閱讀時間約 3 分鐘 #}
{% reading_time article as rt %}        {# 存進變數 rt，稍後再用 #}
```

- `simple_tag` 的參數就是一般函式參數，`{% tag 參數1 參數2 %}`
- 回傳值直接輸出；加 `as 變數` 可存起來

---

## 5-8 `reading_minutes` 是 model 上的 property

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/models.py`**

```python
@property
def reading_minutes(self):
    words = max(len(self.body.split()), len(self.body))   # 中英混排粗估
    return max(1, round(words / 400))
```

- `len(self.body.split())`：英文用「空白切出的字數」
- `len(self.body)`：中文用「字元數」
- 取兩者較大值 / 400，最少 1 分鐘

> template tag 負責「呈現字串」，計算邏輯留在 model——各司其職。

---

## 5-9 inclusion_tag：`tag_cloud`

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal_extras.py`**

```python
from django.db.models import Count

@register.inclusion_tag("journal/_tag_cloud.html")
def tag_cloud(limit=20):
    tags = (
        Tag.objects.filter(articles__status="published")
        .annotate(count=Count("articles"))
        .order_by("-count")[:limit]
    )
    return {"tags": tags}
```

- `inclusion_tag` 回傳一個 dict → 拿去渲染指定的小模板
- 小模板 `_tag_cloud.html` 用 `{{ tags }}` 這個 key

---

## 5-10 這裡就是 GROUP BY（回扣第 4 章）

```python
Tag.objects.filter(articles__status="published")   # 只算有公開文章的標籤
    .annotate(count=Count("articles"))             # 每個標籤數它有幾篇
    .order_by("-count")[:limit]                    # 熱門排前面，取前 20
```

產生的 SQL 大致：

```sql
SELECT tag.*, COUNT(article.id) AS count
FROM tag JOIN article_tag ... JOIN article ...
WHERE article.status = 'published'
GROUP BY tag.id ORDER BY count DESC LIMIT 20;
```

`annotate(Count(反向關聯))` = 「每一列加一個計算欄位」；配合 `filter` 就是分組統計。

---

## 5-11 inclusion_tag 的小模板

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`templates/journal/_tag_cloud.html`**

```django
{% for tag in tags %}
  <a class="badge rounded-pill" href="{{ tag.get_absolute_url }}">{{ tag.name }} <span>{{ tag.count }}</span></a>
{% empty %}
  <p>還沒有標籤。</p>
{% endfor %}
```

- `{{ tag.count }}` 就是 `annotate` 加上去的欄位
- `{% empty %}` 處理沒有標籤的情況（回扣 LearnBoard 的 `{% for %}...{% empty %}`）

---

## 5-12 側欄如何組起來

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`templates/journal/_sidebar.html`**

```django
{% load journal_extras %}
<h2>最新文章</h2>
{% latest_articles 5 %}
<h2>熱門標籤</h2>
{% tag_cloud 20 %}
```

`base.html` 的 `{% block sidebar %}` 預設 `{% include "journal/_sidebar.html" %}`——每頁都有側欄，但查詢邏輯只寫在 `journal_extras.py`。

> Deck 03B 第 8 章會用「片段快取」把這兩個 tag 的結果暫存，避免每頁都查資料庫。

---

## 5-13 `lambda` 與 f-string 在這裡出現（回扣第 1 章）

```python
# 如果 tag_cloud 想在 Python 端再排一次（例如依名稱）：
tags = sorted(tags, key=lambda t: t.name)

# reading_time 的字串：
f"閱讀時間約 {article.reading_minutes} 分鐘"

# 若要顯示佔比：
f"{tag.count / total:.0%}"
```

第 1 章補的語法，到這一章就真的用上了。

---

## 5-14 <span class="label warning">常見錯誤</span> 自訂 tag

- `templatetags/` 少了 `__init__.py` → `TemplateSyntaxError: 'journal_extras' is not a registered tag library`
- 改了 tag 程式碼沒重啟 runserver → 舊行為
- filter 回傳含 HTML 卻沒 `mark_safe` → 畫面看到跳脫後的標籤文字
- 對**使用者輸入**用 `mark_safe` / `|safe` → stored XSS
- inclusion_tag 忘了回傳 dict → 小模板拿不到變數

---

## 第 5 章｜觀念檢核與實作

1. filter、simple_tag、inclusion_tag 三者分別「輸入什麼、輸出什麼」？
2. `markdownify` 為什麼要 `mark_safe`？什麼情況下 `mark_safe` 會變成漏洞？
3. 文章內文用 `|safe`、留言不用，判斷依據是什麼？
4. `tag_cloud` 裡的 `annotate(count=Count("articles"))` 產生什麼 SQL？
5. `templatetags/__init__.py` 少了會發生什麼？

**實作任務：**寫一個 `@register.simple_tag` 叫 `{% comment_count article %}`，回傳該文章「已核准」的留言數（含回覆）；再寫一個 `@register.filter` 叫 `excerptify`，把內文截成 60 字並補「…」。兩者都加上單元測試。

**<span class="label check">配套實作手冊</span>：**[第 5 章答案與步驟](../workbooks/learnjournal_01_content_model_and_publishing_workbook.md#chapter-5)
