---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnJournal 01｜內容模型與發佈"
footer: "初學者教材｜觀念 → 語法 → LearnJournal 實作"
---

<!-- _class: cover -->

# 第 6 章
## 巢狀留言、`FormMixin` 與 signal 入門

<div class="box">能用自我關聯 FK 做巢狀留言、用 `FormMixin` 讓 `DetailView` 收 POST，並解釋 signal 的用途與取捨</div>

<!--
授課提示：回扣 LearnMart 的 add_review 手工 function view——本章展示「同一件事，用 CBV 的組合方式」。
-->

---

## 6-1 需求：文章頁同時要「顯示」與「收留言」

一個 URL `/2026/08/29/<slug>/` 要做兩件事：

- `GET`：顯示文章 + 現有留言 + 一個空白留言表單
- `POST`：收下新留言，存檔，PRG 導回同一頁

**LearnMart 的做法**（Deck 02）：`ProductDetailView` 只管顯示，另外寫一個 `add_review` function view 處理 POST。

**本章的做法**：用 `FormMixin` 讓一個 `DetailView` 同時做兩件事。

---

## 6-2 `DetailView` 少了什麼？

`DetailView` 只有 `get()`：查一個物件、渲染模板。它沒有：

- `form_class` / `get_form()`（怎麼建表單）
- `post()`（怎麼處理送出）

`FormMixin` 補上這些。組合起來：

```python
class ArticleDetailView(FormMixin, DetailView):
    ...
```

> MRO（方法解析順序）：`FormMixin` 寫在 `DetailView` 前面，它的方法優先。
> （回扣先備教材第 10 章 mixin、LearnMart Deck 02 第 3 章 `LoginRequiredMixin` 放前面）

---

## 6-3 <span class="label current">目前 LearnJournal｜節錄</span> `ArticleDetailView` 骨架

**`journal/views.py`**

```python
class ArticleDetailView(FormMixin, DetailView):
    template_name = "journal/article_detail.html"
    context_object_name = "article"
    form_class = CommentForm

    def get_queryset(self):
        return Article.published.prefetch_related("comments__author", "comments__replies", "reactions")
```

- `form_class = CommentForm`：FormMixin 用它建表單
- `get_queryset()` 從 `Article.published` 出發，並預抓留言與作者（避免 N+1）

---

