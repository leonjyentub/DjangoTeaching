---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnMart 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnMart｜環境與示範資料
## 只有商城需要的依賴與初始狀態

```toml
[project]
dependencies = [
    "django>=5.2,<5.3",
    "pillow>=11.0",
]
```

Pillow 是 `Product.image` 的圖片欄位所需依賴；LearnBoard 不需要它。兩個專案各自有 `.venv/` 與 `uv.lock`，不能交叉複製。

---

## seed 後的商城資料

| 項目 | 預期結果 |
|---|---|
| 帳號 | `seller / seller12345`、`buyer / buyer12345` |
| 資料 | 3 個分類、6 個商品、1 則留言 |
| 首頁 | 商品目錄與分類／搜尋 UI |
| 重跑 seed | 同名資料由 `get_or_create()` 保護，不重設既有帳號或角色 |

啟動流程與 uv 檔案的共通意義請見整合教材；本頁僅記錄 LearnMart 的可觀察差異。
