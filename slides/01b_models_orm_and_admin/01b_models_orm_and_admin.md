---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 01B｜資料模型、ORM 與 Django Admin"
footer: "共通教材｜LearnBoard × LearnMart"
---

<!-- _class: cover -->

# Django 01B
## 資料模型、ORM 與 Django Admin

從欄位與關聯設計，到可操作的資料管理後台

---

## 0-1 本冊在課程中的位置

01 第 1～3 章：環境、Request、Template
→ **01B：資料模型與後台管理**
→ 01 第 5 章檢核，再進入第 6～7 章：商品目錄與留言牆
→ 02：表單、身份驗證、交易 → 03：部署與維運

- 01 第 4～5 章只保留六頁銜接與檢核；資料層完整教學集中於本冊。
- 基準：Django 6.1 官方文件；範例以兩個專案的資料命名。
- 「現有實作」可回查專案；「教學延伸」需自行建立，不能直接假設存在。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/

-->

---

## 0-2 學習成果與課堂安排

| 課次 | 重點與建議時間 | 當堂產出 |
|---|---|---|
| A（90 分） | 主鍵 20、欄位 45、練習 25 | 欄位設計表 |
| B（90 分） | 關聯 45、Meta 25、練習 20 | 關係圖與約束 |
| C（90 分） | ORM 35、migration 20、練習 35 | shell 操作紀錄 |
| D（90 分） | Admin 45、操作 35、檢核 10 | 可搜尋的管理後台 |

第 0 章另排 45～60 分鐘帶做；每次練習都留下可觀察的結果。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/

-->

---

## 0-3 兩個專案提供的真實案例

| 來源 | 抽入本冊的重點 |
|---|---|
| LearnBoard 第 4 章 | Message 文字、作者、時間、排序、migration |
| LearnBoard 的 admin.py | 留言列表、作者搜尋、短內容顯示 |
| LearnMart 第 3～5 章 | 商品圖片、分類與賣家關聯、唯一約束 |
| LearnMart 的 admin.py | 商品管理、訂單 Inline、自訂 UserAdmin |

一對一 Profile、多對多 Tag、索引與部分 Admin 客製為**教學延伸**。
兩個專案的業務 models 未宣告這些 Profile／Tag 關聯。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/
來源：slides/learnboard_01_django_foundations_and_message_board/04_chapter_04.md；slides/learnmart_01_django_foundations_and_data_backed_catalog/03_chapter_03.md、04_chapter_04.md、05_chapter_05.md；learnboard/board/admin.py；learnmart/marketplace/admin.py。
-->

---

## 0-4 先學 Django，再對照專案

本冊不要求先讀完商城程式碼。先建立最小練習專案，理解每個步驟，
再把相同觀念套到 LearnBoard 與 LearnMart。

- **基本必學**：Model、欄位、三種關聯、Meta、CRUD、migration、Admin。
- **教學範例**：用留言、商品說明規則；不是只能處理這兩種資料。
- **進階延伸**：索引設計、through、批次操作、併發與權限客製。
- **閱讀方法**：先問用途，再讀語法，執行後觀察結果，最後解釋原因。

尚未懂的英文術語會在第一次使用時定義；不要先背整份 API 清單。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ ; https://docs.djangoproject.com/en/6.1/ref/contrib/admin/ ; https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

## 0-5 最小練習專案：從空資料夾開始

在獨立練習目錄操作；課程使用 Python 3.14.7、Django 6.1.1。

```bash
uv init django_model_lab --python 3.14.7
cd django_model_lab
uv add "django>=6.1.1,<6.2" pillow
uv run django-admin startproject config .
uv run python manage.py startapp catalog
```

uv 管理 Python 與依賴；project 放全站設定；app 放一組功能。
Pillow 供圖片欄位使用。成功後應看到 manage.py、config/、catalog/。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ ; https://docs.djangoproject.com/en/6.1/ref/contrib/admin/ ; https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

## 0-6 把 app 加入設定

開啟 config/settings.py，在原 INSTALLED_APPS 清單最後加入：

```python
"catalog.apps.CatalogConfig",
```

保留原有 admin、auth、sessions 等項目；先用預設 SQLite 練習。

```bash
uv run python -m django --version
uv run python manage.py check
```

若找不到 catalog，先檢查工作目錄、拼字與 app 是否建立成功。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ ; https://docs.djangoproject.com/en/6.1/ref/contrib/admin/ ; https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

## 0-7 最小 models.py：分類

用以下內容開始 catalog/models.py。下一頁接在本頁後面。

```python
from django.db import models

class Category(models.Model):
    name = models.CharField("分類名稱", max_length=80, unique=True)
    slug = models.SlugField("網址代稱", max_length=80, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "商品分類"
        verbose_name_plural = "商品分類"

    def __str__(self):
        return self.name
```

這是獨立的 catalog 範例；稍後逐項解釋欄位、Meta 與 `__str__`。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ ; https://docs.djangoproject.com/en/6.1/ref/contrib/admin/ ; https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

## 0-8 最小 models.py：商品

接在同一檔案的 Category 後面；不需要另外建立賣家或帳號資料。

```python
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT,
                                 related_name="products")
    name = models.CharField("商品名稱", max_length=150)
    description = models.TextField("商品說明", blank=True)
    price = models.DecimalField("售價", max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField("庫存", default=0)
    image = models.ImageField(upload_to="products/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

先保留最小資料；分類與商品的一對多將在第 3 章展開。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ ; https://docs.djangoproject.com/en/6.1/ref/contrib/admin/ ; https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

## 0-9 建表：migration 是資料結構的版本紀錄

```bash
uv run python manage.py makemigrations catalog
uv run python manage.py migrate
uv run python manage.py showmigrations catalog
```

第一個命令應產生 catalog/migrations/0001_initial.py。
第二個命令把資料結構套進資料庫；第三個應看到 `[X] 0001_initial`。

打開 migration，找出 Category、Product 與自動 id；不需手改檔案。
**成功判準不是「指令有輸出」，而是資料表建立且版本顯示已套用。**

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ ; https://docs.djangoproject.com/en/6.1/ref/contrib/admin/ ; https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

## 0-10 Shell：建立第一筆資料

先執行 `uv run python manage.py shell`，再逐行輸入：

```python
from decimal import Decimal
from catalog.models import Category, Product
category = Category(name="文具", slug="stationery")
category.full_clean()
category.save()
product = Product(category=category, name="筆記本",
                  price=Decimal("50.00"), stock=3)
product.full_clean()
product.save()
print(product.pk, product.name, product.category.name)
```

成功會看到主鍵、筆記本、文具。先在全新資料庫執行一次；重跑的分類會撞 unique。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ ; https://docs.djangoproject.com/en/6.1/ref/contrib/admin/ ; https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

## 0-11 Shell：查詢、修改與刪除

延續上一頁已建立的 product 與 category：

```python
Product.objects.filter(stock__gt=0)
category.products.all()
product.stock = 5
product.save()
product.refresh_from_db()
print(product.stock)  # 5
product.delete()
```

delete 刪除資料庫中的這件練習商品；分類仍存在。
需要重建商品時，重跑商品建立段落，不要重複新增同一分類。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ ; https://docs.djangoproject.com/en/6.1/ref/contrib/admin/ ; https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

## 0-12 最小 Admin：把資料放到後台

在 catalog/admin.py 填入：

```python
from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)
```

```bash
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

