---
marp: true
theme: default
size: 16:9
paginate: true
header: "Django 01｜共通基礎：LearnBoard × LearnMart"
footer: "初學者教材｜共通觀念 → 兩個專案對照"
style: |
  section {
    font-family: 'Noto Sans CJK TC', 'Noto Serif CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', 'Heiti TC', sans-serif;
    font-size: 28px;
    line-height: 1.35;
    padding: 58px 70px;
  }
  h1, h2 {
    font-family: 'Noto Sans CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', sans-serif;
  }
  h1 { color: #8f1d2c; }
  h2 { color: #a52a3a; }
  blockquote {
    border-left: 6px solid #d69aa3; padding-left: 18px; color: #4c3438;
    font-family: 'Noto Serif CJK TC', 'Noto Sans CJK TC', 'WenQuanYi Zen Hei', serif;
  }
  code, kbd {
    font-family: 'Noto Sans Mono CJK TC', 'SF Mono', Consolas,
                 'WenQuanYi Zen Hei Mono', 'Courier New', monospace;
    font-size: 0.92em;
  }
  pre { font-size: 0.72em; line-height: 1.28; }
  table { font-size: 0.78em; }
  strong { color: #7d1726; }
---

# Django 01
## 兩個 Django 專案的共通基礎

從可重現的 Python 環境開始，走完：

**瀏覽器 → URL → View → Model / ORM → Template → 響應式頁面**

---

## 這份整合教材服務哪兩個專案？

本冊把兩個 repository 中重複的 Django 基礎合併成一條教學線；每個概念都先講共通規則，再指出兩個專案的實際落點：

| LearnBoard 學言板 | LearnMart 學購商城 |
|---|---|
| `board/` app、`Message`、留言牆 | `marketplace/` app、`Product`、商品目錄 |
| `Message.author` 可為 NULL | `Product.seller`、自訂 `User.role` |
| `?q=` 搜尋留言 | `?q=`＋`?category=` 篩選商品 |
| `ListView`＋分頁 | `ListView`＋分頁＋圖片／分類 |
| `templates/board/` | `templates/marketplace/` |

本冊以共通 Django 模型為主，商城的額外欄位與查詢則作為加深案例；若某些步驟覺得眼熟，那是設計好的。

<!--
授課提示：開場用這頁做前測——請學生在兩個專案中各指出一個 URL、View、Template 與 Model。答得出的共通內容快速帶過，把時間留給差異。
-->

---

## 學完後要能讀懂什麼？

完成本份教材後，你應該能：

- 從零同步並啟動 LearnBoard 與 LearnMart 的本機環境
- 說明一次 HTTP request 如何得到 response
- 看懂 URL、function view、template 與 context 的合作方式
- 讀懂兩個專案的 Model 欄位、關聯、migration 與基本 ORM
- 追蹤留言搜尋、商品搜尋／分類、分頁與卡片的資料流
- 分辨「教學縮小版」與兩個 repository 的目前實作

> 目標不是背 API，而是能回答：「資料從哪裡來？經過什麼？最後在哪裡顯示？」

<!--
授課提示：開場定錨頁。請學生抄下底部引句「資料從哪裡來？經過什麼？最後在哪裡顯示？」，整學期每次實作都回扣這三問。
-->

---

## 六章課程地圖：由環境走到兩種資料驅動頁面

| 章 | 核心問題 | 可觀察成果 |
|---:|---|---|
| 1 | 如何讓每台電腦使用同一套 Python 依賴？ | 兩個專案都可啟動 |
| 2 | Request 如何找到 View？ | 能追蹤 200／404／500 |
| 3 | 資料如何安全形成響應式 HTML？ | Template＋static 頁面 |
| 4 | 資料如何持久化並建立關聯？ | `Message`／`Product`＋migration＋admin |
| 5 | 如何查詢、組合並驗證資料規則？ | ORM＋QuerySet；商城再加 optimization |
| 6 | 各層如何組成資料驅動頁面？ | 留言牆與商品目錄兩條 vertical slice |

每章只新增前一章所需的下一層；Deck 02 再進入表單、權限與商城交易流程。

> LearnBoard 與 LearnMart 的 POST、登入與物件權限會在 Deck 02 並列；商城再加上購物車、訂單與交易一致性。

<!--
授課提示：時間分配參考：第 1 章可指定課前自學；第 4、5 章資訊量最大，建議各排雙倍課時。
-->

---

## 學習方式：每章都走同一個循環

1. **問題**：為什麼需要這個機制？
2. **心智模型**：先用一句話掌握角色
3. **最小範例**：一次只加入一個新概念
4. **語法拆解**：參數與回傳值放在相近頁面
5. **雙專案對照**：回到 `learnboard/` 或 `learnmart/` 的真實檔案
6. **可觀察結果**：知道成功長什麼樣
7. **觀念檢核＋實作任務**：題目在投影片，答案與步驟在配套手冊

<!--
授課提示：向學生聲明這個循環之後不再重複解釋，看到新章節自動對號入座，可降低認知負擔。
-->

---

## 兩個專案的讀檔路線

遇到同一個 Django 概念時，依下表選一條路線實作；另一欄用來確認概念能遷移，而不是要求兩個專案都改一遍。

| 共通概念 | LearnBoard 學言板 | LearnMart 學購商城 |
|---|---|---|
| Project／App | `learnboard/config/`、`learnboard/board/` | `learnmart/config/`、`learnmart/marketplace/` |
| 列表 View | `MessageListView` | `ProductListView` |
| 列表模板 | `templates/board/message_list.html` | `templates/marketplace/home.html` |
| 搜尋 | `Message.content__icontains` | `Product.name/description__icontains` |
| 依賴 | Django | Django＋Pillow（`ImageField`） |

**課堂建議：** 先在 LearnBoard 完成最小 vertical slice，再用 LearnMart 的對照欄找出「相同骨架、更多資料規則」的部分。
