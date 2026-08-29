---
marp: true
theme: default
size: 16:9
paginate: true
header: "Django 課程先備 00b｜HTML/CSS"
footer: "先備自學教材｜看懂網頁的骨架與化妝，再進 Django"
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

# Django 課程先備 00b
## HTML / CSS 先備

給「沒寫過網頁」就要學 Django template 的你。

**目標：看得懂 `templates/base.html` 的每一行，並知道 Bootstrap 在幫你做什麼。**

<!--
授課提示：開場可請學生打開任一常用網站按 F12，
指著 Elements 面板說「你現在看到的就是本冊要教的東西」。
-->

---

## 本課程的兩個專案：本冊為兩者共用

| 階段 | 專案 | 你會實作的頁面 |
|---|---|---|
| 第一階段 | **LearnBoard 學言板**（`learnboard/`） | 留言牆、登入／註冊、發表／編輯留言 |
| 第二階段 | **LearnMart 學購商城**（`learnmart/`） | 商品目錄、購物車、訂單 |

- 本冊所有 HTML/CSS 概念在兩個專案都會用到
- 內文標有「**LearnMart 對照**」的例子是第二階段的伏筆；第一階段請對照 `learnboard/templates/board/` 的同名版面
- 第 6 章實查對象：LearnBoard 的 `base.html` 與留言卡

<!--
授課提示：說明課程順序——先用最小的留言板學會全套基本功，
再用同一套功夫挑戰功能更完整的商城。兩個專案的模板結構高度相似。
-->

---

## 網頁三件套：各司其職

| 技術 | 負責 | 比喻 | 本課程用量 |
|---|---|---|---|
| **HTML** | 內容與結構 | 骨架 | 大量（template） |
| **CSS** | 外觀與排版 | 化妝＋服裝 | Bootstrap 代勞＋少量自訂 |
| JavaScript | 行為與互動 | 反應神經 | 本課程幾乎不用 |

Django 的角色：在伺服器端**把資料填進 HTML 模板**再回傳。

> 所以：不懂 HTML 就看不懂 Django 在做什麼。

<!--
授課提示：明確宣佈本課程不教 JS，降低焦慮。
強調順序：先骨架（HTML）、再化妝（CSS），最後 Django 才接得上。
-->

---

## 如何練習：一個檔案 + 一個瀏覽器就夠

```text
practice/
└── index.html      ← 用任何文字編輯器編輯
```

1. 編輯 `index.html`
2. 用瀏覽器直接開啟這個檔案（雙擊或拖進視窗）
3. 修改 → 存檔 → 重新整理

**必學工具：開發者工具（F12）**

- **Elements**：即時檢視 HTML 結構
- **Computed**：查看某元素的 CSS 最終計算值（含 box model 圖）

> 不需要伺服器；第 3 章之後才會由 Django 接手提供 HTML。

<!--
授課提示：花 2 分鐘帶 F12 的 Elements 與 Computed 面板。
之後所有「為什麼長這樣」的問題，第一動作都是打開 F12 自己查。
-->

---

## 六章地圖

| 章 | 主題 | 對應課程專案 |
|---:|---|---|
| 1 | HTML 文件結構 | `templates/base.html` 的 head |
| 2 | 常用標籤 | 留言卡、商品卡版面 |
| 3 | 表單標籤 | 搜尋列、註冊表單 |
| 4 | CSS 基礎 | `static/css/site.css` |
| 5 | RWD 概念 | Bootstrap grid、斷點 |
| 6 | 實查 LearnBoard | base.html、message_list.html |

每章同樣有「動手試」與附簡答的觀念檢核。

<!--
授課提示：告訴學生第 6 章是驗收站——能讀懂真實專案的模板才算過關。
-->