登入 [本機 Admin](http://127.0.0.1:8000/admin/)，新增一件商品並選擇「文具」。


<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ ; https://docs.djangoproject.com/en/6.1/ref/contrib/admin/ ; https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

## 0-13 圖片顯示所需的開發設定

在 config/settings.py 加入：

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

MEDIA_ROOT 是本機儲存目錄；MEDIA_URL 是瀏覽器存取的網址前綴。
上傳的圖片屬於 media；網站自己的 CSS、圖示屬於 static，兩者分開。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

## 0-13B 開發環境的 media 路由

在 config/urls.py 保留原 urlpatterns，接上：

```python
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
```

可在 Admin 上傳圖片後開啟檔案連結；此服務方式只供開發環境。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ ; https://docs.djangoproject.com/en/6.1/ref/contrib/admin/ ; https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

## 0-14 切換案例前先確認環境

| 你正在操作哪個專案？ | 匯入 models 的位置 | 是否需要現成資料？ |
|---|---|---|
| 最小練習 django_model_lab | catalog.models | 前面自行建立 |
| LearnBoard | board.models | 依專案初始化流程 |
| LearnMart | marketplace.models | 依專案初始化流程 |

之後標示「現有 LearnMart」的範例，需切到 learnmart 的 manage.py 所在目錄。
語法相同不代表模型欄位完全相同；不要跨專案混用 import 或資料庫。

已定義完整 class 的例子可建模；標示「節錄」的例子用來讀語法，不是完整檔案。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ ; https://docs.djangoproject.com/en/6.1/ref/contrib/admin/ ; https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/ -->

---

<!-- _class: cover -->

# 第 1 章
## Model、主鍵與唯一性

---

## 1-1 Model 的三種對應

| Python 世界 | 資料庫世界 | 商品範例 |
|---|---|---|
| Model class | 資料表 | Product |
| Model instance | 一筆資料 | 某一把鍵盤 |
| 一般 Field | 欄位 | name、price |
| ForeignKey | 外鍵欄位 | category_id |

ORM（物件關聯映射）將 Python 查詢轉為 SQL（資料庫查詢語言），再將結果轉成 Python 物件。
ManyToMany 是例外：它透過中介表保存關係，不是單一欄位。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/

-->

---

## 1-2 一個 Model 的完整骨架

**現有 LearnMart｜Category，省略中文欄位名稱**

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=80, unique=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "商品分類"
        verbose_name_plural = "商品分類"

    def __str__(self):
        return self.name
```

欄位描述資料；Meta 描述模型設定；方法描述物件行為。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/
來源：learnmart/marketplace/models.py::Category。
-->

---

## 1-2B `__str__`：物件顯示的文字

放在 Category 類別內的方法：

```python
def __str__(self):
    return self.name
```

- self 是目前這筆物件；return 必須回傳字串。
- print(category)、Admin 關聯選單會使用這段顯示文字。
- 沒定義時常只看到 Category object (1)，不容易辨認資料。
- 這是 Python 方法，不會額外建立資料庫欄位。

不要在這裡任意改資料；若讀取其他關聯，也可能增加查詢。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/ref/models/instances/#str -->

---

## 1-2C Model 方法與商品詳情網址

```python
@property
def average_rating(self):
    result = self.reviews.aggregate(avg=models.Avg("rating"))["avg"]
    return round(result, 1) if result else None

def get_absolute_url(self):
    return reverse("marketplace:product-detail", kwargs={"pk": self.pk})
```

- `@property`：以 attribute 方式讀取計算值
- `get_absolute_url()`：定義商品標準詳情網址

**目前 LearnMart 實作：** 商品 template 以它建立連結；`ProductCreateView`／`ProductUpdateView` 沒有另設 `success_url`，成功儲存後也已透過它決定 redirect。

---

## 1-3 Primary key：資料的穩定身分

同名商品可能有很多筆，名稱不能可靠地辨識「是哪一筆」。

```python
product = Product.objects.get(pk=17)
print(product.pk, product.id)
```

- 兩個專案使用自動 `BigAutoField` 主鍵；不必手動宣告 `id`。
- `pk` 是主鍵的通用別名；主鍵不叫 id 時仍能用 pk。
- 主鍵用來定位與建立關聯，不代表排序名次，也不保證連號。
- 不要以「目前筆數 + 1」自行產生主鍵。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
來源：兩個專案 config/settings.py 的 DEFAULT_AUTO_FIELD。
-->

---

## 1-4 自訂主鍵與 UUID

**教學延伸｜一般情況先保留自動 id**

```python
import uuid
from django.db import models

class Ticket(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False,
    )
    title = models.CharField(max_length=120)
```

`primary_key=True` 隱含唯一且不可為 NULL；設定後不再另加自動 id。
`uuid.uuid4` 是 callable，不加括號；每次建立才產生新值。
不要把可變動的名稱當主鍵，也不要靠 UUID 取代權限檢查。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/

-->

---

## 1-5 Primary key、unique、複合唯一

| 設計 | 回答的問題 | 例子 |
|---|---|---|
| 主鍵 | 這一列是誰？ | Category.id |
| `unique=True` | 此欄位值能否重複？ | Category.slug |
| `UniqueConstraint` | 這組欄位能否重複？ | CartItem(user, product) |

同一張表可以有多個 unique 欄位；它們不會都變成主鍵。
**兩個欄位各自 unique，不等於兩個欄位組合 unique。**

進階：複合主鍵另有 `CompositePrimaryKey`，不是在多個欄位都寫
`primary_key=True`；本課沿用單欄位主鍵＋複合唯一約束。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
https://docs.djangoproject.com/en/6.1/ref/models/constraints/

-->

---

## 1-6 用資料列理解複合唯一

| user_id | product_id | quantity | 是否可同時存在？ |
|---|---|---|---|
| 1 | 10 | 2 | 可以 |
| 1 | 11 | 1 | 可以：同買家不同商品 |
| 2 | 10 | 1 | 可以：不同買家同商品 |
| 1 | 10 | 3 | 不可以：與第一列同一組鍵 |

現有 CartItem 保留一列，修改 quantity；不是多插入一列。
稍後在 `Meta.constraints` 寫出這條規則。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/constraints/
來源：LearnMart 原第 5 章；learnmart/marketplace/models.py::CartItem。
-->

---

<!-- _class: cover -->

# 第 2 章
## 欄位型別與參數：從需求做選擇

---

## 2-1 設計欄位先問五個問題

1. 這是文字、數字、日期，還是另一個物件？
2. 沒填時代表什麼：空字串、未知，還是預設值？
3. 值可否重複？需要哪種範圍與格式限制？
4. 誰可以輸入或修改：使用者、管理員，還是程式？
5. 哪些規則需要資料庫也強制保護？

練習：電話看起來都是數字，為何仍用 `CharField`？
要保留前導 0、加號與分機，而且不拿來做加減乘除。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/

-->

---

## 2-2 常用欄位選擇表

| 資料需求 | Django 欄位 | 例子 |
|---|---|---|
| 短文字／長文字 | CharField／TextField | 名稱／留言 |
| 整數／精確小數 | IntegerField／DecimalField | 庫存／金額 |
| 測量近似值／真假 | FloatField／BooleanField | 感測值／上架 |
| 日期／時間／日期時間 | DateField／TimeField／DateTimeField | 生日／開門／下單 |
| 網址代稱／圖片 | SlugField／ImageField | tech／商品圖 |

先看資料意義，再決定型別；不要全部存成字串。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/

-->

---

## 2-3 讀懂一個欄位宣告

**教學延伸｜修改 Product.name 的說明文字**

```python
name = models.CharField(
    "商品名稱", max_length=150,
    help_text="請填可辨識的名稱，不超過 150 字元。",
)
```

- `name`：Python 與 ORM 使用的名稱。
- `CharField`：資料型別；`max_length`：長度設定。
- 第一個參數是 `verbose_name`：表單／Admin 的人類可讀名稱。
- `help_text`：輸入提示；它不會取代 validator。

ForeignKey 第一個參數是關聯目標，中文標籤改用 `verbose_name=`。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/

-->

---

## 2-4 CharField 與 TextField

**抽入 LearnBoard 留言與 LearnMart 商品案例**

```python
# Product
name = models.CharField("商品名稱", max_length=150)
description = models.TextField("商品說明")
# Message
content = models.TextField("留言內容", max_length=500)
```

短文字通常用 CharField；多行內容通常用 TextField。
TextField 的 max_length 會影響產生的表單，但不等於資料庫長度限制，
也不能假設直接呼叫 Model.full_clean() 就會替 TextField 擋住超長文字。

要在 model 驗證長文上限，可明確加 `MaxLengthValidator(500)`。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
來源：learnboard/board/models.py、learnmart/marketplace/models.py。
-->

---

## 2-5 blank 與 null：兩個不同層次

| 參數 | 管理的層次 | 問題 |
|---|---|---|
| `blank=True` | Django 表單／模型驗證 | 可以不輸入嗎？ |
| `null=True` | 資料庫 | 可以存 SQL NULL 嗎？ |

```python
note = models.CharField(max_length=100, blank=True)
shipped_at = models.DateTimeField(null=True, blank=True)
```

文字通常用空字串表示未填；未出貨的時間則用 NULL。
`blank=False` 不是資料庫「禁止空字串」的約束。
可選又唯一的文字欄位是特例：多個空值需另思考 NULL 與唯一性。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/

-->

---

## 2-6 default、editable 與驗證

```python
stock = models.PositiveIntegerField(default=0)
```

- `default` 在建立物件未提供值時使用，不是自動修正非法輸入。
- callable 預設值寫函式本身；可變物件如 JSON 預設值用 `dict`。
- `editable=False` 讓欄位不出現在自動表單；程式仍可修改資料。
- `db_default` 是資料庫層預設；不要把普通 `default` 當成 SQL DEFAULT。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/ref/models/fields/ -->

---

## 2-6B full_clean 與 save 分開理解

```python
product.full_clean()  # 明確做模型驗證
product.save()        # 儲存；本身不自動呼叫 full_clean()
```

驗證器（validator）判斷值是否符合規則；失敗會產生 ValidationError。
模型驗證還會檢查唯一性與約束；完整流程在第 4 章展開。

練習：如果只用 save，價格小數位數是否一定會先得到清楚的輸入錯誤？
不能保證。輸入驗證與資料庫寫入是不同步驟。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
https://docs.djangoproject.com/en/6.1/ref/models/instances/

-->

---

## 2-7 整數欄位：0 算不算合法？

```python
stock = models.PositiveIntegerField(default=0)
quantity = models.PositiveIntegerField(
    default=1, validators=[MinValueValidator(1)],
)
```

第一行是商品庫存；後三行是 CartItem 數量，需先匯入 validator。

- IntegerField 可存正負整數；PositiveIntegerField 包含 **0**。
- 「非負」與「至少 1」不同，因此購物數量另加最小值驗證。
- Small／Big 版本調整整數範圍；不要靠名稱猜資料庫容量。
- validator（驗證器）提供輸入錯誤訊息；DB 防線另看 CheckConstraint。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
https://docs.djangoproject.com/en/6.1/ref/models/constraints/
來源：learnmart/marketplace/models.py；from django.core.validators import MinValueValidator。
-->

---

## 2-8 DecimalField 與 FloatField

```python
from decimal import Decimal

price = models.DecimalField(max_digits=8, decimal_places=2)
# Python 金額使用 Decimal("199.90")
```

8 是總位數，2 是小數位數，因此整數部分最多 6 位。
FloatField 是二進位近似值，適合能接受誤差的測量資料。

**現有 LearnMart** 使用 `max_digits=10, decimal_places=0`，不含小數。
Decimal 避免 Python 端浮點誤差；SQLite 的小數儲存／運算仍有限制，
不能把欄位宣告等同於所有資料庫都保證精度與範圍。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/

-->

---

## 2-9 Boolean 與 choices

**現有 LearnMart｜User 的角色宣告，節錄**

```python
class Role(models.TextChoices):
    BUYER = "buyer", "買家"
    SELLER = "seller", "賣家"

role = models.CharField(
    max_length=10, choices=Role.choices, default=Role.BUYER,
)
```

真假狀態用 BooleanField；多種有限狀態用 choices。
資料存 `seller`；`user.get_role_display()` 得到「賣家」。
choices 是驗證與選單設定；不自動成為資料庫 CHECK 或狀態轉移流程。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
來源：learnmart/marketplace/models.py::User，程式碼位於 User 類別內。
-->

---

## 2-10 日期、時間、日期時間

| 型別 | Python 值 | 適合需求 |
|---|---|---|
| DateField | date | 生日、截止日期 |
| TimeField | time | 每日開門時間 |
| DateTimeField | datetime | 留言建立、出貨時刻 |
| DurationField | timedelta | 持續多久 |

生日不需要時分秒；交易發生的時刻通常需要日期與時間。
別把格式化的「2026/09/19 08:00」存成 CharField。
格式留給顯示層，資料保留可查詢與比較的型別。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/

-->

---

## 2-11 三種時間設定怎麼選？

| 設定 | 行為 | 適合欄位 |
|---|---|---|
| `auto_now_add=True` | 首次 save 自動填入 | 建立時間 |
| `auto_now=True` | save 寫入該欄位時更新 | 修改時間 |
| `default=timezone.now` | 建立時提供預設，可自行指定 | 發佈／事件時間 |

```python
from django.utils import timezone
published_at = models.DateTimeField(default=timezone.now)
```

同一欄位不要混用這三種選項。auto_now 與 auto_now_add 會設為不可編輯。
`QuerySet.update()` 不觸發 auto_now；`update_fields` 也要包含時間欄位。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
https://docs.djangoproject.com/en/6.1/topics/i18n/timezones/

-->

---

## 2-12 時區與未發生的事件

**現有 LearnMart｜尚未出貨時不應捏造出貨時間**

```python
shipped_at = models.DateTimeField(null=True, blank=True)
```

- 啟用 `USE_TZ` 時，使用 `timezone.now()` 取得 aware datetime。
- 資料儲存與畫面顯示時區分開處理；不要自行加 8 小時再存回去。
- `TIME_ZONE` 影響預設顯示／解讀；不是字串格式設定。
- 未出貨用 `None`；查詢用 `shipped_at__isnull=True`。

練習：建立時間、生日、未出貨時間，哪個需要 null？為什麼？

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/i18n/timezones/
https://docs.djangoproject.com/en/6.1/ref/models/fields/

-->

---

## 2-13 SlugField：可讀的網址代稱

**現有 LearnMart｜Category**

```python
slug = models.SlugField("網址代稱", max_length=80, unique=True)
```

- 例如 `tech`、`daily-tools`；預設接受 ASCII 字母、數字、底線與連字號。
- `allow_unicode=True` 才允許 Unicode 字母，例如中文。
- SlugField 不會自動由 name 產生內容，也不預設唯一。
- 目前商城以 query string 傳分類 slug；商品詳情仍使用 pk。

「有 slug 欄位」不代表 URLconf 已經使用它。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
來源：learnmart/marketplace/models.py::Category；現有篩選使用 ?category=。
-->

---

## 2-14 Slug 生成與重複值

**教學延伸**

```python
from django.utils.text import slugify
slugify("Daily Tools")       # daily-tools
slugify("生活用品", allow_unicode=True)
```

slugify 只做字串轉換；不同名稱可能得到相同 slug。
若網址要求唯一，需設計衝突策略，並以資料庫唯一約束守住競態。

Admin 可用 prepopulated_fields 輔助輸入，但不是所有寫入入口的生成器。
網址若採內建 `<slug:slug>` converter，不能直接假設它接受中文。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 2-15 圖片：資料庫存路徑，storage 存檔案

**抽入 LearnMart 商品圖片案例**

```python
image = models.ImageField(
    "商品圖片", upload_to="products/%Y/%m/", blank=True,
)
```

- 欄位保存檔名／路徑參照；實際內容交給 storage。
- `upload_to` 相對於 storage，不是完整的公開網址。
- `.name` 是儲存名稱；`.url` 是存取網址；`.path` 不保證遠端 storage 支援。
- ImageField 需要 Pillow；驗證圖片不等於所有上傳安全問題都已解決。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/
抽入來源：LearnMart 01 原第 4 章，Product 圖片與歷史的專屬規則。
-->

---

## 2-16 圖片從上傳到顯示

```django
{% if product.image %}
  <img src="{{ product.image.url }}" alt="{{ product.name }}">
{% else %}
  <p>尚無商品圖片</p>
{% endif %}
```

- 先檢查有沒有檔案，再讀 url；空圖片直接讀 url 會出錯。
- 開發環境分清 `MEDIA_ROOT` 與 `MEDIA_URL`。
- 自訂上傳表單需要 multipart 與 request.FILES，接續 02 表單章。
- 備份需包含 DB 與 media；刪除 model 不會自動清除 storage 的檔案。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/
抽入來源：LearnMart 01 原第 3 章，商品卡與圖片狀態；部署接續 03。
-->

---

## 2-17 欄位設計練習（20 分鐘）

請替「校內二手物品」填一份欄位設計表：
名稱、說明、價格、數量、上架狀態、網址代稱、圖片、建立時間、成交時間。

每個欄位寫出：**型別、必要參數、可否空白、預設值與理由**。

驗收：
- 說明價格不用 float，數量是否允許 0。
- 說明成交時間為何不能一律用 auto_now_add。
- 指出哪個是 primary key，slug 的 unique 又保護什麼。
- 同桌交換，找出一項「只在表單驗證，DB 未必保證」的規則。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/

-->

---

<!-- _class: cover -->

# 第 3 章
## 一對一、一對多、多對多

---

## 3-1 關聯先看兩個方向的數量

| 需求 | 正向 | 反向 | 選擇 |
|---|---|---|---|
| 留言與作者 | 一則留言至多一位作者 | 一位作者多則留言 | ForeignKey |
| 帳號與個人檔案 | 一份檔案一個帳號 | 一個帳號至多一份檔案 | OneToOneField |
| 商品與標籤 | 一件商品多個標籤 | 一個標籤多件商品 | ManyToManyField |

「一對多」與「多對一」是同一條關係的兩個方向。
外鍵放在「多」的一方；是否允許沒有對象，再由 null 等設定決定。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/

-->

---

## 3-2 LearnBoard：留言指向作者

**抽入 LearnBoard 第 4 章｜Message，節錄**

```python
from django.conf import settings
from django.db import models

class Message(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True, related_name="messages",
    )
```

一則留言可沒有作者；刪除帳號後，留言保留、author 變成 NULL。
關聯 User 用 AUTH_USER_MODEL，避免綁死 Django 的預設 User。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
來源：learnboard/board/models.py；現有欄位另有 verbose_name="作者"。
-->

---

## 3-3 外鍵值與關聯物件

```python
message.author_id          # 儲存的主鍵值，或 None
message.author             # User instance，或 None
user.messages.all()        # 反向 RelatedManager 產生 QuerySet
user.messages.filter(content__icontains="Django")
```

讀 author_id 通常不需另外載入 User；讀 author 可能查資料庫。
related_name 決定反向入口名稱，不會把資料庫欄位改名為 messages。

沒有設定 related_name 時，預設反向存取常是 `message_set`；
反向查詢名稱通常是 `message`。本課採明確命名，降低混淆。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
https://docs.djangoproject.com/en/6.1/topics/db/queries/

-->

---

## 3-4 on_delete 與刪除方向

| 策略 | 刪除被參照的對象時 | 專案例子 |
|---|---|---|
| CASCADE | 連帶刪除參照列 | 刪 Order → OrderItem |
| PROTECT | 有參照就拒絕刪除 | Category ← Product |
| SET_NULL | 保留列並清空 FK | User ← Message |

SET_NULL 需搭配 null=True。刪留言不會反過來刪作者。
商品同時被訂單保護時，即使 seller 的 FK 用 CASCADE，也可能刪不成。

on_delete 是 Django 刪除收集行為，不是宣告 SQL 的 ON DELETE 子句。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
抽入 LearnMart 原第 4 章的整張關聯圖刪除規則；並列 LearnBoard SET_NULL。
-->

---

## 3-5 一對一：帳號的額外資料

**教學延伸｜新 app practice 的 models.py，兩個專案尚未加入**

```python
from django.conf import settings
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(blank=True)
```

Profile 有自己的自動 id；user_id 另有唯一性。
一個帳號至多一份 Profile；不代表建立帳號時會自動建立 Profile。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/

-->

---

## 3-6 一對一的正反向都是單一物件

**教學延伸｜完成 Profile migration 後**

```python
profile, created = Profile.objects.get_or_create(user=user)
profile.user              # User instance
user.profile              # Profile instance，不是 .all()
```

沒有 Profile 時，讀反向關聯會拋 RelatedObjectDoesNotExist，
不是回空 QuerySet，也不是自動回 None。

ForeignKey(unique=True) 在資料唯一性上類似一對一，
但 OneToOneField 的反向 API 更直接表達「單一物件」。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
https://docs.djangoproject.com/en/6.1/topics/db/queries/

-->

---

## 3-7 多對多：商品可以貼多個標籤

**教學延伸｜建立 practice app，指向現有 Product**

```python
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)
    products = models.ManyToManyField(
        "marketplace.Product", related_name="tags", blank=True,
    )
