---
marp: true
theme: django-teal
transition: fade
size: 16:9
paginate: true
header: "LearnBoard 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

<!-- _class: cover -->

# LearnBoard 01
## 留言板專屬實作補充

<div class="box">留言板專屬實作 ｜ 留言牆與示範資料 ｜ 搜尋與 ListView</div>

共通概念請參見 Django 01 整合教材

---

## 本專案要追的 vertical slice

```text
GET /?q=django
  → board/urls.py
  → MessageListView
  → Message.objects.select_related("author")
  → templates/board/message_list.html
  → 留言卡、搜尋狀態與分頁
```

| 專屬資料 | 對應位置 |
|---|---|
| 留言與作者 | `board/models.py` 的 `Message` |
| 列表與搜尋 | `board/views.py` 的 `MessageListView` |
| 卡片與分頁 | `templates/board/` |
| 自訂外觀 | `static/css/site.css` |

下一冊才會加入帳號、發文、編輯與「只能修改自己留言」的權限規則。
