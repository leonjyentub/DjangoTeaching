---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 02｜表單、身份驗證與工作流程"
footer: "初學者教材｜LearnBoard × LearnMart"
---

<!-- _class: cover -->

# 第 3 章
## Class-based View、Mixin 與物件權限

<div class="box">理解 CBV 的生命週期，並在顯示或修改物件前先套用正確授權範圍</div>

<!--
授課提示：Python 先備不足者先回到 00a 第 9～11 章（類別/繼承/decorator）再進本章。
-->

---

## 先補 Django class 需要的 Python 語法

```python
class ProductListView(ListView):
    model = Product
    paginate_by = 12
```

- `ProductListView` 繼承 `ListView`
- `model`、`paginate_by` 是 class attributes，用來設定行為
- 每個 request 會建立 view instance
- `self` 指向本次 request 使用的 instance

---

## Override：改寫繼承來的方法

```python
def get_queryset(self):
    return Product.objects.filter(is_active=True)
```

`ListView` 原本已知道如何取得 QuerySet；override 讓你替換資料範圍。

方法名稱與 return type 必須符合 generic view contract；回傳 `None` 會讓後續流程失敗。

---

## `super()`：保留父類別既有工作

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["categories"] = Category.objects.all()
    return context
```

`super()` 不是「跳過目前 class」，而是依繼承順序呼叫下一個實作。先取得 Django 已準備的 pagination/object list context，再增加自己的 key。

<!--
授課提示：逐行念 forms.py 的 BootstrapFormMixin：先 super().__init__() 再 apply_bootstrap()，順序有意義。
-->

---

## `*args` 與 `**kwargs` 在 Django 常出現

```python
def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
```

- `*args` 收集額外 positional arguments
- `**kwargs` 收集額外 keyword arguments
- 轉交給父類別，可保留 framework 的彈性

初學時不必背所有參數，但不要把它們刪掉而破壞父類別初始化。

---

## Decorator 與 Mixin 的角色

Function View（checked-in `add_to_cart` 順序）：

```python
@require_POST
@login_required
def add_to_cart(request, pk): ...
```

Class View：

```python
class OrderListView(LoginRequiredMixin, ListView): ...
```

Decorator 包裝 function；Mixin 透過多重繼承把行為組合進 class。

---

## 為什麼 URLconf 不能直接放 CBV class？

URLconf 需要「接 request 並回 response 的 callable」。

```python
path("", ProductListView.as_view(), name="home")
```

`.as_view()` 會回傳 callable；每次 request 時：

1. 建立 view instance
2. 設定 `request`、`args`、`kwargs`
3. 依 HTTP method dispatch 到 `get()` 或 `post()`

---

## CBV request 流程簡圖

```text
URLconf: ProductListView.as_view()
  → setup(request, ...)
  → dispatch()
  → get()
  → get_queryset()
  → paginate_queryset()
  → get_context_data()
  → render_to_response()
```

通常只 override 需要改的 hook，不要重寫整條流程。

---

## 目前 LearnMart ProductListView

<span class="label current">目前 LearnMart｜逐字摘錄｜marketplace/views.py::ProductListView</span>

```python
class ProductListView(ListView):
    model = Product
    template_name = "marketplace/home.html"
    context_object_name = "products"
    paginate_by = 12
```

明確設定 `template_name`，因為專案沒有使用預設的 `marketplace/product_list.html`。

---

## `get_queryset()` 決定可見資料

```python
def get_queryset(self):
    queryset = Product.objects.filter(is_active=True).select_related(
        "category", "seller"
    )
    ...
    return queryset
```

這裡同時定義：

- 只有上架商品
- 預先載入 category/seller
- 後續依 GET 搜尋與分類縮小結果

QuerySet 是資料可見性的第一道門。

---

## `get_context_data()` 增加模板需要的資料

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["categories"] = Category.objects.all()
    context["query"] = self.request.GET.get("q", "")
    context["selected_category"] = self.request.GET.get("category", "")
    return context
```

`self.request` 是目前 request；`super()` 已加入 `products`、pagination 等 context。

---

## DetailView：單筆查詢仍可縮小 queryset

```python
class ProductDetailView(DetailView):
    model = Product
    template_name = "marketplace/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True)
```

URL 的 `pk` 不在這個 queryset 中時，自動得到 404。

---

## CreateView：成功表單的 hook

```python
class ProductCreateView(SellerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "marketplace/form.html"

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
```

先補 server-owned seller，再讓父類別儲存、取得 success URL 並 redirect。

---

## `get_absolute_url()` 與成功 redirect

<span class="label current">目前 LearnMart｜節錄／重排｜marketplace/models.py::Product</span>

