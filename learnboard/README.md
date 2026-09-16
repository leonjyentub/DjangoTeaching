# 學言 LearnBoard

一個為學期前半段後端網站程式設計課打造的 Django 教學留言板。課程分兩階段：先用這個最小的個人留言板走完全套基本功（帳號、資料庫設計、版面設計、權限），再進入第二階段的 [學購 LearnMart](../learnmart/) 商城專案。

## 技術選擇

- Python 3.14.7，由 uv 管理 `.venv`、依賴與 `uv.lock`
- Django 6.1.1
- SQLite
- Bootstrap 5.3 CDN + 少量自訂 CSS，採 mobile-first RWD
- 共用根目錄 `../slides/` 的 Marp 教材與配套實作手冊
- 根目錄教材同時對照 LearnBoard 與 LearnMart，並保留本專案的分章版本

刻意不使用 Pillow／自訂 User model／圖片上傳——把第一階段的程式碼壓到最小，商城階段再逐項加回。

## 快速開始

```bash
cd /path/to/learnboard
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver
```

`manage.py` 與 `pyproject.toml` 所在目錄就是專案根目錄。瀏覽 `http://127.0.0.1:8000/`。

全新資料庫第一次執行 `seed_demo` 時會建立示範帳號：

- alice / `alice12345`
- bob / `bob12345`

若同名帳號已存在，`seed_demo` 不會重設其密碼或 email；它不是帳號重設指令。示範帳號僅供本機教學，請勿沿用到公開環境。建立自己的後台帳號：

```bash
uv run python manage.py createsuperuser
```

## 已實作功能

- Django auth 註冊、登入、POST 登出與密碼雜湊
- 留言牆列表、關鍵字搜尋、分頁
- 登入使用者發布留言（ModelForm＋CSRF＋PRG）
- 只能編輯自己的留言（QuerySet 過濾 → 404）
- 作者本人或 staff 可刪除留言（UserPassesTestMixin → 403）
- 訪客留言保留顯示（author SET_NULL 的 migration 演進）
- messages framework 提示訊息、「已編輯」徽章
- Django admin 與基礎流程測試（9 個 test methods）
- Bootstrap mobile-first RWD

## 專案結構

```text
learnboard/
├── config/                 # Project：settings、根路由、ASGI/WSGI
├── board/                  # App：model、view、form、URL、admin、tests
│   ├── migrations/         # 0001 建表 → 0002 加 author（教學用的演進化石）
│   └── management/commands/seed_demo.py
├── templates/              # base、registration、留言牆頁面
├── static/css/site.css
├── manage.py
├── pyproject.toml
└── .python-version
```

## 教材主題地圖

課程不綁定固定週次，而是依概念先備關係分成「先備自學」與兩份主教材。建議順序：Python 先備 → HTML/CSS 先備 → Deck 01 → Deck 02：

| 教材 | 形式 | 性質 | 主題章節 | 完成里程碑 |
|---|---|---|---|---|
| [Python 語法先備](../slides/00_python_syntax_essentials/00_python_syntax_essentials.md) | 單一 Marp | 先備自學 | Python 基礎、類別、繼承、decorator、型別標註 | 讀得懂三個專案的 Python |
| [HTML/CSS 先備](../slides/00_html_css_page_basics/00_html_css_page_basics.md) | 單一 Marp | 先備自學 | HTML、表單、CSS、box model、RWD、base.html | 能讀懂模板與 Bootstrap class |
| [01 Django 共通基礎](../slides/01_django_foundations_and_two_projects/01_django_foundations_and_two_projects.md) | 單一整合 Marp | 共用主教材 | Project/App、HTTP／URL、View／Template、Model／migration、ORM、留言牆與商品目錄 | 能從請求追到資料庫與模板 |
| [02 表單、身份驗證與工作流程](../slides/02_forms_auth_and_two_projects/00_overview.md) | 7 章分檔 | 共用主教材 | Form、登入、ownership、購物車、訂單、交易、安全、測試 | 完成兩個專案的流程對照 |

