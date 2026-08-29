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

# 第 3 章
## 表單標籤：資料回傳伺服器的橋

**本章成果：**能組出 GET 搜尋表單與 POST 資料表單，說出每個屬性的角色。

<!--
授課提示：本章是 Deck 02 第 1 章的直接地基。
name 屬性（3-2）是最容易被忽略卻最關鍵的一顆螺絲，務必重敲。
-->

---

## 3-1 form：action 與 method

```html
<form action="/search/" method="get">
  …輸入欄位放這裡…
  <button type="submit">搜尋</button>
</form>
```

| 屬性 | 意義 |
|---|---|
| `action` | 資料送到哪個網址 |
| `method` | `get`（查詢）或 `post`（改變狀態） |

- 送出時，瀏覽器把所有「有 name 的欄位」收集成 key=value
- GET 會把參數接到網址上：`/search/?q=鍵盤`

<!--
授課提示：送一次搜尋讓學生看網址列變化，
問「q=鍵盤 的 q 是從哪裡來的？」→ 答案在下一頁。
-->

---

## 3-2 input：type 家族與關鍵的 name

```html
<input type="text" name="q" value="預設值" placeholder="搜尋商品">
```

- `type`：text / number / email / password / hidden…
- `name`：送給伺服器的 key——**沒有 name 的欄位不會被送出**
- `value`：目前的值；`placeholder` 只是灰色提示字

```html
<input type="hidden" name="product" value="3">
```

hidden 一樣會被送出——也一樣能被使用者竄改（安全伏筆）。

**你應該看到：**刪掉 `name="q"` 後再搜尋，網址列不再出現 q 參數。

<!--
授課提示：兩件事必做：(1) 刪 name 看 GET 參數消失；
(2) 用 F12 改 hidden value 體感「瀏覽器不可信」，Deck 02 的信任邊界圖在此埋點。
-->

---

## 3-3 label：點得到的名字

```html
<label for="q">關鍵字</label>
<input id="q" name="q">
```

- `for` 對應欄位的 `id`；綁定後點文字就能聚焦欄位
- 也是螢幕閱讀器唸出欄位名稱的依據（無障礙必備）

> id 是文件內唯一識別；name 是送出的參數名。兩者常相同但意義不同。

<!--
授課提示：示範點 label 文字讓 input 聚焦。
id vs name 的對比請學生抄進筆記。
-->

---

## 3-4 select 與 textarea

```html
<select name="rating">
  <option value="5">★★★★★</option>
  <option value="4">★★★★</option>
</select>

<textarea name="comment" rows="3" placeholder="分享心得"></textarea>
```

- select：下拉選單；value 才是送出的值，標籤文字只是顯示
- textarea：多行文字；用 rows 控制高度

**課程專案對照：**第一階段留言板的發表表單就是 textarea；第二階段商城的評分選單才是 select。

---

## 3-5 上傳檔案：enctype 特殊規格

```html
<form method="post" enctype="multipart/form-data">
  <input type="file" name="image">
</form>
```

- 一般表單只會送文字；要傳檔案必須宣告 `multipart/form-data`
- 忘了它 → 伺服器收不到檔案，而且不會報錯，只是沒資料

**LearnMart 對照（第二階段伏筆）：**商品新增／編輯表單都有這一行；Django 端還要 `request.FILES` 配合。第一階段的留言表單只送文字，不需要 enctype。

<!--
授課提示：「忘了 enctype 不報錯只是空手」是實務超級大坑，
請學生抄進筆記。
-->

---

## 第 3 章｜動手試與觀念檢核

**動手試：**GET 搜尋表單：

```html
<form action="" method="get">
  <label for="kw">搜尋</label>
  <input id="kw" name="q">
  <button type="submit">Go</button>
</form>
```

送出後觀察網址列。

**觀念檢核：**

1. 欄位沒有 name 會怎樣？　**答：不會被送出**
2. GET 和 POST 的用途差別？　**答：查詢 vs 改變狀態**
3. 上傳檔案少了 enctype 會怎樣？　**答：靜默失敗，收不到檔案**

<!--
授課提示：第 1 題務必實作驗證，這是 form 最常見的初學者翻車點。
-->
