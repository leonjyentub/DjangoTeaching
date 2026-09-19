# 學購 LearnMart

一個為學期前半段後端網站程式設計課打造的 Django 教學商城。介面借鏡大型購物平台的資訊架構，但不複製品牌素材；以可讀、可拆解、可逐週擴充為優先。

## 技術選擇

- Python 3.14.7，由 uv 管理 `.venv`、依賴與 `uv.lock`
- Django 6.1.1
- SQLite
- Pillow（商品圖片）
- Bootstrap 5.3 CDN + 少量自訂 CSS，採 mobile-first RWD
- 共用根目錄 `../slides/` 的 Marp 教材與配套實作手冊
- 五張教學 SVG 圖解

Bootstrap 適合這門入門課，因為不需 Node/Sass 建置就能從 CDN 開始，且 grid、navbar、card、form 都能逐步拆解。專案仍保留 `static/css/site.css`，讓學生練習在框架之上建立自己的視覺語言。

## 快速開始

```bash
cd /path/to/learnmart
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver
```

`manage.py` 與 `pyproject.toml` 所在目錄就是專案根目錄。瀏覽 `http://127.0.0.1:8000/`。

## 前置課程：LearnBoard 留言板

本專案是課程的**第二階段**。第一階段是姊妹專案 [LearnBoard 學言板](../learnboard/)——一個功能完整的個人留言板教學專案，涵蓋帳號、資料庫設計、版面設計與擁有權權限：

- 先備自學教材位於 `../slides/00_python_syntax_essentials/` 與 `../slides/00_html_css_page_basics/`
- LearnBoard／LearnMart 的原始分章版本與共用整合版本都整理於 `../slides/`
- 本專案的商城章節可從共用 Deck 01／02 與 LearnMart 原始分章教材交叉對照

全新資料庫第一次執行 `seed_demo` 時會建立示範帳號：

- 賣家：`seller` / `seller12345`
- 買家：`buyer` / `buyer12345`

若同名帳號已存在，`seed_demo` 不會重設其密碼、身份或 email；它不是帳號重設指令。示範帳號僅供本機教學，請勿沿用到公開環境。建立自己的後台帳號：

```bash
uv run python manage.py createsuperuser
```

## 已實作功能

- Django auth 註冊、登入、POST 登出與密碼雜湊
- 買家／賣家身份與賣家權限 mixin
- 商品列表、分類、關鍵字搜尋、詳情、圖片上傳
- 賣家商品新增與編輯（只可編輯自己的商品）
- 購物車新增、更新、移除與庫存檢查
- transaction 結帳、訂單／明細快照、扣庫存
- 買家訂單列表與詳情
- 賣家訂單列表與出貨確認
- 已購買且已出貨商品的 1–5 星評分
- 登入使用者留言板
- Django admin 與基礎流程測試
- Bootstrap mobile-first RWD

## 專案結構

```text
learnmart/
├── config/                 # Project：settings、根路由、ASGI/WSGI
├── marketplace/            # App：model、view、form、URL、admin、tests
│   └── management/commands/seed_demo.py
├── templates/              # base、registration、商城頁面
├── static/css/site.css
├── manage.py
├── pyproject.toml
└── .python-version
```

## 教材主題地圖

課程不綁定固定週次，而是依概念先備關係分成「先備自學」與主教材。建議順序：Python 先備 → HTML/CSS 先備 → Django 連續教學教材（LearnBoard 案例 → LearnMart 案例）：

| 教材 | 形式 | 性質 | 主題章節 | 完成里程碑 |
|---|---|---|---|---|
| [Python 語法先備](../slides/00_python_syntax_essentials/00_python_syntax_essentials.md) | 單一 Marp | 先備自學 | Python 基礎、類別、繼承、decorator、型別標註 | 讀得懂三個專案的 Python |
| [HTML/CSS 先備](../slides/00_html_css_page_basics/00_html_css_page_basics.md) | 單一 Marp | 先備自學 | HTML、表單、CSS、box model、RWD、base.html | 能讀懂模板與 Bootstrap class |

| [Django 連續教學教材](../slides/README.md) | 17 份 Marp | 共用主教材 | Project/App、HTTP／URL、View／Template、Model／ORM／Admin、表單／登入／權限、購物車／訂單／交易、安全測試、部署維運 | 能從請求追到資料庫與模板並完成流程驗證 |


主教材每章末附觀念檢核題；解答、實作步驟與前後程式碼節錄在普通 Markdown 實作手冊中。完整檔案形態與來源對照見 [`../slides/SOURCE_MAP.md`](../slides/SOURCE_MAP.md)。

## 投影片與實作手冊

概念題解答、實作步驟與程式碼節錄放在 `../slides/workbooks/`：

- `../slides/workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md`
- `../slides/workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md`

圖解資產集中於 `../slides/assets/*.svg`，重製方式與提示詞見 `../slides/diagram_prompts.md`。教材 CSS 與 SVG 使用繁中字型鏈。

手冊內的程式碼是課堂練習指引，不代表所有練習都已預先套用到目前的 Django 原始碼。主教材的重點頁與先備教材含 `<!-- 授課提示 -->` 講者備註（Marp 簡報模式可見）。

若已安裝 Marp CLI，可在 workspace 根目錄匯出：

```bash
marp ../slides/01_開發環境與專案建立.md --pdf
marp ../slides/09_表單與資料驗證.md --pdf
```

## 驗證

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

## 教學設計說明

課程分兩階段：第一階段以最小的個人留言板（LearnBoard）走完環境、HTTP、MVT、migration、表單、帳號、擁有權與測試的完整循環；第二階段（本專案）以購物情境重新走過同樣循環並加深。教材先建立可重現的開發環境與 HTTP 心智模型，再依序走過 URL/View → Template/static → Model/migration/ORM → Form/auth/CBV → 購物車與訂單交易 → 安全與測試，並以學生較熟悉的購物情境逐步收斂到目前 LearnMart 實作。Model 設計額外示範訂單快照、資料庫 constraint、transaction 與 QuerySet 最佳化；auth 單元則刻意區分「登入」、「角色權限」與「物件擁有權」。

這是教學版，不應直接當正式商城。正式上線仍需環境變數、HTTPS、部署設定、上傳檔檢查、物件儲存、付款、精細的多賣家 shipment、稅務、日誌、監控與更完整測試。

## 主要參考資料

- [Django 6.1.1 官方文件](https://docs.djangoproject.com/en/6.1/)
- [Django 官方入門教學](https://docs.djangoproject.com/en/6.1/intro/tutorial01/)
- [Django Models and databases](https://docs.djangoproject.com/en/6.1/topics/db/)
- [Django Authentication](https://docs.djangoproject.com/en/6.1/topics/auth/)
- [Django Class-based views](https://docs.djangoproject.com/en/6.1/topics/class-based-views/)
- [Django Testing](https://docs.djangoproject.com/en/6.1/topics/testing/)
- [uv Projects](https://docs.astral.sh/uv/guides/projects/)
- [Bootstrap 5.3 Introduction](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [Bootstrap Grid](https://getbootstrap.com/docs/5.3/layout/grid/)
- [Marp](https://marp.app/)

教材的概念排序也參照常見 Django 專書由小型頁面逐步走向資料模型、表單、帳號與測試的「learning by doing」安排，但程式碼與文字均為本專案重新設計。
