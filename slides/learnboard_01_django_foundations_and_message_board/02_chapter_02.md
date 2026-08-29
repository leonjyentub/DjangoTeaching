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

# 第 2 章
## Django 專案、HTTP、URL 與第一個 View

**本章成果：**能說明一次 HTTP request 如何被路由到 view function 並回傳 response。

<!--
授課提示：本章建立全課程的心智模型。之後所有「網頁怎麼跑出來」的問題，都回到 2-17 的旅程圖。
-->

---

## 2-1 「整個專案」與 Project package

一個 Django project = 一個網站。本專案的配置放在 `config/`：

```text
learnboard/
├── manage.py          # 命令入口
├── config/            # Project package：設定與根路由
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── board/             # App：留言板功能本體
```

`config` 只是名字（learnmart 用同名）。它不是功能所在——功能都在 app 裡。

---

## 2-2 建立指令是「歷史」，不要重跑

```bash
django-admin startproject config .
python manage.py startapp board
```

這兩行只在專案誕生時執行過一次，產生了上面的檔案。

**你不需要也不應該再跑一次**——它們會覆蓋或產生重複結構。

理解「哪些檔案是骨架、哪些是我們寫的」：

- 骨架：`manage.py`、`config/*`、`board/apps.py`
- 我們寫的：models、views、urls、templates、static 全部內容

---

## 2-3 `manage.py` 是專案命令入口

```bash
uv run python manage.py <command>
```

| command | 作用 | 動到的層 |
|---|---|---|
| `runserver` | 啟動開發伺服器 | — |
| `migrate` | 套用 migration 到 DB | schema 層 |
| `makemigrations` | 產生 migration 檔案 | schema 層 |
| `createsuperuser` | 建立管理員 | 資料層 |
| `test` | 執行測試 | — |
| `shell` | 進入互動直譯器（已載入 Django） | — |

它做的事：設定 `DJANGO_SETTINGS_MODULE=config.settings`，再轉交給 Django。

---

## 2-4 settings 是普通 Python 設定值

`config/settings.py` 就是變數清單，沒有魔法：

```python
DEBUG = True
INSTALLED_APPS = [..., "board"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3",
                         "NAME": BASE_DIR / "db.sqlite3"}}
LANGUAGE_CODE = "zh-hant"
TIME_ZONE = "Asia/Taipei"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "board:list"
```

改設定 = 改 Python 變數。之後遇到任何「去哪裡設定的問題」，答案幾乎都在這個檔案。

---

## 2-5 App 註冊與 template 搜尋不是同一件事

```python
INSTALLED_APPS = ["django.contrib.admin", ..., "board"]
TEMPLATES = [{"DIRS": [BASE_DIR / "templates"], "APP_DIRS": True, ...}]
```

- 把 `"board"` 加進 `INSTALLED_APPS`：讓 Django 認得這個 app（models、management commands…）
- `DIRS`：專案根目錄的 `templates/` 也算搜尋範圍
- `APP_DIRS: True`：也會搜尋各 app 資料夾內的 `templates/`

本專案統一放在根目錄 `templates/board/`，避免多處尋找。

---

## 2-6 HTTP：瀏覽器與伺服器的訊息交換

```text
瀏覽器                                Django 伺服器
   │  GET / HTTP/1.1                      │
   │  Host: 127.0.0.1:8000                │
   │ ───────────────────────────────────► │
   │                                      │ 找 URL → 執行 View → 產生 HTML
   │ ◄─────────────────────────────────── │
   │  HTTP/1.1 200 OK                     │
   │  Content-Type: text/html             │
   │  <html>…留言牆…</html>                │
```

Request 有 method（GET／POST）與路徑；Response 有狀態碼與內容。

---

## 2-7 用一個 request 拆解網址

```text
https://127.0.0.1:8000/?q=django
└─┬──┘ └──────┬──────┘ └─┬─┘ └─┬──┘
scheme       host      path  query string
```

- `path` 由 Django 的 **URLconf** 比對
- `?q=django` 不參與路由，由 view 用 `request.GET.get("q")` 讀取
- method 是 GET → 這是一次查詢，不應該改變資料

---

## 2-8 常見 response status

| 狀態碼 | 意思 | 本專案例子 |
|---:|---|---|
| 200 | 成功 | 留言牆正常顯示 |
| 302 | 轉址 | 登入成功跳回首頁 |
| 403 | 有身份但無權限 | 別刪別人的留言（Deck 02） |
| 404 | 找不到資源 | 網址打錯、留言不存在 |
| 500 | 伺服器錯誤 | view 程式碼拋例外 |

除錯第一步：先看狀態碼，再看 terminal traceback。

---

## 2-9 第一個 Function View

```python
# board/views.py
from django.http import HttpResponse


def home(request):
    return HttpResponse("Hello, LearnBoard!")
```

```python
# board/urls.py
from django.urls import path
from . import views

urlpatterns = [path("", views.home, name="home")]
```

view 就是一個收 `request`、回 response 的函式。`HttpResponse("...")` 直接把字串當 body 回傳。

**你應該看到：**瀏覽器顯示 `Hello, LearnBoard!`。

---

## 2-10 `path()` 四個重要位置

