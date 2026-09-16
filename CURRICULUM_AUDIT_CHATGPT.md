# DjangoTeaching 專案結構＋教學內容盤點（ChatGPT 修訂）

> Branch: `chatgpt/curriculum-audit-2026-09-16`
>
> 本文件由 ChatGPT 於 2026-09-16 依 repository 現況整理。目的在於提供授課者一個集中式的專案結構、教學覆蓋、缺口與後續優先級視圖；不取代各專案 README 與 `slides/03_next_project_plan.md`。

## 1. 整體結構

本 repository 已形成三階段、三種不同網站心智模型的 Django 教學路線：

| 階段 | 專案 | App | 核心領域 | 主要教學重點 |
|---|---|---|---|---|
| 第一階段 | `learnboard/` | `board/` | 留言板 / CRUD | Project/App、URL/View/Template、Model/Migration、Form、Auth、Ownership、測試 |
| 第二階段 | `learnmart/` | `marketplace/` | 商城 / 交易 | 角色權限、商品與圖片、購物車、庫存、Order/OrderItem、transaction、資料完整性 |
| 第三階段 | `learnjournal/` | `journal/` | 發佈平台 / CMS | M2M、through、自我 FK、Manager/QuerySet、template tags、signals、data migration、效能與發佈流程 |

此外，`slides/` 是跨專案教材入口；`output/` 放置輸出成果；根目錄 `marp.config.mjs` 支援 Marp 教材匯出。

## 2. 教學遞進是否合理

目前遞進方向是合理且互補的：

1. LearnBoard 先建立「一個 request 如何穿過 URL → View → ORM → Template」的完整心智模型，並用最小功能集教 authentication / authorization。
2. LearnMart 不只是增加頁面，而是把問題提升到「多筆資料的一致性」：購物車、庫存、訂單、交易與角色權限。
3. LearnJournal 再切換到「內容發佈與傳播」，自然引出 M2M、slug/date URL、custom QuerySet、template tags、signals、data migration 與效能議題。

這三階段的領域模型不同，因此不是單純把同一個 CRUD 專案越做越大，而是重複核心 Django 流程、逐步增加新的抽象層。

## 3. 現有教材覆蓋摘要

### Python / HTML/CSS 先備

- Python 基礎語法、資料結構、函式、例外、class、繼承、mixin、decorator、型別標註。
- HTML 文件結構、表單、CSS 選擇器、box model、RWD、Bootstrap grid。

### Django 基礎

- project / app / settings / manage.py
- HTTP、URL、converter、named URL、reverse
- function view、template inheritance/include/filter/if/for
- static / media
- Model、ForeignKey、on_delete、TextChoices、Meta
- migration 與 schema 演進
- ORM filter/get/Q、lazy queryset、aggregate/annotate、select_related/prefetch_related
- admin、pagination

### 表單、帳號與安全

- Form / ModelForm、驗證、`clean()`、`save(commit=False)`
- CSRF、PRG、messages、檔案上傳
- Django auth、LoginView、logout、session、request.user
- CBV 與 mixin
- authentication / authorization / ownership
- 403、404、405、IDOR
- transaction.atomic / select_for_update
- TestCase / Client
- XSS / CSRF / SQL injection / upload 基礎

### LearnJournal 新增的進階主題

- ManyToManyField 與 through model
- self-referential ForeignKey
- custom Manager / QuerySet
- `F()` expression
- CheckConstraint / indexes
- slug + 日期型 URL
- date-based generic views
- `values().annotate()` 分組統計
- custom template tags / filters
- `FormMixin + DetailView`
- signals
- `RunPython` data migration
- timezone 對日期網址的實務影響

## 4. 目前最明顯的教材缺口

### A. Repository 級「全課程地圖」不足

各專案 README 都寫得完整，但根目錄 README 原本偏簡介。此 branch 已補上三階段能力地圖與本盤點文件入口。

### B. LearnJournal 的完成度與後續路線需要持續維護

目前 LearnJournal 已有 Deck 03A 對應實作，但 03B / 04 仍屬後續目標。現況應持續明確區分：

- 已完成並可操作
- 已有掛鉤點但未完成
- 純規劃

### C. 部署與 production readiness 目前仍是「每個 README 結尾提醒」

三個專案都會提到正式環境還需要環境變數、HTTPS、DEBUG=False、監控等，但尚未形成一個真正的 deployment / operations 模組。

適合作為最後一個跨專案總結單元：

- settings split
- environment variables
- static/media deployment
- PostgreSQL
- security headers / HTTPS
- logging / monitoring
- backup / migration strategy
- `check --deploy`

### D. Python 進階語法仍有零散缺口

`slides/03_next_project_plan.md` 已盤點多個尚未完整教過的 Python 主題，例如：

- lambda + key functions
- context manager
- datetime / timedelta
- generator / yield
- dict/set comprehension
- unpacking / dictionary merge
- Counter / defaultdict
- functools
- custom exception chaining

