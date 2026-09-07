---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnBoard 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnBoard｜Message 的資料規則
## 一則留言如何保留作者與時間？

```python
class Message(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name="messages",
    )
    content = models.TextField("留言內容", max_length=500)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        ordering = ["-created_at"]
```

刪除作者時保留歷史留言（`SET_NULL`）；最新留言先顯示（`-created_at`）。這與商城需要保護訂單歷史的多重關聯不同。

---

## migration 與 admin 的專屬歷史

- `board/migrations/0001_initial.py` 建立最初的 `Message`。
- `board/migrations/0002_message_author.py` 是後來加入作者欄位的歷史證據。
- `board/admin.py` 的 `MessageAdmin` 顯示 id、作者、短內容與建立時間，並可搜尋內容或作者名稱。

共通的 model、migration、admin 原理請見整合教材第 4 章；本頁只用來回查 LearnBoard 的實際 schema 演進。