```

關聯只需宣告在其中一邊；另一邊會有反向入口。
Django 建立中介表（專門保存兩筆資料之間的關係），保存 tag_id 與 product_id，預設防止同一組重複。
blank=True 允許不選標籤；ManyToMany 的 null 設定沒有意義。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/fields/
https://docs.djangoproject.com/en/6.1/topics/db/examples/many_to_many/

-->

---

## 3-8 多對多的資料其實在第三張表

| 商品表 id／name | 中介表 product_id／tag_id | 標籤表 id／name |
|---|---|---|
| 10／鍵盤 | 10／1 | 1／二手 |
| 11／滑鼠 | 10／2 | 2／可議價 |
| — | 11／1 | — |

鍵盤有兩個標籤；「二手」同時貼在鍵盤與滑鼠。
不要把標籤存成 `"二手,可議價"`，否則難以可靠地關聯、查詢與去重。

想一想：移除 10／1 這筆關係，需要刪掉「二手」標籤本身嗎？

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/examples/many_to_many/

-->

---

## 3-9 add、remove、set、clear

**教學延伸｜Product 與 Tag 都必須已儲存**

```python
tag, _ = Tag.objects.get_or_create(name="二手")
product.tags.add(tag)
product.tags.all()
tag.products.all()
product.tags.remove(tag)
product.tags.set([tag])
product.tags.clear()
```

add／remove 變更關係；set 以指定集合取代；clear 移除全部關係。
這些方法會寫入中介表，不用再呼叫 product.save()。
remove／clear 不會刪除商品或標籤本身。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/examples/many_to_many/

-->

---

## 3-10 進階｜through：關係本身還有資料

**教學延伸｜若「貼標籤時間」也是資料，改用明確中介模型**

```python
class ProductTag(models.Model):
    product = models.ForeignKey(
        "marketplace.Product", on_delete=models.CASCADE)
    tag = models.ForeignKey("Tag", on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["product", "tag"], name="practice_product_tag",
        )]
