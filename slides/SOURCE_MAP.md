# 來源與整合索引

本頁是 2026-09-19 教材整併的簡要索引。原 01、01B、02、03 資料夾已整併移除，原稿保留於 Git 歷史。

完整逐頁去向集中於 [source_manifest.json](source_manifest.json)，不再另維護重複的 Markdown 逐頁表。授課入口見 [README](README.md)，手冊章號見 [WORKBOOK_MAP](WORKBOOK_MAP.md)，驗證範圍見[維護摘要](../docs/MAINTENANCE.md)。

## 原始來源

共 12 份來源、610 個頁段；503 保留、34 改寫、73 合併（含空白頁處理）。

| 代碼 | 原檔名（歷史路徑） | 頁段數 | 對應課章 |
|---|---|---:|---|
| A | `01_django_foundations_and_two_projects.md` | 154 | 1、2、3、4、5、6、8、12、13 |
| L | `02_first_contact_lab_and_debugging.md` | 22 | 1、2、3、4、9、10、18 |
| B | `01b_models_orm_and_admin.md` | 116 | 2、6、7、8、9、10、11、17 |
| C | `02_forms_auth_and_two_projects.md` | 253 | 4、13、14、15、16、17、18、19、20、21、22、24 |
| D0 | `00_overview.md` | 6 | 22 |
| D1 | `01_settings_and_environment.md` | 8 | 22 |
| D2 | `02_static_media_database.md` | 9 | 23 |
| D3 | `03_security_and_check_deploy.md` | 8 | 24 |
| D4 | `04_process_proxy_logging.md` | 10 | 25 |
| D5 | `05_migrations_backup_recovery.md` | 10 | 26 |
| D6 | `06_ci_and_release_checklist.md` | 9 | 27 |
| D7 | `07_summary.md` | 5 | 27 |

## 查詢詳細對應

- `sources`：來源代碼、歷史路徑、原始 SHA-256 與頁段數。
- `source_slides`：每個原頁的標題、行號、處理方式與目標；以來源代碼及 `source_slide` 查找。
- `target.file` 相對於 `slides/courses/`；`target.chapter` 是新章號。其他位置欄位與頁數為整併時快照，後續編修可能改變。
- `files`：17 份主線教材當時的章節、頁數與 SHA-256。
- `new_slides`：新增或拆頁內容；`derived_from` 說明可追溯的來源。

處理方式：`retained` 保留、`adapted` 改寫、`consolidated` 合併；合併原因記錄於 `reason`。完整清單保持原樣，歷史頁碼不視為目前版面的保證。
