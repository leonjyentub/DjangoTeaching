# DjangoTeaching 專案結構＋教學內容盤點（ChatGPT 修訂）

> Branch: `chatgpt/curriculum-audit-2026-09-16`
>
> 本文件由 ChatGPT 於 2026-09-16 依 `master` 現況整理。目的在於提供授課者一個集中式的專案結構、教學覆蓋、缺口與後續優先級視圖；不取代各專案 README 與 `slides/03_next_project_plan.md`。

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

各專案 README 都寫得完整，但根目錄 README 偏簡介，學生或助教若第一次進 repo，仍要自行拼湊：

- 哪些內容已完成？
- 哪些只是規劃中？
- 三個專案各自新增了哪些 Django 能力？
- 同一概念應該在哪個專案回顧？

建議把「三階段能力矩陣」放到根目錄 README，並連結本盤點文件。

### B. LearnJournal 的完成度與後續路線需要更清楚標示

目前 LearnJournal 已有 Deck 03A 對應實作，但 03B / 04 仍屬後續目標。學生容易把 README 的「尚未實作」與 slides README 的「規劃中」混在一起。

建議明確區分：

- 已完成並可操作
- 已有掛鉤點但未完成
- 純規劃

### C. 部署與 production readiness 目前仍是「每個 README 結尾提醒」

三個專案都會提到正式環境還需要環境變數、HTTPS、DEBUG=False、監控等，但尚未形成一個真正的 deployment / operations 模組。

這很適合作為最後一個跨專案總結單元：

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

`00a Python` → `00b HTML/CSS` → `LearnBoard` → `LearnMart` → `LearnJournal 03A` → `LearnJournal 03B` → `Deployment / Operations`

其中每一階段應有明確 completion milestone：

- LearnBoard：能追 request flow、完成 CRUD + auth + ownership。
- LearnMart：能處理跨模型 workflow、transaction 與庫存一致性。
- LearnJournal 03A：能設計內容模型與 M2M、發佈流程、可重用 ORM 抽象。
- LearnJournal 03B：能加入 cache、middleware、email、search、feed、permission、scheduling。
- Deployment：能把「教學版」與「可部署版」的差異逐項說明並實作。

## 6. 建議下一批教材優先級

### P0：先完成導航與一致性

1. 根目錄 README 加入三階段能力矩陣。
2. 明確標出 LearnJournal 03A 已完成、03B/04 規劃中。
3. README 加入本盤點文件入口。

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

## 8. 本次 ChatGPT 修訂範圍

本 branch 只處理「教學導航與盤點」，不改 Django runtime 行為、不改 model schema、不新增 migration，也不直接修改 `master`。

後續若要實作 P1/P2，建議從這個 branch 再拆更小的 feature branches，讓每個教學單元可獨立 review。