```

在 Tag.products 宣告 `through="ProductTag"`；新增關係亦可直接建立 ProductTag。
這是另一版 schema，別直接改已有資料的 M2M 而忽略資料遷移。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/
https://docs.djangoproject.com/en/6.1/ref/models/constraints/

-->

---

## 3-11 CartItem 與 OrderItem 的建模意義

**抽入 LearnMart 商城資料規則**

- CartItem 連接 User 與 Product，還保存 quantity。
- OrderItem 連接 Order 與 Product，保存商品名與單價快照。
- 兩者都有中介資料的意義，但目前沒有宣告為 ManyToMany 的 through。
- 舊訂單不能只讀目前 Product.price，否則改價會改變歷史呈現。

關聯不是只畫線；要問「這條關係還要保存什麼歷史事實？」

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/
來源：LearnMart 01 原第 5 章；learnmart/marketplace/models.py::CartItem、OrderItem。
-->

---

## 3-11B 訂單快照：保留購買當下的資料

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

## 3-12 關聯練習（20 分鐘）

畫出 User、Profile、Message、Product、Tag 的關係。

每條線標出：數量、FK 所在一方、可否為空、刪除策略與反向名稱。

驗收題：
1. 讀 user.profile 為何不用 all()？不存在時會怎樣？
2. 同一個 user 能有兩則留言嗎？兩份 Profile 呢？
3. 移除一個商品的標籤，為何不應刪除 Tag？
4. 商品單價快照要放在 Product，還是 OrderItem？

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/

-->

---

<!-- _class: cover -->

# 第 4 章
## Meta、資料驗證與 migration

---

## 4-1 Model、表單與 Admin 的設定位置

| 位置 | 管理的事 | 例子 |
|---|---|---|
| Model 欄位 | 單欄位型別與規則 | max_length、blank |
| Model.Meta | 模型整體設定 | ordering、constraints |
| ModelForm.Meta | 表單對應模型與可編輯欄位 | model、fields |
| ModelAdmin | 後台列表與編輯介面 | list_display、search_fields |

Model.Meta 不放 fields 白名單；ModelForm.Meta 不負責資料庫索引。
它們名字相似，但屬於不同 class，也由不同元件解讀。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/options/
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 4-2 ordering 與顯示名稱

**現有 Category.Meta**

```python
class Meta:
    verbose_name = "商品分類"
    verbose_name_plural = "商品分類"
    ordering = ["name"]
