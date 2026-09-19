---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 02｜表單、身份驗證與工作流程"
footer: "初學者教材｜LearnBoard × LearnMart"
---

<!-- _class: cover -->

# Django 02
## 兩個專案的表單、身份驗證與工作流程

<div class="box">能安全地改變資料 ｜ 用測試守住規則 ｜ 貫通 LearnBoard 與 LearnMart</div>

從「能查詢資料」前進到「能安全地改變資料，並用測試守住規則」

---

## 兩個專案共用同一套安全骨架

LearnBoard 是較小的原型；LearnMart 在相同骨架上加入角色、圖片、購物車與交易：

| 你在留言板做過 | 本冊商城版本 |
|---|---|
| `MessageForm` 發文＋PRG | `ProductForm` 上架（多欄位＋圖片） |
| 註冊／登入／session | 相同機制＋買家／賣家角色 |
| `author` FK 的 migration 演進 | 訂單快照、constraint 與交易 |
| 擁有權 mixin（403/404） | `SellerRequiredMixin`、多方限制 |
| CSRF／XSS／IDOR 三課 | 同三課＋transaction 一致性 |
| 9 個 LearnBoard test methods | 商城流程測試與回歸防護 |

**先用 LearnBoard 理解規則，再用 LearnMart 觀察同一規則如何擴展。**

<!--
授課提示：這頁當全冊的索引卡。每章開場都回指一次：購物車章對照「發文表單」、訂單章對照「author migration」、出貨評價章對照「擁有權 mixin」。
-->

---

## 這份教材接續什麼？

你已經能追蹤：

```text
Browser → URLconf → View → ORM → Template → Response
```

這一份要加入三個新問題：

1. 使用者送來的資料可信嗎？
2. 已登入的人可以操作哪些物件？
3. 多筆資料要一起成功或一起失敗，怎麼保證？

<!--
授課提示：開場先花 3 分鐘複習 Deck 01 的完整資料流圖；本冊所有 POST 流程都建立在那張圖上。
-->

---

## Model、表單與 Admin 的先備連結

若還不熟欄位、關聯或後台，先完成 [01B 詳解](../01b_models_orm_and_admin/01b_models_orm_and_admin.md)。

| 層次 | 責任 | 本冊接續 |
|---|---|---|
| Model／Model.Meta | 型別、關聯、排序與資料規則 | 表單驗證與交易 |
| ModelForm.Meta | model 與可編輯 fields | 自訂前台表單 |
| ModelAdmin | 內部後台列表與編輯介面 | 與前台權限比較 |

01B 用 Admin 完成第一輪管理；本冊用 View／Form 建立使用者工作流程。

---

## 本冊最終成果

完成後，你能解釋並追蹤：

- 商品新增／編輯與圖片上傳
- 註冊、登入、session、角色與物件權限
- Generic Class-based View 與 `.as_view()`
- 購物車、結帳、訂單快照、出貨與評價
- CSRF、XSS、IDOR、SQL injection 的防線
- Django `TestCase` 如何保護重要流程

---

## 閱讀標籤

<span class="label">教學用最小範例</span>：省略最終專案細節，只聚焦一個新概念。

<span class="label current">目前 LearnMart｜逐字摘錄</span>：未改寫的 source 片段。<br>
<span class="label current">目前 LearnMart｜節錄／重排</span>：省略無關行、重排換行或加入 `...`；語意對齊，但不是逐字 source。

<span class="label warning">常見錯誤／限制</span>：初學者容易誤解，或教學版尚未處理的情況。

<span class="label check">配套實作手冊</span>：答案、修改步驟與前後程式碼放在另一份 Markdown。

---

## 本冊章節地圖

1. 完整表單生命週期
2. 身份驗證、session 與帳號流程
3. Class-based View、Mixin 與物件權限
4. 購物車、POST 操作與第一批流程測試
5. 訂單、結帳、transaction 與鎖定
6. 賣家出貨、評價與多方交易限制
7. 安全與回歸測試整合

<!--
授課提示：建議每章配一次 lab。第 5 章最重，務必預留完整一堂課。
-->

---

## 兩個專案的實作路線

投影片中的商城節錄以 LearnMart 為主；同一個觀念在 LearnBoard 的目前程式碼可從下表找到。

| 觀念 | LearnBoard | LearnMart |
|---|---|---|
| 表單 | `board/forms.py::MessageForm` | `marketplace/forms.py::ProductForm`、`CheckoutForm` |
| server-owned 欄位 | `MessageCreateView.form_valid()` 指派 `author` | `ProductCreateView.form_valid()` 指派 `seller`；checkout 指派 `buyer`／`total` |
| 登入門禁 | `LoginRequiredMixin` | `LoginRequiredMixin`、`SellerRequiredMixin` |
| 物件擁有權 | `MessageUpdateView.get_queryset()` | `ProductUpdateView.get_queryset()`、訂單 buyer filter |
| POST-only 操作 | 發文、編輯、刪除 | cart、checkout、出貨、review |
| 回歸測試 | `learnboard/board/tests.py` | `learnmart/marketplace/tests.py` |

**選擇一個專案完成 lab 即可；完成後用另一欄做 code reading，不要把兩個資料庫混用。**

---

## 第一次操作建議搭配兩份補充

若學生第一次操作 Django 指令、POST 表單與測試，可穿插本檔後半已整合的內容：

- **「從 HTML Form 到 Database Change」**：DevTools、POST/CSRF、PRG、session/auth、403/404、`refresh_from_db()`、單支測試與 failure 分類。
- **「實用工具箱」**：時間、相對時間、過長文字、humanize、querystring 分頁、集合呈現與 template security。

這兩部分是補充 lab，不改變原本 7 章的概念順序；可依班級熟練度穿插使用。

---

<!-- merged source: 01_chapter_01.md -->

<!-- _class: cover -->

# 第 1 章
## 完整表單生命週期

<div class="box">能從 HTML 表單一路追到 Django 驗證、儲存、redirect 與 message</div>

<!--
授課提示：本章要背的是「生命週期」而非 API 清單；每個語法都要求學生說出它在週期的哪一站。
-->

---

## 為什麼不能直接相信 `request.POST`？

瀏覽器是「資料來源」，不是可信任邊界。

使用者可以：

- 移除 HTML 的 `required`、`min`、`max`
- 修改 hidden input
- 不經過你的頁面，直接送 HTTP request
- 把數字欄位送成文字或極端值

因此 View 必須在伺服器端驗證，再決定是否改資料。

---

## HTML form 的四個核心部分

```html
<form action="/search/" method="get">
  <label for="q">關鍵字</label>
  <input id="q" name="q" value="Django">
  <button type="submit">搜尋</button>
</form>
```

- `action`：送到哪一個 URL
- `method`：GET 或 POST
- `name`：送出的 key
- `value`：送出的 value

---

## GET：查詢，不改變資料

送出後，瀏覽器產生可分享的網址：

```text
/?q=Django&category=book
```

Django 讀取：

```python
query = request.GET.get("q", "")
category = request.GET.get("category", "")
```

`request.GET` 是類似 dictionary 的 `QueryDict`。

---

## GET 參數要保留在畫面上

<span class="label current">目前 LearnMart｜節錄／重排｜templates/base.html</span>

```django
<form action="{% url 'marketplace:home' %}" method="get">
  <input name="q" value="{{ request.GET.q }}"
         placeholder="搜尋商品">
  <button type="submit">搜尋</button>
</form>
```

重新載入結果頁後，搜尋字串仍顯示在 input，使用者知道自己查了什麼。

---

## POST：要求伺服器改變狀態

適合 POST 的操作：

- 新增／編輯商品
- 加入或更新購物車
- 結帳建立訂單
- 確認出貨
- 發表評價

POST 不是「比較秘密的 GET」；它表示這個 request 可能改變伺服器狀態。

---

## Form 與 ModelForm

| 類型 | 用途 | 例子 |
|---|---|---|
| `forms.Form` | 驗證一般輸入，不一定對應資料表 | 搜尋範圍、聯絡表單 |
| `forms.ModelForm` | 依 Model 欄位建立表單並可儲存 instance | 商品、訂單收件資料 |

先理解 `Form` 的驗證流程，再把相同流程套到 `ModelForm`。

---

## <span class="label">教學用最小範例</span> 先從 Form 開始

```python
from django import forms

class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
```

`IntegerField` 同時做兩件事：

1. 把文字輸入轉成 Python `int`
2. 檢查值至少為 1

---

## Unbound form：還沒有收到資料

```python
form = QuantityForm()
```

這個 form：

- 尚未綁定任何 request 資料
- `form.is_bound` 是 `False`
- 適合第一次 GET 顯示空表單
- 不會顯示「必填」錯誤

它不是「驗證成功」，而是「還沒進入驗證」。

---

## Bound form：已經收到資料

```python
form = QuantityForm(request.POST)
```

這個 form：

- `form.is_bound` 是 `True`
- 保留使用者送來的值
- 呼叫 `is_valid()` 後產生 errors 或 `cleaned_data`
- invalid 時應把同一個 bound form 重新 render

<!--
授課提示：demo：invalid POST 後 render bound form 展示欄位值被保留；再示範錯誤寫法（重建空 form）讓輸入消失。
-->

---

## 初學時先寫明確的 GET／POST 分支

```python
if request.method == "POST":
    form = QuantityForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data["quantity"]
        return redirect("marketplace:cart")
else:
    form = QuantityForm()

return render(request, "marketplace/form.html", {"form": form})
```

這比一開始就背 `request.POST or None` 更容易看出狀態轉換。

