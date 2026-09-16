# LearnBoard 01 配套實作手冊

本手冊對應 [Django 基礎與資料驅動留言板](../learnboard_01_django_foundations_and_message_board/00_overview.md)。投影片保留問題與任務；本手冊提供答案、推理、實作步驟與驗收方式。

> 建議先獨立回答，再查看解答。涉及 source code 的練習請在個人練習 branch 進行。每段「修改後」只顯示焦點 excerpt，不代表整個檔案。

## 目錄

1. [第 1 章｜Python 執行環境與 uv](#chapter-1)
2. [第 2 章｜Django 專案、HTTP、URL 與第一個 View](#chapter-2)
3. [第 3 章｜Template、static 與響應式留言牆](#chapter-3)
4. [第 4 章｜Model、migration 與 admin](#chapter-4)
5. [第 5 章｜ORM 查詢：把留言找出來](#chapter-5)
6. [第 6 章｜整合：可搜尋的留言牆](#chapter-6)

---

<a id="chapter-1"></a>
# 第 1 章｜Python 執行環境與 uv

## 觀念檢核答案

### 1. `.venv` 與 `uv.lock` 各解決什麼問題？

`.venv/` 是本機的隔離安裝空間，讓 LearnBoard 的 Python 與套件不和其他專案混在一起；`uv.lock` 記錄 uv 解析出的完整精確版本，使不同電腦能重建相同依賴集合。

只有 `.venv` 沒有 lock，兩位同學可能在不同日期裝到不同 transitive dependency；只有 lock 不隔離，套件仍可能污染其他專案。

### 2. 為什麼 `uv sync` 之後還要 `migrate`？

`uv sync` 的責任是 Python 環境與套件依賴；資料表由 Django migration 系統管理，必須另外執行：

```bash
uv run python manage.py migrate
```

「套件已安裝」與「database schema 已套用」是兩種不同狀態。

### 3. `django>=6.1.1,<6.2` 接受哪些版本？

大於等於 6.1.1 且小於 6.2 的版本，例如 6.1.1、6.1.2。不接受 6.0.x，也不接受 6.2.0。實際安裝哪個精確版本由 `uv.lock` 決定。

### 4. `seed_demo` 做了哪些事？它會重設已存在的帳號密碼嗎？

以 `get_or_create` 建立 `alice` 與 `bob` 兩個帳號（只在「新建」時設定密碼），並建立四則示範留言（含一則 author 為 NULL 的訪客留言）。若同名帳號已存在，**不會**重設其密碼——它不是帳號重設指令。

## 實作任務：從空白本機狀態啟動 LearnBoard

### 影響檔案／符號

不修改 application source。讀取 `.python-version`、`pyproject.toml`、`uv.lock`、`manage.py`；在本機建立 `.venv/` 與 `db.sqlite3`。

### 步驟

```bash
cd <你的路徑>/learnboard
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver
```

### 驗收

- 瀏覽器開啟 `http://127.0.0.1:8000/`，看到四則留言與深藍導覽列
- `alice / alice12345` 能登入（登入功能本身是 Deck 02 主題，此處用 admin 或之後驗證）

---

<a id="chapter-2"></a>
# 第 2 章｜Django 專案、HTTP、URL 與第一個 View

## 觀念檢核答案

### 1. `include()` 在 URLconf 接力中扮演什麼？

把「剩餘路徑」交給另一份 URLconf（通常是 app 的 urls.py）。project 只當總機分接，每個 app 自管自己的路由，避免所有規則擠在同一個檔案。

### 2. `<int:pk>` 做了什麼？

路徑 converter：比對路徑中的一段整數，轉成 Python `int`，並以關鍵字參數 `pk` 傳入 view。view 的參數名稱必須同名。

### 3. 為什麼模板要用 `{% url %}` 而不是寫死 href？

命名路由讓「路徑定義」集中在一處。改路由時模板不用跟著改；寫死的 href 會散落各處成為維護地雷。

### 4. 404 與 500 的成因差別？

404＝路由不符或查無物件（正常流程的「沒有」）；500＝程式拋出未捕捉例外（bug）。除錯時先看狀態碼分類，再決定看 URL 還是 traceback。

## 實作任務：新增 /about/ 頁

### 影響檔案

```text
board/urls.py     # 加一行 path
board/views.py    # 加一個 function view
```

### 焦點前後對照

**修改前：**

```python
urlpatterns = [
    path("", views.MessageListView.as_view(), name="list"),
]
```

**修改後：**

```python
urlpatterns = [
    path("", views.MessageListView.as_view(), name="list"),
    path("about/", views.about, name="about"),
]
```

```python
def about(request):
    return HttpResponse("學言板：Django 教學用留言板")
```

### 步驟

1. 在 `board/views.py` 加入 `about` view
2. 在 `board/urls.py` 註冊路由並命名為 `"about"`
3. `uv run python manage.py shell`：

   ```python
   >>> from django.urls import reverse
   >>> reverse("about")
   '/about/'
   ```

### 驗收

- 瀏覽 `/about/` 顯示文字，狀態 200
- 故意拜訪 `/aboutx/` 得到 404，確認 DEBUG 頁面列出嘗試過的路由

---

<a id="chapter-3"></a>
# 第 3 章｜Template、static 與響應式留言牆

## 觀念檢核答案

### 1. `render()` 的第三個參數是什麼？對應模板裡的什麼？

dict（context）。key 對應模板中的變數名稱：`{"posts": qs}` → `{{ posts }}`／`{% for post in posts %}`。

### 2. `{% empty %}` 解決什麼問題？

QuerySet 為空時的分支。等價於 `{% if posts|length == 0 %}`，但語意更清楚、少一層巢狀。

### 3. `{% static 'css/site.css' %}` 與直接寫 `/static/css/site.css` 差在哪？

`{% static %}` 由 Django 依 `STATIC_URL` 計算網址。部署到非根路徑或 CDN 時只需改設定；寫死則每個模板都要手改。

### 4. 為什麼留言內容不能用 `|safe`？

`|safe` 關閉自動跳脫。使用者輸入可能含 `<script>`，關閉跳脫等於親手打開 XSS 大門。只有可信的 HTML（如管理員撰寫的公告）才考慮。

## 實作任務：footer 文字與 .hero 圓角

### 影響檔案

```text
templates/base.html     # footer 文字
static/css/site.css     # .hero 圓角
```

### 焦點前後對照

**修改前（site.css）：**

```css
.hero { background: linear-gradient(…); }
```

**修改後：**

```css
.hero { background: linear-gradient(…); border-radius: 1.25rem; }
```

### 步驟

1. 編輯 `base.html` footer 內文字，存檔重新整理
2. 在 `site.css` 的 `.hero` 補上 `border-radius`，重新整理觀察圓角
3. 若無效果：Ctrl+F5 強制清快取，並確認 `<link>` 使用的是 `{% static %}`

### 驗收

- footer 新文字出現在每一頁（因為 base.html 被所有頁面繼承）
- hero 區塊四角變圓

---

<a id="chapter-4"></a>
# 第 4 章｜Model、migration 與 admin

## 觀念檢核答案

### 1. `auto_now_add` 與 `auto_now` 的差別？

`auto_now_add=True`：物件**第一次建立**時記錄當下時間，之後不再更新。`auto_now=True`：每次呼叫 `save()` 都更新為當下時間。前者適合 created_at，後者適合 updated_at。

### 2. 為什麼 migration 檔案要 commit 進版本控制？

它是 schema 的歷史紀錄與重建配方。其他電腦與正式環境靠同一組檔案把資料庫推到相同結構；刪掉等於失去版本控制的意義。

### 3. `__str__` 影響哪些地方？

admin 列表與詳情頁標題、shell 中印出 QuerySet 時的顯示、log 訊息等任何「需要把 instance 變成文字」的場合。

### 4. 只跑 `migrate` 不跑 `makemigrations`，新欄位會進資料庫嗎？

不會。`migrate` 只執行「已存在的 migration 檔案」。models.py 改了但沒有產生對應檔案，schema 不會動，還會被 `makemigrations --check` 抓到不同步。

## 實作任務：admin 三則留言演練

### 步驟

```bash
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

1. `/admin/` 登入 superuser
2. Messages → Add：只填 content「admin 建立的測試留言」，author 留空
3. 回首頁：新留言在最上方（Meta.ordering 生效），作者顯示「訪客」（__str__ 與模板雙重保護）
4. 再建兩則，其中一則指定作者 alice
5. 刪除「admin 建立的測試留言」

### 驗收

- admin 列表顯示 id、作者、內容前 30 字、時間（list_display）
- 搜尋框輸入關鍵字能過濾（search_fields）

---

<a id="chapter-5"></a>
# 第 5 章｜ORM 查詢：把留言找出來

## 觀念檢核答案

### 1. QuerySet 何時才會真的執行 SQL？

迭代（for）、`list()`、`bool()`、切片含 step、`print()`（repr）等「需要資料」的時刻。宣告鏈本身只是描述。

### 2. `filter(pk=99)` 查無資料回傳什麼？`get(pk=99)` 又如何？

filter 回傳空的 QuerySet（不例外）；get 直接 raise `DoesNotExist`。列表頁用 filter，單物件事用 get（或 get_object_or_404）。

### 3. `icontains` 與 `contains` 差一字元，差別是什麼？

`icontains` 忽略大小寫（SQL 的 UPPER 比较）；`contains` 分辨大小寫。中文場景兩者常無差異，英文關鍵字差異明顯。

### 4. 為什麼判斷存在要用 `exists()` 而不是 `count() > 0`？

`exists()` 產生 `SELECT … LIMIT 1`，找到一筆即停；`count()` 要數完整個結果集。語意相同，效率不同。

## 實作任務：shell 五連問

### 步驟

```python
>>> from board.models import Message
>>> Message.objects.filter(content__icontains="paginate")       # 1 找留言
>>> Message.objects.filter(content__icontains="paginate").count()  # 2 數筆數
>>> Message.objects.order_by("-created_at")[:3]                 # 3 最新三筆
>>> Message.objects.filter(author__isnull=True)                  # 4 訪客留言
>>> Message.objects.exists()                                     # 5 存在性
```

### 驗收

- 第 4 題至少回傳 seed_demo 建立的那則訪客留言
- 記下每題的 SQL 直覺（可在 log 或 Django debug toolbar 觀察，選做）

---

<a id="chapter-6"></a>
# 第 6 章｜整合：可搜尋的留言牆

## 觀念檢核答案

### 1. `context_object_name` 改掉會發生什麼事？

模板中的變數名稱也要跟著改，否則 `{% for post in posts %}` 迭代不到東西（頁面只剩 empty 分支或空白）。CBV 預設名是 `message_list` 與 `object`。

### 2. 為什麼搜尋要用 GET？用 POST 會失去什麼？

GET 把條件放進網址：可分享、可收藏、可重新整理而不重送表單警告，也符合「查詢不改變資料」的語意。POST 版本無網址參數，上述全失。

### 3. `page_obj.number` 與 `paginator.num_pages` 各是什麼？

前者是目前頁碼；後者是總頁數。模板用它們組出「1 / 2」這類指示。

### 4. 若模板拿掉 `{% if post.author %}`，哪一則留言會壞掉？

不會「壞」，但訪客留言的作者位置會顯示 `None`（或空白）。防禦式渲染的重點正是資料允許 NULL 時 UI 仍合理。

## 實作任務：完整 vertical slice 驗收

### 影響檔案

本章不修改 source。逐項操作既有功能並對照 6-7 清單：

1. 首頁排序：admin 新增留言 → 出現在最上
2. 搜尋保留：搜尋 `paginate` → 搜尋框內仍有 `paginate`
3. 空結果：搜尋 `zzzzz` → 「找不到符合」訊息，200 而非錯誤頁
4. 分頁：admin 補足至 11 筆 → 出現「1 / 2」；翻頁後 query 不丟失
5. 訪客留言：作者欄顯示「訪客」

### 驗收後的反思題

- 從點下搜尋到看到結果，資料經過了哪些函式？（答案：`MessageListView.get_queryset` → ORM → template）
- 哪一段是「目前 LearnBoard 實作」尚未涵蓋的？（發文 POST、帳號、權限——全部指向 Deck 02）
