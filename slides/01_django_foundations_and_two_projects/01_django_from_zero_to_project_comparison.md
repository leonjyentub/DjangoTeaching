---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 基礎｜從零建立網站，再對照完成專案"
footer: "uv・project・app・HTTP・URL・View"
---

# 從零建立第一個 Django 網站

先完成自己的練習，再讀 LearnBoard × LearnMart。

**學習成果：** 建立環境、產生 project 與 app、讀懂設定，
啟動網站並完成可驗證的 URL、View、response。

本教材使用 Python 3.13、Django 5.2 系列與 uv。

<!-- 編輯範圍：整合原 01_chapter_01.md 與 02_chapter_02.md；原檔及其他章節保留。原知識點對應表位於文末。 -->

---

## 學習順序與每段成果

| 階段 | 學習內容 | 要交出的結果 |
|---|---|---|
| A | uv、venv、Python、Django 安裝 | 專案環境可執行 Python 與 Django |
| B | django-admin、project、app | 自己建立的 `config/` 與 `pages/` |
| C | 檔案、Git、TOML、settings | 能指出每份設定管什麼 |
| D | 資料庫、啟動、瀏覽器預覽 | 看見 Django 歡迎頁並記錄檢查結果 |
| E | HTTP、URL、View、安全與測試 | `/hello/` 與動態網址能正確回應 |
| F | LearnBoard × LearnMart 對照 | 依實際檔案追蹤完成專案 |

<!-- 建議分段授課：A–B、C–D、E、F。每段先操作再解釋剛出現的檔案，不以閱讀完成專案作為前置能力。 -->

---

## A-1 先認識 uv：管理 Python 專案的工具

uv 幫我們安裝或選用 Python、建立虛擬環境、安裝套件，
並記錄專案需要哪些套件版本。

- **Python** 執行程式，**Django** 提供網站框架。
- **uv** 準備執行環境，再呼叫 Python 或 Django 指令。
- 先完成環境準備，後面才會建立網站的程式檔案。

```text
uv 準備環境 → Python 執行 Django → Django 處理網站功能
```

**操作位置：** 以下指令輸入終端機，不是 Python 的 `>>>` 視窗。

---

## A-2 安裝 uv，再重新開啟終端機

**macOS / Linux：**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows PowerShell：**

```powershell
winget install --id=astral-sh.uv -e
```

安裝後重新開啟終端機，執行 `uv --version`，應看到版本號。
若找不到 `uv`，先依安裝訊息檢查 PATH，再繼續下一步。

