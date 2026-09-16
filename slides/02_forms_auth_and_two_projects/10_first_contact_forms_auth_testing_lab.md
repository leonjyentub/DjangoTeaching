---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 02｜第一次表單／Auth／測試操作導引"
footer: "補充 lab｜POST、CSRF、session、權限、測試失敗定位"
---

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
