# DjangoTeaching 專案結構＋教學內容盤點（ChatGPT 修訂）

> Branch: `chatgpt/curriculum-audit-2026-09-16`
>
> 本文件由 ChatGPT 於 2026-09-16 依 repository 現況整理並持續更新；`master` 未直接修改。

## 1. 三階段教學結構

| 階段 | 專案 | 核心領域 | 心智模型 | 主要能力 |
|---|---|---|---|---|
| 1 | `learnboard/` | 留言板 | 誰能改哪一筆資料 | request flow、CRUD、Form、Auth、Ownership、Testing |
| 2 | `learnmart/` | 商城 | 多筆資料如何保持一致 | roles、cart、stock、Order/OrderItem、transaction、integrity |
| 3 | `learnjournal/` | 發佈平台 | 內容如何被建立、找到、傳播與排程 | M2M、QuerySet、template tags、signals、cache、email、permissions、feed、scheduler、search |

三個 domain 不同，因此不是把同一 CRUD 不斷加頁面，而是反覆練習 Django 核心 request/data flow，再增加新的系統問題。

## 2. 已完成教材覆蓋

### Python / HTML/CSS

- Python 基礎、容器、函式、例外、class、繼承/mixin、decorator、型別標註。
- HTML 文件、表單、CSS、box model、RWD、Bootstrap grid。

### Django 01 / LearnBoard / LearnMart 基礎

- project/app/settings/manage.py、HTTP、URL、View、Template、static/media。
- Model、ForeignKey、migration、ORM、admin、pagination。
- Form/ModelForm、CSRF、PRG、messages、auth/session、CBV/mixins。
- ownership/authorization、403/404/405/IDOR。
- transaction.atomic/select_for_update、TestCase/Client、安全基礎。

### LearnJournal 03A

- M2M + through、自我 FK、custom Manager/QuerySet。
- `F()`、constraint/index、slug/date URL、date-based views。
- `values().annotate()`、custom template tags/filters、signals、RunPython migration、timezone。

### LearnJournal 03B（本 branch 已完成）

1. sessions / cookies + low-level cache + template fragment cache
2. custom middleware（response time / maintenance 503）
3. email / built-in password reset / double opt-in
4. Group / Permission + `publish_article`
5. RSS / sitemap
6. management commands + `--dry-run` + scheduling 教材
7. PostgreSQL full-text search + SQLite fallback

教材：[`slides/learnjournal_02_distribution_performance_and_accounts/`](slides/learnjournal_02_distribution_performance_and_accounts/)

Workbook：[`slides/workbooks/learnjournal_02_distribution_performance_and_accounts_workbook.md`](slides/workbooks/learnjournal_02_distribution_performance_and_accounts_workbook.md)

## 3. P0 / P0.5 導航與一致性

### P0 已完成

- 修正 `00a_*` / `00b_*` 舊命名與失效入口。
- 釐清 Deck 01 實際是單一主 Marp，Deck 02 是分章教材。
- 修正 LearnBoard / LearnMart README 與 Marp CLI 範例。
- 更新 `slides/SOURCE_MAP.md`。
- 核對 workbook 與原測試數。

### P0.5 已完成

新增：

- `scripts/check_material_links.py`：stdlib-only Markdown 相對連結檢查器。
- `.github/workflows/material-links.yml`：PR、`master`、`chatgpt/**` 自動檢查。

第一次 CI 執行實際抓到 3 個早期單檔教材 stale links。為維持已下載教材／書籤相容性，新增明確標示 deprecated/backward-compatible 的入口頁，而不是把舊路徑從 checker 排除。修正後 GitHub Actions `Teaching material links` 已通過。

## 4. P2 Deployment / Operations（本 branch 已完成）

新增跨三專案共用單元：[`slides/03_deployment_and_operations/`](slides/03_deployment_and_operations/)

六章：

1. settings / environment variables
2. static / media / PostgreSQL
3. security / HTTPS / `check --deploy`
4. WSGI/ASGI process / reverse proxy / logging
5. migrations / backup / recovery
6. CI / release checklist

Workbook：[`slides/workbooks/03_deployment_and_operations_workbook.md`](slides/workbooks/03_deployment_and_operations_workbook.md)

## 5. Deck 01 / 02 第一次接觸學生補強