來源：[uv 安裝說明](https://docs.astral.sh/uv/getting-started/installation/)

<!-- Windows 無 WinGet 時，使用官方安裝頁的 PowerShell 安裝方式。教室電腦若無安裝權限，請先由教師準備工具。 -->

---

## A-3 venv 與 `.venv/` 是什麼？

- **virtual environment（虛擬環境）**：隔離各專案使用的套件。
- **venv**：Python 內建的虛擬環境建立模組。
- **`.venv/`**：本課程放置虛擬環境的資料夾名稱。
- uv 也能建立虛擬環境，主線使用 `uv venv`。

```text
練習 A/.venv/    各自安裝需要的 Django 版本
練習 B/.venv/    不必共用同一組套件
```

虛擬環境不是虛擬機，也不會替我們建立 Django 網頁或資料表。
沒有隔離時，在共用 Python 更新套件可能影響另一個專案。

---

## A-4 Python：真正執行程式的直譯器

先用 uv 準備本課程的 Python：

```bash
uv python install 3.13
```

- **interpreter（直譯器）**：讀取並執行 Python 程式。
- **module（模組）**：可匯入或執行的 Python 程式單位。
- **package（套件）**：此處指可安裝使用的程式，例如 Django。
- **dependency（依賴）**：你的專案需要的套件。

即使電腦已有 Python，也要確認課堂指令使用哪個版本。
本次固定選用 3.13，方便全班依相同流程操作。

---

## A-5 建立自己的空練習資料夾

在自己存放課堂練習的位置開終端機，建立全新的資料夾：

```bash
mkdir django_lab
cd django_lab
```

| 終端機 | 顯示目前位置 | 列出檔案 |
|---|---|---|
| macOS / Linux | `pwd` | `ls -a` |
| Windows PowerShell | `Get-Location` | `Get-ChildItem -Force` |
| Windows CMD | `cd` | `dir /a` |

**後續主線指令都在 `django_lab/` 執行。**
把練習放在現有教材及完成專案之外，避免混用設定。

---

## A-6 初始化 Python 專案與虛擬環境

```bash
uv init --bare --python 3.13 --vcs none
uv python pin 3.13
uv venv --python 3.13
uv run python --version
```

1. `init --bare`：建立最小的 `pyproject.toml`。
2. `python pin`：建立 `.python-version`，記下 Python 版本。
3. `venv`：建立 `.venv/`，存放這份練習使用的環境。
4. `run`：在專案環境執行 Python，應顯示 `Python 3.13.x`。

`--vcs none` 讓本次練習稍後再自行初始化 Git。
`uv run` 會準備、同步專案環境，也會產生需要的鎖檔。

---

## A-7 確認執行的是哪一個 Python

```bash
uv run python -c "import sys; print(sys.executable)"
uv run python -c "print('Python 環境準備完成')"
```

- `-c`：執行後面引號中的 Python 程式。
- 第一行應指向 `django_lab/.venv/` 裡的執行檔。
- 第二行應在終端機印出指定文字。
- `uv run` 後面接一般命令，不是另一套 Python 語法。

**檢查點：** 記下 Python 版本與執行檔位置。
若 VS Code 也要執行程式，選擇這個 `.venv` 的 interpreter。

---

## A-8 安裝 Django，確認 django-admin 可用

```bash
uv add "django>=5.2,<5.3"
uv run django-admin --version
uv run python -m django --version
```

- `uv add` 安裝 Django，也更新依賴宣告及鎖檔。
- 版本條件加上引號，避免終端機把 `<`、`>` 當成特殊符號。
- `django-admin` 是安裝 Django 時一併提供的命令列工具。
- 正確名稱有連字號：`django-admin`，不是 `django admin`。
- 後兩行應顯示相同的 `5.2.x` 版本。

目前只裝好框架，還沒有 `manage.py`、project 或 app。

---

## A-9 `python -m` 到底是什麼？

以下用 pip 說明語法，不在主線練習中額外執行。

```bash
python -m pip install django
```

- `python`：選定一個 Python interpreter。
- `-m pip`：請這個 interpreter 尋找並執行 `pip` 模組。
- `install django`：傳給 pip 的參數。

這種寫法明確指定「使用這一個 Python 所屬的 pip」，
可避免直接輸入 `pip` 時，意外操作另一個 Python 的套件。

同理，`python -m django --version` 由指定 interpreter 執行 Django 模組。

---

## A-10 傳統 venv：另一種環境準備方式

<div style="display: flex; gap: 24px; align-items: flex-start;">
<div style="flex: 1;">

**macOS / Linux (POSIX Shell)**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install "django>=5.2,<5.3"
```

</div>
<div style="flex: 1;">

**Windows (CMD)**

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install "django>=5.2,<5.3"
```

</div>
</div>

- 第一行建立 `.venv/`；第二行讓目前 shell / 終端機優先使用其中的 Python
- 第三行把 Django 安裝進目前 interpreter 的環境
- activation 只影響目前終端機工作階段

**替代方式，不在 `django_lab` 重做。** 此例假設 `python` 已可用；macOS 也可能使用 `python3`。離開環境用 `deactivate`。主線繼續使用 `uv run`，通常不必手動 activate。

---

## B-1 先分清楚 project 與 app

**Django project** 集中網站共用的設定與入口。
**Django app** 集中一組相關功能，可以有自己的資料與頁面。

這份練習採用：

| 名稱 | 用途 | 即將產生的位置 |
|---|---|---|
| `django_lab` | 整份練習的外層資料夾 | 目前所在目錄 |
| `config` | Django project package | `config/` |
| `pages` | 第一個 app，用來練習頁面 | `pages/` |

一個 project 可組合多個 app。App 是功能模組，不必拆成微服務。

---

## B-2 用 django-admin 建立 project

**位置：`django_lab/`。只執行一次：**

```bash
uv run django-admin startproject config .
```

- `uv run`：先使用課堂練習環境。
- `django-admin`：Django 命令列工具。
- `startproject`：產生網站設定與入口檔案。
- `config`：本次 project package 的名稱。
- `.`：把產物放在目前目錄，避免再多包一層資料夾。

**檢查點：** 目前目錄新增 `manage.py` 與 `config/`。
已建立後不重跑此指令，之後直接編輯檔案。

---

## B-3 透過 manage.py 建立第一個 app

仍在 `django_lab/`，與 `manage.py` 同一層：

```bash
uv run python manage.py startapp pages
```

- `manage.py` 是剛才產生的專案命令入口。
- `startapp pages` 建立 `pages/` 及基本 Python 檔案。
- 不要先 `cd config` 或 `cd pages` 才執行。
- `startapp` 不會自動註冊 app，也不會建立 app 的 `urls.py`。

**檢查點：** `config/` 與 `pages/` 現在並排存在。
接著打開資料夾，逐一對照自己剛產生的檔案。

---

## C-1 先看外層：每一項由誰建立？

```text
django_lab/
├── .python-version    uv python pin：Python 版本選擇
├── pyproject.toml     uv init / add：專案資訊與依賴
├── uv.lock            uv：解析後的精確套件版本
├── .venv/             uv：虛擬環境
├── manage.py          startproject：專案命令入口
├── config/            startproject：Django 設定 package
└── pages/             startapp：頁面功能 app
```

`uv init --bare` 不會產生一般 `uv init` 的 `main.py`、README。
`db.sqlite3` 稍後才在資料庫操作時出現，`.git/` 也尚未建立。

---

## C-2 config：網站共用設定與入口

| 檔案 | 初學階段要知道的用途 |
|---|---|
| `config/__init__.py` | 標記一般 Python package，通常保留空白 |
| `config/settings.py` | 啟用哪些 app、資料庫、語言等設定 |
| `config/urls.py` | 網站最上層的網址分派表 |
| `config/wsgi.py` | WSGI 伺服器載入 Django 的入口 |
| `config/asgi.py` | ASGI 伺服器載入 Django 的入口 |

WSGI、ASGI 是 Python 網站與伺服器之間的介面。
這次練習先保留產生的入口檔案，後續部署再深入。

---

## C-3 pages：功能程式從這裡開始

| 檔案／資料夾 | 用途 |
|---|---|
| `__init__.py`、`apps.py` | package 標記、app 設定類別 |
| `models.py` | 定義資料模型 |
| `migrations/` | 保存資料庫結構變更紀錄，起初只有 `__init__.py` |
| `views.py` | 接收 request，產生 response |
| `admin.py` | 註冊後台可管理的 model |
| `tests.py` | 自動檢查程式行為 |

`urls.py`、`forms.py`、`templates/` 不在 `startapp` 產物中，
使用到時才自行新增。`static/` 放 CSS、JS 等資源，`media/` 放上傳檔案。

---

## C-4 `manage.py` 如何知道要用哪份設定？

**練習檔案：`manage.py` 的核心責任**

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

## C-5 Git：記錄你每次完成的修改

Git 保存檔案版本，方便比較修改與回到先前的狀態。
Repository（版本庫）是由 Git 管理的一組檔案與歷史。

在這份**獨立練習**的 `django_lab/` 中：

```bash
git --version
git init
git status
```

- `git init` 建立隱藏的 `.git/`，之後不用反覆執行。
- 若找不到 Git，先安裝 [Git](https://git-scm.com/downloads) 並重新開啟終端機。
- Git 保存本機版本，GitHub 是可存放遠端版本庫的服務。
- `.git/` 是版本歷史，`config/` 是 Django package，兩者用途不同。

---

## C-6 `.gitignore`：哪些檔案可以重建？

在 `django_lab/.gitignore` 新增：

```gitignore
.venv/
__pycache__/
*.py[cod]
*.sqlite3
/media/
.env
.DS_Store
```

保留程式、migration、templates、static、TOML、鎖檔與版本選擇檔。
虛擬環境、快取、本機資料庫與上傳檔可另行重建或備份。
`.env` 若含密鑰不可提交，Django 也不會自動讀取它。

---

## C-7 保存第一個可比較的版本

確認 `git status` 沒有列出 `.venv/`，再執行：

```bash
git add .gitignore .python-version pyproject.toml uv.lock
git add manage.py config pages
git diff --cached
git commit -m "建立 Django 練習骨架"
```

- `add` 放入暫存區，`diff --cached` 檢查即將保存的內容。
- `commit` 建立版本紀錄。稍後編輯檔案可用 `git diff` 比較。
- 若 Git 要求姓名及 email，先以自己的資訊設定 `user.name`、`user.email`。
- `.gitignore` 不會自動取消已追蹤檔案，也不會刪除舊歷史中的密鑰。

---

## C-8 三個環境檔案各管什麼？

```text
.python-version   希望使用的 Python 版本（本練習：3.13）
pyproject.toml    專案直接宣告的需求與允許版本範圍
uv.lock           uv 解析後的完整、精確依賴結果
```

- 修改直接依賴：通常編輯 `pyproject.toml`，再讓 uv 更新鎖檔
- 不要把 `uv.lock` 當成手寫套件清單
- 不要提交 `.venv/`；其他人可由上述檔案重建

---

## C-9 讀懂 pyproject.toml 的基本語法

**練習檔案範例，版本範圍以 `uv add` 結果為準：**

```toml
[project]
name = "django-lab"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "django>=5.2,<5.3",
]
```

`[project]` 是 TOML table；`key = value` 指定設定值。
字串用引號，`dependencies` 是字串陣列。TOML 是設定格式，
不執行 Python 程式，也不負責設定 Django 的資料庫。

---

## C-10 版本範圍與鎖檔的精確版本

```text
requires-python = ">=3.13"
django>=5.2,<5.3
```

- `>=3.13`：3.13 或更高版本；不是「只能 3.13」
- `>=5.2`：允許 5.2 以上
- `<5.3`：排除 5.3，避免跨入下一個 minor 系列
- 兩個條件以逗號連接，表示必須同時成立

`pyproject.toml` 寫「允許範圍」；`uv.lock` 會記錄目前實際解析到的精確版本。

---

## C-11 直接依賴、開發依賴與同步

Django 是執行網站需要的直接依賴。Coverage 用來量測測試涵蓋率，
可在需要時以 `uv add --dev "coverage>=7.6"` 加入開發群組。

```toml
[dependency-groups]
dev = ["coverage>=7.6"]

[tool.uv]
package = false
```

`package = false` 表示不把這份應用程式自身建成可發布的套件。
`uv sync` 依宣告與鎖檔同步 `.venv`，預設會包含 `dev` 群組。
虛擬環境隔離套件，鎖檔記錄精確依賴；重現仍需相容的系統與 Python。

---

## C-12 settings 是 Python：先註冊自己的 app

打開 `config/settings.py`，**保留原有六個內建 app**，
在 `INSTALLED_APPS` 清單最後加上這一項：

```python
"pages.apps.PagesConfig",
```

這個路徑指向 `pages/apps.py` 的 `PagesConfig`。
Django 也接受簡寫 `"pages"`，由 app 的預設設定進行發現。

接著修改同一份檔案的兩個值：

```python
LANGUAGE_CODE = "zh-hant"
TIME_ZONE = "Asia/Taipei"
```

`INSTALLED_APPS` 是 Python list，設定值是變數與字串。

---

## C-13 settings 地圖：先知道要去哪裡找

| 設定 | 負責什麼 |
|---|---|
| `BASE_DIR` | 用 `Path` 找到外層練習資料夾 |
| `INSTALLED_APPS` | 啟用 app，影響 model、admin 等發現機制 |
| `MIDDLEWARE` | request / response 經過的共用處理，例如 session、驗證 |
| `ROOT_URLCONF` | 根網址設定，本次是 `"config.urls"` |
| `TEMPLATES` | HTML 樣板引擎及搜尋位置 |
| `WSGI_APPLICATION` | WSGI 應用入口 |

`asgi.py` 由 `startproject` 產生；完成專案另明列
`ASGI_APPLICATION = "config.asgi.application"`，骨架不一定有此設定。

---

## C-14 settings 地圖：資料、語言與靜態資源

| 設定 | 負責什麼 |
|---|---|
| `DATABASES` | 資料庫引擎、位置及連線資訊，下一段實際操作 |
| `AUTH_PASSWORD_VALIDATORS` | 密碼驗證規則 |
| `LANGUAGE_CODE`、`TIME_ZONE` | 介面語言、預設時區 |
| `USE_I18N`、`USE_TZ` | 翻譯支援、具時區資訊的日期時間 |
| `STATIC_URL` | CSS、JS 等靜態資源的 URL 前綴 |
| `DEFAULT_AUTO_FIELD` | 未明訂主鍵型別時採用的預設型別 |

後續需要共用靜態資料夾、上傳與登入功能時，才加入對應設定。
先能辨識用途，不必一次背完全部設定名稱。

---

## C-15 App 註冊與 template 搜尋的差別

骨架的 `TEMPLATES` 預設包含 `"DIRS": []` 與 `"APP_DIRS": True`。
之後若自行建立外層 `templates/`，可把 `DIRS` 改為：

```python
"DIRS": [BASE_DIR / "templates"],
"APP_DIRS": True,
```

- `DIRS` 指定額外搜尋目錄。
- `APP_DIRS=True` 搜尋已安裝 app 裡的 `templates/`。
- 註冊 app 不等於建立資料夾，也不等於設定所有樣板路徑。
- 即使漏註冊 app，透過 `DIRS` 指定的根目錄樣板仍可能找到。

本次先用文字 response，不必提前建立 HTML 樣板。

---

## C-16 本機開發設定的使用邊界

保留 `startproject` 產生的 `SECRET_KEY`，並在 settings 設定：

```python
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
```

- `SECRET_KEY` 參與簽章等安全機制，正式使用時須保密並外部化。
- `DEBUG=True` 提供除錯資訊，正式環境不能公開這些細節。
- `ALLOWED_HOSTS` 檢查請求的 Host，不是指定伺服器監聽位置。
- 正式部署需另外規劃伺服器、HTTPS、資料庫、備份及權限。

**檢查點：** 能指出 app 註冊、時區、URL 與開發設定的位置。

---

## D-1 資料庫：持續保存網站資料

資料表（table）定義欄位，資料列（row）保存一筆內容。
Schema 指資料庫結構，包含資料表、欄位與限制。

`config/settings.py` 預設使用 SQLite：

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

SQLite 使用本機檔案，適合課堂練習，不需先啟動獨立資料庫服務。
`uv add` / `uv sync` 安裝套件，不會替 Django 建好資料表。

---

## D-2 第一次 migrate：建立內建功能的資料表

**位置：`django_lab/`。**

```bash
uv run python manage.py check
uv run python manage.py migrate
uv run python manage.py showmigrations
```

- `check` 檢查部分設定與程式結構問題。
- `migrate` 套用 migration，準備登入、session、admin 等內建資料表。
- `showmigrations` 的 `[X]` 表示已套用，`[ ]` 表示尚未套用。
- 此時尚未替 `pages` 定義 model，所以沒有自訂資料表。

**檢查點：** 看見 `db.sqlite3`，migration 套用成功。
不要用刪除 migration 檔案的方式處理不懂的錯誤。

---

## D-3 分清楚之後會用到的資料指令

| 命令 | 影響的層次 | 何時使用 |
|---|---|---|
| `uv sync` | Python 套件環境 | 取得既有專案或同步依賴 |
| `makemigrations` | 產生結構變更檔 | 後續新增或修改 model |
| `migrate` | 套用結構變更等 migration 操作 | 準備或更新資料庫 |
| `seed_demo` | 建立示範資料列 | 最後操作完成專案才使用 |

後三種命令接在 `uv run python manage.py` 後面。
`seed_demo` 是完成專案自訂的 command，**新建 Django 沒有它**。
自訂 model 與 ORM 留給後續章節；現在先完成最小網站。

---

## D-4 啟動開發伺服器

```bash
uv run python manage.py runserver
```

終端機應出現類似訊息：

```text
Starting development server at http://127.0.0.1:8000/
```

- `127.0.0.1` 指自己的電腦，`8000` 是服務連接埠（port）。
- 終端機保持運作，用瀏覽器開啟上面的網址。
- 修改 Python 檔通常會自動重載，新增檔案時必要時手動重啟。
- 按 `Ctrl+C` 停止。若 8000 被占用，可用 `runserver 8001`。

這是本機開發伺服器，尚未完成正式部署。

---

## D-5 第一次 preview：看到 Django 歡迎頁

目前 `config/urls.py` 仍是產生的預設內容，只有 admin 路由。
在 `DEBUG=True` 的新專案根網址，應看到 Django 安裝成功頁。

1. 確認終端機仍在執行伺服器。
2. 在瀏覽器開啟 `http://127.0.0.1:8000/`。
3. 重新整理，觀察終端機的新紀錄。
4. 開啟瀏覽器開發者工具的 **Network**，再重新整理。

這裡的 preview 是瀏覽器向 Django 取得頁面。
直接雙擊 `.py` 或使用靜態 HTML 預覽工具，都不會執行 Django 網站。
稍後接入自己的路由後，根網址可能變成 404，屆時改測 `/hello/`。

---

## D-6 啟動前後的檢查不能互相取代

| 檢查 | 能確認什麼 | 尚未證明什麼 |
|---|---|---|
| `check` | 部分設定、model 等結構問題 | 每個頁面都正確 |
| `migrate` | migration 成功套用 | 已有示範資料 |
| `runserver` | 開發服務成功啟動 | 所有路由與業務功能正常 |
| 瀏覽器 preview | 指定頁面可觀察的結果 | 所有輸入與邊界行為 |
| `test` | 已撰寫測試所涵蓋的行為 | 沒寫測試的功能 |

**實作紀錄：** 保存指令、畫面結果及一個遇到的錯誤。
接下來用 HTTP 解釋瀏覽器與終端機剛才發生了什麼。

---

## E-1 HTTP：瀏覽器與伺服器交換訊息

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

---

## E-2 拆開網址，找出路由真正比對的部分

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

## E-3 在 Network 看見 request 與 response

點選 Network 中重新整理產生的文件請求，觀察：

| 請求／回應 | 欄位 | 本機預覽可觀察的例子 |
|---|---|---|
| Request | method、URL | `GET`、`http://127.0.0.1:8000/` |
| Request | headers | `Host`、`Cookie`（若有） |
| Response | status | 成功頁面通常是 `200` |
| Response | headers | `Content-Type` 說明內容型別 |
| Response | body | Response 分頁內的 HTML 或文字 |

GET 通常用來讀取內容，POST 通常用來提交資料。
Query string 與 request body 是不同位置；登入狀態常透過 cookie / session 關聯。

---

## E-4 常見 response status

| 狀態 | 初學者可先這樣理解 |
|---|---|
| 200 | 成功取得內容 |
| 302 | 請瀏覽器再到另一個網址 |
| 403 | 已理解請求，但沒有權限 |
| 404 | 找不到符合的路由或物件 |
| 500 | 伺服器執行時發生未處理錯誤 |

狀態碼不是完整錯誤原因，但能先判斷問題在哪一層。

---

## E-5 第一個 View：先回傳固定文字

**把 `pages/views.py` 改成：**

```python
from django.http import HttpResponse


def hello(request):
    return HttpResponse("Hello Django", content_type="text/plain; charset=utf-8")
```

Django 呼叫 `hello` 時傳入 request 物件。
函式是一種 callable（可呼叫物件），View 必須回傳 response。
這裡明訂純文字型別，將 `Hello Django` 放進 response body。

檔案存好後還不能用網址找到它，下一步要設定路由。

---

## E-6 自行新增 app 的 urls.py

**新增 `pages/urls.py`，內容如下：**

```python
from django.urls import path
from . import views

app_name = "pages"

urlpatterns = [
    path("hello/", views.hello, name="hello"),
]
```

`from . import views` 匯入同一個 app 的 `views.py`。
`views.hello` 交出函式供 Django 之後呼叫，此處不加 `()`。
`app_name` 與路由 `name` 稍後用來反向產生網址。

---

## E-7 `path()` 四個重要位置

**剛才新增的 `pages/urls.py` 路由節錄**

```python
path("hello/", views.hello, name="hello")
```

1. `"hello/"`：要比對的 route，不以 `/` 開頭
2. `views.hello`：匹配後呼叫的 callable
3. 可選 extra kwargs：本例未使用
4. `name="hello"`：反向產生 URL 時使用的名稱

---

## E-8 把 project URL 接到 app URL

**把 `config/urls.py` 改成以下完整內容，保留 admin 路由：**

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("pages.urls")),
]
```

根 URL 比對空前綴 `""`，把剩餘路徑交給 `pages.urls`。
`/hello/` 會由 app 找到 `hello/`，再呼叫 `views.hello`。
`INSTALLED_APPS` 啟用 app，`include()` 接入路由，兩件事都要做好。

---

## E-9 立刻驗收：第一個頁面確實可用

瀏覽器開啟 `http://127.0.0.1:8000/hello/`。
應看到 `Hello Django`，Network 的文件請求應為 `200`。

