---
marp: true
theme: default
size: 16:9
paginate: true
header: "Django 01｜共通基礎：LearnBoard × LearnMart"
footer: "初學者教材｜共通觀念 → 兩個專案對照"
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
  h1 { color: #8f1d2c; }
  h2 { color: #a52a3a; }
  blockquote {
    border-left: 6px solid #d69aa3; padding-left: 18px; color: #4c3438;
    font-family: 'Noto Serif CJK TC', 'Noto Sans CJK TC', 'WenQuanYi Zen Hei', serif;
  }
  code, kbd {
    font-family: 'Noto Sans Mono CJK TC', 'SF Mono', Consolas,
                 'WenQuanYi Zen Hei Mono', 'Courier New', monospace;
    font-size: 0.92em;
  }
  pre { font-size: 0.72em; line-height: 1.28; }
  table { font-size: 0.78em; }
  strong { color: #7d1726; }
---

# 第 2 章
## Django 專案、HTTP、URL 與第一個 View

**本章成果：**能沿著檔案與函式追蹤一個網址，直到 Django 回傳 response。

<!--
授課提示：全冊地基章。若進度落後，優先保 2-6～2-17，App 註冊細節可往後壓縮。
-->

---

## 2-1 「整個專案」與 Django Project package

日常語言的「專案」可能指整個 repository；Django 指令中的 Project 則是設定與入口 package。

```text
learnmart/             整個 repository
├── config/            Django project package
├── marketplace/       Django app
├── templates/
├── static/
└── manage.py
```

- `config`：settings、根 URL、WSGI/ASGI
- `marketplace`：商城領域的 model、view、form、URL、admin、tests

App 不必硬拆成微服務；它首先是 Django 專案內聚合相關功能的模組。

---

## 2-2 建立指令是「歷史」，不要重跑

本 repository 已經建立完成。最初可能使用：

```bash
uv run django-admin startproject config .
uv run python manage.py startapp marketplace
```

- `startproject config .`：在目前目錄建立 `config/` 與 `manage.py`
- 最後的 `.` 是目的地
- `startapp marketplace`：建立 App 的基本檔案
- `startapp` **不會自動建立 `marketplace/urls.py`**，通常要自行新增

在現有資料夾重跑建立指令可能覆蓋或混淆檔案。

---

## 2-2A 建立指令產生哪些檔案？

**教學用最小檔案地圖｜generated skeleton**

```text
config/
├── __init__.py
├── settings.py     專案設定
├── urls.py         root URLconf
├── asgi.py         ASGI server 入口
└── wsgi.py         WSGI server 入口
marketplace/
├── admin.py        admin 註冊
├── apps.py         app 設定
├── migrations/    schema 版本史
├── models.py       資料模型
├── tests.py        tests
└── views.py        request handlers
```

`startapp` 不會生成 `urls.py`、`forms.py` 或 templates；LearnMart 是後續依需求自行加入。

---

## 2-3 `manage.py` 是專案命令入口

**目前 LearnMart 節錄｜`manage.py` 的核心責任**

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
execute_from_command_line(sys.argv)
```

- 指定 settings module 為 `config.settings`
- 把終端機參數交給 Django command 系統
- 因此 `runserver`、`migrate`、`test` 都知道要使用哪個專案設定

常見形式：

```bash
uv run python manage.py <command> [options]
```

---

## 2-4 settings 是普通 Python 設定值

**目前 LearnMart 節錄｜`config/settings.py` 節錄**

```python
INSTALLED_APPS = [
    # Django 內建 apps ...
    "marketplace",
]

ROOT_URLCONF = "config.urls"
LANGUAGE_CODE = "zh-hant"
TIME_ZONE = "Asia/Taipei"
```

這些不是特殊設定語言，而是 Python 變數、list 與字串。Django 啟動時載入它們。

本章先知道位置與用途；template、static/media 會在使用時再深入。

---

## 2-4A 目前資料庫：SQLite 檔案與使用邊界

**目前 LearnMart 節錄｜`config/settings.py` 的 `DATABASES`**

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

- SQLite 把本機 database 放在 repository root 的 `db.sqlite3`
- `migrate` 改 schema；`seed_demo` 改 rows，兩者不是 package installation
- **目前 LearnMart 實作：**適合單機課堂與小型練習
- **補充／進階：**production 常改用獨立 database server、備份、權限與監控；不能只複製本機檔案設定

---

## 2-5 App 註冊與 template 搜尋不是同一件事

**目前 LearnMart 節錄｜`config/settings.py`**

```python
TEMPLATES = [{
    "DIRS": [BASE_DIR / "templates"],
    "APP_DIRS": True,
    # ...
}]
```

- `DIRS`：直接搜尋 repository 根目錄的 `templates/`
- `APP_DIRS=True`：也搜尋已安裝 App 內的 `templates/`
- `INSTALLED_APPS` 影響 App/model/admin 等發現機制

因此，少了 `marketplace` 註冊會造成許多問題，但不能一概說「根目錄 templates 一定找不到」。

---

## 2-6 HTTP：瀏覽器與伺服器的訊息交換

瀏覽器送出 **request**，Django 回傳 **response**：

```text
Browser -- request --> Django
Browser <-- response -- Django
```

Request 常見部分：

- method：GET、POST…
- path：例如 `/products/3/`
- query string：例如 `?q=鍵盤`
- headers、body、登入資訊

Response 常見部分：status、headers、body。HTML 只是 body 的一種內容。

<!--
授課提示：live demo：curl -i http://127.0.0.1:8000/hello/ 展示原始 response headers，把抽象的 request/response 變成看得見的文字。
-->

---

## 2-7 用一個 request 拆解網址

```text
http://127.0.0.1:8000/products/3/?from=home
```

| 部分 | 值 |
|---|---|
| scheme | `http` |
| host | `127.0.0.1` |
| port | `8000` |
| path | `/products/3/` |
| query string | `from=home` |

URLconf 主要比對 path；query string 通常在 View 透過 `request.GET` 讀取。

---

## 2-8 常見 response status

| 狀態 | 初學者可先這樣理解 |
|---|---|
| 200 | 成功取得內容 |
| 302 | 請瀏覽器再到另一個網址 |
| 403 | 已理解請求，但沒有權限 |
| 404 | 找不到符合的路由或物件 |
| 500 | 伺服器執行時發生未處理錯誤 |

狀態碼不是完整錯誤原因，但能先判斷問題在哪一層。

---

## 2-9 第一個 Function View

**教學用最小範例｜`marketplace/views.py`**

```python
from django.http import HttpResponse


def hello(request):
    return HttpResponse("Hello Django")
```

- Django 呼叫 View 時傳入 `request`
- View 是 callable；function 就是一種 callable
- View 必須回傳 response object
- `HttpResponse(...)` 把字串放進 response body

目前 LearnMart 沒有 `hello` view；它只用來隔離最小概念。

---

## 2-10 `path()` 四個重要位置

**教學用最小範例｜`marketplace/urls.py`**

```python
from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.hello, name="hello"),
]
```

1. `"hello/"`：要比對的 route，不以 `/` 開頭
2. `views.hello`：匹配後呼叫的 callable
3. 可選 extra kwargs：本例未使用
4. `name="hello"`：反向產生 URL 時使用的名稱

---

## 2-11 Project URL 如何交給 App URL？

**目前 LearnMart 節錄｜`config/urls.py` 節錄**

```python
from django.urls import include, path

urlpatterns = [
    path("", include("marketplace.urls")),
]
```

空字串 `""` 表示從網站根路徑開始交給 App。

若瀏覽器請求 `/hello/`：

1. `config.urls` 匹配空前綴
2. `include()` 把剩餘的 `hello/` 交給 `marketplace.urls`
3. App URL 找到 `views.hello`

<!--
授課提示：白板畫 config → marketplace 兩層轉交圖。最常見的錯是把 name 寫在根路由，務必點名此坑。
-->

---

## 2-12 動態路徑：converter 與函式參數要相同

**教學用最小範例**

```python
# marketplace/urls.py
path("hello/<str:name>/", views.hello_name, name="hello-name")

# marketplace/views.py
def hello_name(request, name):
    return HttpResponse(f"歡迎 {name}")
```

`<str:name>` 做兩件事：

- 只匹配非空、且不含 `/` 的字串片段
- 以 keyword argument `name=...` 傳給 View

converter 變數名與函式參數名必須對得上。

<!--
授課提示：快問：GET /products/abc/ 時 <int:pk> 會怎樣？（不匹配 → 404）答對代表 converter 觀念成立。
-->

---

## 2-13 常用 converter 不必一次背完

| converter | 匹配結果 | 常見用途 |
|---|---|---|
| `<int:pk>` | 非負十進位整數（包含 0），傳入 Python `int` | 物件主鍵 |
| `<str:name>` | 非空且不含 `/` 的字串 | 短文字 |
| `<slug:slug>` | 字母、數字、`-`、`_` | 可讀網址代稱 |
| `<path:value>` | 可含 `/` | 子路徑 |

LearnMart 主要使用 `<int:pk>`，例如：

```python
path("products/<int:pk>/", views.ProductDetailView.as_view(),
     name="product-detail")
```

Class-based View 會在下一份教材完整解釋。

---

## 2-14 命名 URL：不要把路徑散落各處

**目前 LearnMart 節錄｜`marketplace/urls.py`**

```python
app_name = "marketplace"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
]
```

完整名稱是 `marketplace:home`：

- `marketplace`：namespace，由 `app_name` 提供
- `home`：單一路由名稱

改動 route 字串時，只要名稱不變，其他程式可繼續反向解析。

---

## 2-15 在 Python 與 template 反向產生 URL

```python
from django.urls import reverse

