---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnBoard 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnBoard｜實際路由
## 留言板把哪些網址交給哪個 View？

```python
# board/urls.py（目前實作）
app_name = "board"

urlpatterns = [
    path("", views.MessageListView.as_view(), name="list"),
    path("register/", views.register, name="register"),
    path("new/", views.MessageCreateView.as_view(), name="create"),
    path("messages/<int:pk>/edit/", views.MessageUpdateView.as_view(), name="update"),
    path("messages/<int:pk>/delete/", views.MessageDeleteView.as_view(), name="delete"),
]
```

首頁的名稱是 `board:list`，不是 `home`。編輯與刪除以 `pk` 定位一則留言；建立、修改與權限細節屬於 Deck 02。

---

## 本冊只需追蹤的 request

```text
GET /?q=django
  config/urls.py → include("board.urls")
  board/urls.py  → MessageListView.as_view()
  board/views.py → get_queryset()
  template       → board/message_list.html
```

這條流程是整合教材 URL／request flow 的 LearnBoard 實例。HTTP、`path()`、converter、reverse 與錯誤碼的共通講解不在此重複。