也可在**另一個終端機**執行：

```bash
curl -i http://127.0.0.1:8000/hello/
```

Windows PowerShell 如遇命令別名問題，使用 `curl.exe -i`。
觀察狀態列、`Content-Type: text/plain; charset=utf-8` 與 body。
根網址 `/` 目前沒有自訂路由，顯示 404 屬於預期結果。

**檢查點：** 能從三個檔案解釋為什麼 `/hello/` 回應成功。

---

## E-10 動態路徑：把網址片段傳入函式

**在 `pages/views.py` 後面新增：**

```python
def hello_name(request, name):
    return HttpResponse(f"歡迎 {name}", content_type="text/plain; charset=utf-8")
```

**在 `pages/urls.py` 的 `urlpatterns` 清單中新增：**

```python
path("hello/<str:name>/", views.hello_name, name="hello-name"),
```

`<str:name>` 匹配非空且不含 `/` 的片段，以 `name=...` 傳入。
瀏覽 `/hello/Ada/` 應看到「歡迎 Ada」。參數名必須對得上。

---

## E-11 常用 converter

| converter | 匹配結果 | 常見用途 |
|---|---|---|
| `<int:pk>` | 非負十進位整數（包含 0），傳入 Python `int` | 物件主鍵 |
| `<str:name>` | 非空且不含 `/` 的字串 | 短文字 |
| `<slug:slug>` | 字母、數字、`-`、`_` | 可讀網址代稱 |
| `<path:value>` | 可含 `/` | 子路徑 |

