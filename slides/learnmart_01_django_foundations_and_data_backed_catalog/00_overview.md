---
marp: true
theme: default
size: 16:9
paginate: true
header: "LearnMart 01｜Django 基礎與資料驅動商品目錄"
footer: "初學者教材｜觀念 → 語法 → LearnMart 實作"
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

# LearnMart 01
## Django 基礎與資料驅動商品目錄

從可重現的 Python 環境開始，走完：

**瀏覽器 → URL → View → Model / ORM → Template → 響應式商品頁**

---

## 承接 LearnBoard：你已經會的事

第一階段的留言板課程（見 `../learnboard_01_django_foundations_and_message_board/` 與 `../learnboard_02_forms_auth_and_board_workflows/`）已經帶你走過同樣的六層循環：

| LearnBoard 留言板 | 本冊商城對應 |
|---|---|
| Message model＋migration | Product／Order 等 model 設計 |
| 留言牆搜尋（icontains） | 商品列表搜尋＋分類篩選 |
| ListView＋分頁 | 同款 CBV，加上圖片 |
| base.html／留言卡 RWD | 商品卡 grid |

本冊以商城語境**重新走一遍並加深**；若某些步驟覺得眼熟，那是設計好的。

<!--
授課提示：開場用這頁做前測——請學生指出留言板專案中對應的檔案位置。答得出來的部分快速帶過，把時間留給本章新增的內容。
-->

---

## 這份教材最後要完成什麼？

完成本份教材後，你應該能：

- 從零同步並啟動 LearnMart 的本機環境
- 說明一次 HTTP request 如何得到 response
- 看懂 URL、function view、template 與 context 的合作方式
- 讀懂 Model 欄位、關聯、migration 與基本 ORM
- 追蹤搜尋、分類、分頁與商品卡片的完整資料流
- 分辨「教學縮小版」與「目前 LearnMart 完整實作」

> 目標不是背 API，而是能回答：「資料從哪裡來？經過什麼？最後在哪裡顯示？」

<!--
授課提示：開場定錨頁。請學生抄下底部引句「資料從哪裡來？經過什麼？最後在哪裡顯示？」，整學期每次實作都回扣這三問。
-->

---

## 六章課程地圖：由環境走到商品目錄

| 章 | 核心問題 | 可觀察成果 |
|---:|---|---|
| 1 | 如何讓每台電腦使用同一套 Python 依賴？ | LearnMart 可啟動 |
| 2 | Request 如何找到 View？ | 能追蹤 200／404／500 |
| 3 | 資料如何安全形成響應式 HTML？ | Template＋static 頁面 |
| 4 | 商城資料如何持久化並建立關聯？ | Model＋migration＋admin |
| 5 | 如何查詢、組合並驗證資料規則？ | ORM＋query optimization |
| 6 | 各層如何組成搜尋商品目錄？ | 完整 vertical slice |

每章只新增前一章所需的下一層；Deck 2 才進入 POST、權限與交易流程。

> POST 與物件權限的基本型你在 LearnBoard Deck 02 已經寫過（發文表單、擁有權 mixin）；本課程會在同樣骨架上加深加廣。

<!--
授課提示：時間分配參考：第 1 章可指定課前自學；第 4、5 章資訊量最大，建議各排雙倍課時。
-->

---

## 程式碼來源標籤：先知道「能否直接對照」

### 教學用最小範例
一次隔離一個新概念；可能省略權限、最佳化或 class-based view，且不一定存在於 repository。

### 目前 LearnMart 實作
與 repository 的檔案、名稱、流程一致，未省略影響理解的內容。

### 目前 LearnMart 節錄／重排
來自目前 source，但為版面省略或換行；會顯示檔名與 symbol，不能誤認為完整檔案。

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
5. **LearnMart 對照**：回到真實檔案
6. **可觀察結果**：知道成功長什麼樣
7. **觀念檢核＋實作任務**：題目在投影片，答案與步驟在配套手冊

<!--
授課提示：向學生聲明這個循環之後不再重複解釋，看到新章節自動對號入座，可降低認知負擔。
-->
