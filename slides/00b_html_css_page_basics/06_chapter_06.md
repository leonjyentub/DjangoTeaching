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

# 第 6 章
## 實查 LearnBoard：把所學對號入座

**本章成果：**能逐段讀懂 `templates/base.html`，分清 HTML 與 Django template 語法的界線。

<!--
授課提示：本章請務必投影真實檔案逐段走讀，
學生第一次看到 Django template 與 HTML 混在一起會緊張，這是正常反應。
-->

---

## 6-1 base.html 上半部：head 全家福

```html
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{% block title %}學言板 LearnBoard{% endblock %}</title>
  <link href="https://cdn…/bootstrap.min.css" rel="stylesheet">
  <link href="{% static 'css/site.css' %}" rel="stylesheet">
</head>
```

| 你看到的 | 屬於 |
|---|---|
| `<meta>`、`<link>` | **HTML**（第 1、4 章） |
| `{% block %}`、`{% static %}` | **Django template 語法** |

> 判別口訣：`{% %}` 與 `{{ }}` 是 Django 的，其餘是 HTML。CSS 的載入順序＝覆蓋順序。

<!--
授課提示：帶學生用「口訣」把這段切成兩色高亮，
HTML 與 Django 各一色，混淆立刻現形。
-->

---

## 6-2 base.html 下半部：骨架與洞

```html
<body>
  <nav class="navbar navbar-expand-lg navbar-dark sticky-top">
    …品牌連結、登入／註冊按鈕…
  </nav>

  <main class="container py-4">
    {% for message in messages %}…提示訊息…{% endfor %}
    {% block content %}{% endblock %}
  </main>

  <footer>…</footer>
</body>
```

- navbar 由 Bootstrap classes 排版（`d-flex` 心智的進化版）
- `{% block content %}` 是一個「洞」：每頁把自己的內容填進來
- `py-4` = padding-top/bottom utility（box model 的 class 化）

**你應該看到：**子模板只寫 `{% extends "base.html" %}` ＋填洞，導覽列自動出現在每一頁。

<!--
授課提示：block 機制屬於 Deck 01 第 3 章；
此處只需建立「父版型＋洞」的心智，不必展開語法。
-->

---

## 6-3 留言卡解讀練習

```html
<article class="card border-0 shadow-sm mb-3">
  <div class="card-body">
    <div class="fw-semibold small">{{ post.author.username }}</div>
    <p class="post-content">{{ post.content|linebreaksbr }}</p>
  </div>
</article>
```

逐項自問：

1. 哪些是 HTML 標籤／屬性？（article/div/class）
2. 哪些是 Django 變數與 filter？（`{{ post.content|linebreaksbr }}`）
3. `card`、`shadow-sm` 在做什麼？（Bootstrap 卡片元件＋柔和陰影）

**觀念檢核：**

1. `{{ }}` 和 `{% %}` 差在哪？　**答：輸出變數 vs 流程指令**
2. `h-100` 是 HTML 標題嗎？　**答：不是，是 Bootstrap class（height:100%）**

<!--
授課提示：h2 class="h5" 是經典困惑點——標籤是大綱語意、
class 是視覺大小，兩者獨立。此題值得當場點名。
-->

---

## 00b 完成檢查清單

- [ ] 能畫出 HTML 文件的樹狀結構並說出 head/body 分工
- [ ] 認得留言卡會用到的全部標籤（a/p/div/span/article…）
- [ ] 能組出 GET 搜尋表單，並說明 name 屬性的關鍵角色
- [ ] 能讀懂 `.card p { }` 選到了誰，以及優先權勝負
- [ ] 能用 F12 解釋一段留白來自 padding 還是 margin
- [ ] 能說出 `row-cols-md-3` 的生效範圍
- [ ] 打開 base.html 能區分 HTML 與 `{% %}`／`{{ }}`

全部打勾 → 你已準備好進入 [Deck 01：兩個 Django 專案的共通基礎](../01_django_foundations_and_two_projects/00_overview.md)。

**本冊需要額外圖片嗎？**僅 box model 一張（已內嵌）；其餘皆可用 F12 即時演示取代。

<!--
授課提示：checklist 可當闖關單。全冊授課時間建議 2~3 小時。
第 6 章若時間不足，至少完成 6-3 商品卡練習再放學。
-->
