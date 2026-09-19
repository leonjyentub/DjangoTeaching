# Django 教學投影片（LearnBoard × LearnMart × LearnJournal）

這是三個教學專案共用的投影片入口。早期各專案內的來源教材已整理到根目錄 `slides/`；目前同時保留部分單檔 Marp、原始分章版本，以及整合後的分章教材。實際檔案形態以本頁與 [`SOURCE_MAP.md`](SOURCE_MAP.md) 為準。

## 建議閱讀順序

1. [Python 語法先備](00_python_syntax_essentials/00_python_syntax_essentials.md)（目前為單一 Marp；另有 `00_git.md`）
2. [HTML/CSS 先備](00_html_css_page_basics/00_html_css_page_basics.md)（目前為單一 Marp）
3. [01 Django 共通基礎](01_django_foundations_and_two_projects/01_django_foundations_and_two_projects.md)（單一整合 Marp）
   - [第一次實作／除錯補充](01_django_foundations_and_two_projects/02_first_contact_lab_and_debugging.md)
4. [01B 資料模型、ORM 與 Django Admin 詳解](01b_models_orm_and_admin/01b_models_orm_and_admin.md)（初學者完整教學；01 第 3 章後使用，原第 4～5 章作摘要複習）
5. [02 表單、身份驗證與工作流程](02_forms_auth_and_two_projects/02_forms_auth_and_two_projects.md)（單一整合 Marp，含第一次實作與 DTL 補充）
6. [LearnJournal 01 內容模型與發佈](learnjournal_01_content_model_and_publishing/00_overview.md)（6 章分檔；第三階段 03A）
7. [LearnJournal 02 傳播、效能與帳號](learnjournal_02_distribution_performance_and_accounts/00_overview.md)（7 章分檔；第三階段 03B）
8. [03 Deployment / Operations](03_deployment_and_operations/00_overview.md)（跨三專案共用；6 章）

## 三條實作路線

| 路線 | 專案根目錄 | App | 主要領域 |
|---|---|---|---|
| 第一階段 | `learnboard/` | `board/` | `Message` 留言板 |
| 第二階段 | `learnmart/` | `marketplace/` | `Product`、購物車與訂單 |
| 第三階段 | `learnjournal/` | `journal/` | `Article`、標籤、巢狀留言、發佈與傳播流程 |

每個專案都必須在自己的根目錄執行 `uv sync`、`migrate`、`seed_demo`、`test`；三個專案的 SQLite 資料庫與虛擬環境不要混用。

第三階段最初的規劃與缺口盤點仍保留於 [`03_next_project_plan.md`](03_next_project_plan.md)，方便對照「規劃 → 已完成實作」的演進。

## 配套手冊

整理後的 workbook 位於 `workbooks/`：

- LearnBoard：`workbooks/learnboard_*_workbook.md`
- LearnMart：`workbooks/learnmart_*_workbook.md`
- LearnJournal 03A：[`workbooks/learnjournal_01_content_model_and_publishing_workbook.md`](workbooks/learnjournal_01_content_model_and_publishing_workbook.md)
- LearnJournal 03B：[`workbooks/learnjournal_02_distribution_performance_and_accounts_workbook.md`](workbooks/learnjournal_02_distribution_performance_and_accounts_workbook.md)
- Deployment / Operations：[`workbooks/03_deployment_and_operations_workbook.md`](workbooks/03_deployment_and_operations_workbook.md)

`assets/` 保留共用圖解資產；重製提示詞見 [`diagram_prompts.md`](diagram_prompts.md)。

## 教材連結檢查（P0.5）

Repository 內的 Markdown 相對連結可執行：

```bash
python scripts/check_material_links.py
```

GitHub Actions 的 `.github/workflows/material-links.yml` 也會在 PR 與 `master` push 時執行同一檢查，避免教材改名或搬移後留下 stale links。

## 原始版本與整合版本

根目錄目前有多種教材形態：

- `learnboard_*`／`learnmart_*`：各專案來源教材整理出的分章版本。
- `01_*_two_projects`：LearnBoard × LearnMart 的共通基礎整合版，主教材目前為單一 Marp，另加 first-contact 補充 lab。
- `01b_models_orm_and_admin`：完整 Model／ORM／Admin 教學；[內容與來源索引](01b_models_orm_and_admin/README.md)。
- `02_*_two_projects`：LearnBoard × LearnMart 的單檔整合版，含 first-contact 與 DTL 實用補充。
- `learnjournal_*`：第三階段教材，03A / 03B 都直接以分章形式撰寫。
- `03_deployment_and_operations/`：跨三專案的 production / operations 收尾單元。

Python 與 HTML/CSS 先備目前也保留為單一 Marp，因此不要假設所有資料夾都有 `00_overview.md` 或 `01_chapter_01.md`。需要核對來源與現況時，請查 [`SOURCE_MAP.md`](SOURCE_MAP.md)。
