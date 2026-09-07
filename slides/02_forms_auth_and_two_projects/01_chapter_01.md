---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 02｜表單、身份驗證與工作流程"
footer: "初學者教材｜LearnBoard × LearnMart"
---

# 第 1 章
## 完整表單生命週期

目標：能從 HTML 表單一路追到 Django 驗證、儲存、redirect 與 message。

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
