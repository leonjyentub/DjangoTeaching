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

# 第 3 章
## Template、static 與響應式頁面

**本章成果：**把 Python 資料安全地放入共用版型，並在手機與桌面形成可讀商品頁。

<!--
授課提示：提醒 HTML/CSS 先備需求：沒基礎的學生先讀 00b 教材第 1、4 章，否則節奏會吃力。
-->

---

## 3-1 從字串 response 到 template

直接拼 HTML 很快失去可讀性：

```python
return HttpResponse("<h1>商品</h1><p>...</p>")
```

Template 把責任分開：

- View：準備資料與流程
- Template：描述 HTML 顯示
- context：View 傳給 Template 的命名資料

這也讓 template autoescaping、繼承與重用機制能參與。

---

## 3-2 `render()` 的三個核心參數

**教學用最小範例｜`marketplace/views.py`**

```python
from django.shortcuts import render


def catalog(request):
    products = ["鍵盤", "筆記本"]
    return render(
        request,
        "marketplace/catalog.html",
        {"products": products},
    )
```

- `request`：目前 request
- template name：由設定好的搜尋路徑尋找
- context dict：key 會成為 template 變數名
- `render()` 最後仍回傳 `HttpResponse`

---

## 3-2A MVT 心智模型：不是三個字母各自運作

```text
Request
  │
  ▼
View ──用 ORM 查詢／更新──> Model ──> Database
  │
  ├──建立 context
  ▼
Template ──render──> HTML Response
```

- **Model**：資料結構、關聯與查詢入口
- **View**：接 request、協調 Model、選 template、回 response
- **Template**：使用 context 描述輸出 HTML

Function View 可只回 `HttpResponse`；使用 template 的完整頁面也不一定每次查 Model。MVT 是責任分工，不是強迫每個 request 經過所有層。

---

## 3-2B 圖解：MVT 如何分工

![w:1000](../assets/mvt_model.svg)

<!--
授課提示：強調三個方塊各自住在哪個資料夾（models.py／views.py／templates/）。底部 MVC 對照常被考：Django 的 View ≈ MVC Controller、Template ≈ MVC View。若班上有人學過 MVC，務必在此對焦名詞。
-->

---

## 3-3 Template 到底放在哪裡？

**目前 LearnMart 節錄｜部分 template tree**

```text
templates/
├── base.html
├── registration/
└── marketplace/
    ├── home.html
    ├── product_detail.html
    ├── pagination.html
    └── ...
```

對應設定：

```python
"DIRS": [BASE_DIR / "templates"],
"APP_DIRS": True,
```

Template name 使用 `/` 分層，例如 `marketplace/home.html`，不是作業系統絕對路徑。

---

## 3-4 三種 Django template delimiter

```django
{{ product.name }}          {# 輸出 value #}
{% if product.stock > 0 %}  {# 執行 template tag #}
  有庫存
{% endif %}
{# 只給 template 作者看的註解 #}
```

- `{{ ... }}`：求值並輸出
- `{% ... %}`：流程、載入、繼承、URL 等 tag
- `{# ... #}`：不輸出到回應

Django template language 刻意受限；複雜商業邏輯應留在 Python。

<!--
授課提示：板書三種 delimiter 各一例。{{ }} 誤打成 {% %} 是最高頻 template 錯誤，出現時請學生自己讀錯誤訊息定位。
-->

---

## 3-5 變數與 dot lookup

```django
{{ product.name }}
{{ product.seller.username }}
```

Django 依序嘗試類似：

- dictionary key
- attribute
- list index
- 無參數 callable

對 model relation 而言：

```text
product.seller          → User instance
product.seller.username → User 的 username
```

缺少的 template 變數常呈現空字串，不一定像 Python 一樣立刻拋錯，因此名稱要特別核對。

---

## 3-6 Template autoescaping 的正確邊界

```django
<p>{{ post.content }}</p>
```

預設情況下，`<`、`>` 等特殊字元會被 escape，瀏覽器把它們當文字而不是 HTML tag。

這個保護只適用於 template engine 的輸出流程：

- `{{ value }}`：通常 autoescape
- `HttpResponse(f"{value}")`：沒有 template，沒有 autoescape
- `{{ value|safe }}`：主動關閉保護，使用者內容不應隨意使用

<!--
授課提示：demo：在留言板輸入 <script>alert(1)</script>，觀察被 escape 的輸出。伏筆在 Deck 02 第 7 章 XSS 收割。
-->

---

## 3-7 Filter：改變顯示，不改資料庫

```django
{{ review.created_at|date:"Y/m/d" }}
{{ product.description|truncatechars:80 }}
{{ query|default:"全部商品" }}
```