檢查後結論：既有教材的概念覆蓋已足夠，但第一次自己操作的學生仍需要更明確的「指令 → 預期輸出 → 錯誤分類 → 驗證」節奏，因此新增兩份補充 lab，而不重寫主教材。

### Django 01 補充

[`slides/01_django_foundations_and_two_projects/02_first_contact_lab_and_debugging.md`](slides/01_django_foundations_and_two_projects/02_first_contact_lab_and_debugging.md)

新增重點：

- working directory / `uv sync` / `uv run`
- `check`、migration 三步驟、`showmigrations`、`migrate --plan`、`sqlmigrate`
- runserver 與第二 terminal
- HTTP status、traceback、常見 import/template/reverse error
- ORM shell、小步驗證、單支 test 定位與 failure 閱讀

### Django 02 補充

[`slides/02_forms_auth_and_two_projects/10_first_contact_forms_auth_testing_lab.md`](slides/02_forms_auth_and_two_projects/10_first_contact_forms_auth_testing_lab.md)

新增重點：

- POST lifecycle、request.POST、Form lifecycle
- CSRF、DevTools、PRG
- session/auth、authentication vs authorization
- 403/404、ownership、IDOR
- Arrange/Act/Assert、`force_login`、`refresh_from_db()`
- transaction rollback 與 security regression tests

## 6. Django Template Language 補強

新增：[`slides/02_forms_auth_and_two_projects/11_django_template_language_practical_toolbox.md`](slides/02_forms_auth_and_two_projects/11_django_template_language_practical_toolbox.md)

依 Django 5.2 官方文件與常用情境補充：

- `default` / `default_if_none`
- `date` / `time` / `timesince` / `timeuntil` / `{% now %}`
- `humanize`：`naturaltime` / `naturalday` / `intcomma` / `intword`
- `truncatechars` / `truncatewords` / HTML-aware variants 的限制
- `linebreaks` / `linebreaksbr`
- `filesizeformat` / `floatformat` / `length` / `wordcount`
- `first` / `last` / `join` / `slice` / `dictsort`
- `yesno` / `pluralize` / `urlize`
- `{% with %}` / `{% firstof %}` / `{% cycle %}` / `{% ifchanged %}` / `{% regroup %}`
- Django 5.1+ `{% querystring %}`：搜尋／filter＋分頁保留 query parameters
- `json_script`：較安全地把資料交給 JavaScript
- autoescape / `safe` / `striptags` 的 XSS 邊界
- 何時該改用 view/custom filter/simple_tag/inclusion_tag

## 7. Repository / LearnJournal CI

新增 `.github/workflows/learnjournal-tests.yml`，在 `master` / `chatgpt/**` / PR 執行：

```bash
uv sync
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

這讓 P1 不只是一批程式碼與投影片，而是有可重跑的 runtime 驗證。

## 8. 建議授課順序（更新）

`Python` → `HTML/CSS` → `Django 01 + first-contact lab` → `LearnBoard` → `Django 02 + first-contact lab + DTL toolbox` → `LearnMart` → `LearnJournal 03A` → `LearnJournal 03B` → `Deployment / Operations`

各階段 completion milestone：

- LearnBoard：能追 request flow、完成 CRUD + auth + ownership。
- LearnMart：能處理跨模型 workflow、transaction 與庫存一致性。
- LearnJournal 03A：能設計內容模型、M2M、發佈流程與 reusable ORM abstraction。
- LearnJournal 03B：能處理 state/cache、middleware、email、permission、feed、scheduler、database-specific search。
- Deployment：能說明 local vs production 差異，並建立可驗證的 release/operations checklist。

## 9. 尚可延伸但不阻塞本輪完成

- `00c` 精簡 Python 進階補充（lambda/context manager/datetime/generator/collections/functools）。
- LearnJournal inline formset 多圖。
- 中文 production search tokenizer / GIN/materialized vector。
- Redis/shared cache、production SMTP、async job queue。
- rate limit、spam moderation、observability/object storage 的平台實作。

## 10. 本次 ChatGPT 修訂範圍

本 branch 已從原先「只做導航」擴大為使用者明確要求的 P0.5、P1、P2 與教材補強，因此現在包含 Django runtime、migration、tests、CI 與新教材。所有修改仍只在 `chatgpt/curriculum-audit-2026-09-16`，未直接修改 `master`。
