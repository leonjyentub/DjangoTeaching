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

# 第 6 章
## 組合成可搜尋的資料驅動商品目錄

**本章成果：**把 URL、View、ORM、context、Template、Bootstrap 串成一個可解釋、可觀察的完整 feature。

<!--
授課提示：整合章，節奏放慢。核心任務是 workbook 的 low-stock filter，保留至少半堂操作時間。
-->

---

## 6-1 Vertical slice 前半：request 變成 QuerySet

```text
GET /?q=鍵盤&category=tech
        │
        ▼
config/urls.py
        │ include("marketplace.urls")
        ▼
marketplace/urls.py
        │ home → ProductListView
        ▼
Product QuerySet
active + search + category + select_related
```

這一半的輸入是 HTTP request；輸出是尚可繼續組合、之後才評估的 QuerySet。

---

## 6-1A Vertical slice 後半：context 變成 HTML response

```text
QuerySet + categories + query state
        │
        ▼
View 建立 context 並 pagination
        │
        ▼
templates/marketplace/home.html
        │ extends / include
        ▼
200 HTML
商品卡 + 分類 + 搜尋字串 + 分頁
```

每層只負責自己的部分，但 context key、template variable 與 URL state 契約必須對得上。

---

## 6-2 先用 Function View 看清全部責任

**教學用最小範例**

```python
from django.shortcuts import render
from .models import Product


def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "marketplace/home.html", {
        "products": products,
    })
```

這不是目前 LearnMart 最終 class-based view；它先讓 beginner 看見 query、context 與 render 在同一函式中的資料流。

---

## 6-3 List 與 Detail 是兩種不同查詢形狀

### List

```python
Product.objects.filter(is_active=True)
```

回 QuerySet，可能 0 到多筆。

### Detail

```python
get_object_or_404(Product, pk=pk, is_active=True)
```

回一個 instance；找不到時回 404。

URL 也對應：

```text
/                    商品列表
/products/<int:pk>/  單一商品
```

---

## 6-4 `get_object_or_404` 做了什麼？

```python
product = get_object_or_404(
    Product,
    pk=pk,
    is_active=True,
)
```

可理解為：

1. 用條件查詢一筆物件
2. 找到：回傳 Product instance
3. 找不到：拋出 Http404，由 Django 形成 404 response

這比讓 `DoesNotExist` 變成 500 更符合「網址或可見物件不存在」的語意。

權限章還會使用 scoped queryset 讓無權物件同樣回 404。

---

## 6-5 GET 搜尋表單先建立 URL 狀態

```html
<form action="{% url 'marketplace:home' %}"
      method="get"
      role="search">
  <label for="q">搜尋商品</label>
  <input id="q" name="q" value="{{ query }}">
  <button type="submit">搜尋</button>
</form>
```

送出後瀏覽器形成：

```text
/?q=鍵盤
```

`name="q"` 決定 query string key；GET 適合可分享、可 bookmark、重複執行的查詢。

<!--
授課提示：送出搜尋後立刻指網址列 ?q=…，建立「GET = 可分享、可收藏的狀態」直覺。
-->

---

## 6-6 Query string 由 `request.GET` 讀取

```python
query = request.GET.get("q", "").strip()
```

- `request.GET` 是 QueryDict-like object
- `.get("q", "")`：沒有 q 時使用空字串
- `.strip()`：移除前後空白
- GET value 仍是外部輸入，不能直接當可信 SQL 或任意欄位名稱

接著才決定是否加 filter：

```python
if query:
    queryset = queryset.filter(...)
```

---

## 6-7 搜尋名稱或說明

```python
from django.db.models import Q

if query:
    queryset = queryset.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )
```

- 空 query 不加搜尋條件
- `icontains` 由 ORM 參數化處理 value
- `Q | Q` 表示名稱或說明任一符合
- QuerySet 繼續保持可組合

這一頁只解釋 value filter；若讓使用者選任意排序欄位，仍需要 allowlist。

---

## 6-8 把搜尋字串送回 template

```python
return render(request, "marketplace/home.html", {
    "products": queryset,
    "query": query,
})
```

```django
<input name="q" value="{{ query }}">
{% if query %}
  <p>「{{ query }}」的搜尋結果</p>
{% endif %}
```

這叫 state retention：request 進來的查詢狀態，經 View 正規化後再回到 UI。

