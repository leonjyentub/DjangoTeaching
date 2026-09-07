---
marp: true
theme: django-teal
transition: fade
size: 16:9
paginate: true
header: "LearnBoard 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnBoard 01
## 留言板專屬實作補充

共通的 uv、Django 骨架、HTTP、URL、Template、Model、ORM 與列表頁講解，已集中在：

`../01_django_foundations_and_two_projects/01_django_from_zero_to_project_comparison.md`

本資料夾只保留 LearnBoard 的實際檔案、資料形狀與 UI 行為；請將它當作整合教材的對照索引，而不是第二次閱讀共通概念。

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
