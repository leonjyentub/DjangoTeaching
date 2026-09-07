---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnBoard 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnBoard｜留言搜尋 QuerySet
## 搜尋只加上一層內容條件

```python
def get_queryset(self):
    queryset = Message.objects.select_related("author")
    query = self.request.GET.get("q", "").strip()
    if query:
        queryset = queryset.filter(Q(content__icontains=query))
    return queryset
```

- 只搜尋 `content`，不像商品目錄還要搜尋名稱、說明與分類。
- `select_related("author")` 先取得外鍵作者，避免每張卡片再查一次。
- 空白或不存在的關鍵字都不是錯誤：前者回全部資料，後者回空 QuerySet。

QuerySet lazy、lookup、Q object 與 N+1 的共通說明請見整合教材第 5 章。
