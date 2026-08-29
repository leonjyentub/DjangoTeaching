---
marp: true
theme: default
transition: fade
size: 16:9
paginate: true
header: "LearnBoard 01｜Django 基礎與資料驅動留言板"
footer: "初學者教材｜觀念 → 語法 → LearnBoard 實作"
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
  h1 { color: #1e3a8a; }
  h2 { color: #2c4fb8; }
  blockquote {
    border-left: 6px solid #93b4f0; padding-left: 18px; color: #2d3a55;
    font-family: 'Noto Serif CJK TC', 'Noto Sans CJK TC', 'WenQuanYi Zen Hei', serif;
  }
  code, kbd {
    font-family: 'Noto Sans Mono CJK TC', 'SF Mono', Consolas,
                 'WenQuanYi Zen Hei Mono', 'Courier New', monospace;
    font-size: 0.92em;
  }
  pre { font-size: 0.72em; line-height: 1.28; }
  table { font-size: 0.78em; }
  strong { color: #1e3a8a; }
---

# LearnBoard 01
## Django 基礎與資料驅動留言板

從可重現的 Python 環境開始，走完：

**瀏覽器 → URL → View → Model / ORM → Template → 響應式留言牆**

---

## 這份教材最後要完成什麼？

完成本份教材後，你應該能：

- 從零同步並啟動 LearnBoard 的本機環境
- 說明一次 HTTP request 如何得到 response
- 看懂 URL、function view、template 與 context 的合作方式
- 讀懂 Message model 的欄位、migration 與基本 ORM
- 追蹤搜尋與留言卡片的完整資料流
- 分辨「教學縮小版」與「目前 LearnBoard 完整實作」

> 目標不是背 API，而是能回答：「資料從哪裡來？經過什麼？最後在哪裡顯示？」

<!--
授課提示：開場定錨頁。請學生抄下底部引句「資料從哪裡來？經過什麼？最後在哪裡顯示？」，整個第一階段每次實作都回扣這三問。
-->

---

## 課程地圖：先用留言板練功，再挑戰商城

| 階段 | 專案 | 教材 | 你會做出來的東西 |
|---|---|---|---|
| 第一階段 | **LearnBoard 學言板** | 本冊＋Deck 02 | 留言牆、帳號、發文、擁有權權限 |
| 第二階段 | **LearnMart 學購商城** | LearnMart Deck 01／02 | 商品目錄、購物車、訂單交易 |

概念會直接搬過去：留言 Message ↔ 商品 Product；「只能編輯自己的留言」↔「賣家只能管理自己的商品」。

先把小專案的每一層摸透，商城只是同樣循環的加強版。

<!--
授課提示：這頁是整門課的地圖。強調兩個專案的檔案結構幾乎同構——學會 board/models.py 就等於看懂 marketplace/models.py 的縮影。
-->

---

## 六章課程地圖：由環境走到留言牆

| 章 | 核心問題 | 可觀察成果 |
|---:|---|---|
| 1 | 如何讓每台電腦使用同一套 Python 依賴？ | LearnBoard 可啟動 |
| 2 | Request 如何找到 View？ | 能追蹤 200／404／500 |
| 3 | 資料如何安全形成響應式 HTML？ | Template＋static 頁面 |
| 4 | 留言資料如何持久化？ | Model＋migration＋admin |
| 5 | 如何查詢與過濾留言？ | ORM＋shell 實測 |
| 6 | 各層如何組成可搜尋的留言牆？ | 完整 vertical slice |

每章只新增前一章所需的下一層；Deck 02 才進入 POST、帳號與權限。

<!--
授課提示：時間分配參考：第 1 章可指定課前自學；第 4 章資訊量最大，建議排雙倍課時。若學生已完成 LearnMart 課程（反向修課），本章可當對照複習。
-->

---

## 程式碼來源標籤：先知道「能否直接對照」

### 教學用最小範例
一次隔離一個新概念；可能省略權限、最佳化或 class-based view，且不一定存在於 repository。

### 目前 LearnBoard 實作
與 repository 的檔案、名稱、流程一致，未省略影響理解的內容。

### 目前 LearnBoard 節錄／重排
來自目前 source，但為版面省略或換行；會顯示檔名與 symbol，不能誤認為完整檔案。

> 第一階段尚未實作的功能（發文表單、作者欄位、權限）在最小範例出現時都會標注「Deck 02 回收」。

---

## 教學導航標籤：知道這頁要怎麼使用

- **補充／進階**：重要但不是第一次實作的必要前置；可先建立邊界。
- **常見錯誤**：指出容易混淆、會造成例外或安全問題的寫法。
- **配套實作手冊**：投影片只留問題；答案、修改步驟與驗收放在 workbook。
- **你應該看到**：網址、狀態碼、頁面文字、shell 物件、資料筆數或 test result。

後續 source snippet 會選用上述來源標籤；章末一律連到相同章名的配套手冊。

---

## 學習方式：每章都走同一個循環

1. **問題**：為什麼需要這個機制？
2. **心智模型**：先用一句話掌握角色
3. **最小範例**：一次只加入一個新概念
4. **語法拆解**：參數與回傳值放在相近頁面
5. **LearnBoard 對照**：回到真實檔案
6. **可觀察結果**：知道成功長什麼樣
7. **觀念檢核＋實作任務**：題目在投影片，答案與步驟在配套手冊

<!--
授課提示：向學生聲明這個循環之後不再重複解釋，看到新章節自動對號入座，可降低認知負擔。
-->
