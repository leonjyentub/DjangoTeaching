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

# 第 3 章
## Template、static 與響應式留言牆

**本章成果：**能看懂 base.html 的繼承結構、DTL 語法，並知道 CSS 與 Bootstrap 各自在做什麼。

<!--
授課提示：本章與先備教材 00b 高度互補。00b 教「標籤本身」，本章教「Django 如何把資料填進標籤」。
-->

---

## 3-1 Template：把資料填進洞裡

```html
<h1>{{ query }}</h1>
<p>{{ post.content|linebreaksbr }}</p>
```

Template engine 做兩件事：

1. 把 `{{ }}` 換成真實資料
2. 執行 `{% %}` 裡的流程指令（for、if、block…）

**心智模型：**template 是「HTML＋洞」。View 負責決定填什麼；template 負責決定長什麼樣。

---

## 3-2 render() 三件事

```python
from django.shortcuts import render

render(request, "board/message_list.html", {"posts": posts})
```

| 參數 | 意義 |
|---|---|
| `request` | 帶著使用者身份等資訊的原始 request |
| 模板路徑 | 相對於 templates 目錄 |
| dict（context） | 要填進 `{{ }}` 的資料 |

回傳值就是一個完整的 `HttpResponse`（Content-Type: text/html）。

---

## 3-3 DTL 變數與 filter

```django
{{ post.content }}                    ← 原樣輸出
{{ post.content|truncatechars:50 }}   ← 截斷到 50 字
{{ post.created_at|date:"Y/m/d H:i" }}
{{ post.content|linebreaksbr }}
{{ post.author.username|first|upper }}
```

filter 用 `|` 串接，像流水線。常用組合先記五個即可，其餘用到再查官方文件。

**常見錯誤：**`{{ post.content } }` 多了空格；`|date` 用在字串上不報錯但輸出不變。

---

## 3-4 {% for %}、{% if %} 與 {% empty %}

```django
{% for post in posts %}
  <article class="card mb-3">
    <p>{{ post.content }}</p>
  </article>
{% empty %}
  <div class="alert alert-light">目前還沒有留言。</div>
{% endfor %}
```

`{% empty %}` 是「列表為空」的專用分支——不用自己寫 `{% if posts|length == 0 %}`。

---

## 3-5 base.html：父版型與洞

```html
<main class="container py-4">
  {% for message in messages %}<div class="alert …">{{ message }}</div>{% endfor %}
  {% block content %}{% endblock %}
</main>
```

```html
{# 子模板 board/message_list.html #}
{% extends "base.html" %}
{% block content %}…留言卡片…{% endblock %}
```

- 共同的 navbar／footer／alert 寫一次就好
- `{% block title %}` 讓每頁自訂瀏覽器標籤上的標題

**你應該看到：**子模板只有區塊內容；導覽列自動出現在每一頁。

---

## 3-6 static：CSS／JS／圖片的正確位置

```html
{% load static %}
<link rel="stylesheet" href="{% static 'css/site.css' %}">
```

- static 檔放 `static/`，與 templates 分離
- `{% static %}` 產生實際網址（部署時可換 CDN）
- Bootstrap 本體走 CDN，不必下載

settings 相關設定：`STATIC_URL`、`STATICFILES_DIRS`。

---

## 3-7 site.css：在框架上蓋自己的視覺

```css
:root { --lb-blue: #3b5bdb; --lb-deep: #1e3a8a; --lb-bg: #f5f7fb; }
body { background: var(--lb-bg); }
.navbar { background: linear-gradient(90deg, var(--lb-deep), var(--lb-blue)); }
.avatar { width: 34px; height: 34px; border-radius: 9999px; }
```

- CSS variables 集中管理主題色（商城的 `--lm-red` 同理）
- 自訂 class（`.avatar`）補 Bootstrap 沒有的元件
- 改完重新整理即生效；沒生效先按 Ctrl+F5 清快取

---

## 3-8 Bootstrap navbar 拆解

```html
<nav class="navbar navbar-expand-lg navbar-dark sticky-top">
  <div class="container">
    <a class="navbar-brand" href="{% url 'board:list' %}">學言板</a>
    <button class="navbar-toggler" data-bs-toggle="collapse" …></button>
    <div class="collapse navbar-collapse" id="mainNav">…選單…</div>
  </div>
</nav>
```

- `navbar-expand-lg`：lg 以上展開、以下摺疊成漢堡按鈕
- `sticky-top`：捲動時釘在頂部
- 登入／登出按鈕由 `{% if user.is_authenticated %}` 切換（user 由 auth context processor 注入）

---

## 3-9 留言卡：card 元件實戰

```html
<article class="card border-0 shadow-sm mb-3 post-card">
  <div class="card-body">
    <div class="fw-semibold small">{{ post.author.username }}</div>
    <p class="post-content">{{ post.content|linebreaksbr }}</p>
  </div>
</article>
```

`border-0`＋`shadow-sm` 做出柔和浮起感；hover 上浮效果來自我們自己的 `.post-card:hover`。

**觀察點：**Bootstrap 管「元件長相」，site.css 管「互動細節」——分工明確。

---

## 3-10 RWD grid：欄數隨螢幕變化

```html
<div class="row row-cols-1 row-cols-md-3 g-4">
```

| class | 生效範圍 |
|---|---|
| `row-cols-1` | 所有寬度：每列 1 欄 |
| `row-cols-md-3` | md（≥768px）以上：每列 3 欄 |

留言牆目前是單欄列表；商城商品目錄會用同一招排出 3 欄商品格。

**你應該看到：**拖曳視窗寬度，斷點處欄數瞬間切換。

---

## 3-11 escaping：{{ }} 自動保護你

```python
Message.objects.create(content="<script>alert(1)</script>")
```

模板輸出 `{{ post.content }}` 時，`<` 會被跳脫成 `&lt;`——瀏覽器只顯示文字，不執行程式。

這就是 2-16 手工拼字串的危險在 template 中被解決的原因。

> **補充／進階：**確定要輸出 HTML 才用 `|safe`，而且必須能保證資料來源可信。留言內容絕不加 `|safe`。

---

## 3-12 圖解：MVT 三兄弟

![w:1000](../assets/mvt_model.svg)

<!--
授課提示：Model＝資料的形狀、View＝流程控制、Template＝呈現。請學生用自己的話向鄰座解釋一次，講不清楚的地方就是下一章要補的地方。
-->

---

## 第 3 章｜觀念檢核與實作

**觀念檢核：**

1. `render()` 的第三個參數是什麼？它對應模板裡的什麼？
2. `{% empty %}` 解決什麼問題？
3. `{% static 'css/site.css' %}` 與直接寫 `/static/css/site.css` 差在哪？
4. 為什麼留言內容不能用 `|safe`？

**實作任務：**在 base.html 的 footer 加上「第一階段：留言板」字樣以外的自訂文字，並在 site.css 新增一個 `.hero` 圓角調整，驗證兩處都能看到效果。

→ 步驟與解答在配套手冊第 3 章。