---

## 為什麼不先教 `request.POST or None`？

常見縮寫：

```python
form = QuantityForm(request.POST or None)
```

但空的 `QueryDict` 是 falsey；一個空 POST 可能被當成 `None`，讓 form 變成 unbound，預期的必填錯誤反而不出現。

<span class="label warning">教學原則</span> 先用 `request.method` 明確分支；熟悉生命週期後再判斷何時適合縮寫。

---

## `is_valid()` 做了什麼？

```python
if form.is_valid():
    quantity = form.cleaned_data["quantity"]
```

驗證成功後：

- 必填、型別、範圍等規則通過
- `cleaned_data` 才可安全讀取
- 值已轉成 Python 型別

驗證失敗時，錯誤放在 `form.errors`，不要自行把錯誤字串散落在 View。

<!--
授課提示：板書驗證順序：field clean → clean_xxx() → Form.clean()；之後自訂驗證才不會迷路。
-->

---

## 顯示錯誤，不要丟掉使用者輸入

```django
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">送出</button>
</form>
```

invalid POST 後要 render 同一個 bound form，Django 才能同時顯示：

- 原本輸入值
- 欄位錯誤
- 非欄位錯誤

---

## 自訂單一欄位驗證

```python
from django.core.exceptions import ValidationError

class QuantityForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)

    def clean_quantity(self):
        value = self.cleaned_data["quantity"]
        if value > 20:
            raise ValidationError("單次最多購買 20 件。")
        return value
```

方法名稱必須是 `clean_<field_name>`，且成功時要 return 清理後的值。

---

## 跨欄位驗證使用 `clean()`（1／2）

```python
from django.core.exceptions import ValidationError

class PriceRangeForm(forms.Form):
    minimum = forms.IntegerField(min_value=0)
    maximum = forms.IntegerField(min_value=0)
```

單一欄位先各自驗證；`clean()` 再檢查 minimum 與 maximum 之間的關係。

若其中一個欄位先失敗，它可能不會出現在 `cleaned_data`，所以下一頁不能直接比較兩個 `.get()` 結果。

---

## 跨欄位驗證使用 `clean()`（2／2）

```python
def clean(self):
    data = super().clean()
    minimum = data.get("minimum")
    maximum = data.get("maximum")
    if (
        minimum is not None
        and maximum is not None
        and minimum > maximum
    ):
        raise ValidationError("最低價不可高於最高價。")
    return data
```

這個 method 放在 `PriceRangeForm` 內。先呼叫 `super().clean()`、同時 guard 兩個 `None`，沒有 raise 時最後必須 `return data`。

---

## ModelForm 的 `Meta`

<span class="label current">目前 LearnMart｜節錄／重排｜marketplace/forms.py::ProductForm</span>

```python
class ProductForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "category", "name", "description", "price",
            "stock", "image", "is_active",
        )
```

`Meta` 是內部設定 class；`fields` 是明確 allowlist，不要讓使用者編輯 `seller`。

---

## 為什麼 `seller` 不在 `fields`？

如果表單讓使用者選 seller，他們就能把商品掛到別人的帳號。

正確來源是已驗證的伺服器資訊：

```python
form.instance.seller = request.user
```

安全原則：

> 角色、擁有者、價格、訂單狀態等 server-owned 欄位，不應直接相信瀏覽器提交值。

---

## `save()` 與 `save(commit=False)`

```python
product = form.save(commit=False)
product.seller = request.user
product.save()
```

- `commit=False`：建立尚未寫入資料庫的 instance
- 補上表單沒有提供、但資料庫必須有的欄位
- 最後明確呼叫 `.save()`

目前 LearnMart 的 `CreateView` 使用 `form.instance.seller = self.request.user`，稍後會對照。

---

## CSRF：防止跨站 mutation 濫用既有 session

```django
<form method="post">
  {% csrf_token %}
  ...
</form>
```

`{% csrf_token %}` 會輸出 hidden input。Django 的 CSRF middleware 驗證 cookie/form token，並依 request 情境套用 Origin／Referer policy，阻擋跨站請求濫用既有 session。

CSRF 不代表 browser「可信」，也不負責檢查價格、角色或欄位格式；那些仍要靠表單、權限與商業規則。

<!--
授課提示：demo：暫時刪掉模板的 {% csrf_token %} 提交即得 403；提醒學生修回來、別 commit。
-->

---

## PRG：成功 POST 後 redirect

```text
POST /seller/products/new/
  → 302 Location: /products/7/
  → GET /products/7/
```

Post/Redirect/Get 的好處：

- 重新整理結果頁不會重複新增
- URL 變成資源的標準網址
- message 可跨 redirect 顯示一次

invalid POST 則直接 render，讓錯誤留在同一頁。

<!--
授課提示：demo：把 redirect 換成 render，成功後按 F5 就會重送 POST；親眼見過才記得住 PRG。
-->

---

## Messages：跨 redirect 的一次性回饋

View 端：

```python
messages.success(request, "商品已新增。")
```

<span class="label current">目前 LearnMart｜節錄／重排｜templates/base.html</span>

```django
{% for message in messages %}
  <div class="alert alert-{{ message.tags|default:'info' }}">
    {{ message }}
  </div>
{% endfor %}
```

message 通常顯示一次，適合 PRG 後回報成功或失敗。

---

## 圖片上傳：HTML 必須改 encoding

```django
<form method="post" enctype="multipart/form-data">
  {% csrf_token %}
  {{ form.as_p }}
</form>
```

預設 form encoding 不會傳送檔案內容。`multipart/form-data` 讓文字欄位與 binary file 一起送出。

目前 `templates/marketplace/form.html` 已使用這個設定。

<!--
授課提示：再次強調 00b 的坑：忘了 multipart/form-data 是靜默失敗（request.FILES 空），不會報錯。
-->

---

## Function View 要同時綁定 POST 與 FILES

<span class="label">教學用最小範例</span>

```python
if request.method == "POST":
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        product = form.save(commit=False)
        product.seller = request.user
        product.save()
        return redirect(product)
else:
    form = ProductForm()
```

`request.POST` 是一般欄位；`request.FILES` 是上傳檔案。

---

## Generic editing view 如何處理檔案？

Django 的 `CreateView`／`UpdateView` 會在自己的 form-processing flow 中綁定 POST 與 FILES。

因此你仍需要：

- Model 有 `ImageField`
- HTML 有 `enctype="multipart/form-data"`
- settings 有 `MEDIA_ROOT`／`MEDIA_URL`
- 開發環境有 media URL routing

但通常不必在 `form_valid()` 再手動建立一個 form。

---

## 第 1 章概念檢核

1. Unbound form 與 invalid bound form 有何不同？
2. 為什麼 invalid POST 要 render 原本的 form？
3. `cleaned_data` 何時才能讀？
4. `commit=False` 解決什麼問題？
5. CSRF、表單驗證、物件權限各自保護什麼？

<span class="label check">答案見配套實作手冊第 1 章</span>

<!--
授課提示：commit=False 一題必考；請學生用自己的話說出「哪些欄位不能相信 client」。
-->

---

## 第 1 章 LearnMart 實作

任務：追蹤並擴充商品新增流程，確認 seller 一定來自目前登入者。

驗收重點：

- invalid input 顯示錯誤且保留值
- 商品圖片可上傳與顯示
- seller 不可由 POST 任意指定
- 成功後 redirect 並顯示 message