## 6-4 `GET`：顯示文章並遞增瀏覽數

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/views.py`**

```python
def get(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.register_view()                    # F("view_count") + 1（第 3 章）
    context = self.get_context_data(object=self.object)
    return self.render_to_response(context)
```

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context.setdefault("form", self.get_form())     # 空白留言表單
    context["top_comments"] = self.object.comments.filter(parent__isnull=True, is_approved=True)
    context["reaction_counts"] = self.object.reactions.values("kind").annotate(n=Count("id"))
    return context
```

---

## 6-5 `POST`：處理留言送出

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/views.py`**

```python
def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    if not request.user.is_authenticated:
        return redirect_to_login(request.get_full_path())
    form = self.get_form()
    if not form.is_valid():
        return self.render_to_response(self.get_context_data(form=form))
    comment = form.save(commit=False)
    comment.article = self.object
    comment.author = request.user                  # server-owned（回扣 author / seller）
    parent_id = request.POST.get("parent")
    if parent_id:
        comment.parent = self.object.comments.filter(pk=parent_id).first()
    comment.save()
    messages.success(request, "留言已送出。")
    return redirect(self.object.get_absolute_url() + "#comments")     # PRG
```

---

## 6-6 逐點對應到已學過的觀念

| 這一行 | 對應的舊觀念 |
|---|---|
| `if not request.user.is_authenticated` | 登入門禁（LearnMart Deck 02 第 2 章） |
| `form.save(commit=False)` | 先不寫入，補伺服器欄位（`author` migration 章） |
| `comment.author = request.user` | server-owned 欄位，不放進表單 fields |
| `comment.parent = ...filter(pk=parent_id)` | 從**這篇文章的**留言找 parent，不信任任意 id（IDOR） |
| `redirect(... + "#comments")` | PRG：POST 後導向，避免重送 |

**沒有新觀念，只是新組合方式。**

---

## 6-7 `CommentForm`：只開放一個欄位

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/forms.py`**

```python
class CommentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)               # 只有內文
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "placeholder": "留下你的想法"})}
```

- `article`、`author`、`parent`、`is_approved` 都**不在** `fields`——由 view 決定
- 回扣 LearnMart：「為什麼 `seller` 不在 `fields`？」同一個原則

---

## 6-8 巢狀顯示：只做兩層

**<span class="label current">目前 LearnJournal｜節錄</span>｜`templates/journal/article_detail.html`**

```django
{% for comment in top_comments %}
  <div class="border-start ps-3">
    <div>{{ comment.author.username }} · {{ comment.created_at|naturaltime }}</div>
    <p>{{ comment.body|linebreaksbr }}</p>            {# 不加 |safe：留言 autoescape #}
    {% for reply in comment.replies.all %}
      {% if reply.is_approved %}
        <div class="border-start ps-3">{{ reply.body|linebreaksbr }}</div>
      {% endif %}
    {% endfor %}
  </div>
{% endfor %}
```

`comment.replies.all` 用的是 `Comment.parent` 的 `related_name="replies"`（第 2 章）。

---

## 6-9 審核：`is_approved`

```python
is_approved = models.BooleanField("已核准", default=True)
```

- 教學版預設 `True`（留言立即顯示）
- 模板只顯示 `is_approved=True` 的留言
- admin 可把灌水留言設成 `False`（`CommentAdmin` 的 `list_editable = ("is_approved",)`）

**Deck 03B 第 9 章**會把預設改成 `False`，並用 signal 在有新留言時通知編輯。

---

## 6-10 signal 入門：存檔的「副作用」放哪裡？

文章存檔後要做的事：

- 把 Markdown 原文渲染成 HTML 存進 `body_html`
- （之後）清掉首頁快取、通知訂閱者……

這些可以寫在 `Article.save()` 裡，也可以用 **signal**：

> signal = 「某件事發生時，通知有登記的函式」。發訊的一方**不需要知道**誰在聽。

---

## 6-11 <span class="label current">目前 LearnJournal｜逐字摘錄</span> `post_save` signal

**`journal/signals.py`**

```python
import markdown as md
from django.db.models.signals import post_save
from django.dispatch import receiver
from journal.models import Article

@receiver(post_save, sender=Article)
def render_markdown(sender, instance, **kwargs):
    html = md.markdown(instance.body or "", extensions=["fenced_code", "tables", "toc"])
    if html != instance.body_html:
        Article.objects.filter(pk=instance.pk).update(body_html=html)   # 不會再觸發 post_save
```

- `@receiver(post_save, sender=Article)`：Article 存檔後呼叫這個函式
- 用 `update()` 寫 `body_html`：避免再次觸發 `post_save` 造成無限迴圈

---

## 6-12 signal 要「被連上」才會作用

**<span class="label current">目前 LearnJournal｜逐字摘錄</span>｜`journal/apps.py`**

```python
class JournalConfig(AppConfig):
    name = "journal"

    def ready(self):
        from journal import signals        # 匯入才會註冊 @receiver
```

沒有 `ready()` 裡這行 import，`@receiver` 裝飾器根本沒被執行，signal 不會觸發。

---

## 6-13 <span class="label warning">常見錯誤／限制</span> signal 的取捨

| signal 的好處 | signal 的壞處 |
|---|---|
| 發訊方不需知道誰在聽（低耦合） | 副作用藏在別的檔案，讀 `save()` 看不出來 |
| 多個 app 可各自掛鉤 | 執行順序不保證、難除錯 |
| 內建事件（`post_save`、`m2m_changed`…）現成 | 測試時常常忘記它會跑 |

> **判準**：跨 app、或「本來的程式碼不該知道」的副作用 → signal。
> 同一個 app、邏輯上就屬於存檔的一部分（例如產生 slug）→ 直接寫在 `save()`。

---

## 6-14 完整 request flow：送出一則回覆

```text
POST /2026/8/29/<slug>/   body=... parent=12
  → ArticleDetailView.post()
  → get_object(): Article.published + 日期/slug → 404 or 文章
  → 未登入 → redirect_to_login
  → CommentForm(is_valid?) → 否：重渲染頁面帶錯誤
  → form.save(commit=False) → 補 article / author / parent
  → comment.save() → post_save(Comment) 觸發（目前 no-op，Deck 03B 寄信）
  → redirect 到 get_absolute_url() + "#comments"（PRG）
```

> **你應該看到**：送出後回到文章頁，新回覆出現在對應留言下方，網址沒有殘留 POST。

---

## 6-15 這一章測了什麼

**<span class="label current">目前 LearnJournal｜節錄</span>｜`journal/tests.py`**

```python
def test_anonymous_cannot_post_comment(self):
    response = self.client.post(article.get_absolute_url(), {"body": "匿名留言"})
    self.assertEqual(response.status_code, 302)
    self.assertEqual(Comment.objects.count(), 0)

def test_logged_in_user_can_reply(self):
    root = Comment.objects.create(article=article, author=self.amy, body="root")
    self.client.login(username="ben", password="pw-ben-12345")
    self.client.post(article.get_absolute_url(), {"body": "回覆", "parent": root.pk})
    reply = Comment.objects.get(body="回覆")
    self.assertEqual(reply.parent, root)
    self.assertEqual(reply.author, self.ben)
```

---

## 第 6 章｜觀念檢核與實作

1. `DetailView` 少了哪些東西，需要 `FormMixin` 補？為什麼 `FormMixin` 寫在前面？
2. `comment.author = request.user` 為什麼不放進 `CommentForm.Meta.fields`？
3. 從 `request.POST["parent"]` 取 parent 時，為什麼要 `self.object.comments.filter(pk=...)` 而不是 `Comment.objects.get(pk=...)`？
4. `render_markdown` signal 為什麼用 `update()` 而不是 `instance.save()`？
5. 什麼副作用適合用 signal，什麼適合直接寫在 `save()`？

**實作任務：**把 `Comment` 預設改成 `is_approved=False`，在 `post()` 成功後改成顯示「留言待審核」訊息；新增測試確認未核准留言不出現在文章頁，但作者本人看得到自己的。

**<span class="label check">配套實作手冊</span>：**[第 6 章答案與步驟](../workbooks/learnjournal_01_content_model_and_publishing_workbook.md#chapter-6)
