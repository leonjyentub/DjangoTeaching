---
marp: true
theme: default
size: 16:9
paginate: true
header: "Django 02｜表單、身份驗證與工作流程"
footer: "初學者教材｜LearnBoard × LearnMart"
style: |
  section {
    font-family: 'Noto Sans CJK TC', 'Noto Serif CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', 'Heiti TC', sans-serif;
    font-size: 28px;
    line-height: 1.35;
  }
  h1, h2 {
    font-family: 'Noto Sans CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', sans-serif;
  }
  h1 { color: #8b1e2d; }
  h2 { color: #17324d; }
  blockquote {
    font-family: 'Noto Serif CJK TC', 'Noto Sans CJK TC', 'WenQuanYi Zen Hei', serif;
  }
  code, kbd {
    font-family: 'Noto Sans Mono CJK TC', 'SF Mono', Consolas,
                 'WenQuanYi Zen Hei Mono', 'Courier New', monospace;
    font-size: 0.82em;
  }
  pre { margin-top: 0.35em; margin-bottom: 0.35em; }
  .label { display: inline-block; padding: 0.15em 0.55em; border-radius: 999px; font-size: 0.72em; font-weight: 700; background: #e8eef5; color: #17324d; }
  .current { background: #e5f4ea; color: #17633a; }
  .warning { background: #fff0d9; color: #8a4b08; }
  .check { background: #f3e8ff; color: #6b21a8; }
  .small { font-size: 0.78em; }
---

# 第 4 章
## 購物車、POST 操作與第一批流程測試

目標：把 mutation 的 method、身份、ownership、驗證與測試放在同一條流程。

<!--
授課提示：第一批正式 mutation 測試，節奏放慢；測試慣例在 workbook「如何使用本手冊」。
-->

---

## CartItem 的資料規則

<span class="label current">目前 LearnMart｜節錄／重排｜marketplace/models.py</span>

```python
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name="cart_items")
    quantity = models.PositiveIntegerField(
        "數量", default=1, validators=[MinValueValidator(1)]
    )
```

每一列代表「某 user 的某 product 與數量」。

---

## Database constraint 防止重複 cart row

```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=["user", "product"],
            name="unique_cart_product",
        )
    ]
```

View 的 `get_or_create()` 提供流程便利；database constraint 提供競爭情況下的最後一致性防線。

---

## 加入購物車必須是 POST

```python
@require_POST
@login_required
def add_to_cart(request, pk):
    ...
```

這段與 checked-in source 順序一致。Decorator 由下往上套用：`login_required` 先包 function，`require_POST` 再成為最外層。

因此匿名 **GET** 先被外層 method 檢查擋成 405；匿名 **POST** 通過 method 檢查後才由 `login_required` 302 到 login。若交換兩個 decorator，匿名 GET 會先 redirect，而不是 405。

<!--
授課提示：curl -X GET 示範 405；連回 00b 的口訣「a 是去、button 是做」。
-->

---

## 取得 Product 也要限制狀態

```python
product = get_object_or_404(
    Product,
    pk=pk,
    is_active=True,
)
```

URL 中的 `pk` 是 client-controlled input。除了存在性，也要限制「可購買」狀態，不能只在 template 隱藏已下架商品。

---

## 解析 quantity：瀏覽器限制不是安全規則

```python
try:
    quantity = max(1, int(request.POST.get("quantity", 1)))
except ValueError:
    quantity = 1
```

HTML 的 `min`、`max` 可被移除。伺服器仍要處理：

- 缺少值
- 非整數
- 0 或負數
- 大於庫存

目前實作將多種錯誤 fallback 成 1；正式 UX 可回傳更明確錯誤。

---

## `get_or_create()` 有兩條路

```python
item, created = CartItem.objects.get_or_create(
    user=request.user,
    product=product,
)
```

- `created=True`：剛新增，數量設成提交值
- `created=False`：原本已有，累加但不超過庫存

回傳 tuple 的第二個值讓 View 判斷走哪條流程。

<!--
授課提示：回傳 tuple 解包——複習 00a 3-3 的 unpacking；created 是 False 時代表累加情境。
-->

---

## 目前累加行為與提示有一個細節

```python
item.quantity = (
    quantity if created
    else min(item.quantity + quantity, product.stock)
)
```

若累加超過庫存，數量會靜默 cap 在 `product.stock`，接著仍顯示「已加入」。

<span class="label warning">教學觀察</span> 規則正確不代表回饋最清楚；可在 workbook 練習加入明確提示。

---

## Cart 顯示只取目前 user 的資料

```python
items = request.user.cart_items.select_related(
    "product", "product__seller"
)
total = sum(item.subtotal for item in items)
```

由 `request.user.cart_items` 反向關聯開始，天然限制 ownership；`select_related` 避免逐筆讀 product/seller 的額外 query。

---

## 更新 cart item 先縮小 ownership

```python
item = get_object_or_404(
    CartItem,
    pk=pk,
    user=request.user,
)
```

只有 `pk=pk` 不夠。攻擊者可以改 URL id；加上 `user=request.user` 才能把物件範圍限制在自己的購物車。

---

## 更新與移除都使用 POST

```python
@require_POST
@login_required
def update_cart(request, pk): ...

@require_POST
@login_required
def remove_from_cart(request, pk): ...
```

對應 template 的每個 form 都有：

- 明確 action URL
- method="post"
- CSRF token
- button，而不是改資料的普通 link

---

## Context processor：每頁都需要 cart count

<span class="label current">目前 LearnMart｜逐字摘錄｜marketplace/context_processors.py</span>

```python
def cart_count(request):
    if request.user.is_authenticated:
        return {
            "cart_count": sum(
                item.quantity
                for item in request.user.cart_items.all()
            )
        }
    return {"cart_count": 0}
```

它回傳 dictionary，合併到每個使用該 template backend 的 context。

<!--
授課提示：打開 settings 的 context_processors 註冊清單；移除註冊讓模板炸掉，展示依賴關係。
-->

---

## Context processor 必須在 settings 註冊

```python
"context_processors": [
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    "marketplace.context_processors.cart_count",
]
```

因此 `base.html` 在任何頁面都能顯示 `{{ cart_count }}`，不必每個 View 重複提供。

---

## Context processor 的成本也會遍及每頁

目前實作對每個已登入 request 讀取 cart rows，再由 Python `sum()`。

可能改進方向：

```python
from django.db.models import Sum

request.user.cart_items.aggregate(
    total=Sum("quantity")
)["total"] or 0
```

是否值得優化要看流量與 query；先知道「全域方便」也代表「全域成本」。

---

## Mutation route matrix（1／2）

| Route | GET | POST mutation gate |
|---|---|---|
| register | 顯示 form | anonymous flow；Form 建 User／hash password |
| logout | 405 | CSRF；結束 session（無額外 role gate） |
| product create | seller form | login + seller；server 指派 seller |
| product update | owner seller form | login + seller + owner-scoped Product |
| add cart | 405 | login；active Product；server 指派 user |
| update/remove cart | 405 | login + CartItem owner |

GET 可顯示 form，不代表 GET 執行 mutation。POST form 還需要 CSRF token／Origin policy；表中再列 application authorization。

---

## Mutation route matrix（2／2）

| Route | GET | POST mutation gate |
|---|---|---|
| checkout | unbound form + cart summary | login + user cart；server 算 buyer/total/snapshot |
| shipping | 405 | login + seller + order membership |
| review | 405 | login + purchase/status eligibility；server author |
| board create | authenticated form | login；server author |

目前 checkout 與 review 只要求 authenticated user，再以 cart／purchase rules 限制；**沒有 buyer-role check**。Product create/update 與 board create 則是 GET 顯示 form、POST 才修改資料。

---

## 開始寫流程測試：Arrange–Act–Assert

```text
Arrange：建立 user、product、初始 cart state
Act：登入並 POST add-to-cart
Assert：response 與 database state 都正確
```

測試不是只看「頁面沒有 500」。重要 workflow 通常同時有 HTTP 結果與資料副作用。

<!--
授課提示：投影一個現成 test 用三色標註 AAA 三段；之後所有練習都照此結構寫。
-->

---

## `TestCase` 與真實 transaction 測試

```python
class MarketplaceFlowTests(TestCase):
    def setUp(self): ...
```

- Runner 為整次執行建立 test database，不是每個 method 建一個實體 database。
- `TestCase` 以外層 transaction 與 savepoint／rollback 快速隔離 methods。
- 因此一般 CRUD、response、view-level atomic rollback 很適合用 `TestCase`。
- 真實 commit boundary、blocking／locking 要用 `TransactionTestCase`，並搭配支援功能的 database、separate connections 與審慎的 concurrency test。
- SQLite 不能用來證明 row-level `select_for_update()` 行為。

---

## `setUp()` 每個 test method 前執行

<span class="label current">目前 LearnMart｜節錄／重排｜marketplace/tests.py</span>

```python
def setUp(self):
    self.seller = User.objects.create_user(...)
    self.buyer = User.objects.create_user(...)
    category = Category.objects.create(...)
    self.product = Product.objects.create(...)
```

每個測試從一致且獨立的資料狀態開始。

---

## 測試匿名 cart redirect

```python
def test_anonymous_user_cannot_add_cart(self):
    response = self.client.post(
        reverse("marketplace:add-to-cart", args=[self.product.pk])
    )
    self.assertRedirects(
        response,
        f"/accounts/login/?next=/products/{self.product.pk}/cart/",
    )
```

這個測試驗證身份層與 `next`，不是 CSRF。

---

## 測試 client 預設不強制 CSRF

```python
self.client.post(url, data)
```

Django 一般 `Client()` 預設不執行 CSRF 檢查，方便測試 View 行為。因此成功 POST 測試不能證明 CSRF token 正確。

需要專門驗證時：

```python
Client(enforce_csrf_checks=True)
```

並處理 cookie/token 流程。

---

## 測試登入後的 database state

```python
def test_buyer_can_add_cart(self):
    self.client.login(username="buyer", password="safe-pass-123")
    self.client.post(
        reverse("marketplace:add-to-cart", args=[self.product.pk]),
        {"quantity": 2},
    )
    self.assertEqual(
        CartItem.objects.get(user=self.buyer).quantity,
        2,
    )
```

Act 後直接查 database，確認副作用而非只確認 redirect。

---

## `login()` 與 `force_login()`

- `self.client.login(...)`：驗證 credentials，適合順便驗證密碼可登入
- `self.client.force_login(user)`：直接建立 authenticated session，當測試重點不是登入本身時更清楚

若使用 `login()`，可以先 assert return value，避免密碼打錯導致後續測試用匿名身份執行。

---

## 第 4 章概念檢核

1. Database unique constraint 與 `get_or_create()` 各解決什麼？
2. 為何 cart lookup 必須加 `user=request.user`？
3. Context processor 的便利與成本是什麼？
4. 一個 cart test 應同時 assert 哪些面向？
5. 一般 test client 的成功 POST 為何不能證明 CSRF？

<span class="label check">答案見配套實作手冊第 4 章</span>

<!--
授課提示：ownership 測試需要至少兩位 user——呼應 workbook 的測試撰寫慣例。
-->

---

## 第 4 章 LearnMart 實作

任務：加入「超過庫存不改變 cart」與「不能更新別人的 cart item」測試。

驗收重點：

- status／redirect 符合設計
- 原有 cart quantity 不變
- 不產生跨 user 修改
- full test suite 仍通過

[LearnMart 測試步驟與參考片段](../workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md#chapter-4)；[LearnBoard 對應練習](../workbooks/learnboard_02_forms_auth_and_board_workflows_workbook.md#chapter-4)
