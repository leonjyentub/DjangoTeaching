---
marp: true
theme: django-teal
transition: fade
size: 16:9
paginate: true
header: "LearnMart 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnMart 01
## 商品目錄專屬實作補充

整合教材已集中 uv、Django 骨架、HTTP、URL、Template、Model、ORM 與列表頁的共通講解。本資料夾只保留商城才有的資料關聯、圖片、分類篩選與購買歷史。

```text
GET /?q=鍵盤&category=tech
  → ProductListView
  → active Product + search/category filters
  → category、seller 與商品圖片
  → marketplace/home.html
```

LearnBoard 的 `Message` 是最小資料頁；LearnMart 將同一條資料流延伸到商品、購物車、訂單、評價與賣家角色。帳號、結帳與交易細節在 Deck 02。
