---
marp: true
theme: default
paginate: true
---

# 03B-3 Email / Password Reset / Double Opt-in

Email 本身不難；難的是 token、身份、重送與 side effect。

---

# 先用 console backend

```python
MAILERS = {
    "default": {
        "BACKEND": "django.core.mail.backends.console.EmailBackend",
        "OPTIONS": {},
    }
}
```

好處：

- 不需要 SMTP 帳密
- 信件完整內容出現在 terminal
- 可以直接複製 reset / confirmation URL
- 適合先理解流程，再談寄信服務

---

# 密碼重設不是自己做 token

Django 已提供：

- `PasswordResetView`
- `PasswordResetDoneView`
- `PasswordResetConfirmView`
- `PasswordResetCompleteView`

我們只配置 URL 與 template。

---

# 操作密碼重設

1. 用 `amy@example.com` 對應帳號。
2. 開 `/accounts/password-reset/`。
3. 送出 email。
4. 回到 runserver terminal。
5. 複製 `/accounts/reset/<uid>/<token>/` URL。
6. 設新密碼，再重新登入。

注意：頁面不應透露「某 email 是否存在帳號」。

---

# Double opt-in

訂閱表單只做第一步：

```text
POST email
  ↓
建立 Subscription(is_confirmed=False, token=...)
  ↓
寄確認信
  ↓
使用者點 token URL
  ↓
is_confirmed=True
```

只有 confirmed subscriber 才能進 weekly digest。

---

# 為什麼用 secrets？

```python
secrets.token_urlsafe(32)
```

不要用：

```python
random.randint(...)
```

`random` 用於模擬／遊戲；安全 token 用 `secrets`。

---

# build_absolute_uri

email 需要完整 URL：

```python
confirm_url = request.build_absolute_uri(
    reverse("journal:confirm-subscription", args=[sub.token])
)
```

`reverse()` 只給 path；`build_absolute_uri()` 把 scheme/host 補上。

---

# Signal 寄留言通知

Comment `post_save`：

- 只在 `created=True`
- 作者有 email 才寄
- 自己留言不寄給自己
- 開發環境印到 terminal

這是 signal 適合討論的副作用案例，但也要知道它讓 control flow 變隱性。

---

# 測試 email 不碰真 SMTP

```python
@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
)
def test_subscription(...):
    ...
    self.assertEqual(len(mail.outbox), 1)
```

測試關心「有沒有寄、寄給誰、內容是否有 token」。

---

# 常見錯誤

- terminal 沒看到信：確認 backend 與執行 server 的 terminal
- reset URL host 不對：檢查 request host / proxy config
- token 重複使用：reset token 應失效；訂閱 confirm endpoint 要 idempotent
- 把 SMTP 密碼寫進 settings.py：production 改用環境變數

---

# 本章檢核

1. password reset 為何不應顯示「email 不存在」？
2. double opt-in 解決什麼問題？
3. `reverse()` 和 `build_absolute_uri()` 的輸出差在哪？
4. 測試寄信為什麼用 locmem backend？
