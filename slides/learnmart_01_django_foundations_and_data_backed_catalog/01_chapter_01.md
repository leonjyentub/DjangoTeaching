---
marp: true
theme: default
size: 16:9
paginate: true
header: "LearnMart 01｜Django 基礎與資料驅動商品目錄"
footer: "初學者教材｜觀念 → 語法 → LearnMart 實作"
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

# 第 1 章
## Python 執行環境與 uv

**本章成果：**理解「哪一個 Python、哪些套件、哪一份鎖檔」如何讓每位同學跑出相同環境。

<!--
授課提示：本章適合指定為課前自學。課堂只抽考 1-2（五個名詞）、1-7（三個環境檔案）與 1-9（版本條件）。
-->

---

## 1-1 終端機目前在哪裡？

執行專案指令前，先確認工作目錄：

```bash
pwd
ls
```

先進入你 clone／取得的專案，再確認根目錄：

```text
<你的路徑>/learnmart/
├── manage.py
├── pyproject.toml
├── config/
└── marketplace/
```

真正判斷依據是同時看見 `manage.py` 與 `pyproject.toml`，不是照抄講師電腦的絕對路徑。

> **常見錯誤：**相同指令在不同目錄執行，可能載入另一份設定，或完全找不到專案。

---

## 1-2 先分清楚五個名詞

| 名詞 | 在本課程中的意思 |
|---|---|
| Python interpreter | 真正執行 `.py` 程式的 Python |
| package | 可安裝、可 import 的程式，例如 Django |
| dependency | 這個專案需要的 package |
| virtual environment | 專案專用的 package 安裝空間，通常是 `.venv/` |
| lockfile | 記錄解析後精確版本，本專案是 `uv.lock` |

**虛擬環境負責隔離；鎖檔才負責精確重現。**兩者不是同一件事。

<!--
授課提示：快問快答：「鎖檔和虛擬環境哪個負責精確重現？」此題是期末常見題。
-->

---

## 1-3 沒有虛擬環境會發生什麼？

想像兩個專案：

- 專案 A 需要 Django 4.2
- LearnMart 需要 Django 5.2

若都安裝到同一個系統 Python，升級其中一個可能讓另一個壞掉。

虛擬環境把套件放在專案自己的 `.venv/`：

```text
系統 Python
├── 專案 A/.venv/  → Django 4.2
└── LearnMart/.venv/ → Django 5.2
```

`.venv/` 可重建，所以不提交版本控制。

---

## 1-4 傳統 venv：先理解底層概念

**教學用最小範例｜POSIX shell（Linux／macOS）**

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install django
```

- 第一行建立 `.venv/`；第二行讓目前 shell 優先使用其中的 Python
- 第三行把 Django 安裝進目前 interpreter 的環境
- activation 只影響目前終端機工作階段

**補充／進階：**PowerShell activation 通常使用 `.venv\\Scripts\\Activate.ps1`；若課程平台提供預建 terminal，依平台指示即可。本課程使用 `uv run`，通常不必手動 activate。

---

## 1-5 `python -m` 到底是什麼？

```bash
python -m pip install django
```

可拆成：

- `python`：選定一個 Python interpreter
- `-m pip`：請這個 interpreter 尋找並執行 `pip` 模組
- 後面是傳給 pip 的參數

這比直接打 `pip` 更清楚，因為它明確表示：

> 「使用**這一個 Python**所屬的 pip。」

同理，`python -m django --version` 也是由指定 interpreter 執行 Django 模組。

---

## 1-6 uv 在本專案扮演什麼角色？

uv 會協助：

- 讀取 `.python-version` 與 `pyproject.toml`
- 建立或同步 `.venv/`
- 解析並使用 `uv.lock`
- 透過 `uv run` 在專案環境中執行命令

```bash
uv sync
uv run python --version
uv run django-admin --version
```

`uv run` 的重點不是「另一種 Python 語法」，而是先選對專案環境，再執行後面的命令。

---

## 1-7 三個環境檔案各管什麼？

```text
.python-version   希望使用的 Python 版本（本專案：3.13）
pyproject.toml    專案直接宣告的需求與允許版本範圍
uv.lock           uv 解析後的完整、精確依賴結果
```

- 修改直接依賴：通常編輯 `pyproject.toml`，再讓 uv 更新鎖檔
- 不要把 `uv.lock` 當成手寫套件清單
- 不要提交 `.venv/`；其他人可由上述檔案重建

---

## 1-8 讀懂 `pyproject.toml` 的基本 TOML

**目前 LearnMart 節錄｜`pyproject.toml` 節錄**

```toml
[project]
name = "learnmart"
requires-python = ">=3.13"
dependencies = [
    "django>=5.2,<5.3",
    "pillow>=11.0",
]
```

- `[project]`：一個 TOML table
- `name = "..."`：key 與字串 value
- `dependencies = [...]`：字串陣列
- 逗號分隔陣列項目；最後一項也可保留逗號

---

## 1-9 版本條件怎麼讀？

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

## 1-10 直接依賴與開發依賴

**目前 LearnMart 節錄｜`pyproject.toml`**

```toml
[dependency-groups]
dev = [
    "coverage>=7.6",
]

[tool.uv]
package = false
```

- Django、Pillow 是應用執行需要的 dependency
- Coverage 放在 `dev` 群組，主要供開發與檢查
- `package = false` 表示此 repository 當作應用專案，不把 LearnMart 自身建成可發布 Python package

---

## 1-11 從既有 repository 啟動

在專案根目錄依序執行：

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

<!--
授課提示：現場跑一次四行指令；刻意先在錯誤目錄執行 uv sync，讓學生看到找不到專案的錯誤長相。
-->

---

## 1-12 `seed_demo` 會建立什麼？

**目前 LearnMart 節錄｜`marketplace/management/commands/seed_demo.py`**

在**沒有同名帳號的新資料庫**第一次執行時，會建立：

- 賣家：`seller / seller12345`
- 買家：`buyer / buyer12345`
- 3 個分類、6 個商品、1 則留言

`get_or_create()` 讓重跑不會持續新增同名示範 rows；但若 `seller`／`buyer` 已存在，command **不會重設其 password、role 或 email**，所以它不是 reset command。

> **常見錯誤：**終端機雖會再次印出課堂 credentials，既有同名帳號仍維持原本資料。這些帳號也只限本機課堂，不可沿用到公開環境。

---

## 1-13 你應該看到什麼？

執行 `runserver` 後：

```text
Starting development server at http://127.0.0.1:8000/
```

- 瀏覽器開啟該網址會看到商品頁
- 終端機保持被伺服器占用，按 `Ctrl+C` 停止
- 修改 Python 檔通常會觸發自動重新載入
- 這是開發伺服器，不是正式部署伺服器

`127.0.0.1` 代表自己的電腦；`8000` 是 port。

---

## 第 1 章｜觀念檢核與實作

1. `.venv` 與 `uv.lock` 各解決什麼問題？
2. 為什麼 `uv sync` 不會建立 Django 資料表？
3. `django>=5.2,<5.3` 接受哪些版本？
4. `uv run python manage.py seed_demo` 中，誰負責選環境？誰是 Django 指令入口？
5. 為什麼 `runserver` 成功仍不代表 production ready？

**實作任務：**從專案根目錄完成同步、migration、示範資料與啟動，記錄每步可觀察結果。

**配套實作手冊：**[第 1 章答案與步驟](../workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md#chapter-1)

<!--
授課提示：建議當 10 分鐘隨堂筆試；解答在 workbook 對應章節，驗收以完成檢查表為準。
-->
