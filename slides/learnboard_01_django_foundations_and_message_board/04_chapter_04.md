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

# 第 4 章
## Model、migration 與 admin

**本章成果：**能讀懂 Message model 的每個欄位、執行 migration，並用 admin 管理資料。

<!--
授課提示：本章資訊量最大。migration 心智模型（「schema 的版本控制」）比指令本身重要。
-->

---

## 4-1 ORM 心智模型

ORM（Object-Relational Mapping）：用 Python class 描述表格，用方法呼叫代替 SQL。

```python
class Message(models.Model):   # ← 一張表
    content = models.TextField()  # ← 一個欄位
```

| Python 世界 | 資料庫世界 |
|---|---|
| Model class | table |
| class 屬性 | column |
| instance | row |
| `Message.objects.filter(...)` | SELECT … WHERE … |

---

## 4-2 Message model 逐欄位拆解

```python
# board/models.py（目前 LearnBoard 實作｜節錄）
class Message(models.Model):
    author = models.ForeignKey(          # 作者（Deck 02 第 3 章詳解）
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="messages",
        verbose_name="作者",
    )
    content = models.TextField("留言內容", max_length=500)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)
```

先記住 `content` 與時間戳記；`author` 的故事 Deck 02 才展開。

---

## 4-3 三個核心欄位的行為

| 欄位 | 型別 | 行為 |
|---|---|---|
| `content` | TextField(max_length=500) | 表單層驗證長度；超過會被擋下 |
| `created_at` | DateTimeField(auto_now_add=True) | **建立時**自動記錄，之後不再變動 |
| `updated_at` | DateTimeField(auto_now=True) | 每次 `save()` 都更新 |

`auto_now_add` 與 `auto_now` 一字之差，行為完全不同——這是考試與實務都愛考的差異。

---

## 4-4 Meta、__str__ 與 get_absolute_url

```python
class Meta:
    ordering = ["-created_at"]     # 預設排序：新的在前

def __str__(self):
    who = self.author.username if self.author else "訪客"
    return f"{who}：{self.content[:20]}"

def get_absolute_url(self):
    return reverse("board:list")
```

- `ordering`：所有查詢預設套用，admin 與前台都受惠
- `__str__`：admin 列表、shell 顯示的全靠它
- `get_absolute_url`：告訴 Django「這個物件的代表網址」（CreateView 建立後往哪跳）

---

## 4-5 makemigrations vs migrate

```bash
uv run python manage.py makemigrations   # 產生 recipe（migrations/*.py）
uv run python manage.py migrate          # 照 recipe 施工（改 db.sqlite3）
```

**心智模型：migration 是 schema 的 git commit。**

- `makemigrations` = 寫 commit message 與 diff
- `migrate` = push 到資料庫
- 兩步可以分開執行，也可以先 review 再施工

---

## 4-6 migration 檔案長什麼樣？

```python
# board/migrations/0001_initial.py（節錄）
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.BigAutoField(primary_key=True, …)),
                ("content", models.TextField(max_length=500)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
```

它是普通 Python，可進版本控制、可 review。repository 裡還有一支 `0002_message_author.py`——那就是 Deck 02「加作者欄位」留下的歷史紀錄。

---

## 4-7 admin：最快的資料管理介面

```python
# board/admin.py
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "short_content", "created_at")
    search_fields = ("content", "author__username")
```

```bash
uv run python manage.py createsuperuser
```

**你應該看到：**`/admin/` 出現 Messages 表；可直接新增／搜尋／刪除留言。

---

## 4-8 admin 操作演練

1. 用 superuser 登入 `/admin/`
2. 新增一則留言，只填 content（author 留空 → 顯示「訪客」）
3. 回到首頁確認新留言出現在最上面（`ordering` 生效）
4. 刪除它，再次確認首頁

> admin 不是給終端使用者的介面，是給你（開發者／管理者）的後台。一般訪客的發文表單是 Deck 02 的事。

---

## 4-9 max_length 與 500 字限制的分工

```python
content = models.TextField("留言內容", max_length=500)
```

- Model 層：`max_length` 會反映到 ModelForm 的驗證（超過 → 表單錯誤，不進資料庫）
- Template 層：`truncatechars` 只管顯示截斷，不管儲存

**常見錯誤：**以為 TextField 不能有 max_length。可以，且是表單驗證的好幫手。

---

## 第 4 章｜觀念檢核與實作

**觀念檢核：**

1. `auto_now_add` 與 `auto_now` 的差別？
2. 為什麼 migration 檔案要 commit 進版本控制？
3. `__str__` 影響哪些地方的顯示？
4. 只跑 `migrate` 不跑 `makemigrations`，新欄位會進資料庫嗎？

**實作任務：**用 admin 建立三則留言（其中一則留空 author），確認首頁排序與「訪客」顯示皆正確。

→ 步驟與解答在配套手冊第 4 章。