Template autoescaping 會處理 query 的 HTML 特殊字元；但仍要由 ORM 安全處理 database 查詢。

---

## 6-9 分類篩選同樣是 GET state

```python
category = request.GET.get("category", "").strip()
if category:
    queryset = queryset.filter(category__slug=category)
```

Context 需要：

```python
{
    "categories": Category.objects.all(),
    "selected_category": category,
}
```

Template 才能同時：

- 列出所有分類按鈕
- 標示目前分類
- 建立保留其他搜尋條件的連結

---

## 6-10 多個 query parameters：先讀連結語法

**目前 LearnMart 節錄／重排｜category link 的概念**

```django
<a href="?category={{ category.slug }}{% if query %}&q={{ query|urlencode }}{% endif %}">
  {{ category.name }}
</a>
```

- 第一個參數前使用 `?`
- 後續參數用 `&`
- `urlencode` 把空白與特殊字元編碼成合法 URL component

若切分類時忘記 q，搜尋條件會消失；若分頁忘記 category，分類條件也會消失。

---

## 6-10A 再辨識目前 UI 的 state-retention 邊界

**目前 LearnMart 實作：**

- category links 保留 q
- pagination links 保留 q/category
- navbar search form 目前只提交 q，所以重新搜尋會重設 category

這不是安全規則，而是 UI navigation contract。

**配套實作手冊：**low-stock lab 會使用 `{% querystring %}`，並把「search 同時保留 category」列為 intentional improvement。

---

## 6-11 Pagination 是 QuerySet 與 UI 的共同狀態

目前最終 `ProductListView` 設定：

```python
paginate_by = 12
```

Template 會得到：

- `page_obj`：目前頁
- `paginator`：總頁數、總筆數
- `is_paginated`

Pagination link 不只要改 `page`，還要保留 q/category：

```text
?page=2&q=鍵盤&category=tech
```

否則使用者翻頁時會跳回未篩選結果。反過來，當搜尋／分類條件改變時通常應**移除舊 page、回到第 1 頁**，避免新結果沒有原本頁碼。

<!--
授課提示：提問：q 與 page 同時存在時分頁 link 要帶哪些參數？帶讀 pagination.html 找答案。
-->

---

## 6-12 `include` 適合抽出分頁 UI

**目前 LearnMart 節錄｜`templates/marketplace/home.html`**

```django
{% include "marketplace/pagination.html" %}
```

目前 partial 直接使用 `page_obj`、`query`、`selected_category`；但它也被留言板共用，因此這些 catalog-only names 會讓 reusable boundary 變窄。

**補充／進階｜Django 5.2 generic query preservation**

```django
<a href="{% querystring page=page_obj.next_page_number %}">
  下一頁
</a>
```

`querystring` 會從目前 request query parameters 產生新 URL，只替換 page；可自然保留 q/category/low_stock，也避免共享 partial 硬綁 catalog context。

---

## 6-13 商品卡會讀 relation，所以先載入

**目前 LearnMart 節錄／重排｜`marketplace/views.py` 的 `ProductListView.get_queryset()`**

```python
queryset = Product.objects.filter(
    is_active=True,
).select_related("category", "seller")
```

**目前 LearnMart 節錄｜`templates/marketplace/home.html`**

```django
{{ product.category.name }}
{{ product.seller.username }}
```

Query 與 template 應一起讀：看見 template 取 relation，就回頭確認 QuerySet 是否造成 N+1。

---

## 6-14 圖片、fallback 與 alt 要在同一段理解

```django
{% if product.image %}
  <img src="{{ product.image.url }}"
       alt="{{ product.name }}">
{% else %}
  <div class="placeholder-product">商品圖片</div>
{% endif %}
```

- ImageField 為空時，不可直接取 `.url`
- 有圖時以商品名稱作為替代文字
- 無圖時提供可見 fallback
- 圖片 storage/media routing 必須能提供 URL

安全的 upload validation 會在 Deck 2 補上。

---

## 6-15 空結果不是錯誤，是正常 UI state

```django
{% for product in products %}
  ...商品卡...
{% empty %}
  <div class="alert alert-light border">
    目前找不到符合條件的商品。
  </div>
{% endfor %}
```

- 搜尋 0 筆仍應回 200
- 使用者需要知道「查詢成功但沒有結果」
- 這和 404 不同：404 表示路由／單一物件找不到
- Empty state 應保留搜尋欄與分類控制，讓使用者調整條件

