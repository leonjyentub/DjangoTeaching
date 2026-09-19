# 教材整合驗證紀錄

驗證日期：2026-09-19。交付為可編輯 Marp 與索引文件；HTML／截圖僅在暫存目錄用於 QA，未在教材目錄產生 PDF 或 HTML。

> 後續整理：本驗證完成後，連續授課教材已由 `slides/django_course/` 移到 `slides/` 根目錄；原始四個資料夾（01、01B、02、03）已移除，內容全部整併至本目錄。下表「原始教材保留」為驗證當時的事實紀錄。

## 本次結果

| 檢查 | 結果 |
|---|---|
| 檔案與章序 | 17 份 Marp，章號 1～27 連續；每份含 1～3 章 |
| 實際 HTML 渲染 | 679 頁，逐檔頁數與來源清單一致 |
| 來源對應 | 原 12 份 Marp 的 610 個頁段均有去向；537 頁搬移／調整，73 頁合併或替換導讀，含 1 個空白頁 |
| 原始教材保留 | 四個來源資料夾共 13 個檔案 SHA-256 均與修改前相同 |
| 主題與格式 | 全部 django-teal、16:9，獨立 front matter；程式碼 fence 與 HTML comment 成對 |
| 本目錄相對連結 | 本機目標均存在；新章錨點與 workbook 的 chapter-N 錨點逐一核對 |
| 圖片 | 8 次圖片引用皆成功載入；HTTP 原 inline SVG 已抽出且 XML 可解析 |
| 全頁自動版面檢查 | 679 頁沒有內容越過檢查邊界、遮到頁尾或程式碼水平溢出的旗標 |
| 視覺抽查 | 檢視各份代表頁，以及圖解、長程式碼與密集頁；保留原 theme，修正過密頁 |
| 修改範圍 | 新增連續授課教材並移到 `slides/` 根目錄；更新根 README、本 README 與 SOURCE_MAP 的授課入口 |

## 版面修正

- HTTP 的圖與訊息欄位拆成兩頁，MVT 圖與詳細責任拆成兩頁。
- 保留既有 SVG，調整嵌入尺寸與置中，讓圖解與頁尾分開。
- 部分密集頁在本檔使用 26px compact class，其餘沿用 28px 主題正文。
- 修正模板目錄頁、搜尋分頁頁與欄位說明的冗長措辭，保留教學重點。
- 來源清單記錄拆頁後的主頁位置；兩個延伸頁以 derived_from 記錄來源。

## 檢查方式與範圍

Marp CLI 4.5.1，使用既有 django-teal CSS 生成暫存 HTML；Google Chrome 以 1280 × 720 檢查每一個 section、內容元素邊界、圖片載入與程式碼區塊的水平溢出。逐頁自動檢查不等同每頁人工逐字校對，視覺檢查採代表頁與密集頁抽查。

在 repository 根目錄可用下列方式輸出一份暫存預覽；`--no-config` 避免原本共用設定中的 PDF 選項介入：

```bash
marp --no-config --html --theme-set slides/themes/django-teal.css   --template bare slides/01_開發環境與專案建立.md   -o /private/tmp/django-course-preview.html
```

若把 HTML 放在暫存目錄，圖片的相對路徑需以原 MD 資料夾為 base；本次 QA 已設定此 base。一般 Marp Preview 直接使用來源檔即可。

本次驗證教材結構、來源、連結與渲染；未重新安裝 Django、執行全部課堂練習或部署服務。版本說明依專案宣告一致化，不宣稱已驗證該版本在教室環境中的安裝可用性。外部官方文件網址未逐一做網路存活檢查。

## Repository 既有問題（不屬於新教材）

`python3 scripts/check_material_links.py` 對全 repository 仍回報 7 個既有失效連結，本次新教材沒有失效連結：

| 原文件 | 既有問題 |
|---|---|
| CURRICULUM_AUDIT_CHATGPT.md | 2 個連結指向已併入 02 主檔的 Lab／DTL 舊檔名 |
| learnboard/README.md | 1 個連結指向不存在的 02/00_overview.md |
| learnmart/README.md | 1 個連結指向不存在的 02/00_overview.md |
| slides/00_html_css_page_basics/00_html_css_page_basics.md | 1 個連結指向不存在的 01/00_overview.md |
| slides/00_python_syntax_essentials/00_python_syntax_essentials.md | 2 個連結指向舊 HTML/CSS 目錄與 01/00_overview.md |

`python3 scripts/check_version_baseline.py` 仍因掃到三個專案 `.venv/lib/python3.13/site-packages/` 內的 Django 套件文字而失敗。這是現有檢查範圍與本機環境問題；本次新教材沒有舊版基準字串。原專案程式、套件環境及檢查腳本沒有修改。

## 各檔渲染頁數

| 教材 | 章節 | 頁數 |
|---|---|---|
| [01_開發環境與專案建立](01_開發環境與專案建立.md) | 1、2 | 53 |
| [02_HTTP路由與View](02_HTTP路由與View.md) | 3 | 37 |
| [03_Template與頁面呈現](03_Template與頁面呈現.md) | 4、5 | 45 |
| [04_Model與欄位設計](04_Model與欄位設計.md) | 6、7 | 60 |
| [05_模型關聯與Migration](05_模型關聯與Migration.md) | 8、9 | 42 |
| [06_ORM與Admin](06_ORM與Admin.md) | 10、11 | 49 |
| [07_資料列表搜尋與分頁](07_資料列表搜尋與分頁.md) | 12、13 | 56 |
| [08_DTL進階與元件整理](08_DTL進階與元件整理.md) | 14 | 42 |
| [09_表單與資料驗證](09_表單與資料驗證.md) | 15 | 38 |
| [10_帳號登入與Session](10_帳號登入與Session.md) | 16 | 27 |
| [11_CRUD與物件權限](11_CRUD與物件權限.md) | 17 | 23 |
| [12_購物車與流程測試](12_購物車與流程測試.md) | 18 | 36 |
| [13_訂單結帳與交易](13_訂單結帳與交易.md) | 19 | 35 |
| [14_出貨評價與狀態規則](14_出貨評價與狀態規則.md) | 20 | 22 |
| [15_安全與回歸測試整合](15_安全與回歸測試整合.md) | 21 | 31 |
| [16_部署設定與正式環境](16_部署設定與正式環境.md) | 22、23、24 | 41 |
| [17_服務運行與發布維護](17_服務運行與發布維護.md) | 25、26、27 | 42 |
