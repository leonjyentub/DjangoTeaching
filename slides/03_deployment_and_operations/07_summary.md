---
marp: true
theme: default
paginate: true
---

# Deployment / Operations Summary

把 Django 專案上線，不是把 `runserver` 換成另一條指令而已。

---

# Production readiness 地圖

```text
Code + tests
   ↓
Environment / secrets
   ↓
Database + migrations
   ↓
Static / media
   ↓
WSGI/ASGI + proxy + HTTPS
   ↓
Logs / health / monitoring
   ↓
Backup / restore / scheduler
```

---

# 三個專案各自回扣

| 專案 | Production 特別要注意 |
|---|---|
| LearnBoard | auth、rate limit、audit log |
| LearnMart | media、交易、庫存、付款邊界 |
| LearnJournal | cache、email、scheduler、search、feed |

共通基礎仍是同一套 deployment discipline。

---

# 最後驗證

每個專案：

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

Repository：

```bash
python scripts/check_material_links.py
```

Production-like settings：

```bash
uv run python manage.py check --deploy
```

---

# 完成這門課後應具備的能力

你不只會「把頁面做出來」，還能：

- 說明 request/data/security 邊界
- 寫可測試的 workflow
- 管理 schema 演進
- 區分 local 與 production settings
- 說明 cache / email / scheduler / DB 的運維責任
- 用 checklist 與自動化降低部署風險
