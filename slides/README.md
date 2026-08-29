# Django 教學投影片（LearnBoard × LearnMart × LearnJournal）

這是三個教學專案共用的投影片入口。原始教材仍保留在各自專案的 `slides/`，本資料夾則把重複的 Marp 基礎整合成一套教材，並在必要處並列各專案的實際檔案、命名與工作流程。

## 建議閱讀順序

1. [00a Python 語法先備](00a_python_syntax_essentials/00_overview.md)（每章一檔）
2. [00b HTML/CSS 先備](00b_html_css_page_basics/00_overview.md)（每章一檔）
3. [01 Django 共通基礎](01_django_foundations_and_two_projects/00_overview.md)（每章一檔）
4. [02 表單、身份驗證與工作流程](02_forms_auth_and_two_projects/00_overview.md)（每章一檔）
5. [LearnJournal 01 內容模型與發佈](learnjournal_01_content_model_and_publishing/00_overview.md)（每章一檔；第三階段）
6. LearnJournal 02 傳播、效能與帳號（規劃中，見 `03_next_project_plan.md`）
7. 03 部署與營運（規劃中）

## 三條實作路線

| 路線 | 專案根目錄 | App | 主要領域 |
|---|---|---|---|
| 第一階段 | `learnboard/` | `board/` | `Message` 留言板 |
| 第二階段 | `learnmart/` | `marketplace/` | `Product`、購物車與訂單 |
| 第三階段 | `learnjournal/` | `journal/` | `Article`、標籤、巢狀留言、發佈流程 |

每個專案都必須在自己的根目錄執行 `uv sync`、`migrate`、`seed_demo`、`test`；三個專案的 SQLite 資料庫與虛擬環境不要混用。

第三階段的規劃、缺口盤點與後續章節地圖見 [`03_next_project_plan.md`](03_next_project_plan.md)。

## 配套手冊

整合投影片的章末連結會帶到整理後的 workbook：

- LearnBoard：`workbooks/learnboard_*_workbook.md`
- LearnMart：`workbooks/learnmart_*_workbook.md`
- LearnJournal：`workbooks/learnjournal_*_workbook.md`

`assets/` 只保留去重後的五張圖解：`box_model`、`mvt_model`、`request_flow`、`trust_boundary`、`transaction_rollback`。

## 原始版本與整合版本

為了保留兩邊曾經修改過的內容，根目錄同時保留兩類分章資料夾：

- `learnboard_*`／`learnmart_*`：刪除來源資料夾前，各自原始 Marp 檔的分章版本。
- `01_*_two_projects`／`02_*_two_projects`：整合版與額外新增的 LearnBoard 對照內容。

你可以依章節手動挑選、合併，不需要再回到已刪除的專案內 `slides/`。
