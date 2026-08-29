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

# 第 5 章
## RWD：同一份 HTML，各種螢幕都好看

**本章成果：**能解讀 Bootstrap 斷點 class，理解 mobile-first 的「以上生效」規則。

<!--
授課提示：本章是 Deck 01 3-18、3-19 的先修。
教完這裡，主教材那兩頁會變成複習而不是新知。
-->

---

## 5-1 media query：CSS 的條件判斷

```css
/* 螢幕寬度 768px 以上才套用 */
@media (min-width: 768px) {
  .menu { display: flex; }
}
```

- 條件成立才套用該組規則
- 手機直向約 375px；平板 768px；桌機常見 1200px 以上

> RWD 不是偵測設備型號，而是**依視窗寬度**決定樣式。

<!--
授課提示：讓學生拖曳瀏覽器視窗寬度看 LearnBoard 留言牆欄數變化，
再打開 F12 的裝置模擬模式（手機圖示）玩一輪。
-->

---

## 5-2 mobile-first：小螢幕是預設值

```html
<div class="row row-cols-1 row-cols-md-3">
```

讀法：

| class | 生效範圍 |
|---|---|
| `row-cols-1` | 一律：每列 1 欄（手機預設） |
| `row-cols-md-3` | **md（768px）以上**：每列 3 欄 |

- `md` 不是「只有 md 時」，而是「md 起持續生效」
- 沒寫前綴的 class 是所有寬度的基底

**你應該看到：**把手機模擬調到 767px 與 768px 各看一次——欄數在邊界切換。

<!--
授課提示：「以上生效」是 Deck 01 3-19 的檢核題，
在這裡先用實驗建立直覺。768 前後各測一次的動作請全班做。
-->

---

## 5-3 為什麼本課程用 Bootstrap？

| 不用框架 | 用 Bootstrap |
|---|---|
| 自己寫 grid、斷點、元件 | CDN 一行引入即可開始 |
| 需要建置工具（Node/Sass） | 純 CSS，不需建置 |
| 樣式品質參差不齊 | 元件一致、文件完整 |

代價：class 很長、頁面長得像 Bootstrap。

本課程立場：**先學會在其上客製**（`static/css/site.css`），之後想換 Tailwind 或自製都容易。

<!--
授課提示：說明這是教學取捨而非業界唯一解；
學生問 Tailwind 時給予肯定並指向課後自學。
-->

---

## 第 5 章｜觀念檢核

1. `col-md-6` 在 400px 寬的手機上佔幾欄？　**答：整列（退回預設行為）**
2. 斷點 class 是「只有那個寬度」還是「那個寬度以上」？　**答：以上**
3. RWD 依據的是設備型號嗎？　**答：不是，是視窗寬度**

<!--
授課提示：第 1 題最容易錯——正確心智：
沒有 md 前綴的基底 class 才管小螢幕。
-->
