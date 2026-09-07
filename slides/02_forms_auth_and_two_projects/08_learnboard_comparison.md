---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 02｜表單、身份驗證與工作流程"
footer: "初學者教材｜LearnBoard × LearnMart"
---

# LearnBoard 對照實作
## 表單與 server-owned author

目前 `learnboard/board/views.py` 的新增留言流程：表單只提供 `content`，作者由伺服器從 session 指派。

```python
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "board/message_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "留言已發布。")
        return super().form_valid(form)
```

這和 LearnMart 的 `ProductCreateView` 指派 `seller`、checkout 指派 `buyer`／`total` 是同一條規則：**使用者可提交的欄位不等於伺服器可信的欄位。**

---

## LearnBoard 對照實作
### 兩種 ownership 防線

```python
class MessageUpdateView(LoginRequiredMixin, UpdateView):
    def get_queryset(self):
        return Message.objects.filter(author=self.request.user)
```

```python
class OwnerOrStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        obj = self.get_object()
        return obj.author_id == self.request.user.pk or self.request.user.is_staff
```

- 編輯：scoped queryset 讓非作者得到 404
- 刪除：`test_func()` 讓非作者得到 403，staff 可管理
- LearnMart 同樣先檢查 seller role，再以 `seller=self.request.user` 限制商品或訂單

---

## LearnBoard 對照實作
### 測試矩陣如何遷移到商城？

LearnBoard 目前測試已固定這些規則：

| LearnBoard 測試行為 | LearnMart 對應問題 |
|---|---|
| 匿名不能開新增頁 | 匿名不能加入購物車／進入 checkout |
| 建立留言時 author 是登入者 | 建立商品時 seller 是登入者 |
| 非作者編輯得到 404 | 非 owner seller 編輯商品得到 404 |
| 非作者刪除得到 403 | buyer 出貨得到 403 |
| staff 可刪除留言 | seller 只能處理自己商品所在的訂單 |

每增加一條規則，都同時檢查 response、資料是否改變，以及失敗時的 side effects。
