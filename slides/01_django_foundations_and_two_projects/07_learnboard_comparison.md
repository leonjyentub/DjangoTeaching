---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 01｜共通基礎：LearnBoard × LearnMart"
footer: "初學者教材｜共通觀念 → 兩個專案對照"
---

# LearnBoard 對照實作
## 同一個 vertical slice，資料領域不同

以下是目前 `learnboard/board/views.py` 的真實查詢骨架；它和前面 LearnMart 的 `ProductListView` 使用同一個 CBV／QuerySet／context 模式。

```python
class MessageListView(ListView):
    model = Message
    template_name = "board/message_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        queryset = Message.objects.select_related("author")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(Q(content__icontains=query))
        return queryset
```

| LearnBoard | LearnMart |
|---|---|
| `posts` | `products` |
| 只查 `content` | 查 `name` 或 `description`，另加 `category` |
| `select_related("author")` | `select_related("category", "seller")` |

---

## LearnBoard 的資料模型與 migration 故事

```python
class Message(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

- `0001_initial.py` 先建立留言與時間欄位
- `0002_message_author.py` 再加入可為空的 `author`
- `SET_NULL` 保留使用者刪除後的留言內容

LearnMart 則從初始 migration 就使用自訂 `marketplace.User`，再由 `Product`、`Order` 等模型建立較完整的關聯。

---

## LearnBoard 的搜尋與模板輸出

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["query"] = self.request.GET.get("q", "")
    return context
```

```django
{% for post in posts %}
  <article class="card">
    <p>{{ post.content }}</p>
    <small>{{ post.author|default:"訪客" }}</small>
  </article>
{% empty %}
  <p>目前沒有符合條件的留言。</p>
{% endfor %}
```

同樣的資料流在 LearnMart 會變成商品卡、分類連結、圖片 fallback 與共用 pagination partial；核心仍是「View 準備 context，Template 負責呈現」。
