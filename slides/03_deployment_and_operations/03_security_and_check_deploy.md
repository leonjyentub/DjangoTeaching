---
marp: true
theme: default
paginate: true
---

# P2-3 Security / `check --deploy`

Production security 不是一個 setting，而是一組互相配合的邊界。

---

# 先跑 Django 自己的檢查

```bash
DJANGO_DEBUG=0 \
DJANGO_SECRET_KEY='a-long-random-secret' \
DJANGO_ALLOWED_HOSTS='example.com' \
uv run python manage.py check --deploy
```

不要只看「System check identified no issues」；讀懂每個 warning 在保護什麼。

---

# DEBUG 必須關

`DEBUG=True` 可能暴露：

- stack trace
- settings/context
- SQL/debug 資訊
- filesystem path

production error page 應對使用者簡潔，詳細資訊寫 log。

---

# HTTPS 與 secure cookies

HTTPS 不只是登入頁。

Production 通常需要：

```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

若 TLS 在 reverse proxy 終止，還要正確設定 proxy header，避免 Django 誤判 request scheme。

---

# CSRF / XSS / Clickjacking

這些不是「前面課過就結束」：

- CSRF middleware 不要隨便關
- template autoescape 不要濫用 `safe`
- user HTML 要 sanitize
- `X_FRAME_OPTIONS` / CSP 依需求設定
- upload 內容也要視為不可信

---

# Security headers

LearnJournal 示範：

```python
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
```

真正 production 還要依架構評估 HSTS、CSP、Referrer-Policy 等。

---

# Rate limiting / brute force

Django core 不替你的所有 endpoint 做 rate limit。

要針對：

- login
- password reset
- registration
- comments/reviews
- expensive search

在 proxy、middleware 或專用套件層處理。

---

# 本章檢核

1. `check --deploy` 是自動修復嗎？
2. TLS 在 proxy 終止時 Django 為什麼可能不知道原始 request 是 HTTPS？
3. `safe` filter 為什麼是安全邊界？
4. 哪些 endpoint 特別需要 rate limit？
