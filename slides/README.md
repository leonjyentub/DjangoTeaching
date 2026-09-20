# Django 教學投影片（LearnBoard × LearnMart × LearnJournal）

這是三個教學專案共用的投影片入口。早期各專案內的來源教材已整理到 `slides/`；Python／HTML/CSS 先備、LearnBoard、LearnMart、LearnJournal 分章教材、Django 連續授課主線與部署維運 workbook 目前都以本目錄為主，其中 01～17 主線投影片集中在 `courses/`。實際檔案形態以本頁與 [`SOURCE_MAP.md`](SOURCE_MAP.md) 為準。

## 建議閱讀順序

1. [Python 語法先備](courses/00_python_syntax_essentials.md)、[Git](courses/00_git.md)、[HTML/CSS 先備](courses/00_html_css_page_basics.md)。
2. **[Django 連續教學教材](#django-連續教學教材)**：27 章、17 份 Marp，整合原 01、01B、02、03，依檔名順序授課。
   - 第 1～5 章：環境、HTTP、View、Template 與響應式頁面。
   - 第 6～14 章：Model、ORM、Admin、資料列表、CBV、搜尋分頁與 DTL。
   - 第 15～21 章：表單、帳號、CRUD 權限、購物車、交易、安全與測試。
   - 第 22～27 章：部署設定、服務運行、備份復原與 CI 發布。
3. 延伸：[LearnJournal 01 內容模型與發佈](learnjournal_01_content_model_and_publishing/00_overview.md)。
4. 延伸：[LearnJournal 02 傳播、效能與帳號](learnjournal_02_distribution_performance_and_accounts/00_overview.md)。

原 01／01B／02／03 資料夾已整併進連續教材並移除，不再有獨立入口；原始內容的逐頁去向見 [SOURCE_MAP.md](SOURCE_MAP.md)，與手冊章號對照見 [WORKBOOK_MAP.md](WORKBOOK_MAP.md)。git 歷史仍保留原檔。

## Django 連續教學教材

連續授課主線共 **27 章、17 份 Marp MD**，按下表檔案順序授課，不需在原資料夾之間往返。

- 統一 `django-teal`、16:9、章號 1～27；每份含 1～3 章。檔案數不等於上課次數。
- 主線：環境與頁面、資料層、查詢整合、表單／身份／交易、安全測試、部署維運。
- 每章均有操作環境、學習成果、概念與範例、實作及離堂檢核。
- 教材基準沿用 repository 宣告：Python 3.14.7、Django 6.1.1。實際安裝可用性需依上課環境確認。

### 按順序授課

| 順序與檔案 | 章節 | 完成成果 |
|---|---|---|
| [01_開發環境與專案建立](courses/01_開發環境與專案建立.md) | 第 1 章：Python 與環境管理<br>第 2 章：Django 專案骨架與啟動 | 建立 config 與 pages，確認 app 註冊、migrate、check 及歡迎頁。 |
| [02_HTTP路由與View](courses/02_HTTP路由與View.md) | 第 3 章：Request、URL 與 View | 完成固定路由、動態路由與 query 回應，通過 200／404 的頁面測試。 |
| [03_Template與頁面呈現](courses/03_Template與頁面呈現.md) | 第 4 章：Template 與資料呈現<br>第 5 章：版型、靜態資源與響應式頁面 | 建立共用 base、子模板與 CSS，驗證桌面／手機版面及缺圖狀態。 |
| [04_Model與欄位設計](courses/04_Model與欄位設計.md) | 第 6 章：Model 與資料身分<br>第 7 章：欄位型別與資料規則 | 提出欄位設計表，說明型別、空值、預設、唯一性與圖片存放位置。 |
| [05_模型關聯與Migration](courses/05_模型關聯與Migration.md) | 第 8 章：模型關聯<br>第 9 章：Meta、驗證與資料結構演進 | 修改模型，檢查 migration operations，確認套用狀態與資料規則。 |
| [06_ORM與Admin](courses/06_ORM與Admin.md) | 第 10 章：ORM 查詢與資料操作<br>第 11 章：Admin 資料管理 | 完成可搜尋、可篩選的 Admin，使用不同帳號驗證管理權限。 |
| [07_資料列表搜尋與分頁](courses/07_資料列表搜尋與分頁.md) | 第 12 章：資料驅動頁面<br>第 13 章：CBV 與列表整合 | 以 ListView／DetailView 解釋相同流程，驗證搜尋、分類、分頁能一起工作。 |
| [08_DTL進階與元件整理](courses/08_DTL進階與元件整理.md) | 第 14 章：Template 工具與責任分工 | 整理一個模板元件，保留查詢狀態，說明顯示邏輯與業務規則的分工。 |
| [09_表單與資料驗證](courses/09_表單與資料驗證.md) | 第 15 章：完整表單生命週期 | 以有效與無效 POST 驗證表單，觀察 CSRF、錯誤回顯、上傳及成功轉址。 |
| [10_帳號登入與Session](courses/10_帳號登入與Session.md) | 第 16 章：身份驗證與帳號流程 | 完成註冊、登入、POST 登出，說明 session 與 request.user 的關係。 |
| [11_CRUD與物件權限](courses/11_CRUD與物件權限.md) | 第 17 章：編輯型 CBV 與授權 | 完成留言或商品 CRUD，以作者、他人、匿名帳號驗證可操作範圍。 |
| [12_購物車與流程測試](courses/12_購物車與流程測試.md) | 第 18 章：購物車工作流程與測試 | 驗證購物車增改刪，測試 HTTP response 與資料庫狀態。 |
| [13_訂單結帳與交易](courses/13_訂單結帳與交易.md) | 第 19 章：訂單與交易一致性 | 驗證結帳快照、庫存與購物車變化，讓中途失敗證明 rollback。 |
| [14_出貨評價與狀態規則](courses/14_出貨評價與狀態規則.md) | 第 20 章：交易後續流程 | 以規則表與測試說明誰可出貨／評價，以及目前多賣家流程的限制。 |
| [15_安全與回歸測試整合](courses/15_安全與回歸測試整合.md) | 第 21 章：完整流程的安全驗收 | 完成一份含成功、失敗、越權與副作用的安全回歸驗收表。 |
| [16_部署設定與正式環境](courses/16_部署設定與正式環境.md) | 第 22 章：環境設定與機密<br>第 23 章：Static、Media 與資料庫<br>第 24 章：正式環境安全 | 在類正式設定下執行部署檢查，逐項記錄風險與修正結果。 |
| [17_服務運行與發布維護](courses/17_服務運行與發布維護.md) | 第 25 章：服務程序與監控<br>第 26 章：Migration、備份與復原<br>第 27 章：CI 與發布流程 | 建立 CI 與發布清單，列出發布前後檢查、停止條件及復原方式。 |

> 投影片中「現有程式」「節錄／重排」「教學用最小範例」須分開閱讀。配套 workbook 保持原章號；連結文字中的「原第 N 章」指 workbook，不是本課章號。

### 一條練習主線與兩個專案對照

1. 第 1～5 章在自己的 `django_lab/` 建立 `config`、`pages`。
2. 第 6 章沿用同一環境加入 `catalog`，不重新執行 `uv init`／`startproject`。完成分類、商品、migration、shell 與最小 Admin。
3. 第 6 章後半啟動 LearnBoard／LearnMart，再依範例標示切換；三個環境各有自己的依賴與資料庫。
4. 資料層以完整 catalog 練習配合專案節錄；Profile、Tag、through 與部分 Admin 客製為教學延伸。
5. 列表與寫入流程先看最小例子，再讀 LearnBoard 與 LearnMart。不要把商城的 `seller`／`is_active` 直接套到 catalog。
6. 第 18～20 章以 LearnMart 完成購物車、結帳、出貨與評價。部署可選 LearnBoard 或 LearnMart 副本。

**自訂 User 決策：** 第 2 章在第一次 migrate 前提醒路線；django_lab 沿用內建 User。第 16 章再解釋現有 LearnMart 的自訂 User，不要求中途替換練習資料庫的 User。

### 內容調整

- 原 01 第 4～5 章銜接頁移入資料層開場及第 12 章驗收；不再要求跳到 01B 後折返。
- 第 13 章先解釋查詢型 CBV；第 17 章再解釋編輯型 CBV、Mixin 與權限。
- 第一次實作／除錯 Lab 依環境、路由、模板、migration、表單與測試分散到首次使用處。
- DTL 的常用格式化提前至第 4 章，其餘工具放第 14 章；安全案例在第 21 章整合。
- 安全與測試從第一次使用就加入，最後以跨流程矩陣驗收。
- LearnJournal 的既有提及保留為延伸；不列為本套課程必修先備。
- 原始四個教材目錄已整併並移除，逐頁去向見 [SOURCE_MAP.md](SOURCE_MAP.md)；git 歷史保留原檔。

### 資產、來源與實作

- [來源索引](SOURCE_MAP.md)：原始 12 份 Marp 的整併概要與詳細清單查詢方式。
- [機器可讀來源清單](source_manifest.json)：來源雜湊、章節、投影片數與對應位置。
- [Workbook 對照](WORKBOOK_MAP.md)：新章號對照既有手冊章號及實作範圍。
- 共用圖片沿用 `assets/`。HTTP 圖由原 01 的 inline SVG 原樣抽出到 [assets/http_request_response.svg](assets/http_request_response.svg)，保留可編輯向量內容。
- 主題沿用 [django-teal.css](themes/django-teal.css)，不改動其他教材的主題。
- [維護摘要](../docs/MAINTENANCE.md) 說明歷史驗證範圍、檢查方式與延伸候選。

## 三條實作路線

| 路線 | 專案根目錄 | App | 主要領域 |
|---|---|---|---|
| 第一階段 | `learnboard/` | `board/` | `Message` 留言板 |
| 第二階段 | `learnmart/` | `marketplace/` | `Product`、購物車與訂單 |
| 第三階段 | `learnjournal/` | `journal/` | `Article`、標籤、巢狀留言、發佈與傳播流程 |

每個專案都必須在自己的根目錄執行 `uv sync`、`migrate`、`seed_demo`、`test`；三個專案的 SQLite 資料庫與虛擬環境不要混用。

第三階段後續延伸候選集中於[維護摘要](../docs/MAINTENANCE.md)；最初規劃可由 Git 歷史查閱。

## 配套手冊

整理後的 workbook 位於 `workbooks/`：

- LearnBoard：`workbooks/learnboard_*_workbook.md`
- LearnMart：`workbooks/learnmart_*_workbook.md`
- LearnJournal 03A：[`workbooks/learnjournal_01_content_model_and_publishing_workbook.md`](workbooks/learnjournal_01_content_model_and_publishing_workbook.md)
- LearnJournal 03B：[`workbooks/learnjournal_02_distribution_performance_and_accounts_workbook.md`](workbooks/learnjournal_02_distribution_performance_and_accounts_workbook.md)
- Deployment / Operations：[`workbooks/03_deployment_and_operations_workbook.md`](workbooks/03_deployment_and_operations_workbook.md)

連續授課各章與手冊的章號對照見 [WORKBOOK_MAP.md](WORKBOOK_MAP.md)。

`assets/` 保留共用圖解資產；重製提示詞見 [`diagram_prompts.md`](diagram_prompts.md)。

## 教材連結檢查

Repository 內的 Markdown 相對連結可執行：

```bash
python scripts/check_material_links.py
```

GitHub Actions 的 `.github/workflows/material-links.yml` 也會在 PR 與 `master` push 時執行同一檢查，避免教材改名或搬移後留下 stale links。

## 剩餘教材形態

已整併的來源資料夾（01、01B、02、03）與 LearnBoard／LearnMart 的原始分章版本均已整併進主教材；目前 `slides/` 下的教材形態如下：

- `courses/`：3 份先備教材（Python、Git、HTML/CSS）與 01～17 連續教學主線（27 章），共 20 份 Marp。
- BootstrapFormMixin 定義與套用步驟已整合至 [09 表單與資料驗證](courses/09_表單與資料驗證.md#chapter-15) 的 15-17A～15-17B；權限感知按鈕已整合至 [11 CRUD與物件權限](courses/11_CRUD與物件權限.md#chapter-17) 的 17-6A。
- `learnjournal_*`：第三階段教材，03A / 03B 都直接以分章形式撰寫。
- `workbooks/`：三個專案與部署維運的實作手冊。

不要假設所有資料夾都有 `00_overview.md` 或 `01_chapter_01.md`。需要核對來源與現況時，請查 [`SOURCE_MAP.md`](SOURCE_MAP.md)。
