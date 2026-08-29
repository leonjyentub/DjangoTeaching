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

# 第 1 章
## Python 執行環境與 uv

**本章成果：**理解「哪一個 Python、哪些套件、哪一份鎖檔」如何讓每位同學跑出相同環境。

<!--
授課提示：本章適合指定為課前自學。語法細節請搭配先備教材 00a 第 1 章；課堂只抽考五個名詞與三個環境檔案。
-->

---

## 1-1 終端機目前在哪裡？

執行專案指令前，先確認工作目錄：

```bash
pwd
ls
```

先進入你取得／clone 的專案，再確認根目錄：

```text
<你的路徑>/learnboard/
├── manage.py
├── pyproject.toml
├── config/
└── board/
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
授課提示：快問快答：「鎖檔和虛擬環境哪個負責精確重現？」此題是階段末常見題。
-->

---

## 1-3 沒有虛擬環境會發生什麼？

想像兩個專案：

- 專案 A 需要 Django 4.2
- LearnBoard 需要 Django 5.2

若都安裝到同一個系統 Python，升級其中一個可能讓另一個壞掉。

虛擬環境把套件放在專案自己的 `.venv/`：

```text
系統 Python
├── 專案 A/.venv/     → Django 4.2
└── LearnBoard/.venv/ → Django 5.2
```

`.venv/` 可重建，所以不提交版本控制。

---

## 1-4 uv 在本專案扮演什麼角色？

```bash
uv sync                        # 依 pyproject.toml + uv.lock 建立 .venv
uv run python manage.py ...   # 用 .venv 的 python 執行指令
```

- `uv sync`：讀鎖檔，把 `.venv/` 建到與紀錄完全一致
- `uv run`：確保指令用的是 `.venv/` 裡的 interpreter，不是系統 Python
- 不需要手動 `source .venv/bin/activate`

> **你應該看到：**`uv sync` 列出安裝的套件（django、sqlparse…）；`uv run python -V` 顯示 3.13.x。

---

## 1-5 三個環境檔案各管什麼？

| 檔案 | 角色 | 會 commit 嗎 |
|---|---|---|
| `.python-version` | 指定 Python 版本（3.13） | 會 |
| `pyproject.toml` | 宣告專案與直接依賴範圍 | 會 |
| `uv.lock` | 鎖定全部依賴的精確版本 | 會 |

`.venv/` 是三者重建出來的結果，不 commit。

LearnBoard 只依賴 `django>=5.2,<5.3`——比商城少了 Pillow，因為留言板沒有圖片上傳。

---

## 1-6 從既有 repository 啟動

```bash
uv sync                          # 1. 建 .venv（套件層）
uv run python manage.py migrate # 2. 建資料表（schema 層）
uv run python manage.py seed_demo # 3. 建示範帳號與留言（資料層）
uv run python manage.py runserver # 4. 啟動開發伺服器
```

每一層各司其職：套件、schema、資料、伺服器。任何一層失敗，錯誤訊息都會指出是哪一層。

**示範帳號：`alice` / `alice12345`、`bob` / `bob12345`**

---

## 1-7 你應該看到什麼？

瀏覽 `http://127.0.0.1:8000/`：

- 深藍色導覽列，品牌文字「學言板 LearnBoard」
- 一面留言牆，列出 seed_demo 建立的四則留言（含一則「訪客」）
- 右上角有「登入」「免費註冊」按鈕

終端機：

```text
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

> 目前你還不能發文——因為還沒有表單與帳號機制。這正是 Deck 02 的主題。

---

## 第 1 章｜觀念檢核與實作

**觀念檢核：**

1. `.venv` 與 `uv.lock` 各解決什麼問題？
2. 為什麼 `uv sync` 之後還要 `migrate`？
3. `django>=5.2,<5.3` 接受哪些版本？
4. `seed_demo` 做了哪些事？它會重設已存在的帳號密碼嗎？

**實作任務：**從空白本機狀態完成 1-6 的四步啟動，並截圖留言牆。

→ 步驟與解答在配套手冊第 1 章。
