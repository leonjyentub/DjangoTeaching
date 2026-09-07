---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnMart 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnMart｜可篩選商品目錄
## 目前首頁 QuerySet 的專屬規則

```python
queryset = Product.objects.filter(is_active=True).select_related("category", "seller")
query = self.request.GET.get("q", "").strip()
category = self.request.GET.get("category", "").strip()
if query:
    queryset = queryset.filter(
        Q(name__icontains=query) | Q(description__icontains=query)
    )
if category:
    queryset = queryset.filter(category__slug=category)
```

首頁只顯示 active 商品；關鍵字搜尋名稱與說明，分類以 slug 篩選。這比留言板的單一內容搜尋多了一個 URL state。

---

## 分頁與篩選必須共同保留狀態

```text
?page=2&q=鍵盤&category=tech
```

目前 `paginate_by = 12`。分類連結保留 `q`，分頁連結保留 `q/category`；但 navbar 的新搜尋只提交 `q`，因此會刻意重設 category。這是目前 UI navigation contract，不是 Django 的安全規則。

---

## 商品卡讀取 relation 與圖片

商品卡同時讀 `product.category.name`、`product.seller.username` 與可能為空的 `product.image`。因此 View 的 eager loading、template fallback 與 alt text 必須一起驗收。共通 pagination、GET state 與 vertical slice 請見整合教材第 6 章。
