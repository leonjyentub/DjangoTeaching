---
marp: true
theme: default
paginate: true
---

# 03B-2 Custom Middleware

Middleware 是包住 view 的 request/response pipeline。

```text
request
  ↓ Security
  ↓ Session
  ↓ Auth
  ↓ our middleware
  ↓ URL resolver → view
  ↑ response
```

---

# 最小 middleware 形狀

```python
class ExampleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # before view
        response = self.get_response(request)
        # after view
        return response
```

先看 control flow，再看框架魔法。

---

# 範例一：Response Time

```python
started = perf_counter()
response = self.get_response(request)
elapsed_ms = (perf_counter() - started) * 1000
response["X-Response-Time"] = f"{elapsed_ms:.2f}ms"
```

瀏覽器 DevTools → Network → Response Headers 可以直接看到結果。

---

# 用 curl 看 header

```bash
curl -I http://127.0.0.1:8000/
```

找：

```text
X-Response-Time: 12.34ms
```

如果 Windows 沒有 curl，可直接用瀏覽器 Network 面板。

---

# 範例二：提早結束 request

Maintenance middleware 可以不呼叫 view：

```python
if settings.MAINTENANCE_MODE:
    return HttpResponse("網站維護中", status=503)
return self.get_response(request)
```

這叫 **short-circuit**。

---

# Middleware 順序不是裝飾

我們的 maintenance middleware 需要 `request.user`：

```python
"django.contrib.auth.middleware.AuthenticationMiddleware",
"journal.middleware.MaintenanceModeMiddleware",
```

若放到 AuthenticationMiddleware 前面，`request.user` 尚未被建立。

---

# 開啟維護模式

macOS/Linux:

```bash
DJANGO_MAINTENANCE_MODE=1 uv run python manage.py runserver
```

PowerShell:

```powershell
$env:DJANGO_MAINTENANCE_MODE="1"
uv run python manage.py runserver
```

首頁應回 503；accounts/admin 仍保留入口。

---

# 不要在 middleware 做什麼？

- 每個 request 都做昂貴 DB 查詢
- 把 domain business rule 全塞進去
- 靜默吞掉 exception
- 修改 response 但沒有文件或測試

Middleware 適合橫切 concerns：安全、追蹤、locale、request metadata。

---

# 測試

```python
response = self.client.get(reverse("journal:home"))
self.assertIn("X-Response-Time", response)
```

測行為，不測 `perf_counter()` 的實作細節。

---

# 本章檢核

1. middleware 的 before/after view 分別在哪？
2. 為什麼 Auth middleware 的順序重要？
3. HTTP 503 和 redirect 到首頁有何語意差異？
4. 哪些需求適合 middleware，哪些應該留在 view/service？
