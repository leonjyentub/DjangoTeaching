---
marp: true
theme: default
paginate: true
---

# LearnJournal 03B Summary

你已經把「內容網站」推進到具有狀態、傳播、排程與效能考量的系統。

---

# Request 內外的責任

```text
Browser
  cookies
    ↓
Middleware
  session/auth/timing
    ↓
View + ORM
    ↓
Cache / DB
    ↓
Email / Feed / Sitemap
    ↓
Scheduled commands
```

每一層都有不同生命週期與失敗模式。

---

# 能力矩陣

| 主題 | 你應該能回答 |
|---|---|
| Session/Cookie | 資料存在 client 還是 server？可信嗎？ |
| Cache | key、TTL、invalidation 怎麼設計？ |
| Middleware | 順序與 short-circuit 有何影響？ |
| Email | token 與 side effect 怎麼測？ |
| Permission | capability 與 ownership 怎麼分？ |
| RSS/Sitemap | 公開 QuerySet 如何重用？ |
| Commands | 如何 dry-run、重跑、排程？ |
| PostgreSQL FTS | substring 和 ranking 差在哪？ |

---

# 最後驗證

```bash
cd learnjournal
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
python ../scripts/check_material_links.py --root ..
```

若切 PostgreSQL：

```bash
uv sync --extra postgres
uv run python manage.py migrate
```

---

# 下一步：P2 Deployment / Operations

03B 到這裡仍是「功能完整的教學應用」。

接下來要回答：

- secrets 放哪？
- DEBUG 關掉後 static 怎麼辦？
- migration 怎麼安全部署？
- process 怎麼被監控／重啟？
- DB/媒體怎麼備份？
- 怎麼用 `check --deploy`？

這些放在跨三專案共用的 Deployment / Operations 單元。
