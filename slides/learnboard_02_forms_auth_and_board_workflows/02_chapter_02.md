---
marp: true
theme: default
size: 16:9
paginate: true
header: "LearnBoard 02｜表單、帳號與留言權限"
footer: "Django 初學者課程｜LearnBoard"
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
  h1 { color: #1e3a8a; }
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

# 第 2 章
## 身份驗證：註冊、登入與 session

目標：理解「使用者是誰」如何被伺服器記住，以及密碼為何不能存明文。

<!--
授課提示：本章的三個心智模型——session 是旅館櫃台、cookie 是房卡、密碼雜湊是單向碎紙機——值得板書。
-->

---

## HTTP 是無狀態的，但我們需要記得人

每個 request 都是獨立的——伺服器天生不記得上一秒是誰在連線。

要做出「登入」這件事，需要三件套：

1. **User 帳號**存在資料庫
2. **session**：伺服器端的「已登入名單」
3. **cookie**：瀏覽器持有的憑證（sessionid）

---

## session 心智模型：旅館櫃台

```text
登入成功：
  伺服器建立 session（櫃台登記簿）→ id 存入瀏覽器 cookie（房卡）

之後每個 request：
  瀏覽器自動帶 sessionid cookie（出示房卡）
  Django 查 session → 找到 user → request.user 可用

登出：
  刪掉 session（註銷登記）；房卡作廢
```

cookie 只有 id，不含個資；真正的狀態在伺服器的 django_session 表。

---

## 密碼為什麼不能存明文？

資料庫外洩時，明文密碼直接淪陷；多數人跨站共用密碼，災害擴大。

Django 用 PBKDF2 雜湊儲存：

```text
輸入密碼 ──PBKDF2(多次迭代+鹽)──► 固定長度亂碼字串
驗證：對輸入做同樣計算，比對兩串亂碼是否相同
```

**單向**：由亂碼反推原密碼幾乎不可行。

```bash
uv run python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.first().password
'pbkdf2_sha256$870000$Ab3…'
```

---

## RegistrationForm：繼承 UserCreationForm

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class RegistrationForm(BootstrapFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_bootstrap()
```

UserCreationForm 免費提供 username＋password1/password2 兩次確認＋密碼強度驗證（settings 的 AUTH_PASSWORD_VALIDATORS）。

---

## register view：建立帳號並自動登入

```python
# board/views.py（目前 LearnBoard 實作｜逐字摘錄）
from django.contrib.auth import login


def register(request):
    if request.user.is_authenticated:
        return redirect("board:list")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "註冊成功，歡迎加入學言板！")
        return redirect("board:list")
    return render(request, "registration/register.html", {"form": form})
```

同一份 form 同時服務 GET（顯示）與 POST（驗證）——生命週期的完整落地。

---

## 登入／登出：Django 內建 view

```python
# config/urls.py
from django.contrib.auth import views as auth_views

path("accounts/login/", auth_views.LoginView.as_view(
        template_name="registration/login.html"), name="login"),
path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
```

LoginView 已經處理：渲染表單、呼叫 authenticate/login、依 `?next=` 轉址。

settings 決定去留：

```python
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "board:list"
LOGOUT_REDIRECT_URL = "board:list"
```

> LogoutView 只接受 POST——防止 `<img src="/accounts/logout/">` 這類被動登出攻擊。所以 base.html 的登出按鈕是一個小 form。

---

## authenticate + login：內建 view 底下做了什麼

```python
from django.contrib.auth import authenticate, login

user = authenticate(request, username="alice", password="輸入的密碼")
if user is not None:      # None 代表帳密不符
    login(request, user)  # 建立 session，寫入 request.user
```

- `authenticate`：對照雜湊，確認身份
- `login`：建立 session，把 user 綁上去
- 之後所有 view 都能用 `request.user`

---

## login_required：函式版的門禁

```python
from django.contrib.auth.decorators import login_required


@login_required
def my_page(request):
    ...
```

未登入者 → 302 到 `LOGIN_URL`，並帶上 `?next=/my-page/`：

```text
/accounts/login/?next=/my-page/
```

登入成功後 LoginView 把人送回 next 指的地方。整條鏈路零自訂程式碼。

---

## LoginRequiredMixin：CBV 版的門禁

```python
from django.contrib.auth.mixins import LoginRequiredMixin


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "board/message_form.html"
```

行為與 decorator 相同：未登入 302 到登入頁。

mixin 放在最前面（MRO 慣例），語意是「先驗身份，再做事」。

---

## template 中的 user 與登入狀態切換

```html
{% if user.is_authenticated %}
  <li><a href="{% url 'board:create' %}">發表留言</a></li>
  <li><span>嗨，{{ user.username }}</span></li>
  <li><form method="post" action="{% url 'logout' %}">
        {% csrf_token %}<button>登出</button></form></li>
{% else %}
  <li><a href="{% url 'login' %}">登入</a></li>
  <li><a href="{% url 'board:register' %}">免費註冊</a></li>
{% endif %}
```

`user` 由 auth context processor 注入每個模板——不需要 view 特別傳。

---

## 第 2 章｜觀念檢核與實作

**觀念檢核：**

1. sessionid cookie 被偷走會發生什麼？這告訴我們 HTTPS 為何重要？
2. `authenticate` 回傳 None 代表什麼？
3. `?next=` 的完整流程是什麼？
4. 為什麼登出要用 POST？

**實作任務：**走完註冊→自動登入→登出→再登入流程；故意輸入錯誤密碼三次，觀察錯誤呈現方式。

→ 步驟與解答在配套手冊第 2 章。
