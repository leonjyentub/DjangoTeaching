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

# 第 1 章
## HTML 文件結構

**本章成果：**能畫出一份 HTML 文件的層級，說出 head 與 body 各放什麼。

<!--
授課提示：本章目標只有兩個：標籤解剖圖、head/body 分工。
語意細節交給第 2 章。
-->

---

## 1-1 元素解剖：標籤、屬性、內容

```html
<a href="https://djangoproject.com" target="_blank">
  Django 官網
</a>
```

```text
<a ...>  開始標籤
</a>     結束標籤
href=    屬性名稱        屬性值一律用引號包住
"..."    屬性值
中間文字  內容
```

- 元素 = 開始標籤 ＋ 內容 ＋ 結束標籤
- 屬性提供「額外設定」，寫在開始標籤內

**常見錯誤：**忘記結束標籤 → 版面整個跑掉。F12 的 Elements 面板會自動幫你補齊成奇怪形狀，那就是線索。

<!--
授課提示：示範刪掉 </a> 後版面如何被拖累，
讓「成對」的重要性被親眼看見。
-->

---

## 1-2 最小 HTML 文件

```html
<!DOCTYPE html>
<html lang="zh-Hant">
  <head>
    <meta charset="utf-8">
    <title>我的練習頁</title>
  </head>
  <body>
    <h1>Hello</h1>
  </body>
</html>
```

| 區塊 | 角色 |
|---|---|
| `<!DOCTYPE html>` | 宣告「我是現代 HTML」（固定寫法） |
| `<html>` | 整份文件根元素 |
| `<head>` | 給瀏覽器看的資訊（不顯示在畫面） |
| `<body>` | 使用者看到的內容 |

**你應該看到：**分頁標題變成「我的練習頁」——那就是 `<title>`。

<!--
授課提示：DOCTYPE 和 lang 不必深究原因，當成固定咒語；
重點是 head/body 的分工：一個給機器、一個給人。
-->

---

## 1-3 head 裡的三個常客

```html
<meta charset="utf-8">          <!-- 字元編碼：中文不亂碼 -->
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>學言板</title>
<link rel="stylesheet" href="style.css">   <!-- 接上 CSS -->
```

- `charset`：沒有它中文可能變亂碼
- `viewport`：手機依裝置寬度顯示——RWD 的入場券（Deck 01 3-17 會回頭講）
- `link`：把外部 CSS 接進來；兩個課程專案的 `base.html` 正是這樣載入 Bootstrap 與 `site.css`

<!--
授課提示：打開 templates/base.html 前 15 行對照，
學生會發現四行全部都在，多出來的是 Django template 語法（第 6 章揭曉）。
-->

---

## 1-4 巢狀與縮排：HTML 是一棵樹

```html
<body>                      ← 祖父
  <header>                  ← 父
    <h1>學購</h1>            ← 子
  </header>
  <main>
    <article>…</article>
  </main>
</body>
```

- 縮排只是慣例，但**強烈建議每層 2 格**，樹狀關係一目了然
- 巢狀不可交叉：`<b><i></b></i>` 是非法形狀

**你應該看到：**F12 Elements 面板就是這棵樹的互動版，點哪個節點、畫面就高亮哪塊區域。

<!--
授課提示：請學生在 F12 點幾個節點玩高亮，
建立「DOM 樹 ↔ 畫面區塊」的直覺映射。
-->

---

## 1-5 註解與空元素

```html
<!-- 這段註解不會顯示 -->

<img src="cat.jpg" alt="一張貓">   <!-- 空元素：沒有內容，不需要結束標籤 -->
<br>
<input name="q">
```

- 註解寫法：`<!-- ... -->`
- img、input、br 等**空元素**天生沒有內容，也就沒有結束標籤

**常見錯誤：**把 `</img>` 補上去——不需要，反而困惑。

<!--
授課提示：alt 屬性先埋一句「無障礙＋圖片壞掉時的替代文字」，
Deck 01 6-14 會完整回收。
-->

---

## 第 1 章｜動手試與觀念檢核

**動手試：**做出你的第一頁：

```html
<!DOCTYPE html>
<html lang="zh-Hant">
<head><meta charset="utf-8"><title>自我介紹</title></head>
<body><h1>大家好，我是 OOO</h1></body>
</html>
```

**觀念檢核：**

1. `<head>` 裡的內容會顯示在畫面上嗎？　**答：大多不會**
2. viewport meta 缺了會怎樣？　**答：手機可能以桌面寬度縮放顯示**
3. `<input>` 需要結束標籤嗎？　**答：不需要（空元素）**

<!--
授課提示：三分鐘小關卡，全部通過才進第 2 章。
-->