`pk` 是常用的主鍵參數名。以下為後續資料頁的形式示意：

```python
path("products/<int:pk>/", views.product_detail,
     name="product-detail")
```

此處尚未建立 `product_detail`，不用貼入練習。
`<slug:slug>` 接受的是 ASCII 英文字母、數字、`-`、`_`。

---

## E-12 Query string 由 request.GET 讀取

**在 `pages/views.py` 後面新增：**

```python
def search(request):
    keyword = request.GET.get("q", "")
    return HttpResponse(f"查詢：{keyword}", content_type="text/plain; charset=utf-8")
```

**在 app 的 `urlpatterns` 中新增：**

```python
path("search/", views.search, name="search"),
```

開啟 `/search/?q=django` 應看到「查詢：django」。
路由比對 `search/`，`request.GET.get("q", "")` 讀參數，沒有值時用空字串。
這裡只是顯示查詢文字，尚未搜尋資料庫。

---

## E-13 命名 URL：把名稱與路徑分開

剛才的設定包含：

```python
app_name = "pages"
# urlpatterns 內：
path("hello/", views.hello, name="hello")
```

完整路由名稱為 `pages:hello`：

- `pages`：命名空間（namespace），區分不同 app 的同名路由。
- `hello`：這條路由的名稱。
- `hello/`：瀏覽器實際請求的路徑。