```

ordering 是預設查詢排序；`order_by("-name")` 可覆蓋它。
排序欄位值若相同，需額外唯一鍵才能確保穩定次序。

教學延伸：商品可用 `["-created_at", "-pk"]`，時間相同時再用 pk 排序。
中文常把單複數名稱設成一樣；這不會改變資料表名稱。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/options/

-->

---

## 4-3 進階｜db_table 與 indexes

**教學延伸｜Product.Meta 的設計候選，不是現有設定**

```python
class Meta:
    db_table = "marketplace_product"
    indexes = [models.Index(
        fields=["is_active", "-created_at"],
        name="product_active_created_idx",
    )]
```

預設表名已是 app_label＋model 名，通常不用另設 db_table。
索引協助特定查詢，但增加儲存與寫入成本；先量測，不要每欄都加。
索引不保證值唯一；唯一性另用 unique 或 UniqueConstraint。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/options/

-->

---

## 4-4 完整的 Meta.constraints

**現有 LearnMart｜CartItem，關聯欄位省略**

```python
class CartItem(models.Model):
    # user、product、quantity 等欄位在此宣告

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_cart_product",
            ),
        ]
```

name 是約束名稱；fields 是一起判斷的欄位組合。
新增前先清理既有重複資料；建立 migration 不會替你決定保留哪一筆。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/constraints/
來源：learnmart/marketplace/models.py::CartItem，將原第 5 章片段補完整 nesting。
-->

---

## 4-4B Review 評價唯一約束

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

## 4-5 CheckConstraint：範圍與跨欄位規則

**教學延伸｜可加入 CartItem.Meta.constraints**

```python
models.CheckConstraint(
    condition=models.Q(quantity__gte=1),
    name="cart_quantity_at_least_one",
)
```

- validator 幫使用者得到輸入錯誤訊息。
- CheckConstraint 讓資料庫拒絕不符合條件的寫入。
- 這與 user＋product 的「不可重複」是兩條不同規則。
- nullable 欄位還需明確思考 NULL 的邏輯與資料庫差異。

目前 CartItem 有 MinValueValidator(1)，尚未加入本頁的 CHECK。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/constraints/

-->

---

## 4-6 驗證不是只有一個入口

| 入口 | 會發生什麼？ |
|---|---|
| Admin／ModelForm.is_valid() | 做表單與相應的模型驗證；排除欄位有邊界 |
| instance.full_clean() | 欄位、clean、唯一性、約束驗證 |
| instance.save()／objects.create() | 不自動呼叫完整 full_clean |
| QuerySet.update() | 直接 SQL 更新，不逐筆 save |
| 資料庫約束 | 最後擋住受約束的非法寫入 |

驗證通過到寫入之間仍可能有人先寫入；unique 的競態需處理 IntegrityError。
不能只做 exists() 檢查就宣稱不會重複。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/models/instances/
https://docs.djangoproject.com/en/6.1/ref/models/constraints/
https://docs.djangoproject.com/en/6.1/topics/db/queries/

-->

---

## 4-6B 專案初始化前的 User 決定

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

## 4-7 Model、migration 與資料表

```text
修改 models.py
       ↓ makemigrations
產生 migration operations
       ↓ migrate
更新資料庫 schema
```

- makemigrations 比較模型與 migration 狀態，不是比較實際 DB 的所有差異。
- migrate 套用版本紀錄；不是每次把所有表重建。
- 改 Meta 也可能產生 migration；不一定都對應實際 SQL 變更。
- Admin 的列表設定不屬於 schema，通常不需 migration。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/

-->

---

## 4-7B 取得專案與修改模型的操作差異

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

## 4-7C migration 訊息與狀態檢查

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

## 4-8 新增欄位的操作與證據

**教學延伸｜在 LearnMart 練習分支新增 is_featured**

```python
is_featured = models.BooleanField("精選", default=False)
```

先修改 models.py，再用下一頁命令產生並閱讀 migration。
現有資料也必須有合理預設值；本例用 False 表示尚未設為精選。

<!-- 官方依據：https://docs.djangoproject.com/en/6.1/topics/db/models/ -->

---

## 4-8B 產生、檢查並套用 migration

```bash
uv run python manage.py makemigrations marketplace
uv run python manage.py sqlmigrate marketplace 0002
uv run python manage.py migrate
uv run python manage.py makemigrations --check
```

0002 請換成實際產生的 migration 編號；先讀 operations 與 SQL 再套用。
驗收：現有商品有合理值，Admin 可顯示，沒有遺漏的 migration。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/

-->

---

## 4-9 既有資料讓變更更困難

新增必填欄位時，舊資料要填什麼？新增 unique 時，舊值是否重複？

1. 先定義舊資料如何補值，不要隨意接受同一個假值。
2. 必要時先允許空值，另做資料遷移補齊。
3. 確認符合規則，再加 NOT NULL／unique／constraint。
4. 評估鎖表、備份與回復方式，接續 03 部署章。

配套：保留 LearnBoard 的 0002_message_author.py，觀察後加作者欄位。
不要刪掉既有 migration 來掩蓋問題。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/
抽入 LearnBoard 原第 4 章的 migration 歷史；後續見 03_deployment_and_operations/05_migrations_backup_recovery.md。
-->

---

<!-- _class: cover -->

# 第 5 章
## ORM 操作：先看回傳值，再組查詢

---

## 5-1 Manager、QuerySet、instance

| 表達式 | 得到什麼 | 接著可以做什麼 |
|---|---|---|
| Product.objects | Manager | 建立查詢 |
| Product.objects.filter(...) | QuerySet | 再篩選、排序、迭代 |
| Product.objects.get(...) | Product instance | 讀欄位、save、delete |
| Product.objects.values(...) | 字典結果的 QuerySet | 讀字典鍵 |

get 找不到或多筆會拋例外；filter 找不到仍是空 QuerySet。
別對 instance 呼叫 filter，也別直接讀整個 QuerySet 的 name。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/

-->

---

## 5-2 建立與修改：記憶體不等於已存檔

**練習資料｜在 LearnMart shell 執行**

```python
from marketplace.models import Category
category = Category(name="ORM 練習分類", slug="orm-lab")
category.full_clean()
category.save()
category.name = "ORM 練習分類（已更新）"
category.save(update_fields=["name"])
category.refresh_from_db()
```

第二次重跑前先處理既有 orm-lab 分類，否則 unique 驗證會失敗。
objects.create() 可直接建立並儲存，但不會自動替你 full_clean()。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/
https://docs.djangoproject.com/en/6.1/ref/models/instances/

-->

---

## 5-2B 建立商品前先取得必要關聯

**LearnMart shell｜先確認 seed_demo 已建立 seller 帳號與 tech 分類。**

```python
from marketplace.models import Category, Product, User

