---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnMart 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnMart 01｜專屬重點回顧
## 你應能在 source 中指出的商城差異

- `ProductListView` 如何把 q/category 轉為 active 商品 QuerySet。
- 商品卡為何需要 category、seller 的 eager loading，以及圖片 fallback。
- `Category`、`Product`、`CartItem`、`Order`、`OrderItem`、`Review` 分別守住什麼資料責任。
- 為何訂單保存快照、關聯使用 `PROTECT`、而且自訂 User 不能在 migration 後隨意替換。

登入、賣家權限、購物車、結帳與交易一致性，接續 LearnMart Deck 02。
