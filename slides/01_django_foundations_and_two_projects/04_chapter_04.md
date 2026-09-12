---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 01｜共通基礎：LearnBoard × LearnMart"
footer: "初學者教材｜共通觀念 → 兩個專案對照"
---

# 第 4 章
## Model、關聯與 migration

**本章成果：** 能由需求讀出資料表結構，解釋欄位參數與關聯，並正確區分首次 migrate 與模型變更流程。

<!--
授課提示：資訊量最大的一章，建議拆兩次課：4-1～4-12 欄位與型別一次、關聯與 migration 一次。
-->

---

## 4-1 為什麼 Python list 不夠？

```python
products = ["鍵盤", "筆記本"]
```

伺服器停止後，記憶體內容就消失；多人同時存取也需要可靠的一致資料來源。

Database 提供：

- 持久化保存
- 查詢、排序、篩選
- 關聯與限制
- transaction 等一致性機制

Django Model 是 Python class；ORM 會把 model 操作轉成資料庫操作。

---

## 4-2 關聯式資料庫的基本詞彙

| 資料庫詞彙 | LearnMart 例子 |
|---|---|
| table | `marketplace_product` |
| row | 一件商品 |
| column | `name`、`price`、`stock` |
| primary key | 自動產生的 `id` / `pk` |
| foreign key | Product 指向 Category 或 User |
| constraint | user + product 不可重複的購物車規則 |

Model class 描述 table；model instance 對應一個 row；field 大致對應 column。

---

## 4-3 先看完整領域關係，而不是孤立 class

```text
Category 1 ── * Product * ── 1 User(seller)
User(buyer) 1 ── * CartItem * ── 1 Product
User(buyer) 1 ── * Order 1 ── * OrderItem * ── 1 Product
User(seller) 1 ── * OrderItem
User 1 ── * Review * ── 1 Product
User 1 ── * BoardPost
```

`1 ── *` 表示一對多。User 在不同關係中扮演 buyer、seller、author。

Model 不是把畫面欄位全部塞在同一張表；關係與歷史需求會影響拆分。

---

## 4-4 自訂 User 必須在初始 migration 前決定

**目前 LearnMart 節錄｜`config/settings.py`**

```python
AUTH_USER_MODEL = "marketplace.User"
```

新專案應在第一次正式建立 schema 前設定：

- 後期切換 user model 涉及 migration 與多個關聯，操作困難
- LearnMart 從一開始就繼承 `AbstractUser` 並加入 `role`
- 本章只先認識這個架構決定；密碼、session、權限放在 Deck 2

可重用 app 的 model 關聯常用 `settings.AUTH_USER_MODEL`；runtime 查詢常用 `get_user_model()`。本專案同一 app 的 models 目前直接參照本地 `User` class。

---

## 4-5 Model class 前半：繼承與 field declarations

**目前 LearnMart 節錄／重排｜`marketplace/models.py` 的 `Category`**

```python
class Category(models.Model):
    name = models.CharField(
        "分類名稱", max_length=80, unique=True,
    )
    slug = models.SlugField(
        "網址代稱", max_length=80, unique=True,
    )
```

- 繼承 `models.Model`，成為 Django model
- Field declarations 是 class attributes
- 每個 field 描述 Python／validation／schema contract 的一部分

---

## 4-5A Model class 後半：`Meta` 與 instance method

**目前 LearnMart 節錄｜`marketplace/models.py` 的 `Category`**

```python
class Meta:
    verbose_name = "商品分類"
    verbose_name_plural = "商品分類"
    ordering = ["name"]

def __str__(self):
    return self.name
```

- `Meta` 是所在 model 的 nested configuration class
- `__str__` 是 instance method，第一個參數是 `self`
- Admin／shell 顯示 instance 時會使用 `__str__`

---

## 4-6 Field declaration 的參數層次

```python
name = models.CharField(
    "商品名稱",
    max_length=150,
)
```

- `name`：Python attribute，也是 ORM 欄位名稱
- `CharField`：欄位型別
- 第一個 positional argument：人類可讀名稱 `verbose_name`
- `max_length=150`：Django validation 與 generated form 的長度契約，也影響 schema declaration

**補充／進階：**database 是否獨立強制長度取決於 backend；LearnMart 的 SQLite 不會自行拒絕超長 `varchar`。一般 `.save()` 也不會自動呼叫 `full_clean()`。

