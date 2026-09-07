---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnMart 01｜專屬實作補充"
footer: "共通講解請見 Django 01 整合教材"
---

# LearnMart｜商品卡與圖片狀態
## 商品模板同時處理有圖與無圖

```django
{% if product.image %}
  <img src="{{ product.image.url }}" alt="{{ product.name }}">
{% else %}
  <div class="placeholder-product">商品圖片</div>
{% endif %}
```

圖片欄位空白時不能直接讀 `.url`；有圖時以商品名稱提供替代文字，無圖時仍給可見 fallback。這是商品目錄特有的 media 狀態，留言板沒有對等欄位。

---

## 商品目錄的 template 邊界

- `templates/marketplace/home.html` 負責商品卡與分類結果。
- `{% include "marketplace/pagination.html" %}` 抽出分頁 UI。
- `templates/base.html` 載入 Bootstrap 與 `static/css/site.css`；商品上傳檔案則屬於 media，不等於 static。

Template inheritance、static tag、grid 與 escaping 的共通原理請見整合教材第 3 章。