seller = User.objects.get(username="seller")
category = Category.objects.get(slug="tech")

product = Product.objects.create(
    seller=seller, category=category,
    name="教學鍵盤", description="練習 ORM",
    price=990, stock=5,
)
```

`.create()` 會立即 INSERT 並回傳已儲存 instance；成功後 `product.pk` 有值。

注意：一般 `.create()`／`.save()` 不等同自動呼叫完整 `full_clean()`。

---

## 5-2C 刪除單筆練習商品

接續上一頁，只操作剛建立且尚未被訂單引用的商品。

```python
practice_pk = product.pk
product.delete()
Product.objects.filter(pk=practice_pk).exists()  # False
```

- `.delete()` 是執行刪除的動作；`on_delete` 決定關聯對象被刪除時的規則。
- 刪商品不會反過來刪除它的分類或賣家。
- 若商品已被 OrderItem 保護，刪除會受阻；回查 3-4 的關聯圖。

驗收：查不到練習商品，原分類與賣家仍存在。批次刪除差異見 5-10。

---

## 5-3 篩選、排除、排序與切片

```python
from marketplace.models import Product
qs = (Product.objects
      .filter(is_active=True, stock__gt=0)
      .exclude(category__slug="archived")
      .order_by("price", "pk"))
first_ten = qs[:10]
```

同一 filter 的多個條件預設 AND；exclude 排除符合條件者。
先排序再取前 10 筆，才有明確的「前」。
一般切片形成 LIMIT／OFFSET；不要在切片之後繼續 filter 或重排。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/

-->

---

## 5-4 常用 lookup 與 Q

| 寫法 | 意義 |
|---|---|
| name__icontains="鍵盤" | 包含字串，大小寫細節依 backend |
| price__gte=100、price__lte=1000 | 含端點的範圍條件 |
| category__slug__in=["tech", "books"] | 屬於候選值集合 |
| shipped_at__isnull=True | 沒有出貨時間 |

```python
from django.db.models import Q
Product.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
```

q 是搜尋字串；Q 用 `|` 表達 OR，不是 Python 的 or。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/

-->

---

## 5-5 values 與 values_list 的結果

```python
Product.objects.values("id", "name")
# 每列像 {"id": 17, "name": "鍵盤"}
Product.objects.values_list("id", "name")
# 每列像 (17, "鍵盤")
Product.objects.values_list("name", flat=True)
# 每列像 "鍵盤"
```

這些仍是 QuerySet，但每筆結果不是 Product instance。
flat=True 只適用單一欄位；字典與 tuple 不能呼叫 model.save()。
需要匯出欄位時很好用；需要物件行為時保留 model instances。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/

-->

---

## 5-6 關聯查詢與 distinct

**教學延伸｜完成 Tag 模型後**

```python
Product.objects.filter(tags__name__in=["二手", "可議價"]).distinct()
```

同一商品可能符合兩個標籤，中介表 JOIN 因此產生重複商品列。
distinct 用來去重；先理解 JOIN 為何增加列數，再決定是否需要它。

現有案例：`Message.objects.filter(author__username="amy")`。
雙底線沿關聯走到欄位；它不是 Python 屬性存取的小數點。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/
https://docs.djangoproject.com/en/6.1/topics/db/examples/many_to_many/

-->

---

## 5-7 Lazy evaluation 與查詢成本

```python
qs = Product.objects.filter(is_active=True)  # 組查詢
print(qs.query)                             # 觀察 SQL
rows = list(qs)                             # 執行並取資料
```

- iteration、list、len、bool 等會觸發評估；QuerySet 的 repr 也可能查詢。
- 只問有沒有，用 exists；只要數量，用 count。
- 馬上還要遍歷所有結果時，先 exists 再遍歷可能多查一次。
- QuerySet 有結果快取，但新組出的查詢不能假設共享舊快取。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/

-->

---

## 5-7B N+1：列表逐筆讀取關聯的成本

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

## 5-8 關聯預載取決於資料形狀

**抽入 LearnMart 原第 5 章的列表／詳情案例**

```python
Product.objects.filter(is_active=True).select_related("category", "seller")
Product.objects.prefetch_related("reviews__author")
```

JOIN 是把關聯資料表連接查詢；select_related 用 JOIN 載入單值關聯，例如 FK／一對一。
prefetch_related 分批查詢再組合，適合反向 FK／多對多。

Admin 列表也會讀關聯；list_select_related 可處理相同問題。
先觀察實際 query 數，不要把所有 relation 都一律預載。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/
來源：slides/learnmart_01_django_foundations_and_data_backed_catalog/05_chapter_05.md。
-->

---

## 5-9 aggregate 與 annotate

```python
from django.db.models import Avg, Count
Product.objects.aggregate(avg_price=Avg("price"))
# 整份集合 → 一個摘要字典
Product.objects.annotate(review_count=Count("reviews"))
# 每個 Product → 多一個 review_count attribute
```

集合摘要與每列計算不同；計算 attribute 不是新增資料庫欄位。
Product.average_rating 是現有 property，逐件呼叫可能逐件查詢。
多個關聯一起聚合時要注意 JOIN 造成重複計數，需驗證結果。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/

-->

---

## 5-9B 商品平均評分的查詢行為

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

## 5-10 進階｜更新、刪除與原子運算

**教學延伸｜以一筆練習商品操作**

```python
from django.db.models import F
changed = Product.objects.filter(pk=product.pk, stock__gte=1).update(
    stock=F("stock") - 1,
)
```

條件與扣減在同一個 SQL UPDATE；changed 為 0 表示沒符合條件的資料。
這不等於完整結帳交易；多表一致性仍需 02 的 transaction 設計。
update 不逐筆呼叫 save；批次 delete 也不呼叫每個 model 的 delete 方法。
刪除前確認篩選範圍與關聯保護；只在練習資料上操作。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/

-->

---

## 5-11 get_or_create 與 update_or_create

**現有 LearnMart｜CartItem 與 Review 的重複規則**

- get_or_create 回傳 `(instance, created)`；defaults 用於新建。
- update_or_create 找到就更新，沒找到才建立。
- 查詢鍵需與資料庫唯一約束配合，不能只靠方法名稱避免競態。

```python
review, created = Review.objects.update_or_create(
    product=product, author=user,
    defaults={"rating": 5, "comment": "操作清楚"},
)
```

product、user 要先取得；評分是否合法仍需驗證。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/
來源：LearnMart 原第 5 章的 Review 唯一規則與現有 review workflow。
-->

---

## 5-11B seed_demo 重跑會發生什麼？

**LearnMart 現有初始化指令｜節錄帳號建立流程**

```python
seller, created = User.objects.get_or_create(
    username="seller", defaults={"role": User.Role.SELLER},
)
if created:
    seller.set_password("seller12345")
    seller.save()