讀 field 時要分辨：Django validation、schema 描述，以及真正的 database constraint。

---

## 4-7 Product 的核心 scalar fields

**目前 LearnMart 節錄／重排｜`marketplace/models.py` 的 `Product` scalar fields**

```python
name = models.CharField("商品名稱", max_length=150)
description = models.TextField("商品說明")
price = models.DecimalField("售價", max_digits=10, decimal_places=0)
stock = models.PositiveIntegerField("庫存", default=0)
is_active = models.BooleanField("上架", default=True)
```

- `CharField`：有明確長度的短文字
- `TextField`：長文字
- `PositiveIntegerField`：非負整數
- `BooleanField`：True/False

Field type 會影響 Python value、database column 與自動生成的 form field。

---

## 4-8 `blank` 與 `null` 不同層

```python
image = models.ImageField(..., blank=True)
shipped_at = models.DateTimeField(..., null=True, blank=True)
```

- `blank=True`：Django validation/form 層允許空值
- `null=True`：database column 允許 SQL `NULL`

字串欄位通常使用空字串表示「沒有文字」，不一定要 `null=True`。

LearnMart 的圖片可不填，因此 `blank=True`；尚未出貨時沒有時間，因此 `shipped_at` 同時允許 database NULL 與 form 空白。

<!--
授課提示：快問：Product.image 需要 null=True 嗎？（不必，blank=True 即可）答對代表分層觀念成立。
-->

---

## 4-9 預設值、唯一性與時間欄位

```python
stock = models.PositiveIntegerField(default=0)
slug = models.SlugField(max_length=80, unique=True)
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

- `default`：建立時未提供值就使用預設
- `unique=True`：資料庫不得有重複值
- `auto_now_add`：建立 instance 的第一次 save 時自動寫入
- `auto_now`：一般 `Model.save()` 且欄位參與此次寫入時更新

**常見錯誤：**`save(update_fields=["stock"])` 沒包含 `updated_at`，所以它不會更新；`QuerySet.update()` 也不會自動執行 `auto_now`。

---

## 4-10 金額為何不用 float？

二進位浮點數不能精確表示所有十進位小數；金額需要可預測的十進位運算。

```python
price = models.DecimalField(
    "售價",
    max_digits=10,
    decimal_places=0,
)
```

- `max_digits=10`：Django validation 宣告總位數最多 10 位
- `decimal_places=0`：Django validation 宣告小數點後 0 位
- Field conversion 在 Python 端使用 `Decimal`，不是 float

**補充／進階：**這些參數也影響 generated form 與 schema declaration；SQLite 不把精度當成獨立 database invariant。若必須由 database 保證，需依 backend 與 constraint 設計再驗證。

<!--
授課提示：現場跑 print(0.1 + 0.2) 對照 Decimal 版本，眼見為憑勝過十句解釋。
-->

---

## 4-11 ImageField、Pillow 與儲存路徑

**目前 LearnMart 節錄｜`marketplace/models.py` 的 `Product.image`**

```python
image = models.ImageField(
    "商品圖片",
    upload_to="products/%Y/%m/",
    blank=True,
)
```

- `ImageField` 建立「檔案路徑參照」，圖片本體存於 storage
- Pillow 協助圖片欄位驗證／處理
- `upload_to` 讓檔案依年月放在 `products/YYYY/MM/`
- `blank=True` 允許沒有圖片

Form 的 multipart 與 `request.FILES` 會在 Deck 2 與完整上傳流程一起教。

---

## 4-12 media 在開發環境如何被存取？

**目前 LearnMart 節錄｜`config/settings.py` 與 `config/urls.py`**

```python
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"
```

```python
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
```

- `MEDIA_ROOT`：本機檔案實際儲存位置
- `MEDIA_URL`：瀏覽器 URL 前綴
- Django 這段 serving 僅供 `DEBUG` 開發環境
- production 通常使用專門 web server 或 object storage

---

## 4-13 ForeignKey：資料庫存 ID，Python 看物件

**目前 LearnMart 節錄｜`marketplace/models.py` 的 `Product.seller`**

```python
seller = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name="products",
    verbose_name="賣家",
)
```

- 第一個參數：關聯目標 model
- database 主要保存 seller 的 key
- `product.seller` 取得 User instance
- `on_delete` 決定目標被刪除時的處理
- `related_name` 命名反向查詢入口

<!--
授課提示：強調兩個世界：SQL 欄位存 id、Python 拿到 instance。第 5 章 select_related 全靠這個觀念。
-->

---

## 4-14 正向與反向關聯要成對理解

```python
product.seller
# Product → User，單一物件

