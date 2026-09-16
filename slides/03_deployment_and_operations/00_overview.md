---
marp: true
theme: default
paginate: true
---

# 03 Deployment / Operations
## 從「本機可跑」到「可部署、可維護」

適用：LearnBoard、LearnMart、LearnJournal。

---

# 為什麼做成共用單元？

三個專案都會遇到同一批 production 問題：

- SECRET_KEY / DEBUG / ALLOWED_HOSTS
- static / media
- database
- HTTPS / cookies / security headers
- process / reverse proxy
- logging / monitoring
- migrations / backup / rollback
- CI / release checklist

不需要複製三份。

---

# 本機與 production 的差別

本機常見：

```text
runserver + SQLite + DEBUG=True + local files
```

production 常見：

```text
reverse proxy
   ↓ HTTPS
WSGI/ASGI process manager
   ↓
Django
   ↓
PostgreSQL / shared cache / object storage
```

---

# 這個單元不綁供應商

你可以把概念套到：

- VM
- Docker / container platform
- PaaS
- school server
- managed database

真正要學的是責任邊界與驗證方式。

---

# 建議順序

1. Settings / Environment Variables
2. Static / Media / Database
3. Security / `check --deploy`
4. Process / Reverse Proxy / Logging
5. Migrations / Backup / Recovery
6. CI / Release Checklist

---

# 配套手冊

[`../workbooks/03_deployment_and_operations_workbook.md`](../workbooks/03_deployment_and_operations_workbook.md)