語法：`value|filter_name:argument`

- filter 處理 presentation
- 原本 model value 不會被存回資料庫
- 可串接多個 filter
- 有參數時常以冒號接字串

LearnMart 也使用 `linebreaksbr`、`urlencode` 等 filter。

---

## 3-8 `if`：依狀態決定顯示

```django
{% if product.stock > 0 %}
  <span>有現貨</span>
{% else %}
  <span>已售完</span>
{% endif %}
```

注意：

- `{% if %}` 必須以 `{% endif %}` 結束
- 比較運算子兩側保留空格較易讀
- 隱藏按鈕只是 UI；真正的庫存規則仍須由 server 驗證

---

## 3-9 `for` 與 `{% empty %}`

```django
{% for product in products %}
  <h2>{{ product.name }}</h2>
{% empty %}
  <p>目前沒有商品。</p>
{% endfor %}
```

- `products` 來自 context
- `product` 只在 loop 內代表目前項目
- `{% empty %}` 處理空 QuerySet/list，比在外層再寫一個 `if` 更直接
- `forloop.counter` 可取得從 1 開始的序號

---

## 3-10 URL tag 接回上一章的命名路由

```django
<a href="{% url 'marketplace:product-detail' product.pk %}">
  {{ product.name }}
</a>
```

`marketplace:product-detail` 需要一個 `pk`，因此 tag 後面提供 `product.pk`。

優點：

- 不硬寫 `/products/3/`
- route 文字改動時，只要 name 與參數契約不變，template 不必逐頁搜尋替換

---

## 3-11 Template inheritance：先看 parent

**目前 LearnMart 節錄｜`templates/base.html`**

```django
<title>{% block title %}學購 LearnMart{% endblock %}</title>

<main class="container py-4">
  {% block content %}{% endblock %}
</main>
```

Parent template 定義可被 child 取代的 block：

- `title` 有預設文字
- `content` 提供每頁主要內容插槽
- 導覽列、CSS、messages、footer 只需放在 parent 一次

<!--
授課提示：先看 base.html 再看 child。block 名稱拼錯不會報錯、只會默默空白——現場示範一次讓全班印象深刻。
-->

---

## 3-12 Template inheritance：再看 child

**目前 LearnMart 節錄／重排｜`templates/marketplace/home.html`**

```django
{% extends "base.html" %}

{% block content %}
  <h1 class="display-5 fw-bold">
    學習 Django，也學會打造購物網站
  </h1>
  {# 商品網格與 pagination 省略 #}
{% endblock %}
```

- `{% extends %}` 應放在 child 的最前面
- block name 必須與 parent 相同
- 最終 response 是 parent 與 child 合成的完整 HTML
- Child 不必重新寫 `<html>`、navbar、footer

---

## 3-13 `include` 與 `extends` 的工作不同

```django
{% include "marketplace/pagination.html" %}
```

- `extends`：整張頁面的骨架／繼承關係
- `include`：在某個位置插入局部 template
- include 預設可使用目前 context

LearnMart 把分頁導覽抽成 `pagination.html`；home template 保留商品頁主結構。

如果 partial 依賴 `page_obj`，呼叫它的 View 必須提供該 context。

---

## 3-14 static：開發者提供的固定資產

**目前 LearnMart 節錄｜`templates/base.html`**

```django
{% load static %}
<link rel="stylesheet" href="{% static 'css/site.css' %}">
```

對應來源：

```text
static/css/site.css
```

`{% static %}` 產生可供瀏覽器請求的 URL；它不是把 CSS 內容讀入 template。

設定中的 `STATICFILES_DIRS = [BASE_DIR / "static"]` 告訴 Django 開發工具去哪裡找來源檔。

---

## 3-15 static 與 media 不要混淆

| 類型 | 誰提供 | LearnMart 範例 |
|---|---|---|
| static | 開發者隨程式碼提供 | `site.css` |
| media | 使用者／管理者上傳 | 商品圖片 |

目前設定：

```python
STATIC_URL = "static/"
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
```

本章先認識差異；`ImageField` 與 media 路由會在 Model 章一起說明，上傳表單則放在 Deck 2。

---

## 3-16 Bootstrap 與 Django 各做什麼？

**目前 LearnMart 節錄｜`templates/base.html`**

```html
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css"
      rel="stylesheet">
```

- Django：server-side request、資料、template rendering
- Bootstrap：瀏覽器端 CSS/JS 元件與 utility class
- CDN：瀏覽器從外部網站下載檔案，因此需要網路
- LearnMart 沒有 Django frontend build；本地只保留 `site.css`

Bootstrap class 不會改變 Python 或資料庫邏輯。

