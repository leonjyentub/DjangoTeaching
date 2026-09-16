---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnJournal 01｜內容模型與發佈"
footer: "初學者教材｜觀念 → 語法 → LearnJournal 實作"
---

<!-- _class: cover -->

# 第 1 章
## 專案骨架與 Python 語法補充

<div class="box">能啟動 LearnJournal，讀懂它的 app 結構，並補齊後續章節會用到但先備教材沒教的 Python 語法</div>

<!--
授課提示：本章一半是環境（可課前自學），一半是 Python 語法快閃。
語法頁請對照 learnjournal/ 的真實檔案，不要抽象講。
-->

---

## 1-1 專案結構：一個 `journal` app

**<span class="label current">目前 LearnJournal｜節錄</span>**

```text
learnjournal/
├── config/                 # settings、根路由（比照前兩專案，單一 settings.py）
├── journal/
│   ├── models.py           # User / Category / Tag / Article / ArticleTag / Comment / Reaction / Subscription
│   ├── managers.py         # ArticleQuerySet / PublishedManager（第 3 章）
│   ├── views.py            # function view + generic view + 日期型 view
│   ├── forms.py
│   ├── signals.py          # post_save：渲染 Markdown（第 6 章）
│   ├── templatetags/journal_extras.py   # 自訂 tag（第 5 章）
│   ├── admin.py
│   ├── migrations/         # 0003 是教學用 data migration（第 2 章）
│   └── management/commands/seed_demo.py
├── templates/  static/  manage.py  pyproject.toml
```

---

## 1-2 依賴比前兩專案多一個

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`pyproject.toml`**

```toml
dependencies = [
    "django>=6.1.1,<6.2",
    "markdown>=3.7",
]
```

- `markdown`：把文章的 Markdown 原文轉成 HTML（第 5、6 章）
- 其餘與 LearnBoard 相同：uv 管理 `.venv`、`uv.lock`
- LearnMart 需要的 `Pillow` 這裡**沒有**——本冊不做圖片上傳（留給 Deck 03B 的 formset 章）

```bash
uv sync   # 安裝 django 與 markdown
```

---

## 1-3 settings 的三個新設定

**<span class="label current">目前 LearnJournal｜節錄</span>｜`config/settings.py`**

```python
INSTALLED_APPS = [..., "django.contrib.sitemaps", "django.contrib.humanize", "journal"]

MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
        "OPTIONS": {},
    }
}   # Deck 03B 第 10 章

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", ...}}  # Deck 03B 第 8 章
```

- `humanize`：`{{ n|intcomma }}`、`{{ dt|naturaltime }}` 等顯示 filter，本冊會用
- `sitemaps`：Deck 03B 才接內容，先註冊
- email／cache 先設好後端，功能在 Deck 03B

> `AUTH_USER_MODEL = "journal.User"`：跟 LearnMart 一樣，自訂 User 在第一次 migration 前就決定。

---

## 1-4 為什麼還要補 Python 語法？

先備教材（`../00a_python_syntax_essentials/`）教過：變數、容器、`if`／`for`、`def`、`try`、class、繼承、mixin、decorator、型別標註。

本冊會**額外**用到：

| 語法 | 出現在 | 章 |
|---|---|---|
| `lambda`＋`sorted(key=)` | template tag 排序標籤雲 | 5 |
| f-string 格式規格 `:,`、`:.0%` | 瀏覽數、比例顯示 | 5 |
| `datetime` / `timedelta` | 排程、彙整區間 | 3、4 |
| `with` 區塊型 context manager | `with transaction.atomic():` | 3 |
| generator / `yield` | seed 與匯入指令 | 1 |
| 可空型別標註 `X \| None` | manager 回傳值 | 3 |

<!--
授課提示：這頁只是索引。逐項在後面 1-5～1-10 帶最小範例。
-->

---

## 1-5 `lambda`：一次性的小函式

```python
tags = [("orm", 12), ("測試", 5), ("部署", 9)]

sorted(tags, key=lambda pair: pair[1])            # 依數量升冪
sorted(tags, key=lambda pair: -pair[1])           # 依數量降冪
max(tags, key=lambda pair: pair[1])               # ("orm", 12)
```

- `lambda 參數: 回傳值`——沒有名字的函式，只能寫一行
- 最常見用途就是 `sorted`／`max`／`min` 的 `key=`
- `key` 收一個函式，對每個元素算出「用來比較的值」

> 第 5 章的標籤雲會用 `key=lambda t: t.count` 把熱門標籤排到前面。

---

## 1-6 f-string 格式規格：冒號後面的小語言

```python
count = 1234567
ratio = 0.283

f"{count:,}"        # '1,234,567'   千分位
f"{ratio:.0%}"      # '28%'         百分比、0 位小數
f"{ratio:.1%}"      # '28.3%'
f"{3.14159:.2f}"    # '3.14'        固定 2 位小數
```