```

- 帳號已存在時，defaults 不會重設 role，密碼也不會重設。
- 分類與商品也用 get_or_create 避免反覆新增相同查詢鍵的資料。
- 重跑能補缺少的資料，不能把既有資料庫還原成固定初始狀態。

<!-- 來源：learnmart/marketplace/management/commands/seed_demo.py；移自 01 原 5-17。 -->

---

## 5-12 ORM 操作練習（25 分鐘）

先用 LearnMart 練習資料，在 shell 完成：

1. 查詢有庫存商品，依價格與 pk 排序，取前 5 筆。
2. 只取名稱與價格，說明回傳的是物件、字典還是 tuple。
3. 查特定分類的商品，列出賣家帳號，比較預載前後的 query 數。
4. 依 5-2B～5-2C 建立、修改並刪除練習商品，確認資料庫結果。

驗收：交查詢程式、實際結果與回傳型別；空資料時要能說明原因。
多對多加分題：查兩個標籤並解釋 distinct 的用途。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/queries/

-->

---

<!-- _class: cover -->

# 第 6 章
## Django Admin：可操作的資料管理後台

---

## 6-1 Admin 在系統中的角色

Admin 根據 Model 與設定產生內部管理介面。

- 可以先管理分類、商品與留言，不必先完成每張自訂表單。
- 它讀寫同一個資料庫，不是獨立的示範資料集。
- Model 定義資料，ModelAdmin 定義管理介面。
- 購物車、結帳、賣家工作流程仍使用專用 View，接續 02。

登入後能看到資料，不等於所有使用者都應該拿到管理權限。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 6-2 第一次啟動 Admin

**在 LearnMart 根目錄執行，先確認環境與依賴已同步**

```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

開啟 `http://127.0.0.1:8000/admin/`，使用剛建立的帳號登入。
專案需有 admin／auth／sessions 等 app、相應 middleware 與 template 設定。
兩個專案已配置；路由為 `path("admin/", admin.site.urls)`。

驗收：能登入；但自訂模型還需註冊才會出現在列表。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 6-3 最小註冊與 ModelAdmin

```python
# app 的 admin.py；以下兩種擇一
admin.site.register(Category)
```

```python
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "stock")
```

同一 model 不要重複註冊。現有 ProductAdmin 已存在，練習時修改原 class。
新增 model 要 migration；只改列表欄位通常不需要。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 6-4 LearnBoard：留言列表與搜尋

**抽入現有 MessageAdmin，節錄**

```python
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "short_content", "created_at", "updated_at")
    search_fields = ("content", "author__username")
    empty_value_display = "訪客"

    @admin.display(description="內容")
    def short_content(self, obj):
        return obj.content[:30]
```

short_content 是顯示方法，不是資料庫欄位；它不會截短原始留言。
author__username 讓搜尋沿外鍵找作者；empty_value_display 是空值顯示設定。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/
來源：learnboard/board/admin.py；抽入 LearnBoard 原第 4 章 Admin 提示並展開。
-->

---

## 6-5 LearnMart：商品列表的三個設定

**抽入現有 ProductAdmin**

```python
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "seller", "price", "stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
```

list_display 決定列表欄；list_filter 提供側邊篩選；search_fields 決定搜尋範圍。
操作：搜尋「鍵盤」→ 篩選上架 → 點入一筆商品。
列表沒顯示的欄位，仍可能出現在編輯表單。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/
來源：learnmart/marketplace/admin.py::ProductAdmin。
-->

---

## 6-6 編輯表單：fields、fieldsets、readonly

**教學延伸｜加入既有 ProductAdmin**

```python
readonly_fields = ("created_at", "updated_at")
fieldsets = (
    ("商品", {"fields": ("name", "category", "seller", "description")}),
    ("販售", {"fields": ("price", "stock", "is_active", "image")}),
    ("紀錄", {"fields": ("created_at", "updated_at")}),
)
```

fields 指定平面順序；fieldsets 做分組，兩者不要同時設定。
auto_now 類欄位不可編輯，可透過 readonly_fields 顯示。
readonly 是 Admin 介面規則，不是資料庫不可修改的保證。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 6-7 Admin 的 slug 輸入提示

**教學延伸｜先以本段取代 Category 的簡單註冊**

```python
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
```

移除原 `admin.site.register(Category)`，避免 AlreadyRegistered。
新增時會用 JavaScript 協助填 slug；不是 model.save 的生成規則。
先用英文名稱 Daily Tools 試驗；中文 slug 需另設計 allow_unicode 與路由。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/
https://docs.djangoproject.com/en/6.1/ref/models/fields/

-->

---

## 6-8 關聯選單、autocomplete 與查詢

**教學延伸｜加入既有 ProductAdmin**

```python
autocomplete_fields = ("category", "seller")
list_select_related = ("category", "seller")
list_per_page = 30
```

- autocomplete 的目標 Admin 必須設定 search_fields，並有相應存取權限。
- CategoryAdmin 可用上一頁；UserAdmin 原本已有帳號搜尋設定。
- list_select_related 處理列表讀 FK 的查詢成本。
- 少量資料可用普通選單；多對多亦可考慮 filter_horizontal。

先區分「編輯頁選對象」與「列表頁讀對象」的兩種查詢需求。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 6-9 訂單 Inline：同頁看父子資料

**抽入現有 LearnMart｜節錄**

```python
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "unit_price", "quantity", "seller")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
```

OrderItem 的 order 外鍵把明細連到當前訂單；extra=0 只是不預留空白列。
現有設定不是完整唯讀：product 仍可編輯，新增／刪除也需另看權限。
不要把「部分 readonly」當成訂單歷史已被完整保護。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/
來源：learnmart/marketplace/admin.py::OrderItemInline、OrderAdmin。
-->

---

## 6-10 訂單明細唯讀的教學設計

**教學延伸｜替換上一頁的 Inline 定義**

```python
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product", "product_name", "unit_price", "quantity", "seller")
    readonly_fields = fields
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False
```

這限制本 Inline；父訂單欄位及其他寫入入口仍要各自設計。
若要修改訂單，應透過明確的取消／調整流程，保留歷史與一致性。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 6-11 staff、superuser、Group 與模型權限

| 設定 | 意義 |
|---|---|
| is_active＋is_staff | 預設 Admin 的登入資格 |
| is_superuser | 預設權限系統下擁有全部權限 |
| view／add／change／delete | 每個模型的不同操作權限 |
| Group | 組合一群人的權限 |

staff 不等於能管理所有模型；賣家 role 也不等於 staff。
建一個只含 view_product 的群組，交給一般 staff 試登入。
驗收：能看商品，但不能新增、修改與刪除；不要用 superuser 驗收限制。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/auth/default/
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 6-12 進階｜權限與資料範圍

模型權限回答「能否改 Product」；不自動回答「只能改自己的 Product」。

若要讓 staff 只管理指定資料，至少考慮：
- get_queryset 限制列表可見範圍。
- has_view_permission／has_change_permission 等限制物件操作。
- 關聯欄位的可選資料，不能只隱藏列表。
- 自訂 action 與直接網址也要受相同規則約束。

本課讓 Admin 服務內部管理員；賣家自己的介面在 02 用 View 實作。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/auth/default/
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 6-13 現有 UserAdmin 為何另有一個 class？

**現有 LearnMart｜MarketplaceUserAdmin，節錄**

