# Django 教學專案

這是一套以 Django 為主的後端網站程式設計教學專案，透過三個逐步增加難度的實作專案，搭配投影片與練習手冊，帶學生從 Python 與 Django 基礎一路學到完整網站功能。

> ChatGPT 盤點版本：本 repository 的「專案結構＋教學內容盤點」見 [`CURRICULUM_AUDIT_CHATGPT.md`](CURRICULUM_AUDIT_CHATGPT.md)。該文件集中整理三階段能力矩陣、教材缺口與後續優先級。

## 三階段能力地圖

| 階段 | 專案 | 核心心智模型 | 主要新增能力 |
|---|---|---|---|
| 第一階段 | LearnBoard | 誰能讀／改哪一筆資料 | Django 基礎、CRUD、Form、Auth、Ownership、Testing |
| 第二階段 | LearnMart | 多筆資料如何保持一致 | 角色權限、購物車、庫存、訂單、transaction、資料完整性 |
| 第三階段 | LearnJournal | 內容如何被發佈、找到與擴充 | M2M、custom QuerySet、template tags、signals、data migration、效能議題 |

LearnJournal 目前已有第一批可執行教材與實作；後續的傳播、效能、帳號與部署主題仍依 `slides/03_next_project_plan.md` 逐步完成。

## 資料夾介紹

### [`learnboard/`](learnboard/)

**學言 LearnBoard：留言板入門專案**

以最小但完整的留言板開始學習 Django，練習專案與 App、URL、View、Template、Model、資料庫 migration、表單、登入，以及使用者只能管理自己資料的權限概念。

### [`learnmart/`](learnmart/)

**學購 LearnMart：商城實作專案**

在 LearnBoard 的基礎上，進一步實作商品目錄、賣家與買家角色、購物車、庫存、訂單、結帳交易與商品評分，學習如何處理較完整的資料流程與資料完整性。

### [`learnjournal/`](learnjournal/)

**學誌 LearnJournal：內容發佈平台**

以多作者文章平台延伸 Django 能力，練習文章、標籤、巢狀留言、文章發佈、客製化 QuerySet、template tags、signals、資料 migration 與效能相關概念。

目前可直接操作的內容以 Deck 03A 為主；sessions/cookies、cache、middleware、email/password reset、full-text search、RSS/sitemap、Group/Permission、排程與部署等仍屬後續教材目標。

### [`slides/`](slides/)

**課程投影片與實作教材**

三個專案共用的教學入口，包含 Python、HTML/CSS、Django 基礎、表單與身份驗證，以及各專案的實作章節、練習手冊與圖解教材。

## 建議學習順序

1. 先閱讀 `slides/` 中的 Python 與 HTML/CSS 先備教材。
2. 從 `learnboard/` 開始，建立 Django 基礎與網站開發流程。
3. 進入 `learnmart/`，練習商城、權限、購物車與訂單流程。
4. 最後學習 `learnjournal/`，延伸到內容管理、資料關聯與效能設計。
5. 待 LearnJournal 03B 與部署單元完成後，再補 sessions/cache、middleware、email、搜尋、權限與 production readiness。

每個 Django 專案都是獨立的練習環境，請在各自的資料夾中執行相關指令，不要共用虛擬環境或資料庫。
