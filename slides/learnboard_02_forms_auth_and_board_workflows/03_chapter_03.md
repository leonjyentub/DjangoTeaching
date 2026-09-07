---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnBoard 02｜表單、帳號與留言權限"
footer: "Django 初學者課程｜LearnBoard"
---

# 第 3 章
## Model 演進：把留言連回作者

目標：體驗一次真實的 schema 演進——資料表已經有資料了，還能加欄位嗎？

<!--
授課提示：本章是本冊的靈魂頁之一。repository 裡的 0002_message_author.py 就是這一章的歷史化石，請務必打開來看。
-->

---

## 現狀：留言沒有作者

Deck 01 的 Message 只有內容與時間戳記。匿名發文版（第 1 章過渡版）也只存 content。

要做出「只能編輯自己的留言」，必須先回答：

**這則留言是誰的？**

→ 需要 `author` 欄位，指向 Django 內建的 User。

---

## 加欄位前先想清楚三件事

| 問題 | 選擇 | 理由 |
|---|---|---|
| 刪掉使用者，留言怎麼辦？ | `on_delete=models.SET_NULL` | 留言保留，作者標示為訪客 |
| 資料庫裡已有舊留言（無作者） | `null=True, blank=True` | 歷史資料允許 NULL |
| 反向查詢叫什麼？ | `related_name="messages"` | `alice.messages.all()` |

> CASCADE vs SET_NULL 是設計決策不是語法題：「作者帳號刪除時，他的留言該消失嗎？」——留言板選擇保留。

---

## 新的 model 定義

```python
# board/models.py（目前 LearnBoard 實作｜節錄）
from django.conf import settings


class Message(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
        verbose_name="作者",
    )
    content = models.TextField("留言內容", max_length=500)
    ...
```

`settings.AUTH_USER_MODEL` 是「本專案的使用者 model」的字串指標——比直接 import User 更穩（未來換自訂 User 不用改）。

---

## makemigrations：Django 偵測到變更

```bash
uv run python manage.py makemigrations board
```

```text
Migrations for 'board':
  board/migrations/0002_message_author.py
    + Add field author to message
```

因為資料表已有舊資料、而新欄位允許 NULL，Django 不需要問你預設值——這正是當初選 `null=True` 換來的順滑。

若欄位是必填（null=False），Django 會互動式追問 default。

---

## 產出的 migration 檔案

```python
# board/migrations/0002_message_author.py
class Migration(migrations.Migration):
    dependencies = [
        ("board", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]
    operations = [
        migrations.AddField(
            model_name="message",
            name="author",
            field=models.ForeignKey(blank=True, null=True,
                on_delete=models.SET_NULL,
                related_name="messages",
                to=settings.AUTH_USER_MODEL,
                verbose_name="作者"),
        ),
    ]
```

注意 `dependencies`：它依賴 0001（自己的表）與 auth app——跨 app 的 schema 順序就是這樣保證的。

---

## migrate 之後的世界

```bash
uv run python manage.py migrate
uv run python manage.py shell
>>> from board.models import Message
>>> Message.objects.filter(author__isnull=True).count()
1        ← 訪客留言（seed_demo 建立的）
>>> from django.contrib.auth.models import User
>>> alice = User.objects.get(username="alice")
>>> alice.messages.all()
<QuerySet [<Message: …>]>
```

`related_name="messages"` 讓反向查詢成立；沒有它就得寫 `message_set`。

---

## 發文時把作者綁上去

```python
# board/views.py（目前 LearnBoard 實作｜逐字摘錄）
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "board/message_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "留言已發布。")
        return super().form_valid(form)
```

- 表單只有 content 欄位 → 作者在伺服器端指定
- **絕不讓前端送 author**：否則可偽造「以別人名義發文」（IDOR 家族）

---

## CreateView 幫你省下的程式碼

等價的 function view：

```python
@login_required
def create_message(request):
    form = MessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        message = form.save(commit=False)   # 先不進 DB
        message.author = request.user       # 補上作者
        message.save()                      # 現在才存
        return redirect("board:list")
    return render(request, "board/message_form.html", {"form": form})
```

CreateView 把 GET/POST 分流與 form_valid 流程模板化；你只需覆寫差異點。

`save(commit=False)`：取得 instance 但先不寫入——補欄位的標準手法。

---

## 模板顯示作者（含訪客保護）

```html
<div class="fw-semibold small">
  {% if post.author %}{{ post.author.username }}{% else %}訪客{% endif %}
</div>
```

Deck 01 已埋好的 `{% if post.author %}` 現在意義完整：NULL author＝歷史訪客留言。

**你應該看到：**登入後發文，卡片顯示你的 username；舊留言仍是「訪客」。

---

## 第 3 章｜觀念檢核與實作

**觀念檢核：**

1. 為什麼選 SET_NULL 而不是 CASCADE？
2. `null=True` 與 `blank=True` 分別影響哪一層？
3. 為什麼用 `settings.AUTH_USER_MODEL` 而不 import User？
4. `form.save(commit=False)` 解決什麼問題？

**實作任務：**檢視 `board/migrations/0002_message_author.py`，說出它的 dependencies 各代表什麼；再新增一則留言，確認作者正確綁定。

→ 步驟與解答在配套手冊第 3 章。
