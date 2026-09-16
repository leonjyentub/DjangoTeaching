# Deployment / Operations Workbook

這份手冊跨 LearnBoard、LearnMart、LearnJournal 共用。目標是把「production readiness」拆成可逐項驗證的工作，而不是綁定某一家雲端平台。

## 1. Environment variables

以 LearnJournal 為例：

macOS/Linux：

```bash
export DJANGO_DEBUG=0
export DJANGO_SECRET_KEY='replace-with-a-long-random-value'
export DJANGO_ALLOWED_HOSTS='example.com,www.example.com'
uv run python manage.py shell -c "from django.conf import settings; print(settings.DEBUG, settings.ALLOWED_HOSTS)"
```

PowerShell：

```powershell
$env:DJANGO_DEBUG="0"
$env:DJANGO_SECRET_KEY="replace-with-a-long-random-value"
$env:DJANGO_ALLOWED_HOSTS="example.com,www.example.com"
uv run python manage.py shell -c "from django.conf import settings; print(settings.DEBUG, settings.ALLOWED_HOSTS)"
```

練習：列出 LearnBoard / LearnMart 還有哪些 production 值應改用 env 管理。

---

## 2. Static / Media

### 2-1 Static

先設定 `STATIC_ROOT`（LearnJournal 已示範），再：

```bash
uv run python manage.py collectstatic --noinput
```

確認輸出目錄真的出現 CSS 等檔案。

### 2-2 Media

LearnMart 有商品圖片。回答：

1. redeploy container 後上傳檔是否還在？
2. 多 worker / 多 instance 是否共用同一份 media？
3. backup 是否同時涵蓋 DB 與 media？

若三題答不出來，就還沒有 production media strategy。

---

## 3. PostgreSQL migration drill

以 LearnJournal：

```bash
uv sync --extra postgres
```

設定 `DJANGO_DB_*` 後：

```bash
uv run python manage.py shell -c "from django.db import connection; print(connection.vendor)"
uv run python manage.py migrate
uv run python manage.py seed_demo
```

關鍵觀察：SQLite 舊資料不會自動搬到 PostgreSQL。

---

## 4. Security check

使用 production-like env：

```bash
DJANGO_DEBUG=0 \
DJANGO_SECRET_KEY='replace-with-a-long-random-value' \
DJANGO_ALLOWED_HOSTS='example.com' \
uv run python manage.py check --deploy
```

逐條讀 warning。請不要把作業答案寫成「因為 Django 說不安全」，而要寫出每個 warning 對應的攻擊面或失敗模式。

檢查：

- DEBUG
- ALLOWED_HOSTS
- secure cookies
- HTTPS redirect / proxy scheme
- HSTS（理解後再開）
- clickjacking / MIME sniffing

---

## 5. Process / Proxy 設計題

畫出你的 production request path：

```text
client → DNS → TLS/proxy → WSGI/ASGI → Django → DB/cache/storage
```

對每一箭頭回答：

- timeout 誰控制？
- log 在哪？
- TLS 在哪終止？
- instance 掛掉誰重啟？
- static/media 從哪裡送？

如果使用 PaaS，也要知道平台替你承擔了哪些責任。

---

## 6. Logging drill

把一個重要事件改成 structured-ish log，而不是 `print()`：

```python
import logging
logger = logging.getLogger(__name__)
logger.info("article_published", extra={"article_id": article.pk})
```

討論哪些資料不能進 log：password、reset token、session cookie、完整付款資訊、secret key。

---

## 7. Migration safety

Release 前：

```bash
uv run python manage.py makemigrations --check
uv run python manage.py showmigrations
uv run python manage.py test
```

設計一個 schema change，寫出 expand → migrate → contract 三階段；不要直接先刪舊欄位。

---

## 8. Backup / Restore drill

教學 SQLite 可做：

```bash
cp db.sqlite3 db.sqlite3.backup
```

做一個可逆的破壞性操作後，停止 server，再 restore。

Production PostgreSQL 請改用資料庫原生或 managed backup。作業要記錄：

- backup time
- restore time
- restored row count
- media 是否同步恢復

「有備份」但從沒 restore 過，不算完成。

---

## 9. CI gate

Repository 現在有教材 link checker：

```bash
python scripts/check_material_links.py
```

每個 Django project：

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

把這些視為 merge gate，而不是考前才跑一次。

---

## 10. Release checklist

### Before

- [ ] CI green
- [ ] migration reviewed
- [ ] backup/restore strategy known
- [ ] env/secrets ready
- [ ] DEBUG=False
- [ ] ALLOWED_HOSTS correct
- [ ] static collected
- [ ] scheduler configured
- [ ] rollback/roll-forward plan known

### After

- [ ] homepage 200
- [ ] login/logout works
- [ ] one core write flow works
- [ ] static/media works
- [ ] logs have no new error burst
- [ ] scheduled command executes
- [ ] latency / 5xx are normal

---

## 11. 三專案比較作業

請填表：

| 問題 | LearnBoard | LearnMart | LearnJournal |
|---|---|---|---|
| 最重要的資料 | | | |
| 最重要的 security boundary | | | |
| media | | | |
| background/scheduled work | | | |
| backup 重點 | | | |
| production 最大風險 | | | |

目的不是找標準答案，而是練習從 domain 反推 operations priorities。