seller.products.all()
# User → Product，RelatedManager / QuerySet
```

因為一位 seller 可有多個 products：

- 正向 ForeignKey 是「一個」
- 反向 relation 是「多個」，所以需要 `.all()`、`.filter()` 等 manager 方法

Category 同樣可使用：

```python
product.category
category.products.all()
```

---

## 4-15 `on_delete` 是商業決策

| LearnMart 關聯 | 行為 | 原因 |
|---|---|---|
| Product → Category | `PROTECT` | 有商品時避免刪掉分類 |
| Product → seller | `CASCADE` | 刪 seller 時會嘗試連帶刪商品 |
| Order → buyer | `PROTECT` | 保留訂單歷史 |
| OrderItem → Order | `CASCADE` | 刪訂單時明細一起刪 |
| OrderItem → Product/seller | `PROTECT` | 防止破壞購買歷史參照 |

`on_delete` 只描述一條 relation 的收集規則。若 seller 或商品已被 `OrderItem` 的 `PROTECT` 關聯引用，整次 seller deletion 仍會被阻止；最終結果要看整張 relation graph。

`SET_NULL` 需要 field 同時允許 `null=True`。

<!--
授課提示：提問：刪 Category 時商品該怎樣？刪 User 呢？讓學生先表態再揭曉 PROTECT / CASCADE 的理由。
-->

---

## 4-16 `related_name` 讓反向語意可讀

```python
buyer.orders.all()
seller.products.all()
order.items.all()
product.reviews.all()
```

這些名稱分別來自 ForeignKey 的 `related_name`。

沒有良好命名時，Django 會產生較泛用的預設名稱；在同一 User 扮演 buyer、seller、author 時，明確命名尤其重要。

`related_name` 也可用在跨 relation lookup，例如：

```python
Order.objects.filter(items__seller=seller)
```

---

## 4-17 `TextChoices`：穩定代碼與人類文字

**目前 LearnMart 節錄｜`marketplace/models.py` 的 `Order.Status`**

```python
class Status(models.TextChoices):
    PENDING = "pending", "待出貨"
    SHIPPED = "shipped", "已出貨"
    COMPLETED = "completed", "已完成"
    CANCELLED = "cancelled", "已取消"
```

資料庫存 `pending` 等穩定值；畫面可顯示中文 label。

```python
order.status == Order.Status.PENDING
order.get_status_display()  # 「待出貨」
```

定義 choices 不代表每個狀態轉換都已實作。

---

## 4-18 `Product.Meta`：只說目前真的存在的設定

**目前 LearnMart 節錄｜`marketplace/models.py` 的 `Product.Meta`**

```python
class Product(models.Model):
    # fields 省略

    class Meta:
        ordering = ["-created_at"]
```

Product 目前只有預設排序，沒有自訂 `verbose_name`。

`Meta` 是 nested configuration class；它屬於所在的 model，不能把另一個 model 的選項拼進來。

---

## 4-18A `Category.Meta`：同名 nested class，內容可不同

**目前 LearnMart 節錄｜`marketplace/models.py` 的 `Category.Meta`**

```python
class Meta:
    verbose_name = "商品分類"
    verbose_name_plural = "商品分類"
    ordering = ["name"]
```

- `verbose_name`／`verbose_name_plural` 影響 admin 等人類可讀名稱
- `ordering` 提供沒有明確 `order_by()` 時的 default ordering

**常見錯誤：**看到兩個 class 都叫 `Meta`，不代表它們共享設定。

---

## 4-19 `__str__`、property 與 URL helper

```python
def __str__(self):
    return self.name

@property
def average_rating(self):
    result = self.reviews.aggregate(avg=models.Avg("rating"))["avg"]
    return round(result, 1) if result else None

def get_absolute_url(self):
    return reverse("marketplace:product-detail", kwargs={"pk": self.pk})
