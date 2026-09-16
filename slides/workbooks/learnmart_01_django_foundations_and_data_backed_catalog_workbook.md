# LearnMart 01 配套實作手冊

本手冊對應 [Django 基礎與資料驅動商品目錄](../learnmart_01_django_foundations_and_data_backed_catalog/00_overview.md)。投影片保留問題與任務；本手冊提供答案、推理、實作步驟與驗收方式。

> 建議先獨立回答，再查看解答。涉及 source code 的練習請在個人練習 branch 進行；不要直接把所有答案貼進正式專案。每段「修改後」只顯示焦點 excerpt，不代表整個檔案。

## 目錄

1. [第 1 章｜Python 執行環境與 uv](#chapter-1)
2. [第 2 章｜Django 專案、HTTP、URL 與第一個 View](#chapter-2)
3. [第 3 章｜Template、static 與響應式頁面](#chapter-3)
4. [第 4 章｜Model、關聯與 migration](#chapter-4)
5. [第 5 章｜ORM、QuerySet 與資料規則](#chapter-5)
6. [第 6 章｜組合成可搜尋的資料驅動商品目錄](#chapter-6)

---

<a id="chapter-1"></a>
# 第 1 章｜Python 執行環境與 uv

**相關投影片：第 7–21 頁**

## 觀念檢核答案

### 1. `.venv` 與 `uv.lock` 各解決什麼問題？

`.venv/` 是本機的隔離安裝空間，讓 LearnMart 的 Python 與 packages 不和其他專案混在一起；`uv.lock` 則記錄 uv 已解析出的完整精確版本，使不同電腦能重建相同依賴集合。

兩者缺一仍可能出問題：只有 `.venv` 而沒有 lock，兩位同學可能在不同日期裝到不同 transitive dependency；只有 lock 而不隔離，package 仍可能污染其他專案。

### 2. 為什麼 `uv sync` 不會建立 Django 資料表？

`uv sync` 的責任是 Python environment 與 package dependencies。資料表由 Django migration 系統管理，必須執行：

```bash
uv run python manage.py migrate
```

「套件已安裝」與「database schema 已套用」是兩種不同狀態。

### 3. `django>=6.1.1,<6.2` 接受哪些版本？

同時符合大於等於 5.2 且小於 5.3 的版本，例如 5.2、5.2.1、5.2.9。它不接受 5.1.x，也不接受 5.3.0。實際安裝哪個精確版本再由 `uv.lock` 決定。

### 4. `uv run python manage.py seed_demo` 中，誰負責什麼？

- `uv run`：選擇並準備專案環境。
- `python`：實際 Python interpreter。
- `manage.py`：設定 `DJANGO_SETTINGS_MODULE=config.settings`，進入 Django command 系統。
- `seed_demo`：位於 `marketplace/management/commands/` 的自訂 command 名稱。

### 5. 為什麼 `runserver` 成功不代表 production ready？

Django development server 為開發除錯設計；目前也使用 `DEBUG=True`、課堂用 SECRET_KEY、本機 SQLite 與開發用 media serving。Production 還需要安全設定、正式 web server、static/media 方案、監控、備份等。本章成功標準只限本機課堂環境。

## 實作任務：從空白本機狀態啟動 LearnMart

### 目標

能從 repository 根目錄重建環境、套用 schema、建立示範資料並啟動伺服器；每一步都能說出它改變哪一層。

### 前置條件

- 已安裝 uv。
- 終端機可進入 LearnMart repository。
- `8000` port 未被其他程式占用。

### 影響檔案／符號

本章**不修改 application source**。會讀取：

- `.python-version`
- `pyproject.toml` 的 `[project]`、`dependencies`、`[dependency-groups]`
- `uv.lock`
- `manage.py`
- `marketplace.management.commands.seed_demo.Command`

會在本機建立或更新 `.venv/` 與 `db.sqlite3`；`seed_demo` 只在 database 建立示範 rows，不會建立商品圖片或其他 media files。

### 焦點前後對照

**開始前：環境狀態可能不完整**

```text
.venv/ 不存在或不同步
db.sqlite3 不存在或尚未套用 migration
瀏覽器無法連上 127.0.0.1:8000
```

**完成後：四個層次都有可觀察狀態**

```text
.venv/                 依賴已同步
db.sqlite3             migration 已套用
seller / buyer         示範資料已建立
127.0.0.1:8000         development server 回應
```

### 步驟

1. 確認目前位置與關鍵檔案：

   ```bash
   pwd
   ls
   ```

   應看見 `manage.py`、`pyproject.toml`、`config/`、`marketplace/`。

2. 同步環境：

   ```bash
   uv sync
   ```

3. 驗證 interpreter 與 Django 版本：

   ```bash
   uv run python --version
   uv run python -m django --version
   ```

   Python 應符合 3.13 以上；Django 應在 6.1.x 範圍。

4. 查看 migration 狀態並套用：

   ```bash
   uv run python manage.py showmigrations
   uv run python manage.py migrate
   ```

   第一次套用時會列出多個 `Applying ... OK`；已套用時可能顯示 `No migrations to apply.`。

5. 建立示範資料並觀察重跑行為：

   ```bash
   uv run python manage.py seed_demo
   uv run python manage.py seed_demo
   ```

   第二次不應持續新增同名帳號與商品。但只有在沒有同名帳號的新 database 中，第一次執行才可靠建立教材列出的 password/role；既有 `seller`／`buyer` 不會被 reset。

6. 啟動伺服器：

   ```bash
   uv run python manage.py runserver
   ```

7. 開啟 `http://127.0.0.1:8000/`，再以 `Ctrl+C` 停止 server。

### 指令與預期結果

```bash
uv run python manage.py check
```

預期：

```text
System check identified no issues (0 silenced).
```

```bash
uv run python manage.py shell -c "from marketplace.models import Product; print(Product.objects.count())"
```

預期為大於 0 的整數；目前 seed command 會準備 6 個商品，但若你自行加過資料，總數可能更高。

### 常見失敗

- `manage.py` 找不到：目前不在 repository root。
- `Address already in use`：已有 server 使用 8000；停止舊程序或暫用 `runserver 8001`。
- `no such table`：已 sync package，但尚未 `migrate`。
- 網頁沒有商品：尚未 `seed_demo`，或連到另一份 database。
- Python 版本不符：檢查 `.python-version`、uv 安裝與 `uv sync` 輸出。

### 完成檢查表

- [ ] 我能解釋 `.venv`、`pyproject.toml`、`uv.lock` 的差異。
- [ ] 我能說明 `uv sync`、`migrate`、`seed_demo`、`runserver` 各改變哪一層。
- [ ] 首頁可顯示 seeded 商品。
- [ ] 第二次 seed 不會無限新增重複資料。
- [ ] `manage.py check` 通過。

---

<a id="chapter-2"></a>
# 第 2 章｜Django 專案、HTTP、URL 與第一個 View

**相關投影片：第 22–45 頁**

## 觀念檢核答案

### 1. `/products/3/?q=django` 中，URLconf 主要比對哪一部分？

主要比對 path `/products/3/`。`?q=django` 是 query string，通常不參與 `path()` route matching，而由 View 透過 `request.GET` 讀取。

### 2. `path()` 的 route、view、name 各負責什麼？

```python
path("hello/", views.hello, name="hello")
```

- route `"hello/"`：描述可匹配的 path pattern。
- view `views.hello`：匹配後呼叫的 callable。
- name `"hello"`：讓 Python/template 可以反向產生 URL，不依賴硬寫 route。

### 3. `<int:pk>` 如何和 View 參數連接？

```python
path("products/<int:pk>/", views.product_detail, ...)

def product_detail(request, pk):
    ...
```

converter 先把匹配片段轉成 Python `int`，再以 keyword argument `pk=...` 傳入 View。兩邊名稱不一致會造成呼叫錯誤。

### 4. 為什麼 `HttpResponse(f"{name}")` 沒有 template autoescaping？

f-string 在 Python 中已把 value 插入 response body，沒有經過 template engine。Template autoescaping 只在 template rendering 的輸出流程中生效。動態 HTML 優先交給 template，或使用明確 escaping，不應把 raw interpolation 當成受保護。

### 5. 404 與 500 在這個流程通常表示什麼？

404 常表示 route/converter 沒匹配，或 detail object 不存在；500 表示 server-side 未處理 exception，例如 View import 錯誤、函式參數不一致、View 沒回 response。狀態碼先指出類型，traceback 才提供根因。

## 實作任務：重現並追蹤投影片的 `/hello/` 範例

### 目標

這是「重現投影片範例」而非未知解答：加入靜態文字 function view，從 root URL 追蹤到 app URL 與 View，並驗證 response status 與 reverse 結果。完成後要能不看程式碼畫出 request flow。

### 前置條件

- 第 1 章環境可正常啟動。
- 知道這是**教學用最小範例**，不是 LearnMart 產品功能。

### 影響檔案／符號

- `marketplace/views.py`：新增 `hello`
- `marketplace/urls.py`：新增 route name `hello`
- `config/urls.py`：只閱讀既有 `include("marketplace.urls")`，不需修改

### 步驟 1：新增 View

**修改前｜`marketplace/views.py` import 附近**

```python
from django.http import HttpResponseForbidden
```

**修改後｜只顯示焦點 excerpt**

```python
from django.http import HttpResponse, HttpResponseForbidden


def hello(request):
    return HttpResponse("Hello Django")
```

理由：此頁只需固定文字 response；固定內容不涉及把 user input 插入 HTML。

### 步驟 2：新增命名 route

**修改前｜`marketplace/urls.py`**

```python
urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
```

**修改後｜焦點 excerpt**

```python
urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
    path("hello/", views.hello, name="hello"),
```

理由：route 不以 `/` 開頭；完整路徑由 root URL 的空前綴與 `hello/` 組合。

### 步驟 3：啟動並觀察 request

```bash
uv run python manage.py runserver
```

瀏覽 `http://127.0.0.1:8000/hello/`。

你應該看到：

```text
Hello Django
```

終端機 request log 應含 `GET /hello/` 與 200。

### 步驟 4：驗證 reverse

```bash
uv run python manage.py shell -c \
  "from django.urls import reverse; print(reverse('marketplace:hello'))"
```

預期：

```text
/hello/
```

### 步驟 5：比較 converter 行為（可選）

可選步驟另外影響：

- `marketplace/views.py`：新增 `hello_name`
- `marketplace/urls.py`：新增 route name `hello-name`
- `templates/marketplace/hello.html`：新增 template

另加一個暫時 route：

```python
path("hello/<str:name>/", views.hello_name, name="hello-name")
```

請把動態 value 傳給 template，不要以 f-string 拼 HTML：

```python
def hello_name(request, name):
    return render(request, "marketplace/hello.html", {"name": name})
```

**新增｜`templates/marketplace/hello.html`**

```django
<p>歡迎 {{ name }} 來到 LearnMart</p>
```

輸入 HTML-looking 文字時應顯示為文字，而不是執行 tag/script。

### 常見失敗

- `AttributeError: module 'marketplace.views' has no attribute 'hello'`：route 已加，但函式名稱或檔案不一致。
- `NoReverseMatch`：忘了 namespace，應使用 `marketplace:hello`。
- 404：route 拼字、結尾 slash 或 root `include()` 流程不一致。
- `TypeError ... unexpected keyword argument`：converter 名稱與函式參數不一致。
- `NameError: HttpResponse`：忘記 import。

### 完成檢查表

- [ ] `/hello/` 回 200 與預期文字。
- [ ] `reverse("marketplace:hello")` 回 `/hello/`。
- [ ] 我能畫出 `config.urls → marketplace.urls → hello(request) → HttpResponse`。
- [ ] 我沒有把 user-controlled value 直接插入 raw HTML response。
- [ ] 練習完成後，我知道可移除暫時 route/view，不影響正式 catalog。

---

<a id="chapter-3"></a>
# 第 3 章｜Template、static 與響應式頁面

**相關投影片：第 46–72 頁**

## 觀念檢核答案

### 1. `render()` 的 template name 與 context 各扮演什麼角色？

Template name 是在設定好的 template search paths 中定位檔案的相對名稱；context 是 dict-like mapping，key 成為 template 可用的變數名。`render(request, name, context)` 讓 template engine 合成 HTML，再回傳 response。

### 2. `{{ }}`、`{% %}`、`{# #}` 有何不同？

- `{{ value }}`：求值並輸出，預設 autoescape。
- `{% tag %}`：流程或 template 指令，例如 `if`、`for`、`extends`、`url`。
- `{# comment #}`：template 註解，不輸出到 response。

### 3. `extends` 與 `include` 解決哪兩種重複？

`extends` 解決整頁共同骨架，例如 `<head>`、navbar、messages、main/footer；`include` 解決頁面局部片段，例如 pagination。Child template 覆寫 parent block；include 則在當前位置插入 partial。

### 4. 為什麼 `row-cols-md-3` 不是「只有 md 時三欄」？

Bootstrap 是 mobile-first，breakpoint class 從該寬度起持續生效，直到後續更大的 breakpoint 覆寫。因此 `row-cols-md-3` 表示 768px 以上三欄，不只介於 md 與 lg。

### 5. 為什麼 UI 隱藏按鈕不是 security？

Template 可以根據狀態不顯示控制項，但使用者仍可自行發 request。庫存、角色、ownership 等規則必須在 server-side View/Form/database 再驗證。UI 是 usability，不是可信任邊界。

## 實作任務：建立繼承版型的練習頁

### 目標

建立 `/practice/catalog/`，讓 View 傳 context 至 child template；頁面繼承 `base.html`，並追蹤 parent 如何透過 `{% static %}` 載入 `css/site.css`。同時練習命名 URL、loop/empty、responsive grid 與 autoescaping。

### 前置條件

- 第 2 章路由流程已理解。
- 不覆蓋目前 `marketplace:home`；使用獨立 practice route。

### 影響檔案／符號

- `marketplace/views.py`：新增 `catalog_practice`
- `marketplace/urls.py`：新增 `catalog-practice`
- `templates/marketplace/catalog_practice.html`：新增 template
- `static/css/site.css`：新增 `.practice-card` 的小幅樣式

### 步驟 1：準備固定 context

**修改前**

```python
# views.py 尚無 catalog_practice
```

**修改後｜教學用最小範例**

```python
def catalog_practice(request):
    products = [
        {"name": "Django 入門", "price": 680},
        {"name": "<strong>不是 HTML</strong>", "price": 520},
    ]
    return render(request, "marketplace/catalog_practice.html", {
        "products": products,
    })
```

第二筆名稱故意含 HTML-looking 文字，用來觀察 escaping；它不是惡意 payload 教學。

### 步驟 2：加入 URL

```python
path(
    "practice/catalog/",
    views.catalog_practice,
    name="catalog-practice",
),
```

驗證 reverse：

```bash
uv run python manage.py shell -c \
  "from django.urls import reverse; print(reverse('marketplace:catalog-practice'))"
```

預期 `/practice/catalog/`。

### 步驟 3：建立 child template

**新增｜`templates/marketplace/catalog_practice.html`**

```django
{% extends "base.html" %}

{% block content %}
<h1>Template 練習商品</h1>
<div class="row row-cols-1 row-cols-md-2 g-3">
  {% for product in products %}
    <div class="col"><article class="card practice-card h-100">
      <div class="card-body">
        <h2 class="h5">{{ product.name }}</h2>
        <p>NT$ {{ product.price }}</p>
      </div>
    </article></div>
  {% empty %}
    <p>目前沒有商品。</p>
  {% endfor %}
</div>
{% endblock %}
```

### 步驟 4：加入局部 CSS

**修改前｜`static/css/site.css`**

```css
.product-card { transition: transform .18s ease, box-shadow .18s ease; }
```

**修改後｜保留原規則，另加焦點規則**

```css
.practice-card { border-left: .35rem solid var(--lm-red); }
```

Child 沒有直接呼叫 `{% static %}`，所以不應留下未使用的 `{% load static %}`。請沿著實際繼承鏈追蹤：

```text
catalog_practice.html
→ extends templates/base.html
→ base.html: {% load static %}
→ {% static 'css/site.css' %}
→ browser requests /static/css/site.css
→ source file static/css/site.css
```

這證明 local CSS 是由 parent 載入，而不是 child 自動猜到檔案。

### 步驟 5：驗收 escaping 與 responsive 行為

開啟 `/practice/catalog/`：

- 第二筆應顯示字面 `<strong>不是 HTML</strong>`，而不是粗體。
- 手機寬度一欄，`md` 以上兩欄。
- View source 中應存在 card 結構與 local CSS link。
- 兩筆資料都由 `for` 產生，而非重複貼兩段 HTML。

### 常見失敗

- `TemplateDoesNotExist`：確認檔案位於 `templates/marketplace/` 且 template name 一致。
- `TemplateSyntaxError`：檢查 `{% endfor %}`、`{% endblock %}`。
- CSS 無效果：瀏覽器 Network 檢查 `/static/css/site.css`；再核對 class。
- `NoReverseMatch`：核對 `app_name = "marketplace"` 與 route name。
- HTML 被執行：檢查是否誤加 `|safe`；使用者內容不應這樣處理。

### 完成檢查表

- [ ] Practice page 繼承 `base.html`，沒有重複寫整份 HTML skeleton。
- [ ] Context key `products` 與 template loop 名稱一致。
- [ ] HTML-looking 名稱被顯示為文字。
- [ ] Grid 在不同 viewport 改變欄數。
- [ ] 我能說出 child → base.html → `{% static %}` → `/static/...` → source file 的完整鏈。

---

<a id="chapter-4"></a>
# 第 4 章｜Model、關聯與 migration

**相關投影片：第 73–101 頁**

## 觀念檢核答案

### 1. `blank=True` 與 `null=True` 分別作用在哪一層？

`blank=True` 主要表示 Django validation/form 層允許空白；`null=True` 表示 database column 可以存 SQL NULL。兩者可以一起使用，但不是同義詞。LearnMart 的 optional image 只需 `blank=True`；尚未出貨時間則需要 database NULL，因此 `shipped_at` 同時使用兩者。

### 2. `max_digits=10, decimal_places=0` 如何限制售價？

這是 Django field/validation 契約：總位數最多 10、小數點後 0 位，field conversion 在 Python 端使用 `Decimal`。它也影響 generated form 與 schema declaration；但 LearnMart 的 SQLite 不把這個 precision 當成獨立 database invariant。一般 `.save()` 不會自動 `full_clean()`，所以不能把參數誤解成所有寫入路徑都由 database 強制拒絕。

### 3. 為什麼 Product→Category 使用 `PROTECT`？

如果分類仍有商品，刪除分類會使商品失去必要分類。`PROTECT` 阻止這個刪除，要求管理者先重新分類或處理商品。這是 domain decision，不是所有 ForeignKey 的固定答案。

### 4. clone／取得既有 repository 與修改 model 的 migration 流程有何差異？

既有 repository 已提交 migration，因此 clone／取得後執行 `migrate` 即可。只有真的修改 model state，才執行 `makemigrations` 產生新的 migration，先閱讀 operations，再 `migrate` 套用。對完成版 source 執行 `makemigrations` 出現 `No changes detected` 是合理結果。

### 5. 為什麼自訂 User 要在初始 migration 前決定？

其他 models、admin、auth tables 與 migration dependencies 會參照 user model。後期替換涉及 schema、資料與 dependency 重建，遠比在第一次 migration 前設定 `AUTH_USER_MODEL` 困難。LearnMart 已從 `0001_initial` 使用 `marketplace.User`。

## 實作任務：為商品加入「精選」欄位

### 目標

在練習 branch 為 Product 新增 `is_featured`，產生並閱讀 migration，套用 database，最後在 admin 列表顯示。這個任務用來練習完整 model-change lifecycle，不要求把精選商品顯示到首頁。

### 前置條件

- Database 已套用目前 migration。
- 了解這會產生新的 migration file；若只是閱讀教材，不要在正式解答 branch 直接執行。

### 影響檔案／符號

- `marketplace/models.py`：`Product.is_featured`
- `marketplace/migrations/0002_*.py`：`AddField` operation（實際序號依 branch 而異）
- `marketplace/admin.py`：`ProductAdmin.list_display`、`list_filter`
- 本機 `db.sqlite3` schema

### 概念產出：先畫 relation graph

在改 schema 前，畫出 `Category → Product → seller` 與 `OrderItem → Product/seller`，標示正向 accessor、`related_name` 與 `PROTECT`。特別註記：刪 seller 雖會沿 Product.seller 的 `CASCADE` 嘗試刪商品，但歷史 `OrderItem` 的 protected product/seller references 可阻止整次 deletion。

### 步驟 1：修改 Model

**修改前｜`Product` 焦點 excerpt**

```python
stock = models.PositiveIntegerField("庫存", default=0)
is_active = models.BooleanField("上架", default=True)
```

**修改後**

```python
stock = models.PositiveIntegerField("庫存", default=0)
is_active = models.BooleanField("上架", default=True)
is_featured = models.BooleanField("精選商品", default=False)
```

理由：對既有 rows 提供 `default=False`，migration 可為舊資料建立明確值。BooleanField 在包含此 field 的 admin／form 中可形成 checkbox；但目前 `ProductForm.Meta.fields` **沒有** `is_featured`，所以本 lab 只修改 admin，不會讓商城新增／編輯表單自動出現該欄位。

### 步驟 2：產生 migration

```bash
uv run python manage.py makemigrations marketplace \
  --name add_product_featured
```

預期產生類似：

```text
marketplace/migrations/0002_add_product_featured.py
  + Add field is_featured to product
```

打開 migration，焦點應類似：

```python
migrations.AddField(
    model_name="product",
    name="is_featured",
    field=models.BooleanField(default=False, verbose_name="精選商品"),
)
```

不要只看到檔名就直接套用；確認 model/field/default 都正確。

### 步驟 3：套用與檢查

```bash
uv run python manage.py migrate
uv run python manage.py showmigrations marketplace
```

預期新 migration 前出現 `[X]`。

在 shell 驗證舊商品預設值：

```bash
uv run python manage.py shell -c \
  "from marketplace.models import Product; print(Product.objects.filter(is_featured=True).count())"
```

若尚未標記任何商品，應為 `0`。

### 步驟 4：讓 Admin 可觀察

**修改前｜`ProductAdmin` 焦點 excerpt**

```python
list_display = (
    "name", "category", "seller", "price", "stock", "is_active",
)
list_filter = ("category", "is_active")
```

**修改後**

```python
list_display = (
    "name", "category", "seller", "price", "stock",
    "is_active", "is_featured",
)
list_filter = ("category", "is_active", "is_featured")
```

Admin configuration 不需 migration，因為它不改 schema。接著建立或使用 admin-capable account 並實際觀察：

```bash
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

1. 開啟 `/admin/marketplace/product/`。
2. 確認列表出現「精選商品」欄與 sidebar filter。
3. 把一件商品標記為 featured。
4. 套用 filter，確認只留下該商品。

Seeded seller/buyer 不是 superuser，不能取代此步驟。

### 步驟 5：驗證沒有 migration drift

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
```

兩者應成功；第二行不應再產生未提交 migration。

### 常見失敗

- `no such column ... is_featured`：model 已改但未 `migrate`。
- `makemigrations` 顯示 no changes：檔案未儲存、改錯 model，或 migration 已存在。
- Migration 要求 non-null default：新增必填欄位到既有 table 卻沒提供資料策略。
- Admin 看不到欄位：只改 model，未改 `list_display`；或 server 尚未 reload。
- 直接刪 migration file：database migration history 已套用時會不一致；應先了解 rollback/rebuild 策略。

### 完成檢查表

- [ ] 我畫出 relation graph，並標示 `CASCADE` 可能被歷史 `PROTECT` 阻止。
- [ ] Model field 有明確型別、label 與舊資料 default。
- [ ] 我已閱讀 migration operation，而不只執行命令。
- [ ] `showmigrations` 顯示新 migration 已套用。
- [ ] 我用 superuser 在 admin 實際顯示、標記並篩選精選狀態。
- [ ] 我確認目前 `ProductForm` 不會顯示 `is_featured`。
- [ ] `makemigrations --check` 通過。

---

<a id="chapter-5"></a>
# 第 5 章｜ORM、QuerySet 與資料規則

**相關投影片：第 102–126 頁**

## 觀念檢核答案

### 1. Manager、QuerySet、model instance 各能做什麼？

`Product.objects` 是 manager，提供建立初始 query 的入口；`Product.objects.filter(...)` 回 QuerySet，代表 0 到多筆的可組合 lazy query。`get()` 成功時回一個 instance，0／多筆會拋例外；`first()` 回第一個 instance，但空 QuerySet 會回 `None`。取得 instance 後才能直接讀 `product.name`、修改 attribute、呼叫 `save()`。

### 2. `get()` 找不到與 `filter()` 找不到時有何差異？

`get()` 期待恰好一筆，找不到會拋 `DoesNotExist`；`filter()` 永遠回 QuerySet，找不到就是空 QuerySet。若條件本來就可能多筆，使用 `filter()`；若由 unique/pk 契約保證單筆，可使用 `get()` 並處理例外。

### 3. `select_related` 與 `prefetch_related` 適合什麼 relation？

`select_related` 適合 ForeignKey/OneToOne 等單值 relation，通常透過 SQL JOIN 一起取回；`prefetch_related` 適合 reverse ForeignKey/ManyToMany 等多值 relation，通常先做額外 queries，再於 Python 配對。選擇前先看 template/View 實際會讀哪些 relation。

### 4. 列表顯示每件平均評分時，為何考慮 `annotate()`？

如果每個 product 都呼叫 `average_rating` property，可能每件商品各執行一次 aggregate query，造成 N+1 類型成本。`annotate(avg_rating=Avg("reviews__rating"))` 可讓一個 QuerySet 對每列帶計算值。`aggregate()` 則只回整個集合的一份摘要，形狀不同。

### 5. Validator 與 database constraint 有何差異？

Validator 在 form/model validation 流程檢查，例如 rating 1–5；database constraint 在寫入資料庫時維持資料不變量，例如同一 product/author 不可重複。一般 instance `.save()` 不保證自動呼叫 `full_clean()`，所以不能把 validator 當成所有寫入路徑的 database guarantee。

## 實作任務：在 shell 完成可回復的 ORM 探索

### 目標

建立一筆暫時商品，完成 CRUD、lookup、relation traversal、`Q` 查詢、aggregate/annotate 與 optimized queryset，最後刪除練習資料，讓 database 回到開始狀態。

### 前置條件

- 已執行 `seed_demo`。
- 若你完成第 4 章 `is_featured` 練習，本章不依賴該欄位。

### 影響檔案／符號

本章不修改 source files；只暫時改變本機 database rows。使用：

- `Product.objects`
- `Category.objects`
- `User.objects`
- `Q`、`Avg`
- `Product.seller`／`seller.products`

### 焦點前後對照

**建立前**

```python
Product.objects.filter(name="ORM 練習商品").exists()
# False
```

**探索中**

```python
practice = Product.objects.create(...)
practice.pk
# 一個整數 primary key
```

**清理後**

```python
Product.objects.filter(name="ORM 練習商品").exists()
# False
```

### 步驟 1：進入 Django shell

```bash
uv run python manage.py shell
```

匯入：

```python
from django.db import connection
from django.db.models import Avg, Q
from django.test.utils import CaptureQueriesContext
from marketplace.models import Category, Product, User
```

### 步驟 2：取得必要關聯並建立 instance

```python
seller = User.objects.get(username="seller")
category = Category.objects.get(slug="tech")

practice = Product.objects.create(
    seller=seller,
    category=category,
    name="ORM 練習商品",
    description="只存在於本機練習",
    price=1234,
    stock=2,
)
```

驗證：

```python
practice.pk is not None
practice.seller.username
seller.products.filter(pk=practice.pk).exists()
```

三個結果應為 `True`、`seller`、`True`。

### 步驟 3：Read 與 lookup

```python
Product.objects.get(pk=practice.pk)
Product.objects.filter(name__icontains="ORM")
Product.objects.filter(price__lte=1500, stock__gt=0)
Product.objects.filter(category__slug=category.slug)
```

觀察每個 expression 是 instance 還是 QuerySet：

```python
type(Product.objects.get(pk=practice.pk))
type(Product.objects.filter(pk=practice.pk))
```

### 步驟 4：使用 `Q` 組 OR

```python
matched = Product.objects.filter(
    Q(name__icontains="ORM") |
    Q(description__icontains="本機")
)
list(matched.values_list("name", flat=True))
```

結果應包含 `ORM 練習商品`。

### 步驟 5：Update 並從 database 重新讀取

```python
practice.stock = 7
practice.save(update_fields=["stock"])
practice.refresh_from_db()
practice.stock
```

預期 `7`。`refresh_from_db()` 用來確認不是只改到記憶體。因為 `update_fields` 只有 `stock`，本次不會更新 `updated_at`；`auto_now` 只有在該 field 參與 `Model.save()` 寫入時才生效。

### 步驟 6：比較 aggregate 與 annotate

```python
Product.objects.aggregate(avg_price=Avg("price"))
```

回傳 dict，例如 `{"avg_price": Decimal(...)}`。

```python
rated = Product.objects.annotate(avg_rating=Avg("reviews__rating"))
[(p.name, p.avg_rating) for p in rated[:3]]
```

回傳 Product instances，每個多一個 `avg_rating` attribute；無評價時可為 `None`。

### 步驟 7：讓 N+1 與 optimization 變成可觀察數字

每次都建立 fresh QuerySet；不要重用已 evaluation 的結果：

```python
with CaptureQueriesContext(connection) as baseline:
    for item in Product.objects.order_by("pk")[:3]:
        print(item.name, item.category.name, item.seller.username)
len(baseline)
```

接著比較：

```python
with CaptureQueriesContext(connection) as optimized:
    products = Product.objects.order_by("pk").select_related(
        "category", "seller",
    )[:3]
    for item in products:
        print(item.name, item.category.name, item.seller.username)
len(optimized)
```

兩次畫面文字相同，但有三件商品時 baseline 通常是 1 次商品 query 加 relation queries；optimized consumption 應為 1 次 query。實際數字取決於資料筆數，因此要記錄兩邊結果，而不是背固定 baseline。

### 步驟 8：刪除練習資料

```python
practice.delete()
Product.objects.filter(name="ORM 練習商品").exists()
```

預期 `False`。最後輸入 `exit()`。

### 常見失敗

- `DoesNotExist`：seed 尚未建立 seller，或 username 不一致。
- `AttributeError: 'QuerySet' object has no attribute 'name'`：把多筆 QuerySet 當單一 instance。
- `MultipleObjectsReturned`：用 `get()` 查非唯一條件。
- `IntegrityError`：必要 ForeignKey/constraint 沒滿足。
- 刪除失敗：後續已建立受 `PROTECT` 保護的關聯；先檢查引用資料，不要強制刪除。

### 完成檢查表

- [ ] 我能在每一步辨認 manager、QuerySet 或 instance。
- [ ] 我完成正向與反向 relation traversal。
- [ ] 我能解釋 `Q(... ) | Q(...)`。
- [ ] 我能說出 `aggregate` 與 `annotate` 的回傳形狀。
- [ ] 我記錄 baseline 與 `select_related()` 的 query count，且 optimized consumption 為 1 次。
- [ ] 練習商品已清理，database 回到開始狀態。

---

<a id="chapter-6"></a>
# 第 6 章｜組合成可搜尋的資料驅動商品目錄

**相關投影片：第 127–151 頁；第 152–153 頁為 Deck 總結與銜接**

## 觀念檢核答案

### 1. GET form 的 `name="q"` 如何一路變成 ORM filter？

瀏覽器把 input 的 name/value 編碼為 `?q=...`；Django 由 `request.GET.get("q", "")` 讀值；View 經 `.strip()` 後，把 value 傳入 `Q(name__icontains=query) | Q(description__icontains=query)`；QuerySet 在評估時執行 database query；結果透過 context key `products` 被 template loop 顯示。

### 2. 搜尋＋分類＋分頁時，為什麼要保留多個 query parameters？

它們共同描述目前 catalog state。若 pagination link 只帶 `page=2`，q/category 會消失；若 category link 不帶 q，切分類會丟失搜尋。每個產生新 URL 的控制項都要明確決定哪些 state 應保留、哪些應重設。

### 3. 商品卡讀 category/seller 時，為何使用 `select_related`？

每個 product 的 category 與 seller 都是單值 ForeignKey。若未預先載入，template 逐卡讀 relation 可能造成一筆 catalog query 加上多筆 relation queries。`select_related("category", "seller")` 通常用 JOIN 一次取回所需單值關聯。

### 4. 空 QuerySet 為什麼通常回 200 而不是 404？

列表查詢成功，只是結果集合長度為 0；這是正常 domain/UI state，應顯示 `{% empty %}`。Detail URL 期待特定單一物件，找不到才通常回 404。

### 5. 為什麼低庫存 filter 要由 server 定義規則？

使用者可選擇是否開啟 filter，但「低庫存是多少」及可查哪些欄位應由 application 定義。不要讓 query string 直接變成任意 ORM field/operator。固定 allowlisted parameter `low_stock=1` 與固定 `stock__lte=5` 比動態拼查詢安全且可測試。

## 實作任務：增加「只看低庫存」GET filter

### 目標

為 catalog 增加 `low_stock=1`，定義低庫存為 5 件以下；與 q/category 同時組合，所有 relevant links 保留狀態，空結果有正常訊息，並加一個 focused test。

### 前置條件

- 目前 `ProductListView`、`home.html`、`pagination.html` 尚未加入此功能。
- 理解這是 workbook exercise，不是 checked-in LearnMart 現況。

### 影響檔案／符號

- `marketplace/views.py`
  - `ProductListView.get_queryset`
  - `ProductListView.get_context_data`
- `templates/marketplace/home.html`
  - category/filter links
- `templates/marketplace/pagination.html`
  - previous/next links
- `templates/base.html`
  - global search form 的 hidden state（建議）
- `marketplace/tests.py`
  - `MarketplaceFlowTests.test_low_stock_filter`

### 步驟 1：讀取 allowlisted flag 並套用固定 filter

**修改前｜`get_queryset()` 焦點 excerpt**

```python
query = self.request.GET.get("q", "").strip()
category = self.request.GET.get("category", "").strip()
if query:
    queryset = queryset.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
if category:
    queryset = queryset.filter(category__slug=category)
```

**修改後**

```python
query = self.request.GET.get("q", "").strip()
category = self.request.GET.get("category", "").strip()
low_stock = self.request.GET.get("low_stock") == "1"
if query:
    queryset = queryset.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
if category:
    queryset = queryset.filter(category__slug=category)
if low_stock:
    queryset = queryset.filter(stock__lte=5)
```

理由：外部只能選擇開／關；field、lookup 與 threshold 都由 server 擁有。

### 步驟 2：刻意改善 q/category UI state，再加入 Boolean flag

**目前 source｜`get_context_data()` 讀 raw values**

```python
context["query"] = self.request.GET.get("q", "")
context["selected_category"] = self.request.GET.get("category", "")
```

**修改後｜intentional improvement**

```python
context["query"] = self.request.GET.get("q", "").strip()
context["selected_category"] = self.request.GET.get(
    "category", "",
).strip()
context["low_stock"] = self.request.GET.get("low_stock") == "1"
```

現在 filter 與 UI 使用相同 stripped q/category；`low_stock` 則先正規化為 Boolean，template 不必重解釋任意字串。

### 步驟 3：用 `{% querystring %}` 建立低庫存切換

`request` context processor 已啟用；Django 6.1.1 的 tag 可保留目前參數並只改指定 keys。

```django
{% if low_stock %}
  <a class="btn btn-warning"
     href="{% querystring low_stock=None page=None %}">
    顯示全部庫存
  </a>
{% else %}
  <a class="btn btn-outline-warning"
     href="{% querystring low_stock='1' page=None %}">
    只看低庫存
  </a>
{% endif %}
```

切換 filter 時移除 `page`，回到新結果的第 1 頁；q/category 由 tag 自動保留。

### 步驟 4：分類 controls 保留 q/low_stock、重設 page

**修改後｜category 與「全部」links**

```django
<a href="{% querystring category=category.slug page=None %}">
  {{ category.name }}
</a>

<a href="{% querystring category=None page=None %}">
  全部
</a>
```

這避免手動判斷第一個參數該用 `?` 還是 `&`；也不會產生 `/&low_stock=1` 這種被當成 path 的錯誤 URL。

### 步驟 5：global search form 明確保留 category/low_stock

目前 form 只提交 q，所以 category 原本會被重設。以下是本 lab 的 intentional improvement：

```django
<input name="q" value="{{ query }}" placeholder="搜尋商品">
{% if selected_category %}
  <input type="hidden" name="category" value="{{ selected_category }}">
{% endif %}
{% if low_stock %}
  <input type="hidden" name="low_stock" value="1">
{% endif %}
```

Form 沒有 `page` input，因此新搜尋自然回第 1 頁。Hidden input 只保留 UI state，不是 security control；server 仍需 allowlist 與驗證。

### 步驟 6：讓共享 pagination partial 泛用地保留 query state

**修改前｜partial 硬寫 catalog-specific keys**

```django
href="?page={{ page_obj.previous_page_number }}&q={{ query|urlencode }}&category={{ selected_category }}"
```

**修改後｜previous 與 next 的焦點 excerpts**

```django
href="{% querystring page=page_obj.previous_page_number %}"
href="{% querystring page=page_obj.next_page_number %}"
```

`querystring` 只替換 page，會保留 q/category/low_stock。它也讓同一 partial 被 board list 使用時不必認識 catalog-only context names。

### 步驟 7：加入 deterministic focused test

同一個 test 固定三種 acceptance：stock boundary、超過一頁時的 state retention，以及保證為零筆的 empty state。

```python
def test_low_stock_filter(self):
    Product.objects.create(
        seller=self.seller,
        category=self.product.category,
        name="高庫存商品",
        description="不應出現在低庫存結果",
        price=500,
        stock=20,
    )
    response = self.client.get(
        reverse("marketplace:home"), {"low_stock": "1"}
    )
    self.assertContains(response, "教學鍵盤")  # stock == 5
    self.assertNotContains(response, "高庫存商品")
```

接著在同一 test 中建立**恰好 13 筆**同時符合 q/category/low_stock 的商品，強制產生第 2 頁：

```python
    for index in range(13):
        Product.objects.create(
            seller=self.seller,
            category=self.product.category,
            name=f"paged item {index}",
            description="pagination acceptance",
            price=100,
            stock=5,
        )
    page_two = self.client.get(reverse("marketplace:home"), {
        "q": "paged", "category": "3c",
        "low_stock": "1", "page": "2",
    })
    self.assertEqual(page_two.status_code, 200)
    self.assertEqual(page_two.context["page_obj"].number, 2)
    self.assertEqual(page_two.context["page_obj"].paginator.count, 13)
    self.assertEqual(len(page_two.context["products"]), 1)
    self.assertContains(page_two, "q=paged")
    self.assertContains(page_two, "category=3c")
    self.assertContains(page_two, "low_stock=1")
```

最後使用不可能命中的字串，固定 status 與**目前實際 empty-state text**：

```python
    empty = self.client.get(reverse("marketplace:home"), {
        "q": "guaranteed-zero-result-9f7c",
        "low_stock": "1",
    })
    self.assertEqual(empty.status_code, 200)
    self.assertEqual(empty.context["page_obj"].paginator.count, 0)
    self.assertContains(empty, "目前找不到符合條件的商品。")
```

`setUp()` 的 test category slug 是 `3c`；這裡測的是 test database，不是 `seed_demo` 的手動 URL。

### 步驟 8：準備 seeded manual boundary data，再驗收

Fresh seed 的最低庫存是 8，不會產生 positive low-stock result。先記下「教學用機械鍵盤」原庫存（fresh seed 為 20），暫時改成 5：

```bash
uv run python manage.py shell -c \
  "from marketplace.models import Product; p=Product.objects.get(name='教學用機械鍵盤'); print('原庫存', p.stock); p.stock=5; p.save(update_fields=['stock'])"
```

檢查：

```text
/?low_stock=1
→ 應包含「教學用機械鍵盤」，排除高庫存商品

/?q=鍵盤&category=tech&low_stock=1
→ 應包含「教學用機械鍵盤」
```

自動驗收：

```bash
uv run python manage.py test \
  "marketplace.tests.MarketplaceFlowTests.test_low_stock_filter"
```

最後以 admin 或 shell 把商品恢復成先前記錄的 stock。Focused test 會建立 13 筆 matching rows，保證存在 page 2，並確認 next/previous links 保留 q/category/low_stock；手動驗收時不要把不存在的 `page=2` 當成功條件。

### 常見失敗

- 任何非空字串都被當 True：使用 `bool(request.GET.get(...))` 會把 `"0"` 也當 True；本練習明確比較 `== "1"`。
- 切分類後低庫存消失：category href 忘記帶 flag。
- 搜尋後條件消失：global search form 沒有 hidden inputs。
- 翻頁後回到全部商品：pagination href 未保留 state。
- Template 直接做複雜字串解析：應在 View 正規化成 Boolean。
- 動態使用使用者傳入的 field name：不應寫成 `filter(**{request.GET["field"]: ...})` 而沒有 allowlist。

### 完成檢查表

- [ ] `low_stock=1` 只顯示 stock ≤ 5 的 active products。
- [ ] Boundary assertions 證明 stock=5 被包含、stock=20 被排除。
- [ ] 13 筆 matching products 保證形成 page 2，且 response 保留 q/category/low_stock。
- [ ] Guaranteed-zero request 回 200，並顯示「目前找不到符合條件的商品。」。
- [ ] Category、search、pagination controls 遵守預期的 reset／retention contract。
- [ ] Quoted focused test command 與完整 `uv run python manage.py test` 都通過。

---

# Deck 1 完成後的自我說明題

請不用看投影片，口頭或書面完成以下敘述：

1. `uv sync` 到首頁出現商品，中間至少經過哪些可獨立失敗的層？
2. 一個 `GET /?q=鍵盤` 如何從 URLconf 進入 View，再由 QuerySet 與 Template 形成 HTML？
3. 為什麼 migration file、database schema 與目前 `models.py` 是三個相關但不同的狀態？
4. 商品卡讀 `product.category.name` 時，如何由 model relation 推導適合的 ORM optimization？
5. 哪些資料是外部輸入？哪些規則必須由 server 擁有？

能清楚回答這五題，才進入 Deck 2 的 POST、Form、authentication、ownership、transaction 與 testing。