---

## 3-17 viewport 為何必須放在 `<head>`？

```html
<meta name="viewport"
      content="width=device-width, initial-scale=1">
```

- `width=device-width`：CSS viewport 使用裝置寬度
- `initial-scale=1`：初始縮放比例為 1

沒有這行時，手機可能以較寬的虛擬畫布縮小整頁，導致 responsive breakpoint 與閱讀效果不如預期。

---

## 3-18 Bootstrap grid 的 12 欄心智模型

```html
<div class="container">
  <div class="row">
    <div class="col-md-6">左</div>
    <div class="col-md-6">右</div>
  </div>
</div>
```

- `container`：限制與置中內容寬度
- `row`：建立欄位列與 gutter
- `col-md-6`：從 `md` 寬度起占 6/12，也就是一半
- 小於 `md` 時沒有指定欄寬，兩個 block 會自然堆疊

---

## 3-19 Mobile-first：breakpoint 代表「以上」

| 前綴 | 起始寬度 | 說明 |
|---|---:|---|
| 無前綴 | 0 | 所有寬度先適用 |
| `sm` | 576px | 576px 以上 |
| `md` | 768px | 768px 以上 |
| `lg` | 992px | 992px 以上 |
| `xl` | 1200px | 1200px 以上 |
| `xxl` | 1400px | 1400px 以上 |

`row-cols-2 row-cols-md-3` 表示：預設 2 欄；到 `md` 及以上改為 3 欄。

<!--
授課提示：用裝置模擬在 767px / 768px 各停一次親眼看欄數切換；00b 第 5 章已鋪墊，此處正式回收。
-->

---

## 3-20 商品網格：完整父子結構

**目前 LearnMart 節錄｜`templates/marketplace/home.html`**

```django
<div class="row row-cols-2 row-cols-md-3 row-cols-xl-4 g-3">
  {% for product in products %}
    <div class="col">
      <article class="card h-100">...</article>
    </div>
  {% empty %}
    <div class="col-12">目前找不到商品。</div>
  {% endfor %}
</div>
```

`row-cols-*` 作用在直接 `.col` 子元素；`g-3` 是 gutter spacing scale，不是 3px。

---

## 3-21 Utility class 要讀成組合語言

```html
<section class="rounded-4 p-4 p-md-5 mb-4 text-white">
```

拆解：

- `rounded-4`：圓角尺度
- `p-4`：所有寬度 padding
- `p-md-5`：`md` 以上使用更大 padding
- `mb-4`：margin-bottom
- `text-white`：文字顏色

數字是 Bootstrap 設計尺度，不等於相同數值的 px。

---

## 3-22 語意與無障礙不是最後才補

商品頁範例應同時做到：

- `<nav>`、`<main>`、`<article>` 表示結構
- `<img alt="商品名稱">` 提供替代文字
- 每個 form control 都要有可存取名稱；優先使用可見 `<label for="...">`
- 緊湊控制項在適當情況可使用 `aria-label`，例如目前 navbar 搜尋欄
- 教學範例明確寫 button 的 `type`；目前部分 templates 仍依賴預設 submit，不能把省略當推薦寫法
- 不能只靠顏色傳達「售完」或錯誤

這些是 HTML 正確性的一部分，不是裝飾。

---

## 3-23 常見 template 問題如何定位？

| 現象 | 優先檢查 |
|---|---|
| `TemplateDoesNotExist` | template name、`DIRS`、App template 路徑 |
| `NoReverseMatch` | URL namespace/name、必要參數 |
| 變數顯示空白 | context key、attribute 名稱 |
| `TemplateSyntaxError` | tag 拼字、未關閉 block/if/for、未 load static |
| CSS 沒套用 | static URL、瀏覽器 Network、class 拼字 |

先讀 exception type 與指出的 template 行號，不要一開始就隨機改多個檔案。

---

## 第 3 章｜觀念檢核與實作

1. `render()` 的 template name 與 context 各扮演什麼角色？
2. `{{ }}`、`{% %}`、`{# #}` 有何不同？
3. `extends` 與 `include` 解決的是哪兩種重複？
4. 為什麼 `row-cols-md-3` 不是「只有 md 時三欄」？
5. 為什麼在 UI 隱藏按鈕不能取代 server-side security？

**實作任務：**建立繼承 `base.html` 的頁面，顯示 context、命名 URL，追蹤 parent 的 static CSS 載入鏈，並驗證 HTML-looking 文字被 escape。

**配套實作手冊：**[第 3 章答案與步驟](../workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md#chapter-3)

<!--
授課提示：第 5 題連向安全意識，可預告 Deck 02 的 XSS 與 trust boundary。
-->