```

- `__str__`：shell/admin 顯示名稱
- `@property`：以 attribute 方式讀取計算值
- `get_absolute_url()`：定義商品標準詳情網址

**目前 LearnMart 實作：**商品 template 以它建立連結；`ProductCreateView`／`ProductUpdateView` 沒有另設 `success_url`，成功儲存後也已透過它決定 redirect。

---

## 4-20 Model 改動如何變成資料庫步驟？

```text
models.py（希望的 model state）
        │ makemigrations
        ▼
migrations/0001_...py（可追蹤 operations）
        │ migrate
        ▼
database schema（實際資料表）
```

Migration 是 Python 檔案與版本史，不是直接把目前 models.py 每次重新建立整個 database。

LearnMart 已有 `marketplace/migrations/0001_initial.py`，其中可看到 `CreateModel` 與 `AddConstraint`。

---

## 4-21 clone／取得既有 repository 與修改 model 是兩條流程

### clone／取得既有 repository

```bash
uv run python manage.py migrate
```

Migration 已存在；把它套用到本機 database。

### 你真的改了 model

```bash
uv run python manage.py makemigrations
# 先閱讀產生的 migration
uv run python manage.py migrate
```

`showmigrations` 是檢查套用狀態；不是每次必須的第三個 schema-changing 步驟。

<!--
授課提示：警告：repo 已含 migration，自行亂改 model 會讓 makemigrations --check 失敗；練習請開分支。
-->

---

## 4-22 migration 的常見訊息代表什麼？

```text
No changes detected
```

通常表示 Django 比較 model state 與 migration state 後沒有新差異；在完成版 LearnMart 上這可能是正常結果。

```text
Your models ... have changes that are not yet reflected in a migration
```

表示 model 與 migration 不一致。

驗證指令：

```bash
uv run python manage.py makemigrations --check
```

成功退出表示沒有未建立的 model migration。

---

## 4-23 Admin 是資料管理介面，不是資料模型本身

**目前 LearnMart 節錄｜`marketplace/admin.py` 節錄**

```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "seller", "price", "stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
```

- Model 決定資料結構
- Admin registration 決定後台如何呈現與操作
- `createsuperuser` 建立可登入 `/admin/` 的帳號
- Admin 很適合檢查教學資料，但不是商城使用者 UI
- Chapter lab 的 `is_featured` 只加入 model/admin；目前 `ProductForm.Meta.fields` 不含它，因此商城表單不會自動出現 checkbox

---

## 4-24 使用 Django shell 觀察 model

```bash
uv run python manage.py shell
```

```python
from marketplace.models import Category, Product

Product.objects.count()
Product.objects.first()
Category.objects.all()
```

Django shell 會載入專案設定，適合小步檢查 ORM。

離開：

```python
exit()
```

先觀察回傳型別與內容，再進入下一章 CRUD/QuerySet。

---

## 4-25 Model 常見錯誤

- 修改 model 後忘記建立／套用 migration
- 把 `blank=True` 與 `null=True` 當同義詞
- 金額使用 float
- ForeignKey 沒有思考 `on_delete`
- 改了 `related_name` 卻沒更新反向查詢
- 認為 model validator 一定會在所有 `.save()` 自動執行
- 把完成版 repository 的 `No changes detected` 誤判成環境壞掉

除錯時分開檢查：model state、migration files、database schema。

---

## 第 4 章｜觀念檢核與實作

1. `blank=True` 與 `null=True` 分別作用在哪一層？
2. `max_digits=10, decimal_places=0` 如何限制售價？SQLite 又保證到哪一層？
3. 為什麼 Product→Category 使用 `PROTECT`？
4. clone／取得既有 repository 只需 `migrate`；什麼時候才需 `makemigrations`？
5. 為什麼 custom User 應在 initial migration 前決定？

**概念產出：**畫出 Category、Product、seller 與 OrderItem 的正向／反向 relation，標出可能阻止 deletion 的 `PROTECT`。

**實作任務：**在練習 branch 為 Product 加入 `is_featured`，產生並閱讀 `AddField` migration、套用後於 `ProductAdmin` 顯示／篩選，最後執行 migration drift check。

**配套實作手冊：**LearnMart [第 4 章](../workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md#chapter-4)；LearnBoard [類比第 4 章](../workbooks/learnboard_01_django_foundations_and_message_board_workbook.md#chapter-4)

<!--
授課提示：blank/null 與 on_delete 幾乎必考；workbook「精選欄位」任務請當堂完成前兩步。
-->
