---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnMart 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnMart｜商城關聯與圖片欄位
## 先讀關係圖，再讀單一 Model

```text
Category 1 ── * Product * ── 1 User(seller)
User(buyer) 1 ── * CartItem * ── 1 Product
User(buyer) 1 ── * Order 1 ── * OrderItem * ── 1 Product
User 1 ── * Review * ── 1 Product
```

商城不只有 Product；刪除與查詢的結果由整張關聯圖共同決定。這是 LearnBoard 單一 Message 模型不會遇到的複雜度。

---

## Product 圖片與歷史的專屬規則

```python
image = models.ImageField("商品圖片", upload_to="products/%Y/%m/", blank=True)
```

- `ImageField` 儲存的是 storage 路徑參照；Pillow 協助欄位處理。
- `Product → Category` 使用 `PROTECT`，避免還有商品時刪除分類。
- `OrderItem → Product/seller` 也用 `PROTECT`，保留購買歷史。

自訂 User 必須在初始 migration 前決定；既有專案應閱讀現有 migrations，不要任意切換 `AUTH_USER_MODEL`。
