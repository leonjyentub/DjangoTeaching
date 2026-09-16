---
marp: true
theme: default
paginate: true
---

# P2-6 CI / Release Checklist

部署品質來自「可重複的檢查」，不是上線前記得多小心。

---

# 最小 CI gate

每個 Django 專案至少：

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

Repository 教材再加：

```bash
python scripts/check_material_links.py
```

---

# 為什麼 `makemigrations --check`？

它抓這種情況：

```text
models.py 已改
migration 忘了 commit
```

沒有它，production migrate 可能「成功」但 schema 根本沒包含你的 model change。

---

# CI 不應保存 production secrets

Test settings 使用：

- SQLite / disposable DB
- locmem email/cache
- fake credentials

若 integration test 必須用 secret，使用 CI secret store，不要寫進 YAML。

---

# Release 前 checklist

- tests green
- migrations reviewed
- backup verified
- environment variables present
- `DEBUG=False`
- `ALLOWED_HOSTS` correct
- static collected
- health check ready
- rollback plan understood

Checklist 不是官僚文件，是把記憶外部化。

---

# Release 後驗證

Smoke test：

- homepage 200
- login/logout
- 一個核心 CRUD flow
- static/media 可讀
- DB write 正常
- error log 沒爆量
- scheduled job 有在跑

---

# 監看 deployment

上線後短時間重點看：

- 5xx rate
- latency
- database errors
- login failures
- background job failures
- disk/storage usage

不要部署完就關 terminal 當作完成。

---

# Roll forward vs rollback

小錯誤有時候最快是 hotfix roll forward；重大或未知風險才 rollback。

重點是事先知道：

- code 是否可 rollback
- migration 是否相容
- data 是否被不可逆修改

---

# 本章檢核

1. CI 最小三個 Django command 是什麼？
2. `makemigrations --check` 抓哪一類錯？
3. release checklist 為何有價值？
4. deploy 後為什麼還要 smoke test / monitor？