其他程式透過名稱產生 URL，日後改路徑時就能減少逐處修改。

---

## E-14 在 Python 反向產生網址

開第二個終端機，進入 `django_lab/`，執行：

```bash
uv run python manage.py shell
```

再於 Python 互動環境執行：

```python
from django.urls import reverse
reverse("pages:hello")                       # '/hello/'
reverse("pages:hello-name", kwargs={"name": "Ada"})  # '/hello/Ada/'
```

反向解析需要「完整名稱＋必要參數」。結束使用 `exit()`。
若出現 `NoReverseMatch`，檢查 namespace、name 及必要參數。

---

## E-15 在 template 反向產生網址

之後建立 HTML 樣板時，可以寫：

```django
<a href="{% url 'pages:hello' %}">打招呼</a>
<a href="{% url 'pages:hello-name' 'Ada' %}">歡迎 Ada</a>
```

`{% url ... %}` 是 Django template 標籤，不是 Python 語法。
它必須經過 Django 樣板引擎處理，瀏覽器不會自行解讀。

後續的 Model、Template 章節會完成 HTML 頁面。
此處先理解與 Python 的 `reverse()` 使用同一套路由名稱。

---

## E-16 `HttpResponse` 與安全顯示

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

## E-17 需要 HTML 時，明確處理使用者輸入

本次動態範例用 `content_type="text/plain; charset=utf-8"`，
讓瀏覽器當成文字。如果要建立 HTML，可明確跳脫動態值：

```python
from django.utils.html import format_html


def hello_html(request, name):
    body = format_html("<p>歡迎 {}</p>", name)
    return HttpResponse(body)
```

**補充範例，不需加入本次路由。** `format_html` 會跳脫替換參數。
實際 HTML 頁面通常使用 template 的預設 escaping。
不要對不可信資料使用 `safe` 或 `mark_safe` 來略過保護。

---

## E-18 追蹤一次最小 request 的旅程