建議不要一次做成很厚的純 Python 單元，而是建立精簡 `00c`，再在 LearnJournal 對應章節回扣。

## 5. 建議授課順序

建議維持：

`Python 先備` → `HTML/CSS 先備` → `LearnBoard` → `LearnMart` → `LearnJournal 03A` → `LearnJournal 03B` → `Deployment / Operations`

其中每一階段應有明確 completion milestone：

- LearnBoard：能追 request flow、完成 CRUD + auth + ownership。
- LearnMart：能處理跨模型 workflow、transaction 與庫存一致性。
- LearnJournal 03A：能設計內容模型與 M2M、發佈流程、可重用 ORM 抽象。
- LearnJournal 03B：能加入 cache、middleware、email、search、feed、permission、scheduling。
- Deployment：能把「教學版」與「可部署版」的差異逐項說明並實作。

## 6. 後續教材優先級

### P0：導航與一致性 — 已完成第一輪

本 branch 已完成：

1. 根目錄 README 加入三階段能力矩陣。
2. 明確標出 LearnJournal 03A 已完成、03B/04 規劃中。
3. README 加入本盤點文件入口。
4. 核對 `slides/` 實際教材檔案與 README 連結。
5. 修正舊的 `00a_*` / `00b_*` 路徑名稱。
6. 修正 Deck 01 被誤寫成「每章一檔」的敘述；目前共通 Deck 01 為單一整合 Marp。
7. 修正 LearnBoard / LearnMart README 中失效的 Marp CLI 範例。
8. 更新 `slides/SOURCE_MAP.md`，明確列出單檔與分章教材的差異。
9. 核對 workbook 檔名存在。
10. 核對 LearnBoard 為 9 個 test methods、LearnJournal 為 11 個 test methods；README 宣告與實際一致。

### P1：完成 LearnJournal 03B

依目前規劃優先順序建議：

1. sessions / cookies + cache
2. custom middleware
3. email / password reset
4. Group / Permission
5. RSS / sitemap
6. management command + scheduling
7. PostgreSQL full-text search

### P2：最後整理 production / deployment

建立跨三專案共用的 Deployment / Operations 模組，不必三份重複。

## 7. 品質檢查建議

每次教材或程式碼變更至少維持以下檢查：

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

另外建議增加 repository 級教材檢查：

- README / workbook / slides 的相對路徑是否存在
- 各 README 宣告的測試數是否與實際一致
- slides overview 的章節數與實際檔案數是否一致
- 已完成 / 規劃中狀態是否一致
- Marp CLI 範例所指向的檔案是否存在

長期建議把上述教材檢查自動化成 CI script，避免之後重新命名或拆章時又產生 stale links。

## 8. P0 一致性檢查紀錄（2026-09-16）

### 已發現並修正

| 類型 | 原狀況 | 修正 |
|---|---|---|
| 先備教材路徑 | 文件引用 `00a_python_syntax_essentials` / `00b_html_css_page_basics` | 改為實際 `00_python_syntax_essentials` / `00_html_css_page_basics` |
| 先備教材入口 | 文件引用不存在的 `00_overview.md` | 直接連到實際單一 Marp |
| 共通 Deck 01 | 文件引用不存在的 `00_overview.md`、`01_chapter_01.md` | 改連 `01_django_foundations_and_two_projects.md` |
| 教材形態描述 | 多處宣稱根目錄主教材全部「每章一檔」 | 改為明確區分單一 Marp與分章教材 |
| slides README | 前段稱專案內原始 slides 仍保留，後段又稱已刪除 | 統一描述為已整理到根 `slides/` |
| SOURCE_MAP | 使用已不存在的舊命名 | 依現有檔案重建對照 |
| Marp 指令 | LearnBoard / LearnMart README 有指向不存在檔案的範例 | 改為目前可存在的檔案路徑 |
| 測試數 | 需要確認 README 是否過期 | LearnBoard 9、LearnJournal 11，均與實際 test methods 一致 |
| workbook | 需要確認 README 所列檔名 | LearnBoard、LearnMart、LearnJournal workbook 均存在 |

### 現況教材形態摘要

- `00_python_syntax_essentials/`：單一主 Marp + `00_git.md`
- `00_html_css_page_basics/`：單一 Marp
- `01_django_foundations_and_two_projects/`：單一整合 Marp
- `02_forms_auth_and_two_projects/`：7 章分檔，另有 comparison / integration
- `learnboard_01_*`：6 章分檔
- `learnboard_02_*`：6 章分檔
- `learnmart_01_*`：6 章分檔 + summary
- `learnmart_02_*`：7 章分檔 + integration
- `learnjournal_01_*`：6 章分檔 + summary

## 9. 本次 ChatGPT 修訂範圍

本 branch 只處理「教學導航、盤點與一致性文件」，不改 Django runtime 行為、不改 model schema、不新增 migration，也不直接修改 `master`。

後續若要實作 P1/P2，建議從這個 branch 再拆更小的 feature branches，讓每個教學單元可獨立 review。
