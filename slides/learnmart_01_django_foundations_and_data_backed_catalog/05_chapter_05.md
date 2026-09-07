---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnMart 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnMart｜商城的資料規則
## 重複商品與重複評價各有一條防線

| 規則 | 資料意義 |
|---|---|
| `CartItem` 的 user + product constraint | 同一買家的一項商品只留一列，以數量累加 |
| `Review` 的 product + author constraint | 同一作者對同一商品只留一筆評價 |
| `OrderItem` 的商品名與單價 snapshot | 商品後續改名或改價，不改變已成立訂單 |

這些是商城的 domain rule，不是單靠 template if 就能穩定保護的 UI 規則。

---

## 列表與詳情的 relation 形狀不同

```python
# 列表卡片會讀 category、seller
Product.objects.filter(is_active=True).select_related("category", "seller")

# 詳情頁還要讀多筆 reviews 及各自作者
Product.objects.prefetch_related("reviews__author")
```

選 `select_related` 或 `prefetch_related` 的依據是 relation 形狀，而不是「哪個方法比較快」。共通 ORM 原理請見整合教材第 5 章。