```text
GET /hello/
  config/urls.py    include("pages.urls")
       ↓
  pages/urls.py     path("hello/", views.hello, ...)
       ↓
  pages/views.py    hello(request)
       ↓
  HttpResponse     status 200、headers、文字 body
       ↓
  瀏覽器顯示 Hello Django
```

這裡省略共用 middleware 等處理，先追蹤自己的程式。
此流程沒有 Model 與 Template，每個 View 不一定要用到所有層。

---

## E-19 404 與 500：沿著流程找問題

| 狀態 | 常見原因 |
|---|---|
| 404 | 路徑拼錯或沒有匹配路由、忘記 `include()` |
| 404 | converter 不接受輸入，例如 `<int:pk>` 收到文字 |
| 404 | Detail View 找不到符合的物件 |
| 500 | View 執行時發生未處理例外，或沒有回傳 response |
| 500 | template 或資料存取發生未處理的錯誤 |

語法或 import 錯誤也可能讓伺服器無法啟動，
此時不一定收到 HTTP 500，應先查看終端機。

開發模式的 traceback 是除錯線索，正式環境不可公開。

---

## E-20 按順序排除常見問題

| 現象 | 先檢查 |
|---|---|
| 找不到 `manage.py` | 終端機是否在 `django_lab/` |
| 找不到 Django | `uv run python -m django --version` 是否成功 |
| 瀏覽器連不上 | 伺服器仍在運作嗎？網址及 port 相同嗎？ |
| `/hello/` 得到 404 | 根 `include`、app 的 route、結尾斜線 |
| TypeError：參數不符 | converter 的變數名是否等於 View 參數名 |
| NoReverseMatch | namespace、name 與參數是否一致 |

先讀 traceback 最後一行的例外，再找自己程式的檔案與行號。
一次修改一個原因，重新測同一網址，確認結果有改變。

---

## E-21 把驗收寫進 tests.py

**把 `pages/tests.py` 改成以下內容：**

```python
from django.test import SimpleTestCase
from django.urls import reverse


class PageTests(SimpleTestCase):
    def test_hello(self):
        response = self.client.get(reverse("pages:hello"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode(), "Hello Django")
        self.assertTrue(response["Content-Type"].startswith("text/plain"))
```

`self.client` 模擬請求，不需要先開 `runserver`。
這些頁面不使用資料庫，因此選擇 `SimpleTestCase`。

---

## E-22 再確認動態網址、query 與 404

**接在同一個 `PageTests` 類別內，保留四格縮排：**

```python
    def test_name_and_reverse(self):
        url = reverse("pages:hello-name", kwargs={"name": "Ada"})
        self.assertEqual(url, "/hello/Ada/")
        self.assertContains(self.client.get(url), "歡迎 Ada")

    def test_search(self):
        response = self.client.get(reverse("pages:search"), {"q": "django"})
        self.assertContains(response, "查詢：django")

    def test_missing_url(self):
        self.assertEqual(self.client.get("/missing/").status_code, 404)
```

執行 `uv run python manage.py test pages`，應顯示 4 個測試通過。

---

## E-23 先完成自己的練習，再進行專案對照

1. 從空資料夾完成 uv、Python、Django、project 與 app。
2. 指出 `.venv`、鎖檔、Git、settings、migration 的用途。
3. 完成 `/hello/`、`/hello/Ada/`、`/search/?q=django`。
4. 用 Network 記錄成功的 200 與不存在路徑的 404。
5. 用 `reverse()` 產生網址，並讓 4 個測試通過。
6. 畫出 root URL、app URL、View、response 的流程。

**加練：** 把 `hello/` 改成 `greeting/`，保留名稱 `hello`，
觀察 `reverse("pages:hello")` 與使用該名稱的測試如何跟著改變。
完成後將路徑改回來，再保存一個 Git commit。

---

## F-1 現在才打開 LearnBoard × LearnMart

先對照自己的 `django_lab`，辨認相同職責的檔案：

| 角色 | 你的練習 | LearnBoard | LearnMart |
|---|---|---|---|
| 外層資料夾 | `django_lab/` | `learnboard/` | `learnmart/` |
| Django project | `config/` | `config/` | `config/` |
| 功能 app | `pages/` | `board/` | `marketplace/` |
| 第一個頁面 | 打招呼文字 | 留言列表 | 商品列表 |
| 根路由轉交 | `pages.urls` | `board.urls` | `marketplace.urls` |

完成專案多了 model、form、template、權限與測試，逐步找相同角色即可。
本教材前半段的 `hello` / `search` 是練習範例，沒有加進完成專案。

---

## F-2 教材根目錄與 Django 應用根目錄

```text
DjangoTeaching/          目前整份教材的 Git repository
├── .git/
├── slides/
├── learnboard/          執行 LearnBoard 指令的位置
│   ├── pyproject.toml
│   └── manage.py
└── learnmart/           執行 LearnMart 指令的位置
    ├── pyproject.toml
    └── manage.py
```

日常說的「專案」可能指整份版本庫，也可能指一個應用資料夾。
本教材目前由外層 `.git/` 管理，兩個應用不用再各自 `git init`。
執行 Django 指令時，先確認當前目錄同時有 `manage.py` 與 `pyproject.toml`。

---

## F-3 環境對照：共同版本與 Pillow 差異

**實際檔案：`learnboard/pyproject.toml` 與 `learnmart/pyproject.toml`。**

| 項目 | LearnBoard | LearnMart |
|---|---|---|
| `.python-version` | `3.13` | `3.13` |
| `requires-python` | `>=3.13` | `>=3.13` |
| Django | `django>=5.2,<5.3` | `django>=5.2,<5.3` |
| 圖片套件 | 無 Pillow 依賴 | `pillow>=11.0` |
| 開發群組 | `coverage>=7.6` | `coverage>=7.6` |
| uv 設定 | `package = false` | `package = false` |

LearnBoard 沒有圖片上傳功能，LearnMart 的 `ImageField` 需要 Pillow。
兩者各有自己的 `.venv/` 與 `uv.lock`，不要互相複製虛擬環境。

---

## F-4 實際 TOML 節錄可以這樣讀

**LearnBoard 的 `[project]` 依賴節錄：**