LearnBoard 自己的原始分章教材仍保留為 6 章版本：

- [`learnboard_01_django_foundations_and_message_board/`](../slides/learnboard_01_django_foundations_and_message_board/)
- [`learnboard_02_forms_auth_and_board_workflows/`](../slides/learnboard_02_forms_auth_and_board_workflows/)

完成 Deck 02 後即可用 [LearnMart 原始分章教材](../slides/learnmart_01_django_foundations_and_data_backed_catalog/00_overview.md) 對照第二階段。

## 投影片與實作手冊

教材目前同時存在「單一 Marp」與「分章版」，不要假設每個資料夾都有 `00_overview.md`。完整現況可參考 [`../slides/SOURCE_MAP.md`](../slides/SOURCE_MAP.md)。概念題解答、實作步驟與程式碼節錄放在 `../slides/workbooks/`：

- `../slides/00_python_syntax_essentials/00_python_syntax_essentials.md`
- `../slides/00_html_css_page_basics/00_html_css_page_basics.md`
- `../slides/learnboard_01_django_foundations_and_message_board/`
- `../slides/workbooks/learnboard_01_django_foundations_and_message_board_workbook.md`
- `../slides/learnboard_02_forms_auth_and_board_workflows/`
- `../slides/workbooks/learnboard_02_forms_auth_and_board_workflows_workbook.md`

圖解資產：`../slides/assets/*.svg`，重製提示詞見 `../slides/diagram_prompts.md`。教材 CSS 與 SVG 使用繁中字型鏈。

手冊內的程式碼是課堂練習指引，不代表所有練習都已預先套用到目前的 Django 原始碼。重點頁含 `<!-- 授課提示 -->` 講者備註（Marp 簡報模式可見）。

若已安裝 Marp CLI，可在 workspace 根目錄匯出：

```bash
marp ../slides/00_python_syntax_essentials/00_python_syntax_essentials.md --pdf
marp ../slides/01_django_foundations_and_two_projects/01_django_foundations_and_two_projects.md --pdf
marp ../slides/02_forms_auth_and_two_projects/01_chapter_01.md --pdf
```

## 驗證

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

## 教學設計說明

留言板刻意選擇「最小但完整」的功能集：一個 Message model、四個頁面、九個 test methods。資料庫設計以兩段式 migration 示範 schema 演進（先有留言、後加作者）；權限教學區分「登入門禁」（authentication）與「物件擁有權」（authorization）兩層，並讓 404 與 403 各自對應一段程式碼。所有概念在第二階段商城都有直接對應——Message 對 Product、擁有權 mixin 對賣家權限、發文表單對商品上架——學生遇到困難時永遠可以回到小專案找原型。

這是教學版，不應直接當正式服務上線。正式環境還需要環境變數管理 SECRET_KEY、HTTPS、DEBUG=False、rate limit、帳號鎖定與稽核 log。

## 主要參考資料

- [Django 6.1.1 官方文件](https://docs.djangoproject.com/en/6.1/)
- [Django 官方入門教學](https://docs.djangoproject.com/en/6.1/intro/tutorial01/)
- [Django Authentication](https://docs.djangoproject.com/en/6.1/topics/auth/)
- [Django Forms](https://docs.djangoproject.com/en/6.1/topics/forms/)
- [Django Class-based views](https://docs.djangoproject.com/en/6.1/topics/class-based-views/)
- [Django Migrations](https://docs.djangoproject.com/en/6.1/topics/migrations/)
- [Django Testing](https://docs.djangoproject.com/en/6.1/topics/testing/)
- [uv Projects](https://docs.astral.sh/uv/guides/projects/)
- [Bootstrap 5.3 Introduction](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Marp](https://marp.app/)

教材的概念排序也參照常見 Django 專書由小型頁面逐步走向資料模型、表單、帳號與測試的「learning by doing」安排，但程式碼與文字均為本專案重新設計。
