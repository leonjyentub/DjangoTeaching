# Django 教學投影片（LearnBoard × LearnMart × LearnJournal）

這是三個教學專案共用的投影片入口。早期各專案內的來源教材已整理到根目錄 `slides/`；目前同時保留部分單檔 Marp、原始分章版本，以及整合後的分章教材。實際檔案形態以本頁與 [`SOURCE_MAP.md`](SOURCE_MAP.md) 為準。

## 建議閱讀順序

1. [Python 語法先備](00_python_syntax_essentials/00_python_syntax_essentials.md)（目前為單一 Marp；另有 `00_git.md`）
2. [HTML/CSS 先備](00_html_css_page_basics/00_html_css_page_basics.md)（目前為單一 Marp）
3. [01 Django 共通基礎](01_django_foundations_and_two_projects/01_django_foundations_and_two_projects.md)（目前為單一整合 Marp）
4. [02 表單、身份驗證與工作流程](02_forms_auth_and_two_projects/00_overview.md)（7 章分檔）
5. [LearnJournal 01 內容模型與發佈](learnjournal_01_content_model_and_publishing/00_overview.md)（6 章分檔；第三階段）
6. LearnJournal 02 傳播、效能與帳號（規劃中，見 [`03_next_project_plan.md`](03_next_project_plan.md)）
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

整理後的 workbook 位於 `workbooks/`：

- LearnBoard：`workbooks/learnboard_*_workbook.md`
- LearnMart：`workbooks/learnmart_*_workbook.md`
- LearnJournal：`workbooks/learnjournal_*_workbook.md`

`assets/` 保留共用圖解資產；重製提示詞見 [`diagram_prompts.md`](diagram_prompts.md)。

## 原始版本與整合版本

根目錄目前有三種教材形態：

- `learnboard_*`／`learnmart_*`：各專案來源教材整理出的分章版本。
- `01_*_two_projects`：LearnBoard × LearnMart 的共通基礎整合版，目前保留為單一 Marp。
- `02_*_two_projects`：LearnBoard × LearnMart 的整合分章版。
- `learnjournal_*`：第三階段教材，一開始即以分章形式撰寫。

Python 與 HTML/CSS 先備目前也保留為單一 Marp，因此不要假設所有資料夾都有 `00_overview.md` 或 `01_chapter_01.md`。需要核對來源與現況時，請查 [`SOURCE_MAP.md`](SOURCE_MAP.md)。
