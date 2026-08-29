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

# 第 2 章
## 常用標籤

**本章成果：**能認出課程專案模板中九成的標籤，並知道各自語意。

<!--
授課提示：本節用「商品卡」貫穿：一張卡片就會用到
article、img、h2、p、a、button——教完直接能讀 home.html。
-->

---

## 2-1 標題與段落

```html
<h1>學購商城</h1>       <!-- 一頁最好只有一個 h1 -->
<h2>熱銷商品</h2>
<p>這是說明文字段落。</p>
```

- h1～h6 是**大綱層級**，不是字體大小（大小交給 CSS）
- `<p>` 包一段文字；多餘空白與換行會被壓縮成一格

<!--
授課提示：示範在 HTML 裡按十個空格與三個 Enter，
瀏覽器只顯示一格——想換行請用 <br> 或拆成兩個 <p>。
-->

---

## 2-2 a：連結是網站的血管

```html
<a href="/products/3/">看這個商品</a>
<a href="https://example.com" target="_blank">外部連結</a>
```

- `href` 指定目的地；`target="_blank"` 開新分頁
- **Django 接手後**：href 常由模板語法產生

```django
<a href="{% url 'board:list' %}">回留言牆</a>
```

網址不再寫死，由 Django 的命名路由算出來（Deck 01 第 3 章回收）。

<!--
授課提示：先讓學生手寫死 href，再投影 {% url %} 版本，
問「哪種寫法改路由時不用改一百個檔案？」
-->

---

## 2-3 img：src 與 alt 缺一不可

```html
<img src="/media/products/keyboard.jpg"
     alt="機械鍵盤照片"
     class="card-img-top">
```

| 屬性 | 作用 |
|---|---|
| `src` | 圖片網址（第二階段 LearnMart 由 media 提供；留言板沒有圖片） |
| `alt` | 圖讀不出時的替代文字＋螢幕閱讀器的描述 |

**你應該看到：**把 src 改成不存在的路徑 → 瀏覽器顯示破圖＋alt 文字。

<!--
授課提示：故意改壞 src 讓 alt 現身，
順便預告 Deck 01 商品卡的 onerror fallback 練習。
-->

---

## 2-4 清單：ul / ol / li

```html
<ul>
  <li>3C</li>
  <li>書籍</li>
</ul>

<ol>
  <li>加入購物車</li>
  <li>結帳</li>
</ol>
```

- `ul` 無序（圓點）、`ol` 有序（編號）
- 導覽選單本質上也是一份 ul/li 清單，再用 CSS 排成橫排

<!--
授課提示：打開 base.html 的分類下拉選單或任何清單處對照。
-->

---

## 2-5 div 與 span：兩種通用容器

```html
<div class="card">          <!-- 區塊容器：自己佔一整行 -->
  <span class="badge">熱銷</span>   <!-- 行內容器：跟著文字走 -->
  <p>商品說明…</p>
</div>
```

| 標籤 | 顯示行為 | 典型用途 |
|---|---|---|
| `div` | block（換行） | 版面切塊 |
| `span` | inline（不換行） | 幫一小段文字加樣式 |

它們沒有語意，純粹為了「掛 class 好上妝」。

<!--
授課提示：block/inline 的差別第 4 章 display 屬性會正式登場，
此處先給視覺印象即可。
-->

---

## 2-6 語意標籤：讓結構會說話

```html
<body>
  <header>…logo、導覽…</header>
  <nav>…主選單…</nav>
  <main>…這頁的主要內容…</main>
    <article>…一張商品卡／一篇留言…</article>
  <footer>…版權、聯絡…</footer>
</body>
```

好處：

- 螢幕閱讀器能跳著唸（無障礙）
- 程式碼可讀性遠勝滿地 div

**課程專案對照：**`templates/base.html` 的骨架就是 header/nav/main/footer。

<!--
授課提示：請學生打開 base.html 數語意標籤數量，
體感「真實專案不是全用 div」。
-->

---

## 2-7 button vs a：語意決定用途

```html
<a href="/products/1/">查看詳情</a>     <!-- 移動到某處 → a -->

<form method="post">
  <button type="submit">加入購物車</button>  <!-- 觸發動作 → button -->
</form>
```

| 情境 | 用 |
|---|---|
| 要「去」某個網址 | `a` |
| 要「做」某件事（送表單） | `button type="submit"` |

> 之後的鐵律也在此埋點：**改變資料的操作一律走 form + POST + button**（Deck 02）。

<!--
授課提示：「a 是去、button 是做」口訣送出。
購物車的加減數量按鈕都是 button+form，可以預告。
-->

---

## 第 2 章｜動手試與觀念檢核

**動手試：**組出一張迷你商品卡：

```html
<article class="card">
  <h2>機械鍵盤</h2>
  <p>NT$350</p>
  <a href="#">詳情</a>
</article>
```

**觀念檢核：**

1. 一頁能有幾個 h1？　**答：建議一個**
2. img 缺 alt 的風險？　**答：無障礙差、圖掛了使用者不知道那是什麼**
3. 「加入購物車」該用 a 還是 button？　**答：button（觸發動作）**

<!--
授課提示：第 3 題是 Deck 02 安全章節的遠因，
現在答對的人之後學 POST-only 會特別快。
-->