```python
def get_absolute_url(self):
    return reverse(
        "marketplace:product-detail",
        kwargs={"pk": self.pk},
    )
```

CreateView／UpdateView 未設定 `success_url` 時，可在 model instance 儲存後使用標準網址。

---

## 三層授權模型

對保護操作依序問：

1. **登入**：是否有 authenticated user？
2. **角色**：是否是 seller／buyer？
3. **物件關係**：這個 product/order/cart item 是否屬於他？

只在 navbar 隱藏連結不是權限檢查；request 仍可直接送到 URL。

---

## LoginRequiredMixin 要放在 generic view 前

```python
class OrderListView(LoginRequiredMixin, ListView):
    ...
```

多重繼承依 Method Resolution Order 尋找方法。把 access mixin 放前面，讓它能在 `dispatch()` 階段先檢查登入，再進入 ListView 行為。

<!--
授課提示：只教慣例「mixin 在前、generic view 在最右」，原理到 CBV 流程圖再驗證。
-->

---

## SellerRequiredMixin：角色層

<span class="label current">目前 LearnMart｜逐字摘錄｜marketplace/views.py::SellerRequiredMixin</span>

```python
class SellerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_seller
```

結果：

- 匿名者：導向 login
- 已登入 buyer：測試失敗，通常 403
- seller：繼續處理 request

---

## 角色正確仍不代表擁有物件

危險做法：

```python
Product.objects.get(pk=self.kwargs["pk"])
```

安全範圍：

```python
def get_queryset(self):
    return Product.objects.filter(seller=self.request.user)
```

先縮小 queryset，再由 Generic View 用 URL `pk` 找物件。

<!--
授課提示：兩道門的心智：SellerRequiredMixin 過了角色門，get_queryset 的 filter(seller=...) 才是所有權門。
-->

---

## UpdateView 應一開始就是 ownership-safe

<span class="label current">目前 LearnMart｜節錄／重排｜marketplace/views.py::ProductUpdateView</span>

```python
class ProductUpdateView(SellerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)
```

seller A 送 seller B 的 `pk` 時，查詢結果沒有該物件，因此回 404，而不是先抓出來再忘記檢查。

---

## IDOR：問題不是 ID 可猜，而是存取未被限制

IDOR = Insecure Direct Object Reference。

`/orders/42/` 使用流水號不是漏洞本身；漏洞是任何登入者都能用 `pk=42` 取得別人的訂單。

安全方式：

```python
def get_queryset(self):
    return Order.objects.filter(buyer=self.request.user)
```

<!--
授課提示：雙瀏覽器 demo：buyer A 與 B 各自登入，B 直接送 A 的訂單網址 → 404。
-->

---

## 403、404、405 放在不同層

- 403：已識別使用者，但角色／政策拒絕
- 404：目前可見 queryset 中沒有這個物件
- 405：URL 存在，但不允許這個 HTTP method

這些 status code 讓 API／瀏覽器／測試能區分失敗原因；不要所有錯誤都 redirect 到首頁。

---

## Pagination 也是 CBV 的既有能力

```python
class ProductListView(ListView):
    paginate_by = 12
```

Template 得到 `page_obj`、`is_paginated` 等 context。

若搜尋與分類使用 query string，分頁連結要保留它們，否則點第二頁會丟失目前條件。

---

## CBV 常見錯誤

<span class="label warning">檢查順序</span>

- URL 忘記 `.as_view()`
- `template_name` 指到不存在檔案
- `get_queryset()` 沒有 return
- `get_context_data()` 沒先呼叫 `super()`
- 只檢查 role，沒有 ownership
- `form_valid()` 補 seller 後沒 return `super()`
- mixin 放在 generic view 後，行為不如預期

---

## 第 3 章概念檢核

1. `.as_view()` 為何必要？
2. `get_queryset()` 與 `get_context_data()` 各負責什麼？
3. `super()` 在 context 與 form flow 中保留了什麼？
4. 為何 seller role 不足以保護 UpdateView？
5. 何時應回 403，何時用 scoped queryset 產生 404？

<span class="label check">答案見配套實作手冊第 3 章</span>

<!--
授課提示：授權矩陣表（匿名/buyer/owner/其他 seller × GET/POST）請學生填空一次。
-->

---

## 第 3 章 LearnMart 實作

任務：用兩個 seller 驗證 ProductUpdateView 的三層授權。

驗收重點：

- 匿名者得到 login redirect
- buyer 得到 403
- seller A 可編輯自己的商品
- seller A 對 seller B 商品得到 404

[LearnMart 測試資料、步驟與參考測試](../workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md#chapter-3)；[LearnBoard 對應練習](../workbooks/learnboard_02_forms_auth_and_board_workflows_workbook.md#chapter-3)
