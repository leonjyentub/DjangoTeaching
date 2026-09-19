# 投影片來源／現況對照表

教材歷經整理後，目前不是所有資料夾都採相同的「overview + 每章一檔」格式。這份表記錄來源脈絡與 repository 現況，避免沿用舊檔名造成失效連結。

| 教材來源／主題 | repository 目前位置 | 現況 |
|---|---|---|
| Python 語法先備 | [`00_python_syntax_essentials/`](00_python_syntax_essentials/) | 單一主 Marp：`00_python_syntax_essentials.md`；另有 `00_git.md` |
| HTML/CSS 先備 | [`00_html_css_page_basics/`](00_html_css_page_basics/) | 單一 Marp：`00_html_css_page_basics.md` |
| LearnBoard 01 | [`learnboard_01_django_foundations_and_message_board/`](learnboard_01_django_foundations_and_message_board/) | `00_overview.md` + 6 章 |
| LearnMart 01 | [`learnmart_01_django_foundations_and_data_backed_catalog/`](learnmart_01_django_foundations_and_data_backed_catalog/) | `00_overview.md` + 6 章 + summary |
| Django 01 共通基礎 | [`01_django_foundations_and_two_projects/`](01_django_foundations_and_two_projects/) | 單一整合 Marp + ChatGPT first-contact / debugging 補充 |
| Django 01B Model／ORM／Admin | [`01b_models_orm_and_admin/`](01b_models_orm_and_admin/) | 單一 Marp；抽入兩專案案例並按 Django 6.1 官方文件擴充，詳見同目錄 README |
| LearnBoard 02 | [`learnboard_02_forms_auth_and_board_workflows/`](learnboard_02_forms_auth_and_board_workflows/) | `00_overview.md` + 6 章 |
| LearnMart 02 | [`learnmart_02_forms_auth_and_marketplace_workflows/`](learnmart_02_forms_auth_and_marketplace_workflows/) | `00_overview.md` + 7 章 + integration |
| Django 02 共通工作流程 | [`02_forms_auth_and_two_projects/`](02_forms_auth_and_two_projects/) | 單一 `02_forms_auth_and_two_projects.md`，已整合 7 章、比較、first-contact 與 DTL 補充 |
| LearnJournal 01（03A） | [`learnjournal_01_content_model_and_publishing/`](learnjournal_01_content_model_and_publishing/) | `00_overview.md` + 6 章 + summary；直接以分章形式撰寫 |
| LearnJournal 02（03B） | [`learnjournal_02_distribution_performance_and_accounts/`](learnjournal_02_distribution_performance_and_accounts/) | ChatGPT 依原 `03_next_project_plan.md` 規劃完成：overview + 7 章 + summary |
| Deployment / Operations | [`03_deployment_and_operations/`](03_deployment_and_operations/) | ChatGPT 新增跨三專案共用單元：overview + 6 章 + summary |

## 命名注意事項

舊文件曾使用 `00a_python_syntax_essentials`、`00b_html_css_page_basics` 等名稱；目前實際目錄是 `00_python_syntax_essentials` 與 `00_html_css_page_basics`。同樣地，`01_django_foundations_and_two_projects/` 的主教材不是 `00_overview.md` / `01_chapter_01.md`，而是單一 `01_django_foundations_and_two_projects.md`；新增的 `02_first_contact_lab_and_debugging.md` 是後續補充，不代表主教材被重新拆章。

第三階段最初規劃仍保留於 [`03_next_project_plan.md`](03_next_project_plan.md)，現在可用來對照哪些原先「規劃中」內容已在 LearnJournal 03B 與 Deployment / Operations 落地。