[LearnMart 步驟、前後程式碼與驗收命令](../workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md#chapter-1)；[LearnBoard 對應練習](../workbooks/learnboard_02_forms_auth_and_board_workflows_workbook.md#chapter-1)

---

<!-- merged source: 02_chapter_02.md -->

<!-- _class: cover -->

# 第 2 章
## 身份驗證、Session 與帳號流程

<div class="box">知道「你是誰」如何跨 request 保留，並把 authentication 與 authorization 分開</div>

<!--
授課提示：回收 Deck 01 4-4 的 AUTH_USER_MODEL 伏筆；本章結束後角色模型全部到位。
-->

---

## Authentication 與 Authorization

- **Authentication（身份驗證）**：你是誰？是否已登入？
- **Authorization（授權）**：這個人能做什麼？

已登入不等於：

- 一定是賣家
- 可以編輯任意商品
- 可以查看任意訂單

後面會把授權拆成「登入、角色、物件關係」三層。

---

## 自訂 User 必須很早決定

<span class="label current">目前 LearnMart｜節錄／重排｜config/settings.py</span>

```python
AUTH_USER_MODEL = "marketplace.User"
```

新專案應在第一次 `migrate` 前做這個選擇，而且 custom User model 應出現在其 app 的 `0001_initial` migration；Django 的 swappable dependency 與 migration graph 會依賴這個早期位置。

之後更換涉及外鍵、migration 與資料搬移，並非簡單改一行設定。Deck 1 先介紹決策；現在才深入帳號流程。

<!--
授課提示：講反面故事：專案做到一半才想加 role，要動 migration 與多表關聯——建立「第一天就決定」的紀律。
-->

---

## 三種 User 參照方式不要混為一談

1. 同一個 app 內目前程式可直接參照本地 `User` class。
2. 可重用 app 的 model relation 通常用 `settings.AUTH_USER_MODEL`。
3. 執行時要取得目前 User class，使用 `get_user_model()`。

```python
from django.contrib.auth import get_user_model
User = get_user_model()
```

不要說目前每一個 relation 都「實際寫成設定字串」；LearnMart models 目前直接用本地 `User`。

---

## LearnMart User 繼承 AbstractUser

<span class="label current">目前 LearnMart｜節錄／重排｜marketplace/models.py::User</span>

```python
class User(AbstractUser):
    class Role(models.TextChoices):
        BUYER = "buyer", "買家"
        SELLER = "seller", "賣家"

    role = models.CharField(
        "身份", max_length=10,
        choices=Role.choices, default=Role.BUYER,
    )
```

`AbstractUser` 保留 Django 既有帳號、密碼與權限欄位，再加專案欄位。

---

## Role 是商業角色，不是 Django admin 權限

```python
@property
def is_seller(self):
    return self.role == self.Role.SELLER
```

- `role=SELLER`：LearnMart 商城中的賣家
- `is_staff=True`：能否進 Django admin
- `is_superuser=True`：Django 權限檢查通常全部通過

這些概念用途不同，不要用 `is_staff` 代替商業角色。

---

## 教學版的 seller 註冊限制

<span class="label warning">目前設計取捨</span>

`RegistrationForm` 把 `role` 放在 fields，因此任何註冊者都能自行選「賣家」。

這方便課堂練習，但正式商城通常需要：

- 審核或邀請流程
- 商家資料驗證
- 管理員核准角色

教材必須說清楚「目前能做」不等於「正式環境應這樣做」。

---

## 密碼不是加密後可還原

Django 儲存 salted password hash：

```text
algorithm$iterations$salt$hash
```

登入時，Django 用同一演算法計算候選密碼，再比較結果。

- hash 是單向驗證，不是把密碼解密
- salt 不必保密，用來降低相同密碼產生相同結果
- 密碼強度仍需 validators；hash 不能把弱密碼變強

<!--
授課提示：可選 demo：make_password 兩次產生不同 hash（salt）、check_password 驗證成功，證明不可逆。
-->

---

## 建立 User 的正確方法

```python
User.objects.create_user(
    username="amy",
    password="safe-pass-123",
)
```

或對既有 instance：

```python
user.set_password("safe-pass-123")
user.save(update_fields=["password"])
```

<span class="label warning">錯誤</span> `User.objects.create(password="...")` 會把字串當一般欄位值，不會正確 hash。

---

## `create_user()` 不等於跑過所有 password validators

`create_user()`／`set_password()` 會 hash 密碼，但程式直接呼叫時不會自動替你執行所有表單式密碼強度驗證。

`UserCreationForm` 會：

- 要求兩次密碼一致
- 使用設定中的 password validators
- 正確呼叫 `set_password()`

因此互動式註冊流程適合從它擴充。

---

## LearnMart RegistrationForm

<span class="label current">目前 LearnMart｜節錄／重排｜marketplace/forms.py</span>

```python
class RegistrationForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField(label="電子郵件", required=True)

    class Meta:
        model = User
        fields = ("username", "email", "role",
                  "password1", "password2")
```

email 在這個 form 必填，但目前 model/database 並沒有設定 email unique。

---

## 註冊 View 的完整結果

<span class="label current">目前 LearnMart｜節錄／重排｜marketplace/views.py::register</span>

```python
if request.method == "POST" and form.is_valid():
    user = form.save()
    login(request, user)
    messages.success(request, "註冊成功，歡迎加入學購！")
    return redirect("marketplace:home")
```

成功後同時：建立 hashed-password user、建立登入狀態、加入 message、redirect。

---

## Session：跨 request 記住登入狀態

簡化流程：

```text
登入成功
→ Server 建立 session data
→ Browser 保存 session id cookie
→ 下一次 request 帶 cookie
→ Middleware 找回 User
```

cookie 不應放使用者密碼；它通常只攜帶 session identifier。

<!--
授課提示：F12 看 sessionid cookie；shell 看 django_session 表。函式內區域變數活不過一個 request（回扣 00a 6-6）。
-->

---

## 為什麼 `request.user` 存在？

<span class="label current">目前 LearnMart｜節錄／重排｜config/settings.py</span>

```python
MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    ...,
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]
```

SessionMiddleware 先準備 session；AuthenticationMiddleware 再依 session 將 `request.user` 設為 User 或 AnonymousUser。

---

## `request.user` 的兩種狀態

```python
if request.user.is_authenticated:
    ...
```

- 未登入：`AnonymousUser`
- 已登入：目前 User instance

`is_authenticated` 是 property，不是 `is_authenticated()`。

Template 中的 `user` 來自 auth context processor；View 中使用 `request.user`。

---

## LoginView：使用成熟的內建流程

<span class="label current">目前 LearnMart｜節錄／重排｜config/urls.py</span>

```python
path(
    "accounts/login/",
    auth_views.LoginView.as_view(
        template_name="registration/login.html"
    ),
    name="login",
)
```

`.as_view()` 會把 class-based view 轉成 URLconf 可呼叫的 callable；下一章完整拆解。

---

## `next`：登入後回到原本目的地

匿名使用者造訪 `/cart/`：

```text
/accounts/login/?next=/cart/
```

登入表單保留：

```django
{% if next %}
  <input type="hidden" name="next" value="{{ next }}">
{% endif %}
```

成功後 Django 驗證目標 URL，再導回原頁。

---

## Logout 應使用 POST

<span class="label current">目前 LearnMart｜節錄／重排｜templates/base.html</span>

```django
<form method="post" action="{% url 'logout' %}">
  {% csrf_token %}
  <button type="submit">登出</button>
</form>
```

登出會改變 session 狀態。使用 POST + CSRF 可避免第三方圖片或連結讓使用者在不知情時被登出。

<!--
授課提示：講風險劇情：惡意頁面放 <img src="/logout/"> 即可強制登出——GET mutation 的經典漏洞。
-->

---

## Login redirects 在 settings 定義

```python
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "marketplace:home"
LOGOUT_REDIRECT_URL = "marketplace:home"
```

- `LOGIN_URL`：未登入保護頁要去哪裡
- `LOGIN_REDIRECT_URL`：無 `next` 時登入後去哪裡
- `LOGOUT_REDIRECT_URL`：登出後去哪裡

使用 named URL 比硬編碼 path 更容易維護。

---

## 302、403、404 的身份／權限語意

| 狀況 | 常見結果 |
|---|---|
| 匿名者造訪需登入頁 | 302 到 login，附 `next` |
| 已登入但角色不符 | 403 Forbidden |
| 物件不屬於目前使用者 | 404 Not Found |

用 404 隱藏「別人的物件是否存在」，是物件層權限的常見做法。

---

## 第 2 章概念檢核

1. Authentication 與 authorization 有何不同？
2. 為何 custom user 要在初始 migration 前決定？
3. session cookie 是否包含密碼？
4. `create_user()` 與 `UserCreationForm` 各保證什麼？
5. 為何 logout 應使用 POST？

<span class="label check">答案見配套實作手冊第 2 章</span>

<!--
授課提示：302/403/404 語意快問快答；請學生各舉一個本專案的實際 URL 例子。
-->

---

## 第 2 章 LearnMart 實作

任務：追蹤「匿名進購物車 → 登入 → 回購物車 → POST 登出」完整流程。

驗收重點：

- login URL 含正確 `next`
- 登入後 `request.user` 改變
- session 跨 request 保留
- logout GET 不作為操作入口，POST 含 CSRF

[LearnMart 步驟與觀察表](../workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md#chapter-2)；[LearnBoard 對應練習](../workbooks/learnboard_02_forms_auth_and_board_workflows_workbook.md#chapter-2)

---

<!-- merged source: 03_chapter_03.md -->

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

---

<!-- merged source: 04_chapter_04.md -->

<!-- _class: cover -->

# 第 4 章
## 購物車、POST 操作與第一批流程測試

<div class="box">把 mutation 的 method、身份、ownership、驗證與測試放在同一條流程</div>

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

---

<!-- merged source: 05_chapter_05.md -->

<!-- _class: cover -->

# 第 5 章
## 訂單、結帳、Transaction 與鎖定

<div class="box">讓一個 checkout 不是「做了很多 save」，而是可說明其資料一致性與失敗行為</div>

<!--
授課提示：全冊技術高峰，完整一堂課；transaction_rollback.svg 圖解頁務必停留 3 分鐘。
-->

---

## 為什麼需要 Order 與 OrderItem？

```text
Order（訂單主檔）
├─ buyer、收件資料、狀態、總額、時間
└─ OrderItem（每一項商品）
   ├─ product、seller
   ├─ product_name、unit_price 快照
   └─ quantity
```

一張訂單可包含多項商品；每項商品又需要購買當下的資料。

---

## Order 保存交易層資訊

```python
class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.PROTECT,
                              related_name="orders")
    recipient_name = models.CharField(max_length=80)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=30)
    status = models.CharField(...)
    total = models.DecimalField(...)
```

`PROTECT` 避免刪除 buyer 時破壞歷史訂單關聯。

---

## OrderItem 為什麼同時有 FK 與快照？

```python
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    seller = models.ForeignKey(User, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=150)
    unit_price = models.DecimalField(...)
    quantity = models.PositiveIntegerField()
```

- FK 保留追蹤關係
- `product_name`／`unit_price` 保留購買時歷史
- 商品日後改名或漲價，舊訂單不應跟著改

<!--
授課提示：提問：商品改名或改價後，舊訂單應該顯示什麼？答案決定為什麼需要 product_name / unit_price 快照。
-->

---

## 訂單總額也由伺服器保存快照

危險：

```html
<input type="hidden" name="total" value="1980">
```

hidden input 仍可修改。正確：

```python
order.total = sum(item.subtotal for item in items)
```

價格、seller、buyer、status 都是 server-owned data，不列入 CheckoutForm。

---

## CheckoutForm 的 allowlist

<span class="label current">目前 LearnMart｜節錄／重排｜marketplace/forms.py</span>

```python
class CheckoutForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Order
        fields = ("recipient_name", "phone", "address")
```

使用者只輸入收件資料。Order 的 buyer、total、status 與 items 由 View 根據 authenticated user 與 database state 建立。

---

## Checkout 的入口先處理身份與 cart

```python
@login_required
@transaction.atomic
def checkout(request):
    items = list(
        request.user.cart_items
        .select_related("product", "product__seller")
        .select_for_update()
    )
    if not items:
        messages.info(request, "購物車目前是空的。")
        return redirect("marketplace:cart")
```

目前 implementation 在 GET 與 POST 都先 materialize queryset；後面會討論鎖定位置。

---

## `list(queryset)` 讓查詢立即執行

QuerySet 原本 lazy；轉成 list 會立刻讀資料。

這裡的效果：

- 後續多次迭代使用同一批 CartItem object
- 若 backend 支援 `select_for_update()`，evaluation 時才嘗試取得鎖
- 鎖定必須在 transaction 內才有意義

---

## GET 與 POST 在 checkout 扮演不同角色

- GET：建立 unbound CheckoutForm，顯示收件 form 與 cart summary，不應改資料
- POST：建立 bound form，驗證收件資料後建立訂單、扣庫存、清 cart

目前 `@transaction.atomic` 包住兩者。教學上要看懂現況，也要知道更精準的設計可只在 POST mutation 階段進 transaction／lock。

---

## POST 先建立 bound CheckoutForm

```python
form = CheckoutForm(request.POST or None)
if request.method == "POST" and form.is_valid():
    ...
```

這是目前原始碼的簡寫。因 View 已另外檢查 method，仍能區分成功分支；但本冊先前建議初學範例用明確 GET/POST 分支，以避免空 POST 的 bound/unbound 歧義。

---

## 寫入前再次檢查庫存

```python
for item in items:
    if item.quantity > item.product.stock:
        messages.error(
            request,
            f"「{item.product.name}」庫存不足，請調整數量。",
        )
        return redirect("marketplace:cart")
```

Cart 頁看到的庫存可能在結帳前已改變，因此 checkout 必須重新驗證。

---

## `commit=False` 補上 buyer 與 total

```python
order = form.save(commit=False)
order.buyer = request.user
order.total = sum(item.subtotal for item in items)
order.save()
```

表單只提供收件欄位；View 補上 authenticated buyer 與 server-calculated total，再寫入資料庫。

---

## 建立 OrderItem 快照

```python
for item in items:
    OrderItem.objects.create(
        order=order,
        product=item.product,
        seller=item.product.seller,
        product_name=item.product.name,
        unit_price=item.product.price,
        quantity=item.quantity,
    )
```

每個值都來自 database object，不從 hidden field 信任 client。

---

## 扣庫存並清 cart

```python
item.product.stock -= item.quantity
item.product.save(update_fields=["stock"])

request.user.cart_items.all().delete()
```

`update_fields` 只更新 stock column。清 cart 必須在所有 order items 建立與庫存更新成功後，且仍在同一 transaction 中。

---

## 最後 redirect 到 buyer-scoped 訂單

```python
messages.success(request, f"訂單 #{order.pk} 已成立。")
return redirect("marketplace:order-detail", pk=order.pk)
```

後續 OrderDetailView 仍要用 buyer-scoped queryset。剛建立成功不代表可以讓任意登入者讀取其 URL。

---

## `transaction.atomic` 的核心保證

```python
@transaction.atomic
def checkout(request):
    ...
```

在同一 database connection 上，block 內寫入：

- 全部成功 → commit
- exception 往外拋出 → rollback
- 明確標記 rollback → rollback

<span class="label warning">普通 `return` 不會自動 rollback 已完成寫入。</span>

---

## 圖解：Checkout 的成功路徑與 rollback 路徑

![w:1000](../assets/transaction_rollback.svg)

<!--
授課提示：先問「哪幾步在寫入資料庫？」（②③④⑤），再指紅色分支討論沒有 atomic 時的半套狀態。此頁停留 3 分鐘，是全冊最重要的概念圖之一；SQLite 的 row-lock 注意事項在後兩頁補充。
-->

---

## 為什麼 validation 要盡量在寫入前？

若先建立 Order，再發現庫存不足並普通 return，atomic 不會因「回傳錯誤頁」自動 rollback。

目前程式在任何寫入前先檢查所有 item 庫存，避免這個陷阱。

更複雜流程中可：

- raise exception
- 使用 nested atomic/savepoint
- 明確 `transaction.set_rollback(True)`

但先把 validation 排在 mutation 前最清楚。

---

## Atomicity 與 locking 是不同問題

- **Atomicity**：一組寫入要一起 commit 或 rollback
- **Locking／concurrency control**：兩個 transaction 同時讀改同一份庫存時如何協調

只有 atomic 不一定防止 lost update；只有鎖定也不代表多筆寫入會整體 rollback。

<!--
授課提示：一句話分工：atomic 管「全有全無」、select_for_update 管「排隊」。兩者常被混為一談。
-->

---

## `select_for_update()` 的意圖與範圍

```python
items = request.user.cart_items.select_for_update()
```

在支援的 database 中，query evaluation 後會鎖住 query 選到的 rows，直到 transaction 結束。它必須位於 `atomic()` 中、真正 evaluation，且 target 要是共享競爭資源。

若 query 同時以 `select_related()` join 其他 tables，支援的 backend 也可能鎖 joined Product／seller rows；需要 backend 支援的 `of=(...)` 才能限制鎖定範圍。不能只看到起點是 CartItem 就斷言只鎖 CartItem。

---

## SQLite 不提供這個 row-lock 保證

<span class="label warning">目前 LearnMart 使用 SQLite</span>

Django 在 SQLite 上的 `select_for_update()` 沒有 row-lock effect；不會因此取得 PostgreSQL 那種資料列鎖。

所以本教學版可以理解 API 與意圖，但不能宣稱已具備 production-grade 的並行扣庫存保證。

<!--
授課提示：明講教學環境與 production 的差異：正式環境用 PostgreSQL/MySQL 才有完整 row lock 語意。
-->

---

## 優先明確鎖定 Product

真正競爭的共享資源是 Product stock；不同買家的 CartItem 不同。較清楚的 production 方向是：

1. 先取得 cart 中的 product PKs。
2. 在 POST 的 `atomic()` 內，以固定 PK 順序查詢 Product。
3. 對 Product queryset 使用 `select_for_update()`。
4. 用鎖後最新 stock 重新驗證與扣減。

固定順序可降低多商品 checkout 的 deadlock 風險。`of=(...)` 可調整 joined query 的鎖定範圍，但 explicit Product lock 更直接；仍需在支援 row locks 的 database 做 concurrency test。

---

## Buyer 只能看自己的 Order

```python
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order

    def get_queryset(self):
        return Order.objects.filter(
            buyer=self.request.user
        ).prefetch_related("items__product")
```

URL `pk` 由 generic view 在這個範圍中查找；別人的 order 會 404。

---

## Snapshot template 不依賴目前 Product 名稱／價格

```django
{% for item in order.items.all %}
  <span>{{ item.product_name }} × {{ item.quantity }}</span>
  <span>NT$ {{ item.subtotal }}</span>
{% endfor %}
```

顯示 `product_name` 與 `unit_price` 衍生的 subtotal，符合歷史快照目的。

---

## 目前 checkout test 已保護哪些行為？

```python
def test_checkout_creates_order_and_reduces_stock(self):
    ...
    self.assertRedirects(response, order_detail_url)
    self.assertEqual(self.product.stock, 3)
    self.assertEqual(order.total, 1980)
```

已測：建立 order、redirect、扣庫存、server total。

尚未測：OrderItem snapshot、cart 清空、收件欄位、rollback／庫存不足。

---

## Order privacy test 是 IDOR regression test

```python
def test_user_cannot_read_another_users_order(self):
    ...
    response = self.client.get(
        reverse("marketplace:order-detail", args=[order.pk])
    )
    self.assertEqual(response.status_code, 404)
```

它驗證 URL id 存在但不在 buyer-scoped queryset 中，View 不會洩漏他人訂單。

---

## 第 5 章概念檢核

1. OrderItem 為何同時保存 FK 與 snapshot？
2. `commit=False` 在 checkout 補了哪些 server-owned 值？
3. 普通 `return` 是否會讓 atomic rollback？
4. Atomicity 與 row locking 的差異是什麼？
5. 為何 SQLite 上不能宣稱 `select_for_update()` 保護庫存競爭？

<span class="label check">答案見配套實作手冊第 5 章</span>

<!--
授課提示：rollback 測試設計題討論 5 分鐘：「如何讓失敗發生在寫入之後？」（workbook 實作 5E）
-->

---

## 第 5 章 LearnMart 實作

任務：擴充 checkout test，驗證 snapshot、cart 清空與失敗時資料不變。

驗收重點：

- OrderItem name／price／seller 正確
- 成功後 cart 為空
- 庫存不足時不建立 Order、不扣 stock、不清 cart
- 他人仍無法讀取 order

[LearnMart 測試步驟與參考斷言](../workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md#chapter-5)；[LearnBoard 安全／測試對應](../workbooks/learnboard_02_forms_auth_and_board_workflows_workbook.md#chapter-5)

---

<!-- merged source: 06_chapter_06.md -->

<!-- _class: cover -->

# 第 6 章
## 賣家出貨、評價與多方交易限制

<div class="box">把狀態轉換、參與者關係與規則所在層次說清楚</div>

<!--
授課提示：狀態機思維首次登場：PENDING → SHIPPED 的五件事（起點/終點/條件/副作用/誰能觸發）。
-->

---

## Seller 如何找到有自己商品的訂單？

```python
Order.objects.filter(
    items__seller=self.request.user
).distinct().prefetch_related("items")
```

- `items__seller` 沿 reverse FK 篩選
- 一張 order 可能有多個 matching items
- `distinct()` 避免同一 order 重複出現
- Template 再只列出該 seller 的 items

---

## Seller order list 還有一個 N+1 觀察點

Template 顯示：

```django
{{ order.buyer.username }}
```

目前 queryset prefetch items，但沒有 `select_related("buyer")`。列表有多張 order 時可能額外查 buyer。

這是比「order detail prefetch items__product」更貼近實際模板使用的優化練習。

---

## 出貨操作的四層檢查

```python
@require_POST
@login_required
def ship_order(request, pk):
    if not request.user.is_seller:
        return HttpResponseForbidden(...)
    order = get_object_or_404(
        Order.objects.filter(items__seller=request.user).distinct(),
        pk=pk,
    )
```

method → login → seller role → order membership。

<!--
授課提示：逐層回收前面章節編號：POST-only（第1章）、login（第2章）、角色（第3章）、賣家歸屬 query。
-->

---

## 目前只實作 PENDING → SHIPPED

```python
if order.status == Order.Status.PENDING:
    order.status = Order.Status.SHIPPED
    order.shipped_at = timezone.now()
    order.save(update_fields=["status", "shipped_at"])
```

Model 還定義 COMPLETED 與 CANCELLED，但目前沒有對應 endpoint／transition。

「有狀態值」不等於「所有狀態轉換已實作」。

---

## 狀態轉換要定義五件事

1. 誰可以觸發？
2. 從哪些舊狀態允許？
3. 新狀態是什麼？
4. 有哪些副作用？例如時間、庫存、退款
5. 重複 request 是否 idempotent？

依序送出的重複 POST 中，第一個 request 將狀態改為 shipped，後一個不再改時間，所以具有**序列情境下**的冪等效果。

但兩個 concurrent requests 都可能先讀到 pending；正式方向是 conditional update（例如 `filter(pk=..., status=PENDING).update(...)` 並檢查 affected rows）或適當 row lock，而不能只靠 Python `if` 宣稱 concurrency-safe。

---

## 多賣家訂單的核心限制

<span class="label warning">目前教學版設計</span>

一張 Order 可含 seller A 與 seller B 的 items，但 shipping status 在 Order 層級。

結果：只要 A 是其中一項的 seller，A 就能把整張 order 標成 shipped，B 的 item 也被視為已出貨。

<!--
授課提示：說明這是教學簡化：正式多賣家平台需要 per-seller shipment 子模型，期末報告可挑戰。
-->

---

## 限制還會影響 Review

Review eligibility 使用：

```python
order__status__in=[Order.Status.SHIPPED,
                   Order.Status.COMPLETED]
```

若 seller A 把混合訂單整張標為 shipped，買家也可能開始評 seller B 尚未實際出貨的商品。

正式設計應將 shipment/status 拆到 seller group 或 item 層級。

---

## Review 規則要分層描述

LearnMart 有四個不同機制：

1. View query：是否買過且訂單已出貨／完成
2. Form／model validators：rating 是否 1–5
3. Database unique constraint：每個 author/product 一列
4. `update_or_create()`：再次送出時更新原評價

不要籠統說「全部規則都在 View、validator、constraint」。

---

## Eligibility 在 View 查詢

```python
has_purchased = OrderItem.objects.filter(
    order__buyer=request.user,
    product=product,
    order__status__in=[
        Order.Status.SHIPPED,
        Order.Status.COMPLETED,
    ],
).exists()
```

`.exists()` 只需要回答有沒有符合資料，不必載入完整 OrderItem list。

---

## Rating 1–5 由 validators／form 驗證

```python
rating = models.PositiveSmallIntegerField(
    "評分",
    validators=[MinValueValidator(1), MaxValueValidator(5)],
)
```

ModelForm 會使用 model validators。注意：任意程式碼直接 `.save()` 並不等於自動執行 `full_clean()`。

目前 database 沒有 `CheckConstraint` 強制 rating 1–5。

---

## 每人每商品一列由 database unique constraint

```python
models.UniqueConstraint(
    fields=["product", "author"],
    name="one_review_per_product",
)
```

這個 constraint 保護 row uniqueness；它不檢查購買資格，也不檢查 order status。

---

## `update_or_create()` 讓重送變成編輯

```python
Review.objects.update_or_create(
    product=product,
    author=request.user,
    defaults=form.cleaned_data,
)
```

- 找到既有 row：更新 rating/comment
- 找不到：建立新 row

資料庫 unique constraint 與 lookup fields 必須一致，才能避免重複評價。

<!--
授課提示：對照 get_or_create：defaults 只更新指定欄位；unique constraint 是它的前提（回收 Deck 01 5-16A）。
-->

---

## 評價輸出仍需 template escaping

```django
<div>{{ review.comment|linebreaksbr }}</div>
```

Django 先 escape 變數內容，再由 `linebreaksbr` 處理換行。不要對 user comment 加 `|safe`。

這與購買資格無關：authorization 控制誰能寫，escaping 控制內容如何安全輸出。

---

## 出貨與 Review 應有哪些測試？

- buyer POST ship → 403
- seller A 對無關 order → 404
- 正確 seller 對 pending order → shipped + timestamp
- 非購買者 review → 不建立資料
- 未出貨購買者 review → 不建立資料
- 合格買家 review → 建立
- 同人再送 → 更新同一 row
- rating 超範圍 → form invalid

---

## 第 6 章概念檢核

1. 為何 seller order queryset 需要 `distinct()`？
2. Model 有四個 status 是否代表四種 transition 都存在？
3. Whole-order shipping 對多賣家有什麼副作用？
4. Review 的資格、rating 範圍、唯一性各由哪一層負責？
5. `update_or_create()` 與 UniqueConstraint 如何配合？

<span class="label check">答案見配套實作手冊第 6 章</span>

<!--
授課提示：eligibility 查詢條件請學生口述：buyer + product + status in (SHIPPED, COMPLETED)。
-->

---

## 第 6 章 LearnMart 實作

任務：加入 seller shipping ownership 與 review eligibility tests。

驗收重點：

- 不相關 seller 得到 404
- buyer 不可出貨
- non-purchaser／pending order 不可評
- 合格評價建立，再送時更新而非新增

[LearnMart Fixtures、步驟與參考測試](../workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md#chapter-6)；[LearnBoard 對應練習](../workbooks/learnboard_02_forms_auth_and_board_workflows_workbook.md#chapter-6)

---

<!-- merged source: 07_chapter_07.md -->

<!-- _class: cover -->

# 第 7 章
## 安全與回歸測試整合

<div class="box">把每個防線放回它保護的 trust boundary，並用測試防止日後退步</div>

<!--
授課提示：安全章不是附加品，是把前面各章的防線串成地圖；trust_boundary.svg 務必配合使用。
-->

---

## 安全不是最後才加的一頁

本冊已經在功能旁使用：

- Template autoescaping：輸出 user content
- CSRF：token 與 Origin／Referer policy 防跨站 mutation
- Form validation：輸入型別與規則
- Authentication：確認身份
- Role／ownership：限制操作範圍
- Server-owned fields：價格、seller、buyer、status
- Transaction：多筆寫入一致性
- Tests：把預期行為固定下來

---

## Trust boundary 地圖

```text
Browser-controlled
URL pk / query string / POST / hidden input / uploaded file
        ↓ validate + authorize
Django View / Form / QuerySet scope
        ↓ server-owned decisions
Models / Database / Transaction
        ↓ encode output
Template / Response
```

每跨一條邊界，都要問：「這個值從哪來？誰有權決定？」

---

## 圖解：信任邊界與五層伺服器防線

![w:1000](../assets/trust_boundary.svg)

<!--
授課提示：左側四張卡片可各配實演（devtools 改 required、改 hidden input、curl 送 POST）。右側五層對應回收：② 第 3 章、③ 第 1 章、④⑤ 第 5 章。收尾提問：「哪一層可以省？」（都不能）
-->

---

## XSS：Template autoescaping 的邊界

安全預設：

```django
{{ post.content }}
{{ post.content|linebreaksbr }}
```

危險：

```django
{{ post.content|safe }}
```

`safe` 告訴 Django 不要 escape；若資料來自使用者，就可能形成 stored XSS。

<!--
授課提示：demo 回收 Deck 01 3-6：留言板輸入 <b>粗體</b> 與 <script>，觀察 escape 差異與 |safe 的危險。
-->

---

## Raw HttpResponse 不會套 Template autoescaping

```python
return HttpResponse(f"歡迎 {name}")
```

若 `name` 是 user-controlled HTML，這個字串會直接成為 response body。

更好的教學方向：

```python
return render(request, "hello.html", {"name": name})
```

或在確實需要時使用明確 escaping utility。不要把「Django 預設安全」誤解成所有字串都自動 escape。

---

## BoardPost 是 stored XSS 的實際觀察點

Board create 儲存 user content；list template 顯示：

```django
<div>{{ post.content|linebreaksbr }}</div>
```

測試可建立 `<script>alert(1)</script>` 文字，再 assert response 包含 escaped 版本而非 raw executable markup。

安全測試要針對輸出，不只看「建立成功」。

---

## SQL injection：ORM value 會參數化

```python
Product.objects.filter(name__icontains=query)
```

`query` 當參數傳給 database driver，不要用字串拼 SQL：

```python
# 危險示意，不要用 f-string 拼接 user input
Product.objects.raw(
    f"SELECT * FROM marketplace_product "
    f"WHERE name LIKE '%{query}%'"
)
```

ORM 防 SQL injection 不代表自動做 authorization。

<!--
授課提示：f-string 拼 SQL 的反例只看不跑；強調 ORM 參數化是預設，raw SQL 才需要警戒。
-->

---

## Dynamic field name 仍需要 allowlist

即使 filter value 安全，使用者控制排序欄位也要限制：

```python
allowed = {"price", "-price", "created_at"}
ordering = request.GET.get("ordering", "-created_at")
if ordering not in allowed:
    ordering = "-created_at"
queryset = queryset.order_by(ordering)
```

不要把任意 query string 直接當 field/expression。

---

## CSRF、Login、Role、Ownership 不可互相替代

以 ship_order 為例：

- CSRF：token 與 Origin／Referer policy 是否通過；不判斷 user 是否有權
- login：是誰
- role：是不是 seller
- ownership/membership：是否參與這張 order
- POST：method 語意與 405 enforcement

只通過其中一層不代表操作安全。

<!--
授課提示：表格快問快答：只做其中一項時，攻擊腳本會長怎樣？
-->

---

## Upload：ImageField 不是完整安全策略

目前已有：

- `ImageField`
- Pillow 支援基本 image 驗證
- `upload_to="products/%Y/%m/"`
- local media storage

尚未完整處理：

- 明確 file size policy
- 內容重新編碼／metadata 移除
- 隨機命名與隔離
- malware scanning
- production object storage／CDN

---

## 開發 settings 不等於 production baseline

<span class="label warning">目前 LearnMart 刻意是 classroom config</span>

```python
SECRET_KEY = "django-insecure-..."
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
```

正式部署還需環境變數、HTTPS、secure cookies、HSTS、logging、production database、media strategy 等。

---

## `check` 與 `check --deploy` 不同

```bash
uv run python manage.py check
```

檢查一般 project configuration。

```bash
uv run python manage.py check --deploy
```

會對 production security settings 提出警告；教學版預期會出現多項警告，不代表要在本地課堂設定盲目消除所有項目。

---

## 現有六個測試保護什麼？

1. 搜尋找到商品
2. 匿名 add-to-cart redirect
3. buyer 可加入 cart
4. buyer 進 seller dashboard 得到 403
5. checkout 建 order、扣 stock、算 total
6. 不能讀別人的 order（404）

不要把「教材列出的測試主題」誤說成「目前都已實作」。

---

## 測試矩陣：一個 workflow 至少看五面

| 面向 | 問題 |
|---|---|
| 正常路徑 | 合法使用者能完成嗎？ |
| Invalid input | 邊界值會被拒絕且資料不變嗎？ |
| Authorization | 匿名、錯角色、錯 owner 的結果？ |
| Side effects | 相關 rows、stock、status、message 都正確嗎？ |
| Failure integrity | 中途失敗是否留下半套資料？ |

---

## Response 與 database assertion 都重要

```python
response = self.client.post(url, data)
self.assertRedirects(response, expected_url)

order = Order.objects.get(buyer=self.buyer)
self.assertEqual(order.total, 1980)
self.product.refresh_from_db()
self.assertEqual(self.product.stock, 3)
```

HTTP 正確但資料錯，或資料正確但洩漏 URL，都算 workflow bug。

---

## `refresh_from_db()` 避免看舊 object

測試中的 `self.product` 是記憶體 object；View 在另一段 code 修改 database 後，原 object 不會自動更新。

```python
self.product.refresh_from_db()
```

再 assert stock，才能讀到 database 最新值。

---

## Rollback test 要讓失敗發生在寫入之後

針對目前 checkout，可 patch `Product.save()` 在第一次庫存儲存時拋 exception。此時程式已建立 Order 與至少一個 OrderItem，才真正挑戰 view-level `@transaction.atomic`。

Exception 離開 atomic 後要檢查：

- Order 與 OrderItem 都 rollback
- database stock 不變
- CartItem 仍存在

這是同一 request／connection 的 view-level atomic rollback invariant；不是 row-lock 或 concurrent commit test。

<!--
授課提示：TestCase 包 transaction 的陷阱一句話帶過；細節在 workbook 第 5 章。
-->

---

## 一次跑完整與單一測試

```bash
uv run python manage.py test
```

單一 method：

```bash
uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_checkout_creates_order_and_reduces_stock
```

Dotted label 可指定 app、module、class 或 method，適合快速迭代。

---

## Migration drift 不是 behavior test

```bash
uv run python manage.py makemigrations --check
```

它檢查 models 是否有尚未建立 migration 的變更。

它不會測試：

- View 權限
- Template 輸出
- checkout transaction
- status transition

三種命令目的不同，要一起使用而不是互相取代。

---

## Security regression 的優先順序

先為高風險、容易退步的規則加測試：

1. ownership-scoped update/detail
2. server-calculated total
3. checkout failure integrity
4. seller order membership
5. review eligibility
6. POST-only state changes
7. user content output escaping

測試不能證明完全安全，但能阻止已知規則被後續修改破壞。

---

## 課堂版與正式商城的界線

目前適合學習：

- Django MVT 與 ORM
- 表單、auth、permissions
- transaction 與測試思維

正式營運仍缺：

- payment、tax、refund
- seller onboarding
- shipment grouping
- production concurrency
- object storage、monitoring、audit log
- 更完整 threat model 與 test coverage

<!--
授課提示：念一遍缺漏清單並宣佈：期末考觀念不考部署；想挑戰的同學指向 check --deploy。
-->

---

## 第 7 章概念檢核

1. Template autoescaping 與 raw HttpResponse 的邊界在哪？
2. ORM 防 injection 是否同時保證 ownership？
3. 為何 CSRF、login、role、ownership 都要存在？
4. 一個 workflow test 為何要同時 assert response 與 side effects？
5. `check`、`makemigrations --check`、`test` 各自檢查什麼？

<span class="label check">答案見配套實作手冊第 7 章</span>

<!--
授課提示：測試矩陣五面（匿名/身份/角色/資料/併發）讓學生對照自己的 lab 補洞。
-->

---

## 第 7 章 LearnMart 實作

任務：新增一個 ownership regression test 與一個失敗完整性 test。

驗收重點：

- 非 owner 得到預期 403／404
- forbidden object 不被修改
- 失敗 checkout 不留下 Order 或 stock/cart 半套狀態
- 完整 test suite 與 migration check 都通過

[LearnMart 安全測試手冊](../workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md#chapter-7)；LearnBoard 安全與測試對應見本冊前段的 `board/tests.py` 對照。

---

---

<!-- merged source: 08_learnboard_comparison.md -->

# LearnBoard 對照實作
## 表單與 server-owned author

目前 `learnboard/board/views.py` 的新增留言流程：表單只提供 `content`，作者由伺服器從 session 指派。

```python
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "board/message_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "留言已發布。")
        return super().form_valid(form)
```

這和 LearnMart 的 `ProductCreateView` 指派 `seller`、checkout 指派 `buyer`／`total` 是同一條規則：**使用者可提交的欄位不等於伺服器可信的欄位。**

---

## LearnBoard 對照實作
### 兩種 ownership 防線

```python
class MessageUpdateView(LoginRequiredMixin, UpdateView):
    def get_queryset(self):
        return Message.objects.filter(author=self.request.user)
```

```python
class OwnerOrStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        obj = self.get_object()
        return obj.author_id == self.request.user.pk or self.request.user.is_staff
```

- 編輯：scoped queryset 讓非作者得到 404
- 刪除：`test_func()` 讓非作者得到 403，staff 可管理
- LearnMart 同樣先檢查 seller role，再以 `seller=self.request.user` 限制商品或訂單

---

## LearnBoard 對照實作
### 測試矩陣如何遷移到商城？

LearnBoard 目前測試已固定這些規則：

| LearnBoard 測試行為 | LearnMart 對應問題 |
|---|---|
| 匿名不能開新增頁 | 匿名不能加入購物車／進入 checkout |
| 建立留言時 author 是登入者 | 建立商品時 seller 是登入者 |
| 非作者編輯得到 404 | 非 owner seller 編輯商品得到 404 |
| 非作者刪除得到 403 | buyer 出貨得到 403 |
| staff 可刪除留言 | seller 只能處理自己商品所在的訂單 |

每增加一條規則，都同時檢查 response、資料是否改變，以及失敗時的 side effects。

---

<!-- merged source: 09_integration.md -->

# 全冊整合：兩個專案的兩條旅程

```text
LearnBoard:
GET message list → ORM filter → Template
POST create/update/delete → Form → CSRF/login → ownership → redirect
Tests → response + Message author/content + 403/404 invariants

LearnMart:
GET catalog → ORM filter → Template
POST cart → CSRF/login/stock/ownership
GET checkout → CheckoutForm + cart summary
POST checkout → validation → atomic writes → redirect
GET order → buyer-scoped queryset
POST ship/review → role or purchase rule → constraint
Tests → response + database + failure invariants
```

---

## 你現在應該能回答

- 哪些值由 browser 決定，哪些必須由 server 決定？
- 一個 protected CBV 在哪裡檢查 login、role、ownership？
- atomic 與 row locking 的保證有何不同？
- SQLite 對 `select_for_update()` 有何限制？
- 一項規則應放 Form、View、Model validator、constraint 還是 test？

---

## 建議驗證命令

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

接著使用 workbook 逐章完成 labs；每次只改一個可觀察行為，先跑單一測試，再跑完整 suite。

---

<!-- merged source: 10_first_contact_forms_auth_testing_lab.md -->

<!-- _class: cover -->

# Django 02 補充 Lab
## 從 HTML Form 到 Database Change

<div class="box">先看 request → 再看 form → 再看 auth/permission → 最後看 DB 與 redirect</div>

---

## 1. POST flow 先畫出來

```text
<form method="post">
   ↓
POST /some/url/
   ↓
CSRF middleware
   ↓
View
   ↓
Form(data=request.POST)
   ↓ is_valid()
cleaned_data
   ↓
save / transaction
   ↓
redirect (PRG)
```

Debug 時一次只找一層。

---

## 2. HTML 有欄位，不代表 server 信任它

Browser 送來的：

```python
request.POST
request.FILES
```

全部視為 untrusted input。

`author`、`seller`、`buyer`、`total` 等 server-owned 欄位，不應讓 client 自己決定。

---

## 3. 先觀察 request.POST

開發時可用 debugger / temporary log；概念上先知道：

```python
print(request.POST)
```

會看到 QueryDict。

真正程式不要把 password/token 等敏感 POST 全部寫進 log。

---

## 4. Form lifecycle 要會逐步問

```python
form = ProductForm(request.POST, request.FILES)
form.is_bound
form.is_valid()
form.errors
form.cleaned_data
```

只有 `is_valid()` 成功後，才使用 `cleaned_data`。

---

## 5. 驗證錯誤不等於 exception

Form validation failure 通常是正常的 user input 狀況：

```python
if form.is_valid():
    ...
else:
    return render(..., {"form": form})
```

不要把每個 validation error 都變成 HTTP 500。

---

## 6. CSRF 失敗時先看哪裡？

Template POST form：

```django
<form method="post">
  {% csrf_token %}
  ...
</form>
```

403 CSRF 常見原因：

- 漏 `{% csrf_token %}`
- cookie / origin / HTTPS proxy 設定問題
- 用外部工具 POST 卻沒 token

---

## 7. Browser DevTools 是表單 debugger

Network 面板看：

- Request Method
- Form Data / Payload
- Status Code
- Location response header（302）
- Set-Cookie

不要只看畫面「好像沒反應」。

---

## 8. PRG：為什麼成功後 redirect？

POST 成功：

```python
return redirect("...")
```

瀏覽器接著 GET。

好處：重新整理 GET 不會重送 POST，避免重複建立資料。

---

## 9. LoginRequired：302 不一定是錯

匿名使用者打受保護頁：

```text
302 → /accounts/login/?next=/target/
```

測試應檢查 redirect target，不是只說「不是 200」。

---

## 10. `request.user` 從哪裡來？

```text
SessionMiddleware
  ↓
AuthenticationMiddleware
  ↓
request.user
```

未登入：`AnonymousUser`

已登入：實際 User instance。

---

## 11. Authentication ≠ Authorization

已登入只回答「你是誰」。

還要再問：

- 角色/permission
- 物件 ownership
- workflow state

例如已登入 buyer 仍不能編 seller 的商品。

---

## 12. 403 與 404 的教學差別

- 403：知道資源存在，但你不能做
- 404：查詢範圍本身不讓你看到那筆物件

```python
Product.objects.filter(seller=request.user)
```

對別人的 product 直接得到 404，可以降低 IDOR 資訊洩漏。

---

## 13. 測試的 Arrange / Act / Assert

```python
# Arrange
user = User.objects.create_user(...)

# Act
response = self.client.post(url, data)

# Assert
self.assertRedirects(response, expected)
self.assertTrue(Model.objects.filter(...).exists())
```

看 test 時先標出三段。

---

## 14. `self.client.login` vs `force_login`

```python
self.client.login(username="amy", password="...")
```

會走 authentication backend。

```python
self.client.force_login(user)
```

直接建立已登入 session，適合不想測密碼驗證本身的測試。

---

## 15. 每個重要 POST 至少驗證兩件事

HTTP 行為：

```python
self.assertRedirects(response, expected_url)
```

資料行為：

```python
obj.refresh_from_db()
self.assertEqual(obj.stock, 3)
```

只測 302 不代表資料真的正確。

---

## 16. `refresh_from_db()` 為什麼重要？

Python 手上的 instance 可能是舊值。

```python
product.refresh_from_db()
```

重新從 DB 讀，才是在驗證「真正被寫入的結果」。

---

## 17. Transaction 測試要驗證 rollback

不只測成功案例。

失敗情境應驗證：

- Order 沒建立一半
- stock 沒扣一半
- cart 沒被錯誤清空

「錯時沒有留下半套資料」才是 transaction 的價值。

---

## 18. 單支測試定位

```bash
uv run python manage.py test \
  marketplace.tests.CheckoutTests.test_checkout_creates_order_and_reduces_stock
```

先讓單支綠，再跑 class/app/all。

---

## 19. Test failure 常見類型

```text
AssertionError       → expected/actual 不同
IntegrityError       → constraint / required relation
NoReverseMatch       → URL name/args
DoesNotExist         → fixture/setup 不完整
403/404/405 mismatch → auth/ownership/method 邏輯
```

先分類，再找檔案。

---

## 20. 安全測試不是「掃描器章節」

你可以直接寫 regression tests：

- anonymous POST 被擋
- non-owner 不能 edit
- CSRF template 有 token
- XSS input 被 escape
- stock 不足不建立 order
- GET 不應觸發 state change

Security rule 要變成可重跑的 test。

---

## 21. 每個 lab 的最終 checklist

```text
[ ] GET 頁面正常
[ ] invalid POST 顯示 errors
[ ] valid POST 寫入正確資料
[ ] 成功採 PRG
[ ] anonymous/other user 被正確阻擋
[ ] DB side effects 已驗證
[ ] 單支測試 green
[ ] 全部測試 green
```

---

<!-- merged source: 10_next_steps.md -->

# 下一步

你已建立兩個 server-rendered Django 專案共用的核心心智模型。

後續可深入：

- REST API 與前後端分離
- PostgreSQL transaction isolation／locking
- background jobs、email、cache
- payments、refund、shipment domain
- deployment、observability、security hardening

先把「資料完整性、權限、輸出安全與測試」守穩，再增加複雜度。

---

<!-- merged source: 11_django_template_language_practical_toolbox.md -->

<!-- _class: cover -->

# Django Template Language
## 實用工具箱

<div class="box">少寫重複 view code｜保持 autoescape｜讓清單、時間、文字與分頁更好用</div>

---

## DTL 的定位

Template 應該負責：

- 呈現資料
- 小型格式轉換
- 簡單條件與迴圈
- 組合 reusable partial

不應該負責：

- 複雜 business rule
- database query orchestration
- 大量 Python 計算
- permission 核心判斷

複雜邏輯移到 view / model / QuerySet / custom template tag。

---

## Filter 可以串接

```django
{{ article.title|default:"未命名"|truncatechars:40 }}
```

心智模型：

```text
article.title
  ↓ default
  ↓ truncatechars
  ↓ render
```

每個 filter 都接收前一個輸出。

---

## `default` vs `default_if_none`

```django
{{ value|default:"沒有資料" }}
{{ value|default_if_none:"沒有資料" }}
```

差異：

- `default`：空字串、False、空 list 等 falsy 值也會被替換
- `default_if_none`：只有 `None` 才替換

如果 `0` 是有意義的值，常常要用 `default_if_none`。

---

## 日期格式 `date`

```django
{{ article.published_at|date:"Y-m-d" }}
{{ article.published_at|date:"Y/m/d H:i" }}
```

常見格式：

- `Y`：四位年份
- `m`：月份 01–12
- `d`：日期 01–31
- `H`：24 小時制
- `i`：分鐘

不要在 view 手動 `strftime()` 只為了顯示格式。

---

## 只顯示時間：`time`

```django
{{ event.starts_at|time:"H:i" }}
```

當畫面只需要時間，不需要日期時，比 `date` 語意更清楚。

---

## 相對時間：`timesince`

```django
{{ article.created_at|timesince }} 前
```

可能顯示：

```text
3 天, 4 小時 前
```

適合：

- 留言時間
- 發文多久
- 最近活動

---

## 未來還有多久：`timeuntil`

```django
距離截止還有 {{ deadline|timeuntil }}
```

適合：

- 活動倒數
- 排程發佈
- 訂單付款期限

如果要精準倒數到秒，應交給 JavaScript，而不是 template 每秒重算。

---

## Template 裡取得現在時間：`{% now %}`

```django
{% now "Y-m-d H:i" %}
```

也可以存進變數：

```django
{% now "Y" as current_year %}
© {{ current_year }}
```

適合 footer 等簡單呈現。

---

## 更自然的時間：`humanize`

先載入：

```django
{% load humanize %}
```

常用：

```django
{{ article.created_at|naturaltime }}
{{ article.published_at|naturalday }}
```

可能得到：

```text
3 minutes ago
今天
明天
```

實際語言依 i18n 設定。

---

## 大數字：`intcomma` / `intword`

```django
{% load humanize %}
{{ article.view_count|intcomma }}
{{ total_users|intword }}
```

例：

```text
12,345
1.2 million
```

適合 dashboard / analytics 類畫面。

---

## 長文字：`truncatechars`

```django
{{ article.title|truncatechars:40 }}
```

超過 40 characters 時會截斷並加省略符號。

最常用在：

- card title
- table column
- sidebar link
- mobile layout

---

## 長文字：`truncatewords`

```django
{{ article.excerpt|truncatewords:25 }}
```

以「單字數」截斷。

英文文章很好用；中文沒有空白斷詞時，`truncatechars` 通常更直覺。

---

## HTML 截斷版本要小心

Django 也有 HTML-aware variants，例如：

```django
{{ trusted_html|truncatechars_html:120 }}
```

重點：

**HTML-aware 不等於 XSS sanitizer。**

如果內容來自使用者，仍要先有可信的 sanitization policy。

---

## 純文字換行：`linebreaks`

```django
{{ comment.body|linebreaks }}
```

會把換行轉成 `<p>` / `<br>` 結構。

如果只想換行變 `<br>`：

```django
{{ comment.body|linebreaksbr }}
```

很適合簡單 textarea 內容。

---

## 檔案大小：`filesizeformat`

```django
{{ upload.size|filesizeformat }}
```

可能顯示：

```text
2.4 MB
```

比直接顯示 `2516582` bytes 更友善。

LearnMart 圖片上傳教材可以直接使用。

---

## 小數格式：`floatformat`

```django
{{ rating|floatformat:1 }}
{{ completion_ratio|floatformat:2 }}
```

例：

```text
4.6
0.83
```

如果是 money，仍建議 model/backend 使用 `Decimal`，不要把精度責任交給 template。

---

## `length` / `wordcount`

```django
{{ articles|length }}
{{ article.body|wordcount }}
```

適合純呈現。

如果 `articles` 是 QuerySet，而且你只是要 DB count，通常 view/queryset 的 `.count()` 更能表達意圖。

---

## List helpers

```django
{{ tags|first }}
{{ tags|last }}
{{ tags|join:", " }}
{{ articles|slice:":3" }}
```

適合小型 presentation transformation。

不要為了只顯示前三筆而在大量 QuerySet evaluate 後才 slice；能在 ORM 限制就優先在 ORM。

---

## `dictsort`

```django
{% for item in items|dictsort:"name" %}
  {{ item.name }}
{% endfor %}
```

可用於 template 收到的普通 dict/list data。

如果排序是 domain rule 或會影響 pagination，應在 ORM / view 排好。

---

## `yesno`

```django
{{ order.is_paid|yesno:"已付款,未付款" }}
```

也可給 None 第三種：

```django
{{ value|yesno:"是,否,未知" }}
```

適合 Boolean label。

---

## `pluralize`

英文 UI 常用：

```django
{{ count }} comment{{ count|pluralize }}
```

中文通常不需要單複數變化，但看官方教材或國際化專案時很常遇到。

---

## `urlize` / `urlizetrunc`

```django
{{ plain_text|urlize }}
{{ plain_text|urlizetrunc:30 }}
```

把純文字 URL/email 轉成 link。

注意：它不是 Markdown parser，也不是 sanitization 工具。

---

## `{% with %}`：替長 lookup 取名字

```django
{% with total=order.items.count %}
  共 {{ total }} 項
{% endwith %}
```

適合：

- 提升可讀性
- 同一個值在區塊內重複使用

不要拿 `{% with %}` 取代應該在 view 計算的複雜資料。

---

## `{% firstof %}`：多個 fallback

```django
{% firstof user.get_full_name user.username "匿名" %}
```

相當於「第一個 truthy 值」。

比多層 `{% if %}` 簡潔。

---

## `{% cycle %}`：輪流值

```django
{% for row in rows %}
<tr class="{% cycle 'odd' 'even' %}">
```

常用：

- zebra table
- card variant
- alternating alignment

Bootstrap 已能處理很多 styling，但讀舊模板時很常見。

---

## `{% ifchanged %}`：分組顯示

```django
{% for article in articles %}
  {% ifchanged article.category.name %}
    <h2>{{ article.category.name }}</h2>
  {% endifchanged %}
  ...
{% endfor %}
```

資料必須先按 grouping key 排好。

---

## `{% regroup %}`：Template 層分組

```django
{% regroup articles by category as grouped %}

{% for group in grouped %}
  <h2>{{ group.grouper }}</h2>
  {% for article in group.list %}
    {{ article.title }}
  {% endfor %}
{% endfor %}
```

適合「已經排序好的資料」做 presentation grouping。

不是 SQL `GROUP BY` 的替代品。

---

## `{% querystring %}`：分頁超實用

Django 5.1+ 內建：

```django
<a href="{% querystring page=page_obj.next_page_number %}">
  下一頁
</a>
```

如果目前 URL 是：

```text
/?q=django&category=web&page=1
```

它能只改 `page`，保留其他 query parameters。

---

## 搜尋＋分頁的典型寫法

```django
{% if page_obj.has_previous %}
<a href="{% querystring page=page_obj.previous_page_number %}">
  上一頁
</a>
{% endif %}

{% if page_obj.has_next %}
<a href="{% querystring page=page_obj.next_page_number %}">
  下一頁
</a>
{% endif %}
```

比手動：

```django
?q={{ query }}&page=...
```

更不容易漏掉其他 filter。

---

## `url` tag：不要手拼路徑

```django
{% url 'journal:article-update' article.pk %}
```

有 kwargs：

```django
{% url 'journal:category' slug=category.slug %}
```

URL 結構改名時，named URL 能集中變更。

---

## `json_script`：安全把資料交給 JS

```django
{{ chart_data|json_script:"chart-data" }}
```

JavaScript：

```js
const data = JSON.parse(
  document.getElementById("chart-data").textContent
);
```

比直接把 Python data 插進 `<script>` 字串安全，也更符合 CSP。

---

## Autoescape 是預設安全線

```django
{{ comment.body }}
```

Django 預設會 escape HTML 特殊字元。

例如 user 輸入：

```html
<script>alert(1)</script>
```

不應直接成為可執行 script。

---

## `safe` 要非常克制

```django
{{ value|safe }}
```

它的意思不是「幫我清理 HTML」。

它的意思是：

> 我向 template engine 保證，這段內容已可信，可不要 escape。

如果保證錯了，就是 XSS。

---

## `striptags|safe` 不是 sanitizer

不要假設：

```django
{{ user_html|striptags|safe }}
```

就一定安全。

Django 官方文件也明確提醒 `striptags` 的輸出不應再直接標記 safe。

有 user HTML 需求時，用專門 sanitizer policy。

---

## Template 裡不要呼叫帶參數方法

DTL 允許：

```django
{{ article.get_absolute_url }}
```

但不支援像 Python：

```python
article.some_method("x")
```

需要帶參數的 presentation logic：

- 先在 view 計算
- 自訂 filter
- simple_tag / inclusion_tag

---

## 什麼時候做 custom filter？

當你一直重複：

```django
{{ value|...一串處理... }}
```

而且它是純 presentation transformation。

例：LearnJournal 的 `markdownify`。

Custom filter 應盡量是 deterministic、沒有 DB side effect。

---

## 什麼時候做 inclusion tag？

當一小塊 UI 同時需要：

- 自己的 query/context
- 自己的 partial template
- 多頁重用

例：

```django
{% latest_articles 5 %}
{% tag_cloud 20 %}
```

比每個 view 都塞相同 context 更乾淨。

---

## LearnBoard 可以立刻用的補強

留言清單：

```django
{{ message.content|truncatechars:120 }}
{{ message.created_at|naturaltime }}
```

搜尋分頁：

```django
{% querystring page=page_obj.next_page_number %}
```

---

## LearnMart 可以立刻用的補強

```django
{{ product.description|truncatewords:30 }}
{{ product.image.size|filesizeformat }}
{{ product.rating|floatformat:1 }}
{{ order.created_at|date:"Y-m-d H:i" }}
```

數量：

```django
{{ cart_items|length }} 項商品
```

---

## LearnJournal 可以立刻用的補強

```django
{% load humanize %}
{{ article.published_at|naturaltime }}
{{ article.view_count|intcomma }} 次瀏覽
{{ article.excerpt|truncatechars:140 }}
```

Scheduled：

```django
距離發佈還有 {{ article.published_at|timeuntil }}
```

---

## 判斷「該放哪一層」

如果你正在 template 想做：

```text
多次 DB query
複雜排序
permission decision
transaction
API call
多層資料轉換
```

停下來。

大多數情況應該移到 Python 層。

---

## 本章實作題

1. LearnBoard 留言列表加 `naturaltime`。
2. LearnMart 商品卡改用 `truncatechars` / `floatformat`。
3. 任一搜尋分頁改用 `{% querystring %}` 保留 `q`。
4. 做一頁展示 `default` 和 `default_if_none` 對 `0` 的差別。
5. 用 `json_script` 把 5 個文章瀏覽數交給前端 console 印出。

---

## 參考資料

- Django 6.1.1 Template language：<https://docs.djangoproject.com/en/6.1/ref/templates/language/>
- Built-in tags / filters：<https://docs.djangoproject.com/en/6.1/ref/templates/builtins/>
- Humanize：<https://docs.djangoproject.com/en/6.1/ref/contrib/humanize/>
- Time zones in templates：<https://docs.djangoproject.com/en/6.1/topics/i18n/timezones/>

---

## 最後記住三件事

1. **格式化留在 template，business rule 留在 Python。**
2. **autoescape 是預設安全線，不要隨便 `safe`。**
3. **如果同一段 presentation logic 重複出現，就考慮 custom filter/tag。**
