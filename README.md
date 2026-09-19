# Django 教學專案

這是一套以 Django 為主的後端網站程式設計教學專案，透過三個逐步增加難度的實作專案，搭配投影片與練習手冊，帶學生從 Python 與 Django 基礎一路學到完整網站功能與 production readiness。

> ChatGPT 盤點版本：本 repository 的「專案結構＋教學內容盤點」見 [`CURRICULUM_AUDIT_CHATGPT.md`](CURRICULUM_AUDIT_CHATGPT.md)。

## 三階段能力地圖

| 階段 | 專案 | 核心心智模型 | 主要新增能力 |
|---|---|---|---|
| 第一階段 | LearnBoard | 誰能讀／改哪一筆資料 | Django 基礎、CRUD、Form、Auth、Ownership、Testing |
| 第二階段 | LearnMart | 多筆資料如何保持一致 | 角色權限、購物車、庫存、訂單、transaction、資料完整性 |
| 第三階段 | LearnJournal | 內容如何被發佈、找到、傳播與排程 | M2M、custom QuerySet、template tags、signals、cache、email、permissions、feed、scheduler、search |

LearnJournal 03A 與 03B 現在都有可執行程式與分章教材；最後另有跨三專案共用的 Deployment / Operations 單元。

## 資料夾介紹

### [`learnboard/`](learnboard/)

**學言 LearnBoard：留言板入門專案**

以最小但完整的留言板開始學習 Django，練習 Project/App、URL、View、Template、Model、migration、表單、登入，以及使用者只能管理自己資料的權限概念。

### [`learnmart/`](learnmart/)

**學購 LearnMart：商城實作專案**

在 LearnBoard 的基礎上，進一步實作商品目錄、賣家與買家角色、購物車、庫存、訂單、結帳交易與商品評分，學習跨模型 workflow、transaction 與資料完整性。

### [`learnjournal/`](learnjournal/)

**學誌 LearnJournal：內容發佈平台**

03A 練習文章、標籤、巢狀留言、客製化 QuerySet、template tags、signals 與 data migration；03B 進一步實作 sessions/cookies、cache、middleware、email/password reset、Group/Permission、RSS/sitemap、排程 command 與 PostgreSQL full-text search。

### [`slides/`](slides/)

**課程投影片與實作教材**

包含 Python、HTML/CSS、Django 基礎、表單與身份驗證、first-contact 操作補充、Django Template Language 實用工具箱、LearnJournal 03A/03B，以及跨專案 Deployment / Operations 教材與 workbook。

## 建議學習順序

1. Python、Git 與 HTML/CSS 先備教材。
2. [Django 連續教學教材](slides/README.md)：27 章、17 份 Marp，整合環境、頁面、資料層、表單、權限、商城流程、安全測試及部署維運。
3. LearnJournal 03A：內容模型、M2M、發佈與進階 ORM。
4. LearnJournal 03B：state/cache、middleware、email、permissions、feed、scheduler、PostgreSQL search；再將部署維運檢核套到第三專案。

主線按 `slides/` 下的連續教材檔名順序授課；LearnBoard／LearnMart 作章內案例，LearnJournal 為後續延伸。原 01、01B、02、03 教材已整併至連續教材並移除，逐頁去向見 [來源索引](slides/SOURCE_MAP.md)。全部教材入口見 [slides/README.md](slides/README.md)。

## Repository 級教材驗證

```bash
python scripts/check_material_links.py
```

`.github/workflows/material-links.yml` 會在 PR、`master` 與 `chatgpt/**` branch push 時檢查 Markdown 相對連結。LearnJournal 另有 `.github/workflows/learnjournal-tests.yml` 跑 `check`、migration drift 與 tests。

每個 Django 專案都是獨立的練習環境，請在各自資料夾執行相關指令，不要共用虛擬環境或 SQLite 資料庫。
