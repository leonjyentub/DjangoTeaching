---
marp: true
theme: default
size: 16:9
paginate: true
header: "Django 01｜共通基礎：LearnBoard × LearnMart"
footer: "初學者教材｜共通觀念 → 兩個專案對照"
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

# 第 5 章
## ORM、QuerySet 與資料規則

**本章成果：**能分辨 manager、QuerySet、instance，完成 CRUD、關聯查詢與第一輪 query optimization。

<!--
授課提示：進入前先複習 4-13 反向關聯語法；本章大量使用 related_name。
-->

---

## 5-1 三種物件不要混在一起

```python
Product.objects
Product.objects.filter(is_active=True)
Product.objects.get(pk=1)
```

| 表達式 | 回傳／角色 |
|---|---|
| `Product.objects` | Manager：建立查詢入口 |
| `.filter(...)` | QuerySet：可能有 0 到多筆 |
| `.get(...)` | 一個 Product instance；找不到／多筆會例外 |

Instance 有 `name`、`save()`；QuerySet 有 `filter()`、`count()`；兩者方法不同。

---

## 5-2 Create：先準備必要關聯

```python
from marketplace.models import Category, Product, User

seller = User.objects.get(username="seller")
category = Category.objects.get(slug="tech")

product = Product.objects.create(
    seller=seller,
    category=category,
    name="教學鍵盤",
    description="練習 ORM",
    price=990,
    stock=5,
)
```

`.create()` 會立即 INSERT 並回傳已儲存 instance；成功後 `product.pk` 有值。

注意：一般 `.create()`／`.save()` 不等同自動呼叫完整 `full_clean()`。

---

## 5-3 Read：`get()` 與 `filter()` 的契約

```python
Product.objects.get(pk=1)
Product.objects.filter(is_active=True)
```

- `get()`：期待恰好一筆
  - 0 筆：`Product.DoesNotExist`
  - 多筆：`Product.MultipleObjectsReturned`
- `filter()`：永遠回 QuerySet；0 筆也是空 QuerySet
- `pk` 是 primary key 的通用別名，本專案對應自動 `id`

若條件本來就可能多筆，不要用 `get()`。

---

## 5-4 Update 與 Delete

```python
product.stock = 8
product.save(update_fields=["stock"])
```

`update_fields` 讓 UPDATE 只送指定欄位；它不是 validation allowlist。

```python
product.delete()
```

Delete 會依關聯的 `on_delete` 產生 cascade 或保護錯誤。刪除前先確認歷史資料與關聯規則。

大量更新另有 `QuerySet.update()`；其 hook/訊號行為與逐筆 `save()` 不完全相同。

---

## 5-5 Lookup：雙底線拆成路徑與操作

```python
Product.objects.filter(
    name__icontains="鍵盤",
    price__lte=2000,
)
```

- `name__icontains`：name 包含文字，通常不分大小寫
- `price__lte`：price 小於或等於
- 多個 keyword conditions 預設是 AND

雙底線也可跨 relation：

```python
Product.objects.filter(category__slug="tech")
```

先走 `category`，再比較其 `slug`。

---

## 5-6 `Q` object 表達 OR

```python
from django.db.models import Q

products = Product.objects.filter(
    Q(name__icontains=q) |
    Q(description__icontains=q)
)
```

- `Q(...)` 包裝查詢條件
- `|` 組成 SQL OR
- `&` 組成 SQL AND
- `~` 表示 NOT
- 括號會影響組合優先順序

這裡不能改成 Python `or`；`Q` 使用 operator overloading 建立查詢樹。

---

## 5-7 QuerySet 的 lazy 心智模型

```python
qs = Product.objects.filter(is_active=True)
qs = qs.filter(stock__gt=0)
```

上面通常只是在建立／組合 query，尚未立即讀 database。

常見 evaluation 時機：

- iteration：`for product in qs`
- `list(qs)`、`len(qs)`、`bool(qs)`
- indexing/slicing 的某些形式
- template 迭代

QuerySet method 通常回傳新的 QuerySet，不會原地修改舊變數所代表的查詢。

<!--
授課提示：shell 三步演示：建 queryset 不查庫 → print(qs.query) 看 SQL → list(qs) 才執行。
-->

---

## 5-8 `count()`、`exists()` 與取整份資料

如果只要數量：

```python
qs.count()
```

如果只問有沒有：

```python
qs.exists()
```

若之後本來就要遍歷全部資料，重複 `exists()` 再 iterate 可能造成兩次 query。選擇方法時要看後續需求，而不是背「永遠最快」。

