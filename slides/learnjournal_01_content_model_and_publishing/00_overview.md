---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnJournal 01｜內容模型與發佈"
footer: "初學者教材｜觀念 → 語法 → LearnJournal 實作"
---

<!-- _class: cover -->

# LearnJournal 01
## 內容模型與發佈

<div class="box">多對多內容結構 → 發佈生命週期 → 可被搜尋、被彙整、被回應的頁面</div>

課程第三階段：從「能安全地改資料」前進到高階內容系統

<!--
授課提示：開場問學生：前兩個專案的資料關聯只有 ForeignKey（一對多）。
「一篇文章有很多標籤、一個標籤有很多文章」要怎麼存？這就是本冊的起點。
-->

---

## 課程三階段：這是第三根支柱

| 階段 | 專案 | 領域主軸 | 你已建立的心智模型 |
|---|---|---|---|
| 一 | LearnBoard 學言板 | 社群 CRUD ＋擁有權 | 誰可以改哪一筆資料 |
| 二 | LearnMart 學購商城 | 交易 ＋資料完整性 | 多筆寫入一起成功或一起失敗 |
| **三** | **LearnJournal 學誌** | **內容發佈與傳播 ＋效能** | **內容做出來 → 被找到 → 被回應** |

前兩階段見 `../learnboard_01_*`／`../learnboard_02_*`／`../learnmart_01_*`／`../learnmart_02_*`。

> 本冊不再雙軌對照。LearnJournal 是單一專案；需要對照時直接回指 LearnBoard／LearnMart 的具體檔案。

<!--
授課提示：強調「不再雙軌」是刻意的——前兩冊用兩個專案互相印證骨架，
到第三個專案學生已經有骨架，重點放在新結構本身。
-->

---

## 承接前兩個專案：你已經會的事

| 你已經寫過 | 本冊如何延伸 |
|---|---|
| `ForeignKey`、`related_name`、`on_delete` | 加上 **`ManyToManyField`** 與 **中介模型 `through`** |
| `Product.objects.filter(is_active=True)` 到處重複 | 收斂成 **自訂 Manager**：`Article.published.all()` |
| LearnMart 扣庫存 `stock -= n`（有 race） | 用 **`F()` 表達式**做原子遞增，這次做對 |
| `ListView`／`DetailView` | 加上 **日期型 generic view**（年／月彙整） |
| `aggregate()`／`annotate()` | 用 **`values().annotate()`** 做 GROUP BY（標籤雲） |
| LearnMart `add_review` 手工 function view | 用 **`FormMixin` 疊在 `DetailView`** |
| context processor | 加上 **自訂 template tag** 與 **signal** |

<!--
授課提示：這頁當前測。請學生在 learnmart 專案指出對應檔案；答得出的部分快速帶過。
-->

---

## 完成本冊後你應該能……

- 設計「一對多」與「多對多」混合的資料模型，並解釋為何需要中介模型
- 用一支 `RunPython` data migration 把舊資料轉成新關聯
- 把重複的查詢條件收斂到自訂 Manager／QuerySet
- 說明 `F()` 表達式為什麼能避免 race condition，SQLite 又保證到哪
- 追蹤 `/2026/08/29/<slug>/` 這種網址從 URLconf 到 template 的完整流程
- 解釋自訂 template tag 的三種形式，以及 `mark_safe` 的安全邊界
- 用自我關聯 ForeignKey 實作巢狀留言，並用 `FormMixin` 讓 DetailView 收 POST

> 核心問題：**「這個內容跟哪些東西有關聯？它什麼時候該公開？讀者怎麼找到它、怎麼回應它？」**

---

## 六章課程地圖

| 章 | 核心問題 | 可觀察成果 |
|---:|---|---|
| 1 | 第三個專案怎麼啟動？還缺哪些 Python 語法？ | LearnJournal 可啟動、seed 完成 |
| 2 | 一篇文章多個標籤怎麼存？舊資料怎麼搬？ | M2M、through、data migration |
| 3 | 「已發佈」的定義到處重複，怎麼收斂？ | 自訂 Manager、`F()`、CheckConstraint |
| 4 | 文章網址要含日期，彙整頁怎麼做？ | `/2026/08/`、`/2026/08/29/<slug>/` |
| 5 | Markdown、閱讀時間、標籤雲放哪裡？ | 自訂 template tag／filter |
| 6 | 巢狀留言與審核 | self-FK、`FormMixin`、signal 入門 |

每章只新增前一章之上的一層；Deck 03B 才進入快取、signal 深入、middleware、email 與全文檢索。

<!--
授課提示：時間分配：第 1 章可課前自學；第 2、4 章資訊量最大，各排雙倍課時。
-->

---

## 程式碼來源標籤（沿用前兩冊）

<span class="label">教學用最小範例</span>：一次隔離一個新概念；可能省略最佳化或錯誤處理，不一定存在於 repository。

<span class="label current">目前 LearnJournal｜逐字摘錄</span>：未改寫的 `learnjournal/` source 片段。<br>
<span class="label current">目前 LearnJournal｜節錄／重排</span>：省略無關行、重排換行或加入 `...`；語意對齊，不是逐字 source。

<span class="label warning">常見錯誤／限制</span>：初學者容易誤解，或教學版尚未處理的情況。

<span class="label check">配套實作手冊</span>：答案、修改步驟與前後程式碼放在 `../workbooks/learnjournal_01_*_workbook.md`。

---

## 學習方式：每章都走同一個循環

1. **問題**：為什麼需要這個機制？
2. **心智模型**：先用一句話掌握角色
3. **最小範例**：一次只加入一個新概念
4. **語法拆解**：參數與回傳值放在相近頁面
5. **回扣舊專案**：指出 LearnBoard／LearnMart 的對應檔案
6. **可觀察結果**：知道成功長什麼樣（網址、狀態碼、`test` 結果、shell 物件）
7. **觀念檢核＋實作任務**：題目在投影片，答案與步驟在配套手冊

<!--
授課提示：這個循環在前兩冊已聲明過；本冊只提醒一次，看到新章節自動對號入座。
-->

---

## 環境提醒：三個專案的資料庫不要混用

```bash
cd learnjournal
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver
```

- `learnjournal/` 有自己的 `.venv`、`db.sqlite3`、`uv.lock`
- 示範帳號：`amy/amy12345`、`ben/ben12345`、`editor/editor12345`
- 驗證指令與前兩冊相同：

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

> **你應該看到**：11 支 `TestCase` 全數通過，`makemigrations --check` 顯示 `No changes detected`。