```toml
[project]
name = "learnboard"
requires-python = ">=3.13"
dependencies = ["django>=5.2,<5.3"]
```

**LearnMart 的 `[project]` 依賴節錄：**

```toml
[project]
name = "learnmart"
requires-python = ">=3.13"
dependencies = ["django>=5.2,<5.3", "pillow>=11.0"]
```

這是兩份檔案的節錄，不能把兩個 `[project]` 合貼到同一份檔案。

---

## F-5 settings 對照：先找共同設定

| 設定 | 兩個完成專案的共同做法 |
|---|---|
| `ROOT_URLCONF` | `config.urls` |
| `DATABASES` | SQLite，應用根目錄的 `db.sqlite3` |
| `TEMPLATES` | `DIRS` 指定根 `templates/`，`APP_DIRS=True` |
| 語言／時區 | `zh-hant`、`Asia/Taipei` |
| 靜態資源 | `STATICFILES_DIRS = [BASE_DIR / "static"]` |
| 本機開發 | `DEBUG=True`，Host 允許 localhost 與 127.0.0.1 |

內建 middleware、密碼驗證器與入口檔案也能找到相同職責。
兩份 `SECRET_KEY` 都是課堂示例，不能沿用到公開正式環境。

---

## F-6 settings 對照：功能增加後的差異

| 項目 | LearnBoard | LearnMart |
|---|---|---|
| App 註冊 | `board` | `marketplace` |
| User model | Django 預設 User | `AUTH_USER_MODEL = "marketplace.User"` |
| 登入／登出導向 | `board:list` | `marketplace:home` |
| 上傳檔案 | 無 media 設定 | `MEDIA_URL`、`MEDIA_ROOT` |
| 額外 context processor | 無購物車處理 | `marketplace.context_processors.cart_count` |

兩者 `LOGIN_URL` 都是 `login`，`MESSAGE_TAGS` 把錯誤訊息標籤對應為 `danger`。
自訂 User 已在完成專案的 migration 設計內，照既有檔案執行即可。
不要在已建立資料表的練習隨意切換 `AUTH_USER_MODEL`。

---

## F-7 建立指令：完成專案只讀取，不再重跑

對照你剛才使用的指令，理解兩個完成專案的骨架建立方式：

```bash
# LearnBoard 骨架的等價建立指令（只供對照）
uv run django-admin startproject config .
uv run python manage.py startapp board

# LearnMart 骨架的等價建立指令（只供對照）
uv run django-admin startproject config .
uv run python manage.py startapp marketplace
```

這些指令只產生骨架，不會自動產生完整商城或留言板。
`urls.py`、`forms.py`、templates、示範資料 command 都是後續實作。
既有資料夾已建立完成，下一頁改走「同步與啟動」流程。

---

## F-8 從完成專案啟動

在選定的專案根目錄依序執行（兩個專案指令相同）：

```bash
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver
```

四行分別影響：

1. Python 環境與依賴
2. 資料庫 schema
3. 課堂示範資料
4. 本機開發伺服器

不要把 `uv sync` 與 `migrate` 混為一談：前者管套件，後者管資料庫。

---

## F-9 `seed_demo` 建立哪些資料？

**目前專案實作｜`*/management/commands/seed_demo.py`**

在**沒有同名帳號的新資料庫**第一次執行時：

| 專案 | 示範帳號與資料 |
|---|---|
| LearnBoard | `alice / alice12345`、`bob / bob12345`；4 則留言，其中 1 則是訪客 |
| LearnMart | `seller / seller12345`、`buyer / buyer12345`；3 個分類、6 個商品、1 則留言 |

`get_or_create()` 讓重跑不會持續新增同名示範 rows；若帳號已存在，兩個 command 都**不會重設既有 password、role 或 email**，所以它們不是 reset command。

> **常見錯誤：** 終端機雖會再次印出課堂 credentials，既有同名帳號仍維持原本資料。這些帳號也只限本機課堂，不可沿用到公開環境。

---

## F-10 預覽完成專案並記錄結果

執行 `runserver` 後：

```text
Starting development server at http://127.0.0.1:8000/
```

- 瀏覽器開啟該網址會看到 LearnBoard 留言牆或 LearnMart 商品頁
- 終端機保持被伺服器占用，按 `Ctrl+C` 停止
- 修改 Python 檔通常會觸發自動重新載入
- 這是開發伺服器，不是正式部署伺服器

`127.0.0.1` 代表自己的電腦；`8000` 是 port。

---

## F-11 URL、View 與反向解析的實際對照

| 項目 | LearnBoard | LearnMart |
|---|---|---|
| 根 URL | `include("board.urls")` | `include("marketplace.urls")` |
| `app_name` | `board` | `marketplace` |
| 首頁 route | `""` | `""` |
| 首頁 View | `MessageListView.as_view()` | `ProductListView.as_view()` |
| 首頁名稱 | `board:list` | `marketplace:home` |

兩者根 URL 都保留 admin、登入與登出路由。
`as_view()` 把 class-based View 轉成可呼叫的 View，後續章節再深入。
你寫的函式 View 與這些 View，都遵守接收 request、回傳 response 的約定。

---

## F-12 對照動態路由與反向產生網址

**LearnMart 的 `marketplace/urls.py` 節錄：**

```python
path("products/<int:pk>/", views.ProductDetailView.as_view(),
     name="product-detail")
```

```python
reverse("marketplace:home")                         # '/'
reverse("marketplace:product-detail", kwargs={"pk": 3})  # '/products/3/'
```

```django
{% url 'marketplace:product-detail' product.pk %}
```

LearnBoard 也以 `<int:pk>` 定位要編輯或刪除的留言。
成功產生網址不保證那筆資料存在，物件不存在時仍可能回應 404。

---

## F-13 從文字回應走向資料頁

![w:1120](../assets/request_flow.svg)

圖中以 `product_detail(request, pk)` 示意；LearnMart 實際使用 `ProductDetailView.as_view()`。

---

## F-14 從自己的最小流程擴充到完整頁面

