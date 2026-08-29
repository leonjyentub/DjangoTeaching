---
marp: true
theme: default
size: 16:9
paginate: true
header: "LearnBoard 02｜表單、帳號與留言權限"
footer: "Django 初學者課程｜LearnBoard"
style: |
  section {
    font-family: 'Noto Sans CJK TC', 'Noto Serif CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', 'Heiti TC', sans-serif;
    font-size: 28px;
    line-height: 1.35;
  }
  h1, h2 {
    font-family: 'Noto Sans CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', sans-serif;
  }
  h1 { color: #1e3a8a; }
  h2 { color: #17324d; }
  blockquote {
    font-family: 'Noto Serif CJK TC', 'Noto Sans CJK TC', 'WenQuanYi Zen Hei', serif;
  }
  code, kbd {
    font-family: 'Noto Sans Mono CJK TC', 'SF Mono', Consolas,
                 'WenQuanYi Zen Hei Mono', 'Courier New', monospace;
    font-size: 0.82em;
  }
  pre { margin-top: 0.35em; margin-bottom: 0.35em; }
  .label { display: inline-block; padding: 0.15em 0.55em; border-radius: 999px; font-size: 0.72em; font-weight: 700; background: #e8eef5; color: #17324d; }
  .current { background: #e5f4ea; color: #17633a; }
  .warning { background: #fff0d9; color: #8a4b08; }
  .check { background: #f3e8ff; color: #6b21a8; }
  .small { font-size: 0.78em; }
---

# 第 4 章
## CBV 與物件擁有權

目標：實作「只能編輯／刪除自己的留言」，並分辨兩種拒絕方式（404 vs 403）。

<!--
授課提示：本章的防禦是雙層的——QuerySet 過濾與 test_func。請學生各用一句話說出兩層各自擋下誰。
-->

---

## 擁有權：身份之外的第二道門

到目前為止的門禁只問「你有沒有登入」。

但 bob 登入後不該編輯 alice 的留言：

- **Authentication**：你是誰？（第 2 章）
- **Object ownership / authorization**：*這個物件*歸你管嗎？（本章）

商城對照：買家能看自己的訂單，不能看別人的；賣家只能管理自己的商品。

---

## UpdateView：編輯的最小骨架

```python
class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "board/message_form.html"
```

UpdateView 依 URL 的 `<int:pk>` 抓物件、用同一個 ModelForm 預填、合法就 save()。

模板不需要區分新增/編輯——`{% if object %}` 可判斷目前模式：

```html
<h1>{% if object %}編輯留言{% else %}發表留言{% endif %}</h1>
```

---

## 第一層防禦：QuerySet 過濾

```python
class MessageUpdateView(LoginRequiredMixin, UpdateView):
    ...
    def get_queryset(self):
        return Message.objects.filter(author=self.request.user)
```

CBV 抓物件的 `get_object()` 是從**這個 queryset**抓的。

bob 打開 `/messages/<alice的id>/edit/`：

- queryset 只含 bob 的留言
- 查無此物件 → **404**

**攻擊者甚至無法確認那個 id 存在。**

---

## 第二層防禦：test_func 明確判斷

刪除走另一條路——管理員可以刪任何人的留言，所以不能用 queryset 過濾：

```python
# board/views.py（目前 LearnBoard 實作｜逐字摘錄）
class OwnerOrStaffMixin(LoginRequiredMixin, UserPassesTestMixin):
    """作者本人可以操作；is_staff 管理員可以管理任何留言。"""

    raise_exception = True

    def test_func(self):
        obj = self.get_object()
        return obj.author_id == self.request.user.pk or self.request.user.is_staff


class MessageDeleteView(OwnerOrStaffMixin, DeleteView):
    model = Message
    template_name = "board/message_confirm_delete.html"
    success_url = reverse_lazy("board:list")
```

---

## 403 vs 404：兩種拒絕的語意

| 做法 | 觸發結果 | 訊息 |
|---|---|---|
| QuerySet 過濾 | 404 Not Found | 「查無此物件」（不洩漏存在性） |
| UserPassesTestMixin + `raise_exception=True` | 403 Forbidden | 「我知道它在，但你不行動它」 |

- 一般使用者編輯他人留言 → 404（隱匿存在性）
- 管理員流程需要「看得到但部分操作受限」→ 403

**兩層可以同時存在**；重點是你有意識地選擇，而不是不小心漏防。

---

## DeleteView：確認頁與 POST

```html
{# board/message_confirm_delete.html #}
<form method="post">
  {% csrf_token %}
  <button class="btn btn-danger">確認刪除</button>
  <a class="btn btn-outline-secondary" href="{% url 'board:list' %}">取消</a>
</form>
```

- GET 顯示確認頁、POST 才真的刪——避免爬蟲或預覽誤觸
- `success_url = reverse_lazy("board:list")`：URLconf 載入階段 reverse 尚不可用，所以用 lazy 版本

> **常見錯誤：**在類別屬性寫 `reverse(...)` → `ImproperlyConfigured` 或循環匯入。類別載入時機問題就用 `reverse_lazy`。

---

## 模板中的權限感知按鈕

```html
{% if post.author == user %}
  <a class="btn btn-outline-primary btn-sm" href="{% url 'board:update' post.pk %}">編輯</a>
  <a class="btn btn-outline-danger btn-sm" href="{% url 'board:delete' post.pk %}">刪除</a>
{% elif user.is_staff %}
  <a class="btn btn-outline-danger btn-sm" href="{% url 'board:delete' post.pk %}">刪除</a>
{% endif %}
```

模板按鈕只是**體驗**；真正的關卡永遠在 view（queryset/test_func）。

直接打網址繞過按鈕？view 會擋——這才是安全的分界。

---

## 手動實測 IDOR 場景

```text
1. alice 登入 → 對某留言按右鍵複製編輯網址 → 登出
2. bob 登入 → 貼上 alice 的編輯網址
   → 404（queryset 過濾生效）
3. bob 改貼 delete 網址
   → 403（OwnerOrStaffMixin 生效）
4. staff 登入 → 同一個 delete 網址
   → 200 確認頁，可刪除
```

四種身份、兩種拒絕、一種放行——全部符合預期才算通關。

---

## 第 4 章｜觀念檢核與實作

**觀念檢核：**

1. `get_queryset` 過濾如何同時做到授權與「隱匿存在性」？
2. 為什麼刪除不用 queryset 過濾，而用 test_func？
3. `reverse_lazy` 解決什麼時序問題？
4. 為什麼說「模板藏按鈕不算安全措施」？

**實作任務：**完整跑一遍 4-9 的四身份實測；截圖或筆記每一步的狀態碼。

→ 步驟與解答在配套手冊第 4 章。
