---
marp: true
theme: default
paginate: true
---

# P2-4 Process / Reverse Proxy / Logging

`runserver` 是開發伺服器，不是 production process manager。

---

# Production request path

常見架構：

```text
Internet
  ↓ HTTPS
Reverse proxy / load balancer
  ↓
WSGI/ASGI server
  ↓
Django
```

每一層都有不同責任。

---

# Reverse proxy 常做什麼？

- TLS termination
- domain / virtual host
- static file serving
- request size / timeout
- rate limit
- compression
- access log

Django 不需要自己做完所有網路層工作。

---

# WSGI / ASGI server

Django 提供：

- `config/wsgi.py`
- `config/asgi.py`

Production 常交給 Gunicorn、uWSGI、Uvicorn/Daphne 或平台內建 server。

選擇取決於 sync/async、平台與運維方式，不是「哪個名字最潮」。

---

# Process manager 要解決什麼？

- crash 後重啟
- 多 worker
- graceful shutdown
- boot on restart
- stdout/stderr 收集
- health check

systemd、container orchestrator、PaaS 都可以扮演這個角色。

---

# Log 不只 `print()`

至少分：

- application log
- access log
- error log
- audit/security log（視需求）

Production log 應可搜尋、保留適當期間，且不要洩漏 secrets/password/token。

---

# Django logging 心智模型

```python
import logging
logger = logging.getLogger(__name__)

logger.info("article published", extra={...})
```

真正 production 可以把 handler 指到 stdout，再由平台集中收集。

---

# 可觀測性

至少知道三種訊號：

- logs：發生了什麼
- metrics：整體趨勢
- traces：一次 request 穿過哪些服務

本課先把 log、HTTP status、response time 建立起來，再延伸監控。

---

# Health check

Health endpoint 不等於「首頁回 200」。

要思考：

- process alive
- app ready
- database 是否必要
- 外部 service 掛掉時是否也要判 unhealthy

過度嚴格的 health check 也可能造成重啟風暴。

---

# 本章檢核

1. reverse proxy 與 Django 各負責什麼？
2. process manager 為什麼比 `nohup runserver` 好？
3. 哪些資料不應出現在 log？
4. health check 為什麼不一定要檢查所有外部服務？