- 冒號 `:` 之後是「格式規格」，控制**怎麼顯示**，不改變值本身
- `,` 千分位、`%` 百分比、`.2f` 小數位數、`>10` 靠右補空白

> LearnJournal 文章頁顯示「瀏覽 {{ article.view_count|intcomma }}」用的是 template filter，
> 但在 Python 端算閱讀時間字串時就是 f-string。

---

## 1-7 `datetime` 與 `timedelta`：時間也能加減

```python
from datetime import timedelta
from django.utils import timezone

now = timezone.now()                       # 帶時區的「現在」
week_ago = now - timedelta(days=7)         # 七天前
soon = now + timedelta(hours=2)

now > week_ago                             # True
```

- `timezone.now()`：專案設定 `USE_TZ=True` 時回傳 **aware datetime**（帶時區）
- `timedelta`：一段「時間長度」，可與 datetime 相加減
- 比較兩個 datetime 就是比大小

> 第 3 章的 `published()` 用 `published_at__lte=timezone.now()` 判斷「發佈時間到了沒」。

---

## 1-8 `with`：區塊型 context manager

```python
from django.db import transaction

with transaction.atomic():
    order.save()
    for item in items:
        item.save()
# 離開區塊：沒有例外就 COMMIT，有例外就 ROLLBACK
```

- LearnMart Deck 02 用的是 `@transaction.atomic` **裝飾器**形式
- `with` 是**區塊**形式：只包住需要一起成功的幾行，範圍更精準
- `with` 保證「進入時做一件事、離開時做一件事」，即使中途丟例外

> 也適用檔案：`with open(path) as f:` 離開時自動關檔（本冊匯入指令練習會用到）。

---

## 1-9 generator：用 `yield` 一次吐一個

```python
def read_titles(path):
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield line          # 不是 return：吐出一個值後暫停

for title in read_titles("titles.txt"):
    print(title)
```

- 有 `yield` 的函式呼叫後不會立刻執行，而是回傳一個 **generator**
- 每次 `for` 拿一個值才執行到下一個 `yield`——不用把整份資料一次讀進記憶體
- 適合「逐筆處理大量資料」的管理指令

---

## 1-10 型別標註：`X | None` 與容器泛型

```python
def find_slug(slug: str) -> "Article | None":
    return Article.objects.filter(slug=slug).first()

def top_tags(limit: int = 20) -> list["Tag"]:
    ...
```

- `X | None`：這個值可能是 `X`，也可能是 `None`（`.first()` 找不到就回 `None`）
- `list["Tag"]`、`dict[str, int]`：容器裡裝什麼
- 標註**不會被強制執行**，是給讀者與工具看的（先備教材第 12 章）

---

## 1-11 啟動與示範資料

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/management/commands/seed_demo.py` 說明**

```bash
uv run python manage.py migrate
uv run python manage.py seed_demo      # 可重複執行
uv run python manage.py runserver
```

`seed_demo` 建立：

- 三個帳號：`editor`／`amy`／`ben`（密碼 `<名字>12345`）
- 三個分類、五個標籤、三篇已發佈文章（含 Markdown 內文與程式碼區塊）
- 一組巢狀留言（`ben` 留言、`amy` 回覆）

> **你應該看到**：`http://127.0.0.1:8000/` 出現三篇文章卡片、右側欄有「熱門標籤」。

---

## 1-12 先在 shell 認識模型

```bash
uv run python manage.py shell
```

```python
from journal.models import Article, Tag

Article.objects.count()          # 3（全部，含草稿）
Article.published.count()         # 3（只有已發佈）
Article.objects.first().tags.all()   # <QuerySet [<Tag: 教學筆記>, <Tag: ORM>]>
Tag.objects.first().articles.all()   # 反向：這個標籤的所有文章
```

注意 `Article.objects` 與 `Article.published` 是**兩個不同的 manager**（第 3 章詳解）。

---

## 第 1 章｜觀念檢核與實作

1. `journal` app 底下 `managers.py` 與 `signals.py` 各自的責任是什麼？
2. 為什麼 LearnJournal 的 `pyproject.toml` 沒有 `Pillow`？
3. `lambda p: -p.count` 和 `lambda p: p.count` 排序結果差在哪？
4. `with transaction.atomic():` 與 `@transaction.atomic` 有什麼差別？
5. `timezone.now()` 回傳的 datetime 和 `datetime.now()` 差在哪？

**實作任務：**在 shell 建立一篇 `status="draft"` 的文章，確認它出現在 `Article.objects` 但不在 `Article.published`；再把它改成 `published` 並存檔，觀察 `published_at` 自動被填。

**<span class="label check">配套實作手冊</span>：**[第 1 章答案與步驟](../workbooks/learnjournal_01_content_model_and_publishing_workbook.md#chapter-1)
