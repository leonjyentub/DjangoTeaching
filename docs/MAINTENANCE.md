# 教材維護摘要

整理日期：2026-09-20。原盤點報告、第三專案規劃與驗證紀錄合併於此；完整舊稿可由 Git 歷史查閱。本文件保留維護決策與延伸候選，不逐次累加修改流水帳。

## 目前入口與維護原則

- 授課順序、教材清單與能力地圖：[專案 README](../README.md)、[教材 README](../slides/README.md)。
- Django 主線為 17 份 Marp、27 章；LearnBoard／LearnMart 作章內案例，LearnJournal 為後續延伸。
- LearnJournal 的啟動方式與功能以[專案說明](../learnjournal/README.md)為準；原規劃中的「03B 尚未做」已過時。
- First-contact lab 與 DTL 工具已併入主線；部署與維運位於第 22～27 章。
- 三個專案各自管理環境與資料庫。版本宣告以各專案 `pyproject.toml`、`.python-version` 與 `uv.lock` 為準。
- 既有 migration 的產生版本屬歷史資訊，不為文字一致而改寫。
- [來源索引](../slides/SOURCE_MAP.md)保留整併概要；完整逐頁對應與當時雜湊集中於 [source_manifest.json](../slides/source_manifest.json)。
- [Workbook 對照](../slides/WORKBOOK_MAP.md)仍用於授課；[圖解提示詞](../slides/diagram_prompts.md)仍用於重製資產。

## 歷史驗證摘要（2026-09-19）

以下是原 QA 文件的歷史結果，並非本次重新渲染或執行 Django 的結果。

- 當時 17 份教材渲染為 679 頁；12 份來源的 610 個頁段均有去向（503 保留、34 改寫、73 合併，含空白頁處理）。
- 使用 Marp CLI 4.5.1 與 Chrome，在 1280 × 720 檢查內容邊界、頁尾、程式碼溢出與圖片載入；8 次圖片引用成功，全頁自動檢查無旗標，另抽查代表頁與密集頁。
- HTTP／MVT 圖與說明拆頁；部分密集頁採 compact class，沿用 django-teal 主題。
- 原資料夾當時以雜湊確認未變更，之後已整併移除；原稿留在 Git 歷史。
- 當時未重新驗證 Django 安裝、全部課堂練習、部署或外部網址。頁碼、頁數及雜湊均是整併時快照，教材後續修改須重新確認。
- 原 QA 提及的 7 個失效連結已不代表目前狀態：2026-09-20 整理前重跑連結檢查，59 份 Markdown 全數通過。
- 原 QA 記錄版本檢查器會掃到 `.venv` 套件內容而失敗；本次未修訂該掃描範圍，也未重驗版本基準。

## 常用檢查

在 repository 根目錄執行：

```bash
python3 scripts/check_material_links.py
python3 scripts/check_version_baseline.py
```

Django 功能有變更時，在受影響專案內執行 `uv run python manage.py check`、`uv run python manage.py makemigrations --check` 與 `uv run python manage.py test`；CI 設定見 [.github/workflows](../.github/workflows/)。

Marp 版面修改後可輸出暫存 HTML：

```bash
marp --no-config --html --theme-set slides/themes/django-teal.css --template bare slides/courses/01_開發環境與專案建立.md -o /private/tmp/django-course-preview.html
```

暫存 HTML 的圖片需以原 Markdown 所在資料夾作 base；檢查圖片、頁尾與密集頁。日常閱讀可直接使用 Marp Preview。

## 待評估延伸

下列保留自原規劃與盤點，屬候選方向，未承諾排程；實作前先核對現有教材與程式，避免把舊規劃誤認為已完成或仍然缺漏。

- Python 補充：lambda／排序鍵、格式規格、條件運算、context manager、datetime、generator、comprehension／解包、collections／functools、自訂例外、dunder、進階型別、re、Enum、pathlib。
- LearnJournal 內容操作：inline formset 多圖／外部連結、追蹤與收藏、Markdown 匯入與每週摘要、媒體驗證。
- 搜尋與效能：中文斷詞、GIN／持久化搜尋向量、Redis 共用快取與失效策略。
- 正式環境：SMTP、背景工作佇列、rate limit、垃圾內容審核、監控與物件儲存。
- 選修：i18n／l10n、輕量 AJAX／HTMX、進階 ORM 與 signal 副作用測試。

## 查閱舊稿

完整盤點、規劃、逐頁表與 QA 都保留在整理前的 Git 版本，例如：

```bash
git show c14f346:CURRICULUM_AUDIT_CHATGPT.md
git show c14f346:slides/03_next_project_plan.md
git show c14f346:slides/QA.md
git show c14f346:slides/SOURCE_MAP.md
```
