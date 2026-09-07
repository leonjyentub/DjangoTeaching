---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnBoard 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnBoard｜可搜尋留言牆
## ListView 的實際設定

```python
class MessageListView(ListView):
    model = Message
    template_name = "board/message_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context
```

`posts`、`query` 與 `page_obj` 是這個模板需要的列表狀態。分頁連結必須保留 `q`，否則翻頁會遺失搜尋條件。

---

## LearnBoard 驗收條件

- `/?q=...` 只顯示內容相符的留言，且搜尋框保留關鍵字。
- 新增第 11 則留言後，可看見 10 筆一頁的分頁。
- 沒有資料時顯示空狀態；訪客留言不會因缺少作者而造成 500。
- 最新留言位於最上方，這是 `Message.Meta.ordering` 的結果。

共通 vertical slice、GET state、pagination 與 template include 請見整合教材第 6 章。
