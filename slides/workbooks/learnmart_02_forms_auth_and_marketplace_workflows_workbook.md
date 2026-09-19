# LearnMart 02 配套實作手冊

**對應課程：** [Django 課程教材](../README.md) 的 LearnMart 第二階段  
**用途：** 概念檢核解答、逐步實作、聚焦前後程式碼與驗收方式。  
**注意：** 這是一般 Markdown，不是 Marp 投影片。  
**返回課程：** [Django 課程教材](../README.md)

本手冊以目前 repository 中的 LearnMart 為基準。每個練習先要求你讀現有行為，再以小範圍修改或測試固定規則；不要一次複製整個檔案。

---

## 目錄

| 章 | 投影片頁碼 | 主題 | 實作成果 |
|---|---:|---|---|
| [第 1 章](#chapter-1) | 6–33 | 完整表單生命週期 | 測試 ProductForm allowlist 與 server-owned seller |
| [第 2 章](#chapter-2) | 34–55 | 身份驗證與 session | 測試 `next`、登入 session 與 POST logout |
| [第 3 章](#chapter-3) | 56–80 | CBV、Mixin 與物件權限 | 建立 ProductUpdateView 授權矩陣 |
| [第 4 章](#chapter-4) | 81–105 | Cart 與第一批流程測試 | 測試超量與跨使用者 cart mutation |
| [第 5 章](#chapter-5) | 106–133 | Checkout、transaction 與 locking | 擴充 snapshot、清空與失敗完整性測試 |
| [第 6 章](#chapter-6) | 134–150 | 出貨、狀態與評價 | 測試 seller membership 與 review eligibility |
| [第 7 章](#chapter-7) | 151–174 | 安全與回歸測試 | 測試 XSS escaping、POST-only 與 invariants |

投影片 1–5 是閱讀方式與全冊地圖；175–178 是端到端整合與後續方向。

---

## 如何使用本手冊

每章採相同節奏：

1. **先回答，不先看解答**：用自己的話寫出規則。
2. **讀現有程式**：確認規則目前放在哪一層。
3. **做一個小變更**：以 focused excerpt 修改，不覆蓋整檔。
4. **先跑單一測試**：縮短回饋時間。
5. **再跑完整驗證**：確認沒有破壞其他流程。

### 前置條件與編輯符號

- 先完成 Deck 1，並確認 checked-in 六個 tests 在你的環境通過。
- 本手冊練習按章累積；後一章的 snippet 可能使用前一章加入的 `self.category`、helper 或 import。
- **插入**：把新 method 放進既有 `MarketplaceFlowTests` class；不要刪除原 tests。
- **取代**：只有標示「修改前／修改後」或「取代 import block」時才替換指定 focused excerpt。
- `...` 代表保留原碼，不可把省略號貼進可執行檔。
- 投影片標示「逐字摘錄」才是 verbatim source；「節錄／重排」以及本手冊的 focused excerpt 都可能省略無關行或調整換行。

完成全冊後，`marketplace/tests.py` 的累積 imports 可整理為：

```python
from unittest.mock import patch

from django.test import Client, TestCase
from django.urls import reverse

from .models import (
    BoardPost,
    CartItem,
    Category,
    Order,
    OrderItem,
    Product,
    Review,
    User,
)
```

若只做部分章節，只 import 實際使用的 names；不要因尚未做到後章而複製未使用 import。

基準命令：

```bash
uv sync
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

若你只在 `marketplace/tests.py` 增加測試，不需要 `makemigrations`；仍可執行 `makemigrations --check`，確認沒有意外改到 model。

### 測試撰寫慣例

- Arrange：準備 User、Product、CartItem、Order 等資料。
- Act：使用 `self.client` 發出 request。
- Assert：同時檢查 response 與 database state。
- 權限測試要有至少兩位使用者，否則無法證明 ownership。
- View 修改資料後，對舊 instance 呼叫 `refresh_from_db()`。

---

<a id="chapter-1"></a>
# 第 1 章｜完整表單生命週期

**對應投影片：6–33**

## 概念檢核解答

### 1. Unbound form 與 invalid bound form 有何不同？

Unbound form 沒有綁定提交資料，通常用於第一次 GET 顯示；它不應立即顯示「必填」錯誤。Invalid bound form 已綁定 request data 並完成驗證，但至少一條規則失敗；它保留使用者輸入與 errors，應重新 render 給使用者修正。

### 2. 為什麼 invalid POST 要 render 原本的 form？

如果 invalid POST 後重新建立空 form，使用者輸入與具體錯誤都會消失。直接 render 原本 bound form，Django 才能把欄位值、欄位錯誤與 non-field errors 一起顯示。

### 3. `cleaned_data` 何時才能讀？

在 `form.is_valid()` 回傳 `True` 後讀取。驗證前，輸入仍是未可信任的字串或檔案；驗證失敗時，某些欄位也可能不存在於 `cleaned_data`。

因此 `Form.clean()` 的跨欄位比較要先呼叫 `data = super().clean()`，用 `data.get(...)` 取值，確認兩個值都不是 `None` 後才比較，最後無論是否新增 non-field error 都要 `return data`。自訂訊息使用 `from django.core.exceptions import ValidationError`。

### 4. `commit=False` 解決什麼問題？

它讓 `ModelForm` 先建立 model instance，但暫不寫入 database。View 可補上不應由 client 控制的欄位，例如 `seller=request.user`、`buyer=request.user`、server-calculated total，再呼叫 `.save()`。

### 5. CSRF、表單驗證、物件權限各自保護什麼？

- CSRF：驗證 cookie/form token，並依情境套用 Origin／Referer policy，阻止跨站 request 濫用既有 session；它不判斷 browser 或 user 是否「可信」。
- Form validation：轉換型別並檢查欄位／跨欄位規則。
- Object authorization：判斷目前使用者是否可對指定 Product、CartItem、Order 操作。

三者不可互相替代。

## 現有程式追蹤

依序開啟：

1. `marketplace/forms.py::ProductForm`
2. `marketplace/views.py::ProductCreateView`
3. `templates/marketplace/form.html`
4. `marketplace/models.py::Product.get_absolute_url`

將現有流程畫成：

```text
GET product-create
→ CreateView 建 unbound ProductForm
→ form.html（multipart + CSRF）

POST product-create
→ ProductForm bound with POST/FILES
→ invalid: render bound form
→ valid: form_valid()
→ seller = request.user
→ save Product
→ get_absolute_url()
→ 302 product detail + success message
```

### 要特別觀察的安全決策

`ProductForm.Meta.fields` 沒有 `seller`：

```python
fields = (
    "category",
    "name",
    "description",
    "price",
    "stock",
    "image",
    "is_active",
)
```

真正的 seller 來自：

```python
form.instance.seller = self.request.user
```

所以即使攻擊者自行在 POST 加入 `seller=<other-id>`，ModelForm 也不會採用該欄位。

## 實作 1A｜讓 category 可在後續測試重用

目前 `setUp()` 的 category 只是一個 local variable。

### 修改前｜`marketplace/tests.py`

```python
category = Category.objects.create(name="3C", slug="3c")
self.product = Product.objects.create(
    seller=self.seller,
    category=category,
    ...
)
```

### 修改後｜只改這個 focused excerpt

```python
self.category = Category.objects.create(name="3C", slug="3c")
self.product = Product.objects.create(
    seller=self.seller,
    category=self.category,
    ...
)
```

這不是功能變更，只讓後面的 test 能取得 category id。

## 實作 1B｜測試 seller 是 server-owned

在 `MarketplaceFlowTests` 加入：

```python
def test_product_create_uses_logged_in_seller(self):
    other_seller = User.objects.create_user(
        username="other-seller",
        password="safe-pass-123",
        role=User.Role.SELLER,
    )
    self.client.force_login(self.seller)

    response = self.client.post(
        reverse("marketplace:product-create"),
        {
            "category": self.category.pk,
            "name": "安全測試滑鼠",
            "description": "seller 必須來自 request.user",
            "price": 650,
            "stock": 4,
            "is_active": "on",
            "seller": other_seller.pk,
        },
    )

    product = Product.objects.get(name="安全測試滑鼠")
    self.assertRedirects(
        response,
        reverse("marketplace:product-detail", args=[product.pk]),
    )
    self.assertEqual(product.seller, self.seller)
```

### 這個測試證明什麼？

- 登入 seller 可以建立商品。
- Client 額外送出的 `seller` 不在 `ProductForm.Meta.fields`，不會被採用。
- `ProductCreateView.form_valid()` 以 `request.user` 指派 owner。
- 成功後採 PRG，redirect 到 `get_absolute_url()`。

它不證明 CSRF，因為一般 Django test client 預設不強制 CSRF checks。

## 實作 1C｜測試 invalid bound form 不建立商品

```python
def test_product_create_rejects_negative_stock(self):
    self.client.force_login(self.seller)

    response = self.client.post(
        reverse("marketplace:product-create"),
        {
            "category": self.category.pk,
            "name": "錯誤庫存商品",
            "description": "應保留表單並顯示錯誤",
            "price": 100,
            "stock": -1,
            "is_active": "on",
        },
    )

    self.assertEqual(response.status_code, 200)
    self.assertFalse(Product.objects.filter(name="錯誤庫存商品").exists())
    self.assertTrue(response.context["form"].is_bound)
    self.assertIn("stock", response.context["form"].errors)
```

`PositiveIntegerField` 透過 ModelForm 的驗證拒絕負值。Response 是 200，因為 invalid POST 重新 render 同一頁，而不是成功 redirect。

## 實作 1D｜手動驗證圖片上傳

1. 以 seller 登入。
2. 開啟 `/seller/products/new/`。
3. 選取小型 JPG 或 PNG。
4. 送出後確認商品詳情頁顯示圖片。
5. 檢查檔案位於 `media/products/<year>/<month>/`。

請同時指出四個必要條件：

- `Product.image` 是 `ImageField`。
- form template 有 `enctype="multipart/form-data"`。
- View/Generic editing flow 綁定 uploaded file。
- 開發環境以 `MEDIA_URL`／`MEDIA_ROOT` 提供檔案。

不要把本地 `static(settings.MEDIA_URL, ...)` 當成 production media server。

## 單章驗收

```bash
uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_product_create_uses_logged_in_seller

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_product_create_rejects_negative_stock
```

完成條件：兩個測試通過，既有六個測試也仍通過。

---

<a id="chapter-2"></a>
# 第 2 章｜身份驗證、Session 與帳號流程

**對應投影片：34–55**

## 概念檢核解答

### 1. Authentication 與 authorization 有何不同？

Authentication 確認目前 request 對應哪位使用者；authorization 決定這位使用者是否有權執行特定操作。登入 seller 仍不能編輯其他 seller 的 Product；登入 buyer 也不能查看其他 buyer 的 Order。

### 2. 為什麼 custom user 要在初始 migration 前決定？

User 會被大量 foreign key、auth table 與 migration dependency 參照。新專案要在第一次 `migrate` 前設定 `AUTH_USER_MODEL`，而 custom User 應建立在該 app 的 `0001_initial` migration，讓 swappable dependencies 能正確建立 migration graph。建立資料表後才更換，需要重寫關聯與搬移既有資料，不是只改 `AUTH_USER_MODEL`。

### 3. Session cookie 是否包含密碼？

不包含。典型 server-side session cookie 攜帶的是 session identifier；server 依它找回 session data，再由 AuthenticationMiddleware 設定 `request.user`。Cookie 仍需 Secure、HttpOnly、SameSite 等 production 設定保護。

### 4. `create_user()` 與 `UserCreationForm` 各保證什麼？

`create_user()` 會用正確方法 hash password；它不等於執行互動式註冊所需的全部 password validators。`UserCreationForm` 會驗證兩次密碼一致、套用設定中的 password validators，並正確設定 hash。

### 5. 為什麼 logout 應使用 POST？

Logout 改變 session 狀態。若 GET 即可登出，第三方頁面可用 link/image request 讓使用者在不知情時登出。POST 明確表達 mutation；CSRF middleware 再驗證 token 與適用的 Origin／Referer policy，而不是宣稱 request 所在 browser 已被信任。

## 現有程式追蹤

- `config/settings.py`：`AUTH_USER_MODEL`、login/logout redirects。
- `config/urls.py`：`LoginView`、`LogoutView`。
- `templates/registration/login.html`：hidden `next`。
- `templates/base.html`：POST logout form。
- `marketplace/views.py::register`：註冊後 `login(request, user)`。

## 實作 2A｜測試登入 redirect 的 `next`

現有匿名 cart test 以硬編碼 path 檢查 redirect。新的測試先讓 `reverse()` 組出目的地，降低 route 變更時的維護成本。

```python
def test_anonymous_cart_page_redirects_with_next(self):
    cart_url = reverse("marketplace:cart")

    response = self.client.get(cart_url)

    self.assertRedirects(
        response,
        f"{reverse('login')}?next={cart_url}",
    )
```

### 為什麼這裡期待 302，而不是 403？

匿名者尚未完成 authentication；`login_required` 將其送到 login，並保留原目的地。403 較適合「已登入但政策不允許」的情況。

## 實作 2B｜測試 session 跨 request 保留

```python
def test_login_session_is_reused_on_next_request(self):
    logged_in = self.client.login(
        username="buyer",
        password="safe-pass-123",
    )
    self.assertTrue(logged_in)

    response = self.client.get(reverse("marketplace:cart"))

    self.assertEqual(response.status_code, 200)
    self.assertTrue(response.wsgi_request.user.is_authenticated)
    self.assertEqual(response.wsgi_request.user, self.buyer)
```

`self.client` 會保存 response 設定的 cookies，因此下一個 request 帶著同一個 test session。

## 實作 2C｜測試 logout 是 POST mutation

加入 `from django.test import TestCase` 的現有 import 不需改；直接加入 test methods：

```python
def test_logout_post_ends_session(self):
    self.client.force_login(self.buyer)

    response = self.client.post(reverse("logout"))

    self.assertRedirects(response, reverse("marketplace:home"))
    next_response = self.client.get(reverse("marketplace:cart"))
    self.assertRedirects(
        next_response,
        f"{reverse('login')}?next={reverse('marketplace:cart')}",
    )
```

再加入 method 行為測試：

```python
def test_logout_get_does_not_log_user_out(self):
    self.client.force_login(self.buyer)

    response = self.client.get(reverse("logout"))

    self.assertEqual(response.status_code, 405)
    cart_response = self.client.get(reverse("marketplace:cart"))
    self.assertEqual(cart_response.status_code, 200)
```

Django 5 的內建 `LogoutView` 使用 POST；GET 預期得到 405。

## 延伸思考｜目前 role 註冊政策

`RegistrationForm.Meta.fields` 包含 `role`，所以訪客可自行選 seller。課堂版方便，但 production 不應直接把高權限商業角色交給 client 決定。

請設計兩種替代方案，不必立即修改：

1. 公開註冊永遠建立 buyer，seller 由 staff 後台核准。
2. Seller 有獨立申請 model/status，核准後才更新 role。

指出 server-owned 欄位在哪一個 View/service/admin action 中被寫入。

## 實作 2D｜修正 register 的 empty POST bound state

Checked-in `register()` 使用：

```python
form = RegistrationForm(request.POST or None)
```

空 `QueryDict` 是 falsey，所以 `POST {}` 會傳入 `None`，產生 unbound form，必填錯誤不會顯示。先插入 regression test；修改前應失敗：

```python
def test_empty_registration_post_returns_bound_errors(self):
    response = self.client.post(reverse("marketplace:register"), {})

    self.assertEqual(response.status_code, 200)
    form = response.context["form"]
    self.assertTrue(form.is_bound)
    self.assertIn("username", form.errors)
    self.assertIn("password1", form.errors)
```

再只取代 form 建立那一行：

```python
form = RegistrationForm(
    request.POST if request.method == "POST" else None
)
```

這個寫法讓 GET 得到 unbound form，任何 POST（包含空 POST）都得到 bound form。若課程此階段不修改 app，必須把它列為已知 deferred issue，不能宣稱 checked-in register 已正確處理 empty POST。

## 單章驗收

```bash
uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_anonymous_cart_page_redirects_with_next

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_logout_post_ends_session

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_logout_get_does_not_log_user_out

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_empty_registration_post_returns_bound_errors
```

---

<a id="chapter-3"></a>
# 第 3 章｜Class-based View、Mixin 與物件權限

**對應投影片：56–80**

## 概念檢核解答

### 1. `.as_view()` 為什麼必要？

URLconf 需要一個可接收 request 並回傳 response 的 callable。`.as_view()` 建立這個 callable；每次 request 再建立 view instance、設定 `request/args/kwargs`，並由 `dispatch()` 依 method 呼叫 `get()` 或 `post()`。

### 2. `get_queryset()` 與 `get_context_data()` 各負責什麼？

`get_queryset()` 決定能查到哪些 model rows，常同時承擔可見性、ownership 與 query optimization。`get_context_data()` 在既有 object list/detail context 上增加 template 顯示需要的其他資料。

### 3. `super()` 在 context 與 form flow 中保留了什麼？

在 `get_context_data()` 中，`super()` 保留 generic view 建立的 object、pagination 等 context；在 `form_valid()` 中，`super()` 保留 ModelForm save、success URL resolution 與 redirect。少了 return 或 super，流程可能中斷。

### 4. 為什麼 seller role 不足以保護 UpdateView？

Role 只證明「是某個 seller」，沒有證明「擁有 URL 指定的 product」。因此 `get_queryset()` 必須加 `seller=self.request.user`。

### 5. 何時應回 403，何時用 scoped queryset 產生 404？

若已知使用者角色不符合整個操作，可回 403；若 URL 指定的物件不在目前使用者可見／可操作範圍，先 scope queryset 並讓 lookup 回 404，可避免洩漏物件存在性。

## 實作目標｜建立 ProductUpdateView 授權矩陣

| 使用者 | 目標 Product | 預期 |
|---|---|---|
| anonymous | 任意 | 302 login + `next` |
| buyer | 任意 | 403 |
| seller A | seller A 的 product | 200 |
| seller A | seller B 的 product | 404 |

這四格分別驗證 login、role、正常 ownership、錯誤 ownership。

## 實作 3A｜匿名與 buyer

```python
def test_anonymous_user_cannot_open_product_update(self):
    url = reverse("marketplace:product-update", args=[self.product.pk])

    response = self.client.get(url)

    self.assertRedirects(
        response,
        f"{reverse('login')}?next={url}",
    )


def test_buyer_cannot_open_product_update(self):
    self.client.force_login(self.buyer)

    response = self.client.get(
        reverse("marketplace:product-update", args=[self.product.pk])
    )

    self.assertEqual(response.status_code, 403)
```

## 實作 3B｜owner seller 可開啟

```python
def test_seller_can_open_own_product_update(self):
    self.client.force_login(self.seller)

    response = self.client.get(
        reverse("marketplace:product-update", args=[self.product.pk])
    )

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.context["object"], self.product)
```

Generic UpdateView 同時提供 `object` 與 form；這裡先確認查到正確 object。

## 實作 3C｜其他 seller 得到 404

```python
def test_seller_cannot_open_another_sellers_product_update(self):
    other_seller = User.objects.create_user(
        username="other-seller",
        password="safe-pass-123",
        role=User.Role.SELLER,
    )
    self.client.force_login(other_seller)

    response = self.client.get(
        reverse("marketplace:product-update", args=[self.product.pk])
    )

    self.assertEqual(response.status_code, 404)
```

這個 test 對應目前：

```python
def get_queryset(self):
    return Product.objects.filter(seller=self.request.user)
```

### 反例：不要只在 POST 後檢查

```python
# 不建議
product = Product.objects.get(pk=pk)
if product.seller != request.user:
    ...
```

問題不只在「是否最後拒絕」；在拒絕前可能已讀取、render、記錄或修改不該接觸的 object。以 scoped queryset 作為 retrieval boundary 更一致。

## 實作 3D｜驗證 POST 也受同一個 queryset 保護

```python
def test_seller_cannot_post_update_to_another_sellers_product(self):
    other_seller = User.objects.create_user(
        username="other-seller-post",
        password="safe-pass-123",
        role=User.Role.SELLER,
    )
    self.client.force_login(other_seller)

    response = self.client.post(
        reverse("marketplace:product-update", args=[self.product.pk]),
        {
            "category": self.category.pk,
            "name": "被竄改的名稱",
            "description": self.product.description,
            "price": self.product.price,
            "stock": self.product.stock,
            "is_active": "on",
        },
    )

    self.assertEqual(response.status_code, 404)
    self.product.refresh_from_db()
    self.assertEqual(self.product.name, "教學鍵盤")
```

權限測試不能只 assert status；還要 assert forbidden mutation 沒有發生。

## 單章驗收

```bash
uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_seller_cannot_open_another_sellers_product_update

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_seller_cannot_post_update_to_another_sellers_product
```

---

<a id="chapter-4"></a>
# 第 4 章｜購物車、POST 操作與第一批流程測試

**對應投影片：81–105**

## 概念檢核解答

### 1. Database unique constraint 與 `get_or_create()` 各解決什麼？

`get_or_create()` 讓一般流程可以「有就取、沒有就建立」並回報 `created`；`UniqueConstraint(user, product)` 在 database 層禁止同一組 key 出現兩列，是競爭與其他寫入路徑下的最後一致性防線。

### 2. 為什麼 cart lookup 必須加 `user=request.user`？

CartItem 的 `pk` 由 URL/client 控制，可以被猜或修改。只用 `pk` 會形成 IDOR；加入 owner filter 才能保證查到的是目前 user 的 item，否則回 404。

### 3. Context processor 的便利與成本是什麼？

便利是每個 template 都自動取得 `cart_count`；成本是每個使用相同 template backend 的 authenticated request 都執行該查詢／計算。全域 context 應保持小、可預期且高效。

### 4. 一個 cart test 應同時 assert 哪些面向？

至少包含 HTTP 結果（status/redirect）、正確 owner/product row、quantity，以及錯誤輸入時原資料是否不變。若有 message，也可檢查使用者回饋。

### 5. 一般 test client 的成功 POST 為何不能證明 CSRF？

`Client()` 預設不強制 CSRF checks。它適合測 View 邏輯，但要驗證 CSRF middleware 必須使用 `Client(enforce_csrf_checks=True)` 並先取得 token/cookie。

## 選擇 `TestCase` 還是 `TransactionTestCase`

- `TestCase` 以外層 transaction 與 savepoint／rollback 隔離 methods，速度快，適合本手冊多數 request、CRUD、authorization 與 view-level atomic rollback assertions。
- 這個外層包裝會改變真實 commit boundary；不要用它宣稱已觀察到 production transaction blocking。
- 真實 commit、`on_commit()` 時機、row-lock blocking 或多 connection concurrency 應使用 `TransactionTestCase`，搭配支援目標功能的 database 與 separate connections／threads。
- SQLite 不提供 row-level `select_for_update()`，即使用 `TransactionTestCase` 也不能證明 PostgreSQL 式 row locks。

## 現有 cart mutation 防線

```text
@require_POST
→ @login_required
→ get_object_or_404(..., user=request.user)
→ parse quantity
→ compare product.stock
→ save/delete
→ redirect cart
```

這個 decorator 順序與 checked-in source 一致：Python 先套內層 `login_required`，再套外層 `require_POST`。所以 anonymous GET 先得到 405；anonymous POST 通過 method gate 後才 302 到 login。交換順序會讓 anonymous GET 先 redirect，外部可觀察行為不同。

`add_to_cart` 的 Product lookup 也加 `is_active=True`。

## 實作 4A｜超過庫存時不建立 CartItem

```python
def test_add_cart_over_stock_does_not_create_item(self):
    self.client.force_login(self.buyer)

    response = self.client.post(
        reverse("marketplace:add-to-cart", args=[self.product.pk]),
        {"quantity": self.product.stock + 1},
    )

    self.assertRedirects(response, self.product.get_absolute_url())
    self.assertFalse(
        CartItem.objects.filter(
            user=self.buyer,
            product=self.product,
        ).exists()
    )
```

這個 test 固定目前 `if quantity > product.stock` 的規則。

## 實作 4B｜更新超量時保留原 quantity

```python
def test_update_cart_over_stock_keeps_original_quantity(self):
    item = CartItem.objects.create(
        user=self.buyer,
        product=self.product,
        quantity=2,
    )
    self.client.force_login(self.buyer)

    response = self.client.post(
        reverse("marketplace:update-cart", args=[item.pk]),
        {"quantity": 99},
    )

    self.assertRedirects(response, reverse("marketplace:cart"))
    item.refresh_from_db()
    self.assertEqual(item.quantity, 2)
```

## 實作 4C｜不能更新別人的 CartItem

```python
def test_user_cannot_update_another_users_cart_item(self):
    other = User.objects.create_user(
        username="cart-owner",
        password="safe-pass-123",
    )
    item = CartItem.objects.create(
        user=other,
        product=self.product,
        quantity=2,
    )
    self.client.force_login(self.buyer)

    response = self.client.post(
        reverse("marketplace:update-cart", args=[item.pk]),
        {"quantity": 4},
    )

    self.assertEqual(response.status_code, 404)
    item.refresh_from_db()
    self.assertEqual(item.quantity, 2)
```

## 實作 4D｜GET mutation URL 應回 405

```python
def test_remove_cart_rejects_get(self):
    item = CartItem.objects.create(
        user=self.buyer,
        product=self.product,
        quantity=1,
    )
    self.client.force_login(self.buyer)

    response = self.client.get(
        reverse("marketplace:remove-from-cart", args=[item.pk])
    )

    self.assertEqual(response.status_code, 405)
    self.assertTrue(CartItem.objects.filter(pk=item.pk).exists())
```

第二個 assert 證明錯誤 method 不只回 405，也沒有 side effect。

## 選做｜讓「已存在 cart + 超量累加」回饋更明確

目前：

```python
item.quantity = (
    quantity if created
    else min(item.quantity + quantity, product.stock)
)
item.save()
messages.success(request, f"已將「{product.name}」加入購物車。")
```

可能的 focused 改寫：

```python
requested_quantity = quantity if created else item.quantity + quantity
if requested_quantity > product.stock:
    messages.error(request, "購物車中的總數量會超過目前庫存。")
else:
    item.quantity = requested_quantity
    item.save()
    messages.success(request, f"已將「{product.name}」加入購物車。")
```

### 修改前先決定產品規則

- 要保留原 quantity，還是 cap 到 stock？
- 新建 item 超量時，`get_or_create()` 是否已建立暫時 row？
- 若採上述寫法，`created=True` 但超量時需刪除 newly created item，或先驗證再呼叫 `get_or_create()`。

因此更穩定的順序是：先驗證單次 quantity 不超過 stock，再取得 item，算累加後總數，再決定是否 save。不要只貼片段而忽略 `get_or_create()` 的 side effect。

## 單章驗收

```bash
uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_add_cart_over_stock_does_not_create_item

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_user_cannot_update_another_users_cart_item

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_remove_cart_rejects_get
```

---

<a id="chapter-5"></a>
# 第 5 章｜訂單、Checkout、Transaction 與鎖定

**對應投影片：106–133**

## 概念檢核解答

### 1. OrderItem 為什麼同時保存 FK 與 snapshot？

FK 讓系統保留與目前 Product／seller 的關聯；`product_name`、`unit_price` 保存購買當下事實。商品之後改名或改價，歷史訂單仍顯示交易成立時的內容。

### 2. `commit=False` 在 checkout 補了哪些 server-owned 值？

目前補 `buyer=request.user` 與由 cart/database 計算的 `total`。OrderItem 的 seller、product name、unit price、quantity 也由 server objects 取得，不信任 hidden fields。

### 3. 普通 `return` 是否會讓 `atomic` rollback？

不會。只要沒有未處理 exception、也沒有明確標記 transaction rollback，正常離開 atomic block 會 commit。因此驗證應盡量在第一次寫入前完成；若寫入後發現失敗，要 raise 或採明確 rollback 策略。

### 4. Atomicity 與 row locking 的差異是什麼？

Atomicity 保證一組 database writes 一起 commit 或 rollback；row locking 協調 concurrent transactions 對同一批 rows 的讀改。兩者解決不同問題。

### 5. 為什麼 SQLite 上不能宣稱 `select_for_update()` 保護庫存競爭？

Django 在 SQLite backend 上不會取得 `SELECT ... FOR UPDATE` 的 row-level lock 效果。教學程式展示 API 意圖，但 production concurrency 必須在支援 row locks 的 database（常見如 PostgreSQL）上重新設計並測試。

## 實作 5A｜擴充 imports

目前：

```python
from .models import CartItem, Category, Order, Product, User
```

修改為：

```python
from .models import CartItem, Category, Order, OrderItem, Product, User
```

只增加後續測試直接查 snapshot row 所需的 `OrderItem`。

## 實作 5B｜擴充既有成功 checkout test

找到 `test_checkout_creates_order_and_reduces_stock`。保留現有 arrange/act，於 `order = ...` 後加入 focused assertions：

```python
order_item = OrderItem.objects.get(order=order)
self.assertEqual(order_item.product, self.product)
self.assertEqual(order_item.seller, self.seller)
self.assertEqual(order_item.product_name, "教學鍵盤")
self.assertEqual(order_item.unit_price, 990)
self.assertEqual(order_item.quantity, 2)
self.assertFalse(CartItem.objects.filter(user=self.buyer).exists())
```

### 為什麼不只 assert `order.total`？

Total 正確仍可能發生：snapshot 名稱錯、seller 錯、cart 未清、quantity 錯。每個 domain invariant 都要有可觀察 assertion。

## 實作 5C｜商品之後改價，snapshot 不變

```python
def test_order_item_keeps_purchase_time_snapshot(self):
    self.client.force_login(self.buyer)
    CartItem.objects.create(
        user=self.buyer,
        product=self.product,
        quantity=1,
    )
    self.client.post(
        reverse("marketplace:checkout"),
        {
            "recipient_name": "王小明",
            "phone": "0912345678",
            "address": "台北市教學路 1 號",
        },
    )
    order_item = OrderItem.objects.get(
        order__buyer=self.buyer,
        product=self.product,
    )

    self.product.name = "改名後鍵盤"
    self.product.price = 1200
    self.product.save(update_fields=["name", "price"])
    order_item.refresh_from_db()

    self.assertEqual(order_item.product_name, "教學鍵盤")
    self.assertEqual(order_item.unit_price, 990)
```

## 實作 5D｜庫存不足時維持所有資料

```python
def test_checkout_stock_failure_keeps_all_original_state(self):
    self.client.force_login(self.buyer)
    item = CartItem.objects.create(
        user=self.buyer,
        product=self.product,
        quantity=6,
    )

    response = self.client.post(
        reverse("marketplace:checkout"),
        {
            "recipient_name": "王小明",
            "phone": "0912345678",
            "address": "台北市教學路 1 號",
        },
    )

    self.assertRedirects(response, reverse("marketplace:cart"))
    self.assertFalse(Order.objects.filter(buyer=self.buyer).exists())
    self.assertFalse(OrderItem.objects.exists())
    self.product.refresh_from_db()
    item.refresh_from_db()
    self.assertEqual(self.product.stock, 5)
    self.assertEqual(item.quantity, 6)
```

這條失敗在任何 write 前被發現，所以資料保持不變。它主要測 validation ordering，不是模擬「建立 Order 後拋 exception」的 rollback。

## 實作 5E｜在 Order 與 OrderItem 寫入後觸發 rollback

本章累積 import 已包含：

```python
from unittest.mock import patch
```

Patch `Product.save()`，讓 failure 發生在 checkout 已建立 Order 與 OrderItem、正準備保存扣減庫存時：

```python
def test_checkout_rolls_back_after_order_item_write(self):
    self.client.force_login(self.buyer)
    cart_item = CartItem.objects.create(
        user=self.buyer,
        product=self.product,
        quantity=2,
    )

    with patch(
        "marketplace.views.Product.save",
        side_effect=RuntimeError("simulated stock save failure"),
    ):
        with self.assertRaisesMessage(
            RuntimeError,
            "simulated stock save failure",
        ):
            self.client.post(
                reverse("marketplace:checkout"),
                {
                    "recipient_name": "王小明",
                    "phone": "0912345678",
                    "address": "台北市教學路 1 號",
                },
            )

    self.assertFalse(Order.objects.filter(buyer=self.buyer).exists())
    self.assertFalse(OrderItem.objects.exists())
    self.product.refresh_from_db()
    cart_item.refresh_from_db()
    self.assertEqual(self.product.stock, 5)
    self.assertEqual(cart_item.quantity, 2)
```

### 為什麼這比 patch `OrderItem.objects.create()` 更強？

目前 loop 先 `OrderItem.objects.create(...)`，再呼叫 `item.product.save(...)`。因此 exception 前已有 Order 與 OrderItem database writes；若 `@transaction.atomic` 沒有包住整段，測試會留下半套 rows。Patch path 指向 `views.py` 實際使用的 `Product` class。

這條 test 驗證**同一 request、同一 connection 的 view-level atomic rollback invariant**：Order／OrderItem 消失、stock 與 cart 還原。它不是 real commit、row lock 或 concurrent transaction test。

### `TestCase` 與 transaction 邊界提醒

`TestCase` 本身以外層 transaction 加 savepoints／rollback 隔離 methods，適合這種 View exception 後的狀態 assertion。若要驗證真正 commit、blocking、deadlock 或 `select_for_update()`，改用 `TransactionTestCase`，搭配支援 row locks 的 database 與 separate connections；SQLite 不能證明 row-level locking。

## 設計練習｜更精準的 locking target

目前：

```python
items = list(
    request.user.cart_items
    .select_related("product", "product__seller")
    .select_for_update()
)
```

請寫出問題說明，不急著把它宣稱為 production fix：

1. Query 在 GET 也 evaluation。
2. SQLite 的 `select_for_update()` 沒有 row-level lock effect。
3. 在支援的 backends 上，`select_related("product", "product__seller")` 形成 joined query；除了 CartItem，joined Product／seller rows 也可能被鎖，除非使用 backend 支援的 `select_for_update(of=(...))` 限定範圍。
4. 不同 user 有不同 CartItem；真正共享競爭資源是 Product stock。
5. 較清楚的方向是在 POST `atomic()` 中，先收集 product PKs，再以 deterministic PK order 明確查詢並 `select_for_update()` Product，最後用鎖後最新 stock 驗證。
6. 固定鎖定順序可降低多商品 transaction deadlock 風險，但仍需 failure/retry policy。

只有換成 PostgreSQL 仍不會自動修正 target、joined-lock scope 與流程順序；real lock test 需要 `TransactionTestCase`、separate connections 與支援該行為的 database。

## 實作 5F｜修正 checkout 的 empty POST bound state

Checked-in checkout 使用：

```python
form = CheckoutForm(request.POST or None)
```

與 register 相同，`POST {}` 會建立 unbound form。先插入 regression test：

```python
def test_empty_checkout_post_returns_bound_errors(self):
    self.client.force_login(self.buyer)
    CartItem.objects.create(
        user=self.buyer,
        product=self.product,
        quantity=1,
    )

    response = self.client.post(reverse("marketplace:checkout"), {})

    self.assertEqual(response.status_code, 200)
    form = response.context["form"]
    self.assertTrue(form.is_bound)
    self.assertIn("recipient_name", form.errors)
    self.assertFalse(Order.objects.filter(buyer=self.buyer).exists())
```

再只取代 form 建立那一行：

```python
form = CheckoutForm(
    request.POST if request.method == "POST" else None
)
```

GET 仍是 unbound `CheckoutForm` 加 cart summary；empty POST 則是帶 errors 的 invalid bound form。若不修改 application code，要明確把此 test／修正標為 deferred，而不是把 checked-in `request.POST or None` 說成已解決。

## 單章驗收

```bash
uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_order_item_keeps_purchase_time_snapshot

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_checkout_stock_failure_keeps_all_original_state

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_checkout_rolls_back_after_order_item_write

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_empty_checkout_post_returns_bound_errors
```

---

<a id="chapter-6"></a>
# 第 6 章｜賣家出貨、狀態與評價

**對應投影片：134–150**

## 概念檢核解答

### 1. 為什麼 seller order queryset 需要 `distinct()`？

`Order` 經 reverse relation `items__seller` 做 join；同一張 Order 若有多個符合 seller 的 OrderItem，SQL result 可能重複該 Order row。`distinct()` 讓列表每張訂單只出現一次。

### 2. Model 有四個 status 是否代表四種 transition 都存在？

不是。Choices 只定義可儲存值。Transition 還需定義 actor、允許的舊狀態、side effects、timestamp 與 endpoint。現有 UI/View 只實作 pending → shipped。

### 3. Whole-order shipping 對多賣家有什麼副作用？

任何參與 seller 都能把整張 Order 改為 shipped，使其他 seller 尚未出貨的 items 也共享 shipped status；Review eligibility 也可能因此提早成立。正式模型應引入 per-seller shipment/group 或 item-level fulfillment state。

### 4. Review 的資格、rating 範圍、唯一性各由哪一層負責？

- 購買且已出貨／完成：View query。
- rating 1–5：Model validators 經 ModelForm 驗證。
- 每位 author 對每個 product 一列：database UniqueConstraint。
- 重複送出更新同一列：View 的 `update_or_create()`。

### 5. `update_or_create()` 與 UniqueConstraint 如何配合？

`update_or_create(product=..., author=..., defaults=...)` 用同一組唯一 key 查找；找到就 update，找不到才 create。UniqueConstraint 在 database 層保證競爭或其他寫入路徑不能留下重複 key。

## 實作 6A｜擴充 imports

目前第 5 章後可能是：

```python
from .models import CartItem, Category, Order, OrderItem, Product, User
```

加入 Review：

```python
from .models import (
    CartItem,
    Category,
    Order,
    OrderItem,
    Product,
    Review,
    User,
)
```

這是 focused import rewrite，不代表要重排整個 tests file。

## 實作 6B｜建立可重用的已購買資料 helper

在 `MarketplaceFlowTests` 內加入：

```python
def create_order_item(
    self,
    *,
    buyer=None,
    product=None,
    status=Order.Status.PENDING,
):
    buyer = buyer or self.buyer
    product = product or self.product
    order = Order.objects.create(
        buyer=buyer,
        recipient_name="測試買家",
        phone="0912345678",
        address="台北市測試路 1 號",
        status=status,
        total=product.price,
    )
    OrderItem.objects.create(
        order=order,
        product=product,
        seller=product.seller,
        product_name=product.name,
        unit_price=product.price,
        quantity=1,
    )
    return order
```

`create_order_item` 不以 `test_` 開頭，所以 Django 不會把它當 test method。

## 實作 6C｜buyer 不可出貨

```python
def test_buyer_cannot_ship_order(self):
    order = self.create_order_item()
    self.client.force_login(self.buyer)

    response = self.client.post(
        reverse("marketplace:ship-order", args=[order.pk])
    )

    self.assertEqual(response.status_code, 403)
    order.refresh_from_db()
    self.assertEqual(order.status, Order.Status.PENDING)
    self.assertIsNone(order.shipped_at)
```

## 實作 6D｜不相關 seller 得到 404

```python
def test_unrelated_seller_cannot_ship_order(self):
    order = self.create_order_item()
    other_seller = User.objects.create_user(
        username="unrelated-seller",
        password="safe-pass-123",
        role=User.Role.SELLER,
    )
    self.client.force_login(other_seller)

    response = self.client.post(
        reverse("marketplace:ship-order", args=[order.pk])
    )

    self.assertEqual(response.status_code, 404)
    order.refresh_from_db()
    self.assertEqual(order.status, Order.Status.PENDING)
```

## 實作 6E｜正確 seller 可做單一 transition

```python
def test_related_seller_can_ship_pending_order(self):
    order = self.create_order_item()
    self.client.force_login(self.seller)

    response = self.client.post(
        reverse("marketplace:ship-order", args=[order.pk])
    )

    self.assertRedirects(response, reverse("marketplace:seller-orders"))
    order.refresh_from_db()
    self.assertEqual(order.status, Order.Status.SHIPPED)
    self.assertIsNotNone(order.shipped_at)
```

可以再**依序** POST 一次並保存第一次 `shipped_at`，確認 sequential duplicate request 不更新 timestamp。這只證明序列情境的冪等效果；兩個 concurrent requests 仍可能同時讀到 PENDING。正式方向可用 `filter(pk=..., status=PENDING).update(...)` 檢查 affected-row count，或在支援的 database 使用適當 row lock。

## 實作 6F｜非購買者與 pending buyer 不可評價

```python
def test_non_purchaser_cannot_review_product(self):
    self.client.force_login(self.buyer)

    response = self.client.post(
        reverse("marketplace:add-review", args=[self.product.pk]),
        {"rating": 5, "comment": "沒有買卻想評"},
    )

    self.assertRedirects(response, self.product.get_absolute_url())
    self.assertFalse(Review.objects.exists())


def test_pending_order_buyer_cannot_review_product(self):
    self.create_order_item(status=Order.Status.PENDING)
    self.client.force_login(self.buyer)

    self.client.post(
        reverse("marketplace:add-review", args=[self.product.pk]),
        {"rating": 5, "comment": "尚未出貨"},
    )

    self.assertFalse(Review.objects.exists())
```

## 實作 6G｜合格評價建立，再送時更新

```python
def test_eligible_buyer_updates_existing_review(self):
    self.create_order_item(status=Order.Status.SHIPPED)
    self.client.force_login(self.buyer)
    url = reverse("marketplace:add-review", args=[self.product.pk])

    self.client.post(url, {"rating": 4, "comment": "第一次評價"})
    self.client.post(url, {"rating": 5, "comment": "更新後評價"})

    self.assertEqual(
        Review.objects.filter(
            product=self.product,
            author=self.buyer,
        ).count(),
        1,
    )
    review = Review.objects.get(
        product=self.product,
        author=self.buyer,
    )
    self.assertEqual(review.rating, 5)
    self.assertEqual(review.comment, "更新後評價")
```

## 實作 6H｜超範圍 rating 不建立 row

```python
def test_review_rejects_rating_outside_one_to_five(self):
    self.create_order_item(status=Order.Status.SHIPPED)
    self.client.force_login(self.buyer)

    self.client.post(
        reverse("marketplace:add-review", args=[self.product.pk]),
        {"rating": 9, "comment": "超出範圍"},
    )

    self.assertFalse(Review.objects.exists())
```

這裡是 `ReviewForm` 使用 model field validators；UniqueConstraint 不是 rating range 的來源。

## 多賣家限制分析題

建立：

- seller A 的 Product A
- seller B 的 Product B
- 同一個 Order 中各一個 OrderItem

讓 seller A POST ship endpoint，觀察整張 Order 變成 SHIPPED。回答：

1. seller B 的商品是否真的出貨？
2. buyer 是否已通過 Product B 的 review eligibility query？
3. 若新增 `Shipment(order, seller, status, shipped_at)`，哪個 query 與 template 要改？
4. 若改成 `OrderItem.fulfillment_status`，order-level status 要如何聚合？

這是一個已知 domain limitation，不要求在本章直接重構 production data model。

## 單章驗收

```bash
uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_unrelated_seller_cannot_ship_order

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_eligible_buyer_updates_existing_review

uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_review_rejects_rating_outside_one_to_five
```

---

<a id="chapter-7"></a>
# 第 7 章｜安全與回歸測試整合

**對應投影片：151–174**

## 概念檢核解答

### 1. Template autoescaping 與 raw HttpResponse 的邊界在哪？

Django template 中一般 `{{ variable }}` 會 escape HTML-sensitive characters；raw `HttpResponse(f"...")` 不經 template engine，因此不會自動獲得這個保護。`|safe` 也會明確關閉該值的 escaping。

### 2. ORM 防 injection 是否同時保證 ownership？

不保證。ORM parameterization 能防止 filter value 改變 SQL 結構，但 `Product.objects.get(pk=pk)` 仍可能合法查到別人的物件。Ownership 要靠 scoped queryset 或明確授權規則。

### 3. 為什麼 CSRF、login、role、ownership 都要存在？

它們回答不同問題：CSRF token 與 Origin／Referer policy 是否通過、目前是誰、是否具有某角色、是否與指定 object 有允許關係。CSRF 通過不代表 browser 或 user 被信任；任何一層通過都不能推論其他層也通過。

### 4. Workflow test 為什麼要同時 assert response 與 side effects？

正確 redirect 可能伴隨錯誤 total／stock；正確 database update 也可能向錯誤使用者洩漏頁面。HTTP contract 與資料 invariants 都是 workflow 的一部分。

### 5. `check`、`makemigrations --check`、`test` 各自檢查什麼？

- `check`：Django project/system configuration。
- `makemigrations --check`：models 是否有未建立 migration 的變更。
- `test`：程式實際行為是否符合 assertions。

三者互補，不互相替代。

## 實作 7A｜匯入 BoardPost

將 model imports 加入 `BoardPost`：

```python
from .models import (
    BoardPost,
    CartItem,
    Category,
    Order,
    OrderItem,
    Product,
    Review,
    User,
)
```

## 實作 7B｜Stored content 預設被 escape

```python
def test_board_escapes_user_supplied_html(self):
    BoardPost.objects.create(
        author=self.buyer,
        title="XSS 測試",
        content='<script>alert("xss")</script>',
    )

    response = self.client.get(reverse("marketplace:board-list"))

    self.assertContains(
        response,
        "&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;",
    )
    self.assertNotContains(response, '<script>alert("xss")</script>')
```

如果 test 因 HTML entity 表示方式不同而失敗，先檢查 response body 實際 encoding；目標是 raw executable `<script>` 不存在，不要為了讓測試通過而對 template 加 `|safe`。

## 實作 7C｜所有 mutation route 的 GET matrix

可以使用 `subTest` 減少重複：

```python
def test_state_changing_routes_reject_get(self):
    self.client.force_login(self.buyer)
    cart_item = CartItem.objects.create(
        user=self.buyer,
        product=self.product,
        quantity=1,
    )
    urls = [
        reverse("marketplace:add-to-cart", args=[self.product.pk]),
        reverse("marketplace:update-cart", args=[cart_item.pk]),
        reverse("marketplace:remove-from-cart", args=[cart_item.pk]),
        reverse("marketplace:add-review", args=[self.product.pk]),
    ]

    for url in urls:
        with self.subTest(url=url):
            response = self.client.get(url)
            self.assertEqual(response.status_code, 405)

    cart_item.refresh_from_db()
    self.assertEqual(cart_item.quantity, 1)
    self.assertFalse(Review.objects.exists())
```

`ship-order` 需要 seller 與 order fixture，可放在第 6 章相應 test；不要為追求一個大 matrix 而讓 setup 難以理解。

## 實作 7D｜加一個跨使用者 remove regression test

```python
def test_user_cannot_remove_another_users_cart_item(self):
    other = User.objects.create_user(
        username="remove-owner",
        password="safe-pass-123",
    )
    item = CartItem.objects.create(
        user=other,
        product=self.product,
        quantity=2,
    )
    self.client.force_login(self.buyer)

    response = self.client.post(
        reverse("marketplace:remove-from-cart", args=[item.pk])
    )

    self.assertEqual(response.status_code, 404)
    self.assertTrue(CartItem.objects.filter(pk=item.pk).exists())
```

這個測試的第二個 assertion 是重要的 failure invariant：禁止操作不應有 side effect。

## 實作 7E｜建立安全測試檢查表

對所有 checked-in form／mutation routes 填寫。GET 顯示 form 與 POST mutation 必須分開描述：

| Route | GET behavior | POST mutation與 CSRF | Authentication／role | Object scope／server-owned values |
|---|---|---|---|---|
| registration | anonymous 顯示 form；authenticated 會 redirect | form token；建立 User | 公開 anonymous flow；目前可自行選 role | password 由 form hash；role 目前不是 server-owned |
| logout | 405 | base form token；清 session | View 無額外 role gate | session state |
| product create | seller 顯示 form | multipart form token；建立 Product | login + seller | seller=`request.user` |
| product update | owner seller 顯示 form | multipart form token；更新 Product | login + seller | owner-scoped Product；不可改 seller |
| add cart | 405 | product-detail form token；create/update CartItem | **任何 authenticated user** | active Product；user=`request.user`；stock rule |
| update cart | 405 | cart form token；更新／刪除 | **任何 authenticated user** | CartItem owner + stock rule |
| remove cart | 405 | cart form token；刪除 | **任何 authenticated user** | CartItem owner |
| checkout | unbound CheckoutForm + cart summary | checkout form token；建立 order flow | **任何 authenticated user；沒有 buyer-role check** | user cart；buyer/total/snapshots 由 server 決定 |
| shipping | 405 | seller-order form token；改 status/time | login + seller | seller 必須出現在 order items |
| review | 405 | product-detail form token；create/update | **任何 authenticated user；沒有 buyer-role check** | purchase/status eligibility；author=`request.user` |
| board create | authenticated 顯示 form | generic form token；建立 BoardPost | **任何 authenticated user** | author=`request.user` |

表中「form token」描述 template 有 `{% csrf_token %}`；真正 enforcement 還包含 middleware 的 token 與適用 Origin／Referer policy。一般 `Client()` 成功 POST 不等於已測這層。每一列還應各自補 normal、invalid、authorization、side effects、failure integrity 五個面向。

## 實作 7F｜專門的 CSRF test（選做）

需要額外 import：

```python
from django.test import Client, TestCase
```

最小負向測試：

```python
def test_add_cart_rejects_post_without_csrf_when_checks_enabled(self):
    client = Client(enforce_csrf_checks=True)
    client.force_login(self.buyer)

    response = client.post(
        reverse("marketplace:add-to-cart", args=[self.product.pk]),
        {"quantity": 1},
    )

    self.assertEqual(response.status_code, 403)
    self.assertFalse(CartItem.objects.exists())
```

這只證明缺 token 被拒絕。再加入正向 token/cookie flow：

```python
def test_add_cart_accepts_valid_csrf_token(self):
    client = Client(enforce_csrf_checks=True)
    client.force_login(self.buyer)
    client.get(
        reverse("marketplace:product-detail", args=[self.product.pk])
    )
    token = client.cookies["csrftoken"].value

    response = client.post(
        reverse("marketplace:add-to-cart", args=[self.product.pk]),
        {
            "quantity": 1,
            "csrfmiddlewaretoken": token,
        },
    )

    self.assertRedirects(response, self.product.get_absolute_url())
    self.assertTrue(
        CartItem.objects.filter(
            user=self.buyer,
            product=self.product,
            quantity=1,
        ).exists()
    )
```

第一次 GET render 含 `{% csrf_token %}` 的 product detail，讓 client 收到 CSRF cookie；POST 同時送 cookie 與 form token。這對正、負路徑驗證 token enforcement。若另以 HTTPS／Origin 情境測試，還要設定匹配的 host/origin，不能把成功只歸因於「authenticated browser」。

## 實作 7G｜完整回歸命令

先跑剛改的單一 test：

```bash
uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_board_escapes_user_supplied_html
```

再跑 class：

```bash
uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests
```

最後跑全專案與靜態檢查：

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

### 如何判讀結果

- `check` 無 issue：基本 Django configuration 一致。
- `makemigrations --check` exit 0：沒有 model/migration drift。
- `test` 全過：目前 assertions 保障的行為沒有退步。
- 沒有測到的 behavior 仍不能宣稱被驗證。

## Production 邊界清單

課堂專案目前刻意簡化。提交部署建議前，至少逐項設計：

- `SECRET_KEY` 由 secrets/environment 提供。
- `DEBUG=False` 與正確 `ALLOWED_HOSTS`。
- HTTPS、secure session/CSRF cookies、HSTS。
- PostgreSQL 等 production database 與實際 concurrency tests。
- 上傳檔案大小、格式重新處理、隔離 storage、惡意檔案策略。
- Seller onboarding、支付、退款、per-seller fulfillment。
- Error monitoring、structured logging、audit trail、backup/restore。

`python manage.py check --deploy` 可以指出部分 settings；它不會替你完成 domain threat model。

---

# 全冊完成檢查

你應能不看答案完成以下口頭追蹤：

1. 從 product-create POST 到 Product row 與 redirect。
2. 從 session cookie 到 `request.user`。
3. 從 `.as_view()` 到 `get_queryset()` ownership scope。
4. 從 add-to-cart POST 到 CartItem uniqueness。
5. GET checkout 如何建立 unbound CheckoutForm + cart summary，以及 POST 如何建立 Order／OrderItem snapshot、扣 stock、清 cart。
6. 從 seller membership 到 pending → shipped。
7. 從 purchase eligibility 到 `update_or_create()` review。
8. 從 user content 到 escaped template response。

## 最終驗收

- [ ] 每章概念題都能用自己的話回答。
- [ ] 所有新增 tests 的名稱描述行為而非實作細節。
- [ ] 權限失敗同時 assert status 與「資料未改」。
- [ ] Checkout 成功與失敗 invariants 都有測試。
- [ ] 沒有用 `|safe` 顯示 user-generated content。
- [ ] 沒有把 seller、buyer、price、total、status 交給 hidden input 決定。
- [ ] `check`、migration check、完整 test suite 都執行並記錄真實結果。

## 進一步練習

依風險與前置知識排序：

1. 為 Product price 加非負 validator 與 test。
2. 將 cart quantity parsing 改成 dedicated Django Form。
3. 為 seller order list 加 `select_related("buyer")`，用 query-count test 驗證。
4. 把 review form errors 顯示在 product detail，而不只顯示一般 message。
5. 在 PostgreSQL 環境重新設計並測試 Product stock locking。
6. 建立 per-seller Shipment model，修正混合 seller 訂單的 fulfillment 與 review eligibility。

每次只做一項，先寫會失敗的 test，再完成最小實作，最後跑完整 suite。
