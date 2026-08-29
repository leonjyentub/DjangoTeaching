---
marp: true
theme: default
transition: fade
size: 16:9
paginate: true
header: "LearnBoard 01｜Django 基礎與資料驅動留言板"
footer: "初學者教材｜觀念 → 語法 → LearnBoard 實作"
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
  h1 { color: #1e3a8a; }
  h2 { color: #2c4fb8; }
  blockquote {
    border-left: 6px solid #93b4f0; padding-left: 18px; color: #2d3a55;
    font-family: 'Noto Serif CJK TC', 'Noto Sans CJK TC', 'WenQuanYi Zen Hei', serif;
  }
  code, kbd {
    font-family: 'Noto Sans Mono CJK TC', 'SF Mono', Consolas,
                 'WenQuanYi Zen Hei Mono', 'Courier New', monospace;
    font-size: 0.92em;
  }
  pre { font-size: 0.72em; line-height: 1.28; }
  table { font-size: 0.78em; }
  strong { color: #1e3a8a; }
---

# 第 5 章
## ORM 查詢：把留言找出來

**本章成果：**能在 shell 中完成過濾、排序、計數，並理解 QuerySet 的惰性。

<!--
授課提示：全程開著 uv run python manage.py shell 示範。每個語法立刻看到回傳，比投影片講十遍有效。
-->

---

## 5-1 shell：已載入 Django 的 REPL

```bash
uv run python manage.py shell
```

```python
>>> from board.models import Message
>>> Message
<class 'board.models.Message'>
>>> Message.objects.count()
4
```

`objects` 是 manager，所有查詢的入口。離開用 `exit()`。

**你應該看到：**count 與你在 admin 看到的筆數一致。

---

## 5-2 all() 回傳 QuerySet：lazy 的集合

```python
>>> Message.objects.all()
<QuerySet [<Message: alice：歡迎來到學言板！…>, …]>
```

QuerySet 特點：

- **惰性**：現在只是描述，還沒真的 SELECT
- 真正執行的時機：迭代、list()、bool()、print 它的時候
- 可以一直接龍：`Message.objects.all().filter(...).order_by(...)[:5]`

> 惰性的好處：描述可以一路加工，最後一次性執行。

---

## 5-3 filter：條件查詢

```python
>>> Message.objects.filter(content__icontains="django")
<QuerySet […]>
```

`欄位__lookups` 語法：雙底線接查找方式。

| lookup | 意思 |
|---|---|
| `icontains` | 包含（不分大小寫） |
| `startswith` | 前綴 |
| `gt` / `gte` | 大於／大於等於 |
| `exact` | 完全相等（預設） |

留言牆的搜尋框就是 `icontains`。

---

## 5-4 order_by 與預設排序

```python
>>> Message.objects.order_by("-created_at")   # 新→舊
>>> Message.objects.order_by("created_at")    # 舊→新
```

model 已宣告 `Meta.ordering = ["-created_at"]`，所以 `all()` 天生就是新的在前。

`order_by(...)` 會覆蓋預設；`-` 前綴表示降冪。

---

## 5-5 get vs filter

```python
>>> Message.objects.get(pk=1)
<Message: alice：歡迎…>

>>> Message.objects.get(content__icontains="不存在")
DoesNotExist                     ← 查無 → 例外
>>> Message.objects.get(author__isnull=True)
MultipleObjectsReturned          ← 多筆 → 例外
```

`get`：期望恰好一筆，否則炸例外。
`filter`：0 到多筆都回 QuerySet，永不炸。

view 裡「找不到就回 404」的 `get_object_or_404` 正是把 `get` 的例外轉成 404。

---

## 5-6 count、first、exists 與切片

```python
>>> Message.objects.filter(content__icontains="django").count()
2
>>> Message.objects.first()
<Message: alice：歡迎…>
>>> Message.objects.exists()
True
>>> Message.objects.all()[:3]     # LIMIT 3
```

只要「有沒有」就用 `exists()`（效率最好）；只要數字就用 `count()`。

---

## 5-7 Q 物件：OR 條件

```python
from django.db.models import Q

>>> Message.objects.filter(Q(content__icontains="django") | Q(content__icontains="uv"))
```

逗號分隔 = AND；`Q(...) | Q(...)` = OR。

目前留言只有 content 一個欄位可搜；第二階段商城搜尋會同時打 name 與 description，正是同一招。

---

## 5-8 目前 LearnBoard 實作：搜尋的真正樣子

```python
# board/views.py（目前 LearnBoard 實作｜逐字摘錄）
def get_queryset(self):
    queryset = Message.objects.select_related("author")
    query = self.request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(Q(content__icontains=query))
    return queryset
```

- `select_related("author")`：一次 JOIN 抓作者，避免每張卡片多查一次（FK 存在才有意義）
- `.strip()`：防止全空白的 query 觸發無意義的 filter
- 沒有 query 就原樣返回全部——「搜尋」只是加了一層 filter

> `select_related` 的原理與 N+1 問題，Deck 02 配合 author 欄位完整展開。

---

## 第 5 章｜觀念檢核與實作

**觀念檢核：**

1. QuerySet 何時才會真的執行 SQL？
2. `filter(pk=99)` 查無資料時回傳什麼？`get(pk=99)` 又如何？
3. `icontains` 與 `contains` 差一字元，差別是什麼？
4. 為什麼判斷存在要用 `exists()` 而不是 `count() > 0`？

**實作任務：**在 shell 中找出「包含 paginate 的留言」、統計筆數、取最新三筆，並把過程貼進練習紀錄。

→ 步驟與解答在配套手冊第 5 章。