```python
from django.contrib.auth.admin import UserAdmin

@admin.register(User)
class MarketplaceUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("市集身份", {"fields": ("role",)}),
    )
```

繼承 UserAdmin 保留使用者管理與密碼處理；再加入 role。
新增使用者的畫面另用 add_fieldsets；現有專案也有設定。
不要用普通字串欄位方式直接改 password；使用既有密碼修改介面。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/
https://docs.djangoproject.com/en/6.1/topics/auth/default/
來源：learnmart/marketplace/admin.py::MarketplaceUserAdmin。
-->

---

## 6-14 進階｜Admin action：批次下架

**教學延伸｜放進既有 ProductAdmin class 內**

```python
actions = ["deactivate"]

@admin.action(description="將選取商品下架", permissions=["change"])
def deactivate(self, request, queryset):
    count = queryset.update(is_active=False)
    self.message_user(request, f"已下架 {count} 件商品")
```

queryset 是使用者選取的資料；此處只改上架旗標。
update 不觸發逐筆 save／auto_now；若需更新時間，必須明確指定。
結帳、出貨與退款不適合只改一個欄位，應呼叫完整業務流程。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/actions/

-->

---

## 6-15 Admin 操作實驗（35 分鐘）

在 LearnMart 練習分支依序操作：
1. 登入 Admin，建立「ORM 練習分類」，輸入 slug。
2. 修改 ProductAdmin，加入時間唯讀與關聯預載。
3. 為現有商品選分類、填價格、上傳圖片；回前台看結果。
4. 用名稱搜尋、分類篩選；比較列表與編輯頁欄位。
5. 建立只有 view_product 的 staff 帳號，驗證操作限制。

驗收：後台畫面＋前台資料一致；超出位數的價格／重複 slug 都能顯示錯誤。
關聯對象的「＋」按鈕是否出現，取決於目標模型註冊與使用者權限。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/
https://docs.djangoproject.com/en/6.1/topics/auth/default/

-->

---

## 6-15B 整合 migration 與 Admin 的精選欄位

接續第 4 章的 is_featured 練習，在同一個 LearnMart 分支操作。

1. 確認已閱讀並套用新增欄位的 migration。
2. 在現有 ProductAdmin 的 list_display、list_filter 加入 is_featured。
3. 將一件商品設為精選，檢查列表顯示與篩選結果。
4. 執行 makemigrations --check，確認沒有遺漏的模型變更。

ProductForm.Meta.fields 目前不含 is_featured，前台商品表單不會自動新增此欄。

**配套手冊：** LearnMart [第 4 章](../workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md#chapter-4)、[第 5 章](../workbooks/learnmart_01_django_foundations_and_data_backed_catalog_workbook.md#chapter-5)；LearnBoard [第 4 章](../workbooks/learnboard_01_django_foundations_and_message_board_workbook.md#chapter-4)、[第 5 章](../workbooks/learnboard_01_django_foundations_and_message_board_workbook.md#chapter-5)。

---

## 6-16 Admin 常見問題排查

| 現象 | 優先檢查 |
|---|---|
| 登入被拒絕 | 密碼、is_active、is_staff |
| 登入後看不到模型 | app 安裝、模型註冊、模型權限 |
| AlreadyRegistered | 同一 model 重複註冊 |
| autocomplete 系統檢查錯誤 | 目標 Admin 註冊與 search_fields |
| 時間欄位放 fields 後報錯 | 是否需加入 readonly_fields |
| 圖片有資料卻顯示 404 | storage 檔案、MEDIA_URL、開發路由 |

先執行 `uv run python manage.py check`，再根據錯誤定位設定。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

<!-- _class: cover -->

# 第 7 章
## 整合練習與後續課程

---

## 7-1 一對一與多對多實作路線

**在 LearnMart 的練習分支；既有 Product 不需增加欄位**

```bash
uv run python manage.py startapp practice
```

1. 加入 INSTALLED_APPS；在 practice/models.py 放第 3 章 Profile、Tag。
2. 建立並套用 practice migration；先採自動中介表版本。
3. shell 匯入 Profile、Tag、Product，取得一位 user 與一件商品。
4. 建立 Profile，新增兩個 Tag，用 add／remove／set／clear 觀察關係。

驗收：user.profile 是單一物件；product.tags.all() 是集合。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/
https://docs.djangoproject.com/en/6.1/topics/db/examples/many_to_many/

-->

---

## 7-2 綜合設計：商品、標籤與管理後台

分組交付三份可檢查的成果：

- **設計表**：各欄位型別、pk／unique、NULL 與預設值理由。
- **操作紀錄**：一對一／一對多／多對多的正反向查詢與結果型別。
- **管理介面**：列表、搜尋、篩選、唯讀時間、staff 權限的驗收畫面。

每組互問：如果改名字、刪帳號、重複送出、沒上傳圖片，會發生什麼？
能用資料規則解釋結果，比只展示「畫面可以開」更重要。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 7-3 離堂檢核

1. pk 與 unique 的目的有什麼不同？
2. blank=True 能否保證 DB 接受 NULL？
3. auto_now 與 default=timezone.now 有什麼差別？
4. FK 應放在哪一方？一對一的反向結果是什麼？
5. 多對多 clear 會刪掉對方物件嗎？
6. Model.Meta、ModelForm.Meta、ModelAdmin 各管理哪一層？
7. save 是否自動 full_clean？staff 是否擁有全部模型權限？

請各選一題，用 LearnBoard 或 LearnMart 的具體例子回答。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 7-4 01、02、03 的銜接

| 接續教材 | 已具備的基礎 | 下一步 |
|---|---|---|
| 01 第 5～7 章 | Model 與 QuerySet | 先檢核，再組成商品目錄／留言牆 |
| 02 第 1 章 | 欄位驗證、ModelForm.Meta | 自訂表單與圖片上傳 |
| 02 身份／交易章 | 關聯、唯一約束、原子更新 | 權限、結帳與交易一致性 |
| 03 migration／備份 | schema 與 media 的差異 | 部署順序與復原 |

Admin 是內部資料管理的起點；它不會自動實作前台的所有業務規則。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->

---

## 7-5 官方參考：Model 與 ORM

以 Django 6.1 文件為教材基準：

- [Models：模型與關聯](https://docs.djangoproject.com/en/6.1/topics/db/models/)
- [Field reference：欄位與參數](https://docs.djangoproject.com/en/6.1/ref/models/fields/)
- [Meta options：排序、表名、索引](https://docs.djangoproject.com/en/6.1/ref/models/options/)
- [Constraints：唯一性與檢查約束](https://docs.djangoproject.com/en/6.1/ref/models/constraints/)
- [Making queries：查詢與寫入](https://docs.djangoproject.com/en/6.1/topics/db/queries/)
- [Model instances：full_clean 與 save](https://docs.djangoproject.com/en/6.1/ref/models/instances/)

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/topics/db/models/

-->

---

## 7-6 官方參考：關聯、檔案與 Admin

- [Many-to-many：關聯操作範例](https://docs.djangoproject.com/en/6.1/topics/db/examples/many_to_many/)
- [Time zones：時間與時區](https://docs.djangoproject.com/en/6.1/topics/i18n/timezones/)
- [File uploads：上傳資料](https://docs.djangoproject.com/en/6.1/topics/http/file-uploads/)
- [Admin site：註冊、列表、表單與 Inline](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/)
- [Admin actions：批次操作](https://docs.djangoproject.com/en/6.1/ref/contrib/admin/actions/)
- [Authentication：使用者與權限](https://docs.djangoproject.com/en/6.1/topics/auth/default/)

查文件先確認版本，再定位到類別、參數與使用限制。

<!--
官方依據：
https://docs.djangoproject.com/en/6.1/ref/contrib/admin/

-->
