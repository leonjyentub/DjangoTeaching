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

# 第 4 章
## CSS 基礎

**本章成果：**能讀懂選擇器與規則、看懂 box model，並知道 Bootstrap utility class 在做什麼。

<!--
授課提示：目標是「讀懂」而非「從零手刻」。
本課程外觀由 Bootstrap 代勞，學生需要的是看懂它加了什麼。
-->

---

## 4-1 三種套用 CSS 的方式

```html
<!-- 1. 行內樣式（優先度高，但難維護） -->
<p style="color: red;">…</p>

<!-- 2. 頁內樣式表 -->
<style>p { color: red; }</style>

<!-- 3. 外部檔案（本課程標準做法） -->
<link rel="stylesheet" href="style.css">
```

| 方式 | 適合 |
|---|---|
| inline | 一次性微調（少用） |
| `<style>` | 單頁實驗 |
| 外部 `.css` 檔 | 全站共用——兩個專案的 `static/css/site.css` |

<!--
授課提示：打開 base.html 找出兩個 link：
Bootstrap CDN 與 site.css。順序有意義——後載入的可以覆蓋前者。
-->

---

## 4-2 規則語法：誰 → 改什麼

```css
h1 {                        /* 選擇器 */
  color: #8f1d2c;           /* 屬性: 值; */
  font-size: 28px;
}
```

```text
選擇器 { 屬性: 值; }
```

- 一條規則可多個屬性；值有單位（px、rem、%）
- 註解用 `/* ... */`

**你應該看到：**改 `color` 存檔重新整理，標題變色——CSS 的回饋迴圈就是這麼快。

<!--
授課提示：讓每個學生把 site.css 某個顏色改錯一版再改回來，
確認「編輯→存檔→重新整理」的循環沒問題。
-->

---

## 4-3 選擇器四兄弟

```css
p          { }   /* 元素：所有 <p> */
.card      { }   /* class：class="card" 的元素（最常用） */
#header    { }   /* id：唯一的那個 */
.card p    { }   /* 後代：.card 裡面的 <p> */
```

```html
<article class="card featured">    <!-- 可掛多個 class，空格分隔 -->
```

> Bootstrap 的本質：一大包寫好的 class。`class="btn btn-primary"` 就是套用兩條現成規則。

<!--
授課提示：class 是絕對主力。請學生在 home.html 數一張商品卡掛了幾個 class。
-->

---

## 4-4 疊加與優先權：最後說的、說得越準的贏

```css
p        { color: gray; }     /* 先被套用 */
.card p  { color: navy; }     /* 更具體 → 贏 */
```

判斷直覺（由弱到強）：

1. 元素選擇器 `p`
2. class `.card`
3. 行內 `style="…"`
4. `!important`（核彈，別用）

同強度時，**寫在越後面**的贏。

**常見錯誤：**「明明改了卻沒變」九成是被更具體或更晚的規則覆蓋——F12 Computed 面板會列出每一條規則的勝負。

<!--
授課提示：示範一次「改了沒效」的排查流程：
F12 → 選元素 → 看 Styles/Computed 面板找被劃掉的屬性。
這個技能之後調 Bootstrap 樣式天天用。
-->

---

## 4-5 Box model：每個元素都是一個盒子

![box model](../assets/box_model.svg)

<!--
授課提示：用 F12 Computed 面板把同一張圖叫出來對照，
再改一次 padding 讓學生看到留白即時變化。
-->

---

## 4-5A Box model 快問快答

```css
.card {
  padding: 16px;
  border: 4px solid #8f1d2c;
  margin-bottom: 24px;
}
```

1. 內容與框線之間的空白是？　**答：padding**
2. 相鄰元素之間的距離是？　**答：margin**
3. `width` 預設只算 content；Bootstrap 用 border-box 讓 width 含 padding＋border

> Bootstrap 全站套了 `box-sizing: border-box`，所以你設多寬就幾乎是多寬。

<!--
授課提示：border-box 只需知道結論與好處，
細節等遇到尺寸怪異時再回來查。
-->

---

## 4-6 display：元素的排版性格

| display | 行為 | 例子 |
|---|---|---|
| `block` | 獨佔一行，可設寬高 | div、p、h1 |
| `inline` | 隨文字流動，寬高無效 | span、a |
| `inline-block` | 排一起但可設寬高 | 小徽章 |
| `flex` | 子元素排成彈性列／欄 | navbar |

```css
.nav-menu {
  display: flex;      /* 子項目橫排 */
  gap: 12px;          /* 項目間距 */
}
```

**常見錯誤：**給 `span` 設 `width` 卻沒反應——它是 inline，寬高無效。

<!--
授課提示：flex 只教到「能讓子元素排成一直列」即可；
Bootstrap 的 d-flex 就是 display:flex 的 class 版。
-->

---

## 第 4 章｜動手試與觀念檢核

**動手試：**

```html
<style>
  .box { padding: 12px; border: 2px solid red; margin: 8px; }
</style>
<div class="box">盒子 A</div>
<div class="box">盒子 B</div>
```

用 F12 觀察兩盒之間的距離來源。

**觀念檢核：**

1. `.card` 是哪種選擇器？　**答：class**
2. padding 和 margin 差在哪？　**答：框線內 vs 框線外**
3. 為什麼 span 設寬度無效？　**答：預設 inline**
4. `d-flex` 對應哪條 CSS？　**答：display: flex**

<!--
授課提示：四題全對代表第 4 章過關，可以進 RWD。
-->