reverse("marketplace:home")
# 回傳 "/"
```

```django
<a href="{% url 'marketplace:home' %}">首頁</a>
```

有參數時也要提供：

```django
{% url 'marketplace:product-detail' product.pk %}
```

反向解析的核心是「名稱＋必要參數」，不是手寫 `/products/.../`。

---

## 2-16 原始 `HttpResponse` 不會套 template escaping

危險的誤解：

```python
def hello_name(request, name):
    return HttpResponse(f"歡迎 {name}")
```

若 `name` 來自使用者，f-string 已先把文字直接插入 body；Django template engine 根本沒有參與，因此**沒有自動 escaping**。

初學階段的安全方向：

- 動態 HTML 優先交給 template 顯示
- 或使用明確 escaping 工具
- 不要把「Django 預設 escape」誤套到所有 `HttpResponse`

---

## 2-17 一次最小 request 的旅程

```text
GET /hello/
   │
   ▼
config/urls.py
   │ include("marketplace.urls")
   ▼
marketplace/urls.py
   │ path("hello/", views.hello, ...)
   ▼
marketplace/views.py
   │ hello(request)
   ▼
HttpResponse("Hello Django") → 200
```

這個流程沒有 Model，也沒有 Template。MVT 是常見完整流程，不代表每個 View 都必須使用所有層。

<!--
授課提示：配合下一頁 2-17A 圖解使用。先帶文字流程，再用圖做隨堂指認，兩種表徵互相強化。
-->

---

## 2-17A 圖解：一次 request 的旅程

![w:1020](../assets/request_flow.svg)

<!--
授課提示：用此圖做隨堂快問——指著任一箭頭請學生說出「輸入什麼、輸出什麼、對應哪個檔案」。商品詳情版（/products/3/）比 /hello/ 多了 Model 與 Template 兩步，可預告第 3～4 章會逐格補齊。建議停留 2 分鐘。
-->

---

## 2-18 404 與 500 怎麼分辨？

### 404 常見原因
- path 拼錯或沒有匹配路由
- 忘記 `include()`
- converter 不接受輸入，例如 `<int:pk>` 卻傳文字
- Detail View 找不到符合物件

### 500 常見原因
- import、語法或執行期例外
- View 沒回傳 response
- template 或資料存取發生未處理錯誤

開發模式的 traceback 是除錯線索；正式環境不可公開。

---

## 2-19 settings 的開發邊界

**目前 LearnMart 節錄｜`config/settings.py`**

```python
SECRET_KEY = "django-insecure-learnmart-classroom-only-change-in-production"
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
```

- 這是課堂本機設定，不是 production baseline
- `DEBUG=True` 顯示詳細錯誤，可能洩漏資訊
- `SECRET_KEY` 正式環境必須外部化並保密
- `ALLOWED_HOSTS` 控制可接受的 Host header

本教材先辨識邊界；完整部署不在本份範圍。

---

## 第 2 章｜觀念檢核與實作

1. `/products/3/?q=django` 中，URLconf 主要比對哪一部分？
2. `path()` 的 route、view、name 各負責什麼？
3. `<int:pk>` 如何和 View 參數連接？
4. 為什麼 `HttpResponse(f"{name}")` 不會自動套 template escaping？
5. 404 與 500 在這條 request flow 通常代表什麼？

**實作任務：**建立或追蹤一個命名路由，畫出 root URL → app URL → View → response，並確認 200 與 reverse 結果。

**配套實作手冊：**LearnMart [第 2 章](../workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md#chapter-2)；LearnBoard [第 2 章](../workbooks/learnboard_01_django_foundations_and_message_board_workbook.md#chapter-2)

<!--
授課提示：第 3、4 題最容易暴露「背路徑而不理解」；請學生畫 request flow 圖代替文字回答。
-->
