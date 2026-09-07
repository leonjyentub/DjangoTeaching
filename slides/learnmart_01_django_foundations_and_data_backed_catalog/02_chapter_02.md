---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnMart 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnMart｜首頁與本機資料庫
## 首頁不是教學用 hello View

```python
# marketplace/urls.py
app_name = "marketplace"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(),
         name="product-detail"),
    # register、cart、checkout、orders、seller/... 等流程在 Deck 02
]
```

目前首頁名稱是 `marketplace:home`。教學中的 `hello` function view 只用來拆解共通概念，並不在完成的商城路由裡。

---

## SQLite 是這個專案的本機邊界

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

`migrate` 改 schema、`seed_demo` 改 rows；它們都不是安裝套件。這份 SQLite 設定適合單機課堂練習；正式環境需另行處理 database service、備份、權限與監控。