QuerySet 評估後可有結果 cache，但建立新 QuerySet 或不同操作仍可能再查一次。

---

## 5-9 N+1：一個列表為何變很多 SQL？

```python
products = Product.objects.all()
for product in products:
    print(product.seller.username)
```

可能發生：

- 1 次查 products
- 每個 product 再查 seller
- 20 商品可能約 21 次 query

問題不是 Python loop 本身，而是每次讀尚未載入的 relation 都觸發 database access。

先觀察問題，再選擇 optimization。

<!--
授課提示：用 connection.queries 或 debug-toolbar 展示 N+1 實際筆數，數字最有說服力。
-->

---

## 5-10 `select_related`：單值關聯使用 JOIN

**目前 LearnMart 節錄／重排｜`marketplace/views.py` 的 `ProductListView.get_queryset()`**

```python
queryset = Product.objects.filter(
    is_active=True,
).select_related("category", "seller")
```

適合：ForeignKey、OneToOne 等單值 relation。

因為商品卡會讀：

```django
{{ product.category.name }}
{{ product.seller.username }}
```

同一 query 先帶回 category/seller，可避免每張卡片再查。

---

## 5-11 `prefetch_related`：多值關聯分批查再組合

**目前 LearnMart 節錄｜`marketplace/views.py` 的 `ProductDetailView.get_queryset()`**

```python
Product.objects.prefetch_related("reviews__author")
```

適合：

- reverse ForeignKey
- ManyToMany
- 其他多值 relation

Django 通常執行額外 query，再於 Python 把結果對應回 parent。Detail template 會 iterate reviews 並讀 author，因此這是有實際用途的例子。

---

## 5-12 選 optimization 前先問 relation 形狀

```text
product.category       一個 → select_related
product.seller         一個 → select_related
product.reviews.all()  多個 → prefetch_related
order.items.all()      多個 → prefetch_related
```

不要把所有 relation 都塞進兩種方法：

- 先看 template/View 是否真的會讀
- 確認關聯方向與數量
- 測量 query 數
- 不必要 prefetch 也會增加查詢與記憶體

Optimization 應由使用方式驅動。

---

## 5-13 `aggregate()`：整個集合回一組摘要

**目前 LearnMart 節錄｜`marketplace/models.py` 的 `Product.average_rating`**

```python
result = self.reviews.aggregate(
    avg=models.Avg("rating")
)["avg"]
```

`aggregate()` 回 dictionary，表示整個 QuerySet 的摘要：

```python
{"avg": 4.5}
```

常見函式：`Count`、`Sum`、`Avg`、`Min`、`Max`。

若每個 product 都呼叫 property，列表可能每件商品多一次 aggregate query。

---

## 5-13A 同一個 property 在 template 讀兩次，也可能查兩次

**目前 LearnMart 實作的注意點｜`Product.average_rating`**

一般 `@property` 不會自動 cache。若 template 在 `{% if product.average_rating %}` 與輸出時各讀一次，背後的 `aggregate()` 也可能執行兩次。

**補充／進階｜只評估一次的 template 寫法**

```django
{% with rating=product.average_rating %}
  {% if rating %}
    <span class="text-warning">★ {{ rating }}</span>
  {% endif %}
{% endwith %}
```

`prefetch_related("reviews__author")` 不會讓 `aggregate()` 自動改用 prefetched rows；需要依實際 query 測量再設計。

---

## 5-14 `annotate()`：替每一列加計算欄位

```python
from django.db.models import Avg

products = Product.objects.annotate(
    avg_rating=Avg("reviews__rating")
)
```

- `aggregate()`：整個集合得到一份摘要
- `annotate()`：QuerySet 每個結果多一個計算 attribute

```django
{{ product.avg_rating }}
```

若要在商品列表一次顯示每件平均分數，`annotate()` 通常比逐件 property query 更適合。

---

## 5-15 Validator 與 database constraint 是不同防線

```python
rating = models.PositiveSmallIntegerField(
    validators=[MinValueValidator(1), MaxValueValidator(5)]
)
```

Validator 在 ModelForm／明確 validation 流程中檢查 1–5；一般 `.save()` 不保證自動跑 `full_clean()`。

```python
models.UniqueConstraint(
    fields=["product", "author"],
    name="one_review_per_product",
)
```

UniqueConstraint 由 database 協助防止重複 row。兩者保護的規則與時機不同。

<!--
授課提示：左右表格朗讀一遍；Deck 02 測試章會回收「validator 擋 form、constraint 擋所有寫入路徑」。
-->