---

## 6-16 從 Function View 收斂到目前 LearnMart

**目前 LearnMart 節錄｜`ProductListView`**

```python
class ProductListView(ListView):
    model = Product
    template_name = "marketplace/home.html"
    context_object_name = "products"
    paginate_by = 12
```

- `get_queryset(self) -> QuerySet`：active、搜尋、分類、select_related
- `self.request`：目前 HttpRequest
- `get_context_data(self, **kwargs) -> dict`：加入 categories 與 query state
- `super().get_context_data(**kwargs)`：保留 parent 已建立的 pagination context
- 兩個 overrides 都必須 `return` 結果

完整 `.as_view()`、inheritance 與 override lifecycle 放在 Deck 2；本章先建立實作 low-stock filter 必需的 method contract。

---

## 6-16A 目前 source 的 query state 有一個可改善細節

**目前 LearnMart 節錄｜`get_context_data()`**

```python
context["query"] = self.request.GET.get("q", "")
context["selected_category"] = self.request.GET.get(
    "category", "",
)
```

Filter 端使用 `.strip()`，但 context 端再次讀 raw value。因此 `q="   "` 不會 filter，UI 卻可能把空白視為有搜尋字串。

**配套實作手冊的 intentional improvement：**把送回 UI 的 q/category 也 `.strip()`；這不是聲稱目前 source 已正規化。

---

## 6-17 完整 request flow：逐層說出輸入與輸出

1. Browser：`GET /?q=鍵盤`
2. URLconf：名稱 `marketplace:home` 指向 list view callable
3. View：從 `request.GET` 取得 q
4. ORM：組成 active + `Q(...)` QuerySet
5. View：加 categories/query context，執行 pagination
6. Template：loop products、反向 URL、讀 relation
7. Bootstrap/static：形成 responsive 商品卡
8. Django：回 200 HTML response

若你能指出每一步的檔案與資料型別，就不是只會複製程式碼。

---

## 6-17A 圖解：Catalog 的完整資料流

![w:1020](../assets/request_flow.svg)

<!--
授課提示：同一張圖第二次登場。此時左半部全部教完，請學生逐格說出「這一格在 LearnMart 是哪個 class/method」，例如第 4 格是 ProductListView.get_queryset。能走完全圖即可進入章末驗收。
-->

---

## 6-18 手動驗證 catalog 的可觀察行為

- `/` 顯示 seeded 商品
- `/?q=鍵盤` 只顯示符合名稱／說明的商品
- category links 可保留 q；global search 目前會重設 category
- 搜尋／分類改變時回到第 1 頁；pagination 保留查詢條件
- 空結果顯示正常 empty state 且 status 仍為 200
- detail link 由命名 URL／`get_absolute_url()` 產生
- 手機、平板、桌面欄數按 breakpoint 改變

**你應該看到：**每一項都能指出 URL、頁面文字或 viewport 變化，而不是只說「看起來可以」。

<!--
授課提示：逐項現場驗證；一位學生操作瀏覽器、其他人對照清單記錄，模擬 QA 流程。
-->

---

## 6-18A 用 focused test 固定搜尋行為

**目前 LearnMart 實作｜單一 test label**

```bash
uv run python manage.py test \
  "marketplace.tests.MarketplaceFlowTests.test_search_finds_product"
```

預期：

```text
Ran 1 test
OK
```

反斜線只延續 command；完整 dotted label 維持在同一個 quoted shell argument。完整 test suite 仍使用 `uv run python manage.py test`。

---

## 第 6 章｜觀念檢核與實作

1. GET form 的 `name="q"` 如何一路變成 ORM filter？
2. 搜尋＋分類＋分頁時，為什麼要保留多個 query parameters？
3. 商品卡讀 category/seller 時，為何使用 `select_related`？
4. 空 QuerySet 為什麼通常回 200 而不是 404？
5. 為什麼 low-stock threshold 與可查欄位必須由 server 定義？

**實作任務：**增加「低庫存」GET filter；變更 q/category/low_stock 時重設 page，pagination 則保留三個 filter states，並提供空結果與 boundary test。

**配套實作手冊：**[第 6 章答案與步驟](../workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md#chapter-6)

<!--
授課提示：第 5 題直接對應 workbook 任務驗收標準；做完練習回來重答效果最好。
-->