```python
path(route, view, kwargs=None, name=None)
```

| 參數 | 作用 |
|---|---|
| `route` | 比對的路徑字串（不含 host） |
| `view` | 比對成功時呼叫的函式 |
| `kwargs` | 額外傳給 view 的字典（少用） |
| `name` | 反向查詢用的名字，全站唯一 |

`""` 代表網站根路徑。`name="home"` 之後可在模板 `{% url 'home' %}` 引用。

---

## 2-11 Project URL 如何交給 App URL？

```python
# config/urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("board.urls")),
]
```

- `include()`：把剩餘路徑交給 `board/urls.py` 接手
- 好處：每個 app 管自己的路由；project 只當總機

**心智模型：**URLconf 是一串接力。`config/urls.py` 先比對前綴，剩下的交給 app 繼續比。

---

## 2-12 動態路徑：converter 與函式參數要相同

```python
# board/urls.py
path("messages/<int:pk>/", views.message_detail, name="message-detail")

# board/views.py
def message_detail(request, pk):
    return HttpResponse(f"想看第 {pk} 號留言")
```

`<int:pk>` 會把路徑中的數字轉成 int，並以關鍵字參數 `pk` 傳入 view。

**參數名稱必須與 converter 名稱完全相同**，否則 `TypeError`。

**你應該看到：**拜訪 `/messages/3/` 顯示「想看第 3 號留言」。

---

## 2-13 常用 converter 不必一次背完

| converter | 符合 | 傳入型別 |
|---|---|---|
| `<int:pk>` | 0 或任意整數 | `int` |
| `<str:name>` | 任意非空字串（不含 `/`） | `str` |
| `<slug:title>` | 英數、`-`、`_` | `str` |
| `<uuid:key>` | UUID 格式 | `UUID` |

留言板的編輯／刪除網址都用 `<int:pk>`；slug 在第二階段商城的分類網址才登場。

---

## 2-14 命名 URL：不要把路徑散落各處

```html
<!-- 寫死：改路由要改一百個檔案 -->
<a href="/">回首頁</a>

<!-- 命名：路由改了連結自動跟著改 -->
<a href="{% url 'home' %}">回首頁</a>
```

本專案的 app 加了命名空間，模板中寫成：

```html
<a href="{% url 'board:list' %}">回留言牆</a>
```

`board:list` = app_name `board` ＋ name `list`。命名空間避免不同 app 的同名路由打架。

---

## 2-15 在 Python 與 template 反向產生 URL

```python
from django.urls import reverse

reverse("board:list")            # "/"
reverse("board:update", args=[3])  # "/messages/3/edit/"
```

```html
{# board/message_list.html #}
<a href="{% url 'board:update' post.pk %}">編輯</a>
```

規則：帶參數的路由，反向時一定要給參數；漏給會 raise `NoReverseMatch`。

---

## 2-16 原始 `HttpResponse` 不會套 template escaping

```python
return HttpResponse("<h1>" + user_input + "</h1>")
```

若 `user_input` 是 `<script>alert(1)</script>`，瀏覽器會真的執行它——這叫 XSS。

**教訓：**永遠不要手工拼 HTML 字串。用 template（下一章），它預設會跳脫 `<`、`>`、`&`。

> 這是 Deck 02 安全章的伏筆，此處先建立警覺。

---

## 2-17 一次最小 request 的旅程

```text
1. 瀏覽器送出 GET /
2. WSGI/ASGI server 交給 Django
3. middleware 依序處理（session、CSRF…）
4. config/urls.py 比對 "" → include board.urls
5. board/urls.py 比對 "" → MessageListView
6. view 查資料庫、渲染 template
7. response 200 HTML 回到瀏覽器
```

目前 5→6 對你還是黑箱：view 怎麼查資料、template 怎麼長出 HTML，正是第 3～5 章的主題。

---

## 2-17A 圖解：一次 request 的旅程

![w:1020](../assets/request_flow.svg)

<!--
授課提示：這張圖值得投影十分鐘。請三位學生分別指著「URL routing」「View」「Template」說出各自收到什麼、交出什麼。第二階段商城課程開場也會再考一次。
-->

---

## 2-18 404 與 500 怎麼分辨？

- **404**：路由沒有符合，或 view 判定「查無此物件」——是*正常的查無資料*
- **500**：view 程式碼拋出未捕捉的例外——是*程式有 bug*

`DEBUG=True` 時 500 會附完整 traceback；找到最後一個 frame 通常就是兇手行。

**練習：**把 `views.home` 裡加一行 `1 / 0`，重載頁面，讀懂 traceback 再移除。

---

## 第 2 章｜觀念檢核與實作

**觀念檢核：**

1. `include()` 在 URLconf 接力中扮演什麼？
2. `path("messages/<int:pk>/", ...)` 中 `<int:pk>` 做了什麼？
3. 為什麼模板要用 `{% url %}` 而不是寫死 href？
4. 404 與 500 的成因差別？

**實作任務：**新增一個 `/about/` 路由與 view，回傳 `HttpResponse`，並給它 name，再用 shell 以 `reverse()` 取得網址。

→ 步驟與解答在配套手冊第 2 章。