---

## 5-16 CartItem：同一商品只保留一個購物車 row

**目前 LearnMart 節錄｜`CartItem.Meta.constraints`**

```python
models.UniqueConstraint(
    fields=["user", "product"],
    name="unique_cart_product",
)
```

同一 user/product 只保留一筆 row；數量放在 `quantity`，而不是重複插入多筆。

- 新增 constraint 需要 migration
- Application 仍要正確處理競態下可能的 `IntegrityError`

---

## 5-16A Review：同一作者對商品只保留一筆

**目前 LearnMart 節錄｜`Review.Meta.constraints`**

```python
models.UniqueConstraint(
    fields=["product", "author"],
    name="one_review_per_product",
)
```

同一 author/product 只保留一筆 review；目前 workflow 使用 `update_or_create()` 更新內容。

這個 database uniqueness 與 rating 1–5 validator 是不同規則、不同防線。

---

## 5-17 `seed_demo`：先讀 `get_or_create()` 回傳值

**目前 LearnMart 節錄｜`marketplace/management/commands/seed_demo.py`**

```python
seller, created = User.objects.get_or_create(
    username="seller",
    defaults={"role": User.Role.SELLER},
)
if created:
    seller.set_password("seller12345")
    seller.save()
```

- `get_or_create()` 回 `(object, created)`
- `created=True` 才進入 password hashing 與 save
- `defaults` 只在建立新 row 時套用

---

## 5-17A 「可重跑」不等於「重設既有資料」

- 新帳號才執行 `set_password()`；role/email defaults 也只在建立時套用
- 同名帳號已存在時，password、role、email 都不會被 reset
- 商品與分類也使用 `get_or_create()`，避免無限複製同名 seed rows

因此它是：

> 重跑不持續新增同名資料的 idempotent-ish seed。

它**不是**把既有 database 還原成固定狀態的 reset command。Fresh database 與已有同名 rows 的結果必須分開描述。

---

## 5-18 Admin 顯示也使用 ORM 關聯

**目前 LearnMart 節錄／重排｜`marketplace/admin.py` 的 `ProductAdmin`**

```python
list_display = (
    "name", "category", "seller", "price", "stock", "is_active",
)
list_filter = ("category", "is_active")
search_fields = ("name", "description")
```

- `list_display`：列表欄位
- `list_filter`：側邊篩選器
- `search_fields`：admin 搜尋欄位

OrderAdmin 另用 `OrderItemInline` 顯示快照明細。Admin configuration 不改變 schema，但會影響管理體驗。

---

## 5-19 訂單快照先理解「為什麼」

OrderItem 同時保留 relation 與購買當下資料：

```python
product = models.ForeignKey(Product, on_delete=models.PROTECT, ...)
product_name = models.CharField(max_length=150)
unit_price = models.DecimalField(max_digits=10, decimal_places=0)
quantity = models.PositiveIntegerField()
```

商品日後改名或漲價，舊訂單仍顯示購買當時名稱與單價。

本 Deck 先理解 schema 決策；建立快照、扣庫存與 transaction 的完整 checkout 放在 Deck 2。

---

## 5-20 ORM 常見錯誤

- 把 QuerySet 當單一 instance：`qs.name`
- 把 instance 當 QuerySet：`product.filter(...)`
- 用 `get()` 查可能多筆的條件
- 建立必要 ForeignKey 時傳入不存在的變數
- 忘記 `.save()`，只改到記憶體
- 在 template loop 中逐筆觸發 relation query
- 把 `aggregate()` 與 `annotate()` 用途混淆
- 認為 model validator 等於 database constraint

先印出 `type(...)`、觀察 query 與回傳形狀。

---

## 第 5 章｜觀念檢核與實作

1. Manager、QuerySet、model instance 各能做什麼？
2. `get()` 找不到與 `filter()` 找不到時有何差異？
3. `select_related` 與 `prefetch_related` 分別適合什麼 relation？
4. 列表顯示每件商品平均評分時，為何要考慮 `annotate()`？
5. Validator 與 database constraint 有何差異？

**實作任務：**在 shell 完成 CRUD、relation traversal、`Q` 查詢，並用 query counter 比較未最佳化與 `select_related()` 的 query 數。

**配套實作手冊：**LearnMart [第 5 章](../workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md#chapter-5)；LearnBoard [類比第 5 章](../workbooks/learnboard_01_django_foundations_and_message_board_workbook.md#chapter-5)

<!--
授課提示：select_related / prefetch_related 選擇題務必全班舉手作答，最能區分理解的單題。
-->
