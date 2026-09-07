---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnMart 02｜表單、身份驗證與商城工作流程"
footer: "Django 初學者課程｜LearnMart"
---

# 第 2 章
## 身份驗證、Session 與帳號流程

目標：知道「你是誰」如何跨 request 保留，並把 authentication 與 authorization 分開。

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

[步驟與觀察表](../workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md#chapter-2)