| 層次 | `django_lab` | 完成專案 |
|---|---|---|
| URL | 指向 `hello` | 指向留言／商品 View |
| View | 建立文字 response | 取得資料並準備頁面內容 |
| Model | 此次沒有使用 | `Message`、`Product` 等資料模型 |
| Template | 此次沒有使用 | HTML 頁面與反向 URL 標籤 |
| Response | 純文字 body | 通常是 HTML body |

MVT 分別是 Model、View、Template。
前頁圖是較完整的資料頁流程，用來和 `/hello/` 比較，
不是宣稱每個請求都必須走過 Model 與 Template。

---

## F-15 專案對照實作：先找檔案，再說明理由

1. 分別啟動兩個專案，記錄環境同步、migration、seed、預覽結果。
2. 找出 `config/urls.py`、app 的 `urls.py` 與首頁 View。
3. 在兩個專案各用 shell 執行首頁的 `reverse()`，確認皆為 `/`。
4. 說明相同 `/` 為何顯示不同頁面，以及各自用了哪份 settings。
5. 比較 TOML、app 註冊、User、media、context processor。
6. 在新資料庫比對示範資料筆數，重跑 seed 後說明哪些值不會重設。

依序測試時先用 `Ctrl+C` 停止前一個伺服器。
若要同時看兩個網站，可讓第二個使用 8001，注意 cookie 仍可能互相影響。

---

## F-16 兩個首頁目前各自做了哪些事？

這一頁只描述目前完成專案，不是要你立刻仿寫所有 class-based View。

| 首頁責任 | LearnBoard | LearnMart |
|---|---|---|
| View | `MessageListView` | `ProductListView` |
| 基礎資料 | `Message`，並預先取得 `author` | 啟用的 `Product`，並預先取得列表卡片所需關聯 |
| URL 狀態 | `q`：留言文字搜尋 | `q`：文字搜尋；`category`：分類篩選 |
| Template | `board/message_list.html` | `marketplace/home.html` |
| 列表 UI | 留言卡、作者、時間、分頁 | 商品卡、圖片 fallback、分類、分頁 |

兩者都是「URL → View 讀取 `request.GET` → QuerySet → context → template」；差別在領域資料與篩選規則。
第 3 到第 6 章再拆開 Template、Model、ORM 與列表頁的細節。

---

## F-17 從一個 `Message` 到商城的關聯圖

| 觀察角度 | LearnBoard | LearnMart |
|---|---|---|
| 最小資料核心 | `Message` 的作者、內容、建立時間 | `Product` 的分類、賣家、價格、庫存與圖片 |
| 關聯複雜度 | 一則留言對應一位作者 | 商品還會連到購物車、訂單明細與評價 |
| 專案特有需求 | 作者顯示與留言搜尋 | 自訂 User、圖片處理、分類篩選與購買歷史 |
| 為何要先學小專案 | 能清楚追一筆資料如何顯示 | 再把同一條資料流延伸到多個關聯與規則 |

不要把兩個 model 硬湊成同一份 class。先找出各自的資料責任，才能正確判斷要用 `select_related`、`prefetch_related`、constraint 或 migration 的時機。

---

## F-18 專案版教材如何接續使用

本份整合教材是**共通講解的唯一來源**。需要實作時，再依下列檔案查閱各專案的專屬補充：

| 要觀察的內容 | LearnBoard | LearnMart |
|---|---|---|
| 首頁與搜尋 | `board/views.py`、`templates/board/message_list.html` | `marketplace/views.py`、`templates/marketplace/home.html` |
| 資料模型 | `board/models.py` 與 migrations | `marketplace/models.py` 與 migrations |
| 前端樣式／資產 | `static/css/site.css` | `static/css/site.css`、`media/` 與商品圖片 |
| 專案版投影片 | `learnboard_01_*` | `learnmart_01_*` |

專案版投影片只保留上述實作差異；uv、Django 骨架、HTTP、Template、migration 與 ORM 的共通原理，以本份教材為準，避免三份投影片講出不同版本的同一件事。

---

## F-19 觀念檢核：環境與啟動

1. `.venv` 與 `uv.lock` 各解決什麼問題？
2. 為什麼 `uv sync` 不會建立 Django 資料表？
3. `django>=5.2,<5.3` 接受哪些版本？
4. `uv run python manage.py seed_demo` 中，誰選環境？誰是專案入口？
5. 為什麼 `runserver` 成功還不代表可正式部署？

**繳交：** 自己的環境檢查結果，以及兩個完成專案的啟動紀錄。

配套手冊：[LearnBoard 第 1 章](../workbooks/learnboard_01_django_foundations_and_message_board_workbook.md#chapter-1)、[LearnMart 第 1 章](../workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md#chapter-1)。
手冊仍沿用原章號，請在完成本份練習後作對照。

---

## F-20 觀念檢核：URL 與 request flow

1. `/products/3/?q=django` 中，URLconf 主要比對哪個部分？
2. `path()` 的 route、view、name 各負責什麼？
3. `<int:pk>` 如何和 View 參數連接？
4. 為什麼原始 `HttpResponse(f"{name}")` 沒有 template escaping？
5. 404 與 500 分別可能發生在哪裡？如何區分啟動失敗？

**繳交：** 命名路由、200 / 404 紀錄、reverse 結果、測試與流程圖。

配套手冊：[LearnBoard 第 2 章](../workbooks/learnboard_01_django_foundations_and_message_board_workbook.md#chapter-2)、[LearnMart 第 2 章](../workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md#chapter-2)。
接續原第 3 章起的 Model、ORM 與 Template 等內容。

---

## 查閱來源

- [uv 安裝](https://docs.astral.sh/uv/getting-started/installation/)、[專案操作](https://docs.astral.sh/uv/guides/projects/)、[專案檔案結構](https://docs.astral.sh/uv/concepts/projects/layout/)
- [Django 5.2 入門第一部分](https://docs.djangoproject.com/en/5.2/intro/tutorial01/)
- [Django 命令列工具](https://docs.djangoproject.com/en/5.2/ref/django-admin/)
- [Django URL dispatcher](https://docs.djangoproject.com/en/5.2/topics/http/urls/)

教學實作採用本份 `django_lab` 範例；F 段才是既有專案實際對照。
安裝、指令及路由觀念已依官方文件核對。
