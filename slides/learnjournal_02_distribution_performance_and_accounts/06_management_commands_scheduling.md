---
marp: true
theme: default
paginate: true
---

# 03B-6 Management Commands / Scheduling

不是每個工作都應該由 HTTP request 觸發。

---

# 什麼適合 command？

- 匯入／匯出資料
- 批次修正
- 排程發佈
- 每週摘要
- 清理過期資料
- 維護任務

Command 是 Django 環境內的 CLI entry point。

---

# `add_arguments`

```python
class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--limit", type=int, default=100)
```

現在指令有可驗證的介面，而不是改 code 才能換參數。

---

# 先 dry-run

```bash
uv run python manage.py publish_scheduled --dry-run
```

確認列出的文章正確後才執行：

```bash
uv run python manage.py publish_scheduled
```

對有副作用的批次工作，`--dry-run` 是非常值得養成的習慣。

---

# 排程文章條件

```python
Article.objects.filter(
    status=Article.Status.SCHEDULED,
    published_at__lte=timezone.now(),
)
```

條件本身要可重跑：已經改成 `PUBLISHED` 的文章，下次不會再次符合。

---

# Transaction 邊界

```python
with transaction.atomic():
    for article in articles:
        article.status = Article.Status.PUBLISHED
        article.save(...)
```

這裡示範「一批一起成功或失敗」。

是否真的要整批 atomic，要依工作量與鎖定成本決定。

---

# Weekly digest

預覽：

```bash
uv run python manage.py send_weekly_digest --dry-run
```

指定 14 天：

```bash
uv run python manage.py send_weekly_digest --days 14
```

只有 `Subscription.is_confirmed=True` 的 email 會收到。

---

# Django 不負責「幾點執行」

Command 定義 **做什麼**；scheduler 定義 **何時做**。

Linux cron 範例：

```cron
*/5 * * * * cd /srv/learnjournal && uv run python manage.py publish_scheduled
0 8 * * 1 cd /srv/learnjournal && uv run python manage.py send_weekly_digest
```

production 也可用 systemd timer、container scheduler、managed cron。

---

# 排程要注意執行環境

Scheduler 必須知道：

- working directory
- Python/uv 路徑
- environment variables
- database credentials
- log 去哪裡
- 同一工作會不會重疊執行

「我手動跑成功」不等於 cron 一定成功。

---

# 測 command

```python
out = StringIO()
call_command("publish_scheduled", "--dry-run", stdout=out)
article.refresh_from_db()
self.assertEqual(article.status, Article.Status.SCHEDULED)
```

再跑非 dry-run，確認 status 變成 published。

---

# 常見錯誤

- command 找不到：檢查 `management/commands/<name>.py`
- cron 找不到 uv：使用絕對路徑或正確 environment
- 重跑重複寄信：設計 idempotency / delivery log
- 一次處理太多：提供 `--limit` 或 chunking

---

# 本章檢核

1. 為什麼 command 和 scheduler 要分開？
2. `--dry-run` 的安全價值是什麼？
3. 怎麼讓 command 可重跑？
4. 什麼情況不適合把整批包在同一個 transaction？
