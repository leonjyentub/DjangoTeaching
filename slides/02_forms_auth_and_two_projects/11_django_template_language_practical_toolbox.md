---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django Template Language｜實用工具箱"
footer: "補充教材｜Django 6.1.1"
---

<!-- _class: cover -->

# Django Template Language
## 實用工具箱

<div class="box">少寫重複 view code｜保持 autoescape｜讓清單、時間、文字與分頁更好用</div>

---

## DTL 的定位

Template 應該負責：

- 呈現資料
- 小型格式轉換
- 簡單條件與迴圈
- 組合 reusable partial

不應該負責：

- 複雜 business rule
- database query orchestration
- 大量 Python 計算
- permission 核心判斷

複雜邏輯移到 view / model / QuerySet / custom template tag。

---

## Filter 可以串接

```django
{{ article.title|default:"未命名"|truncatechars:40 }}
```

心智模型：

```text
article.title
  ↓ default
  ↓ truncatechars
  ↓ render
```

每個 filter 都接收前一個輸出。

---

## `default` vs `default_if_none`

```django
{{ value|default:"沒有資料" }}
{{ value|default_if_none:"沒有資料" }}
```

差異：

- `default`：空字串、False、空 list 等 falsy 值也會被替換
- `default_if_none`：只有 `None` 才替換

如果 `0` 是有意義的值，常常要用 `default_if_none`。

---

## 日期格式 `date`

```django
{{ article.published_at|date:"Y-m-d" }}
{{ article.published_at|date:"Y/m/d H:i" }}
```

常見格式：

- `Y`：四位年份
- `m`：月份 01–12
- `d`：日期 01–31
- `H`：24 小時制
- `i`：分鐘

不要在 view 手動 `strftime()` 只為了顯示格式。

---

## 只顯示時間：`time`

```django
{{ event.starts_at|time:"H:i" }}
```

當畫面只需要時間，不需要日期時，比 `date` 語意更清楚。

---

## 相對時間：`timesince`

```django
{{ article.created_at|timesince }} 前
```

可能顯示：

```text
3 天, 4 小時 前
```

適合：

- 留言時間
- 發文多久
- 最近活動

---

## 未來還有多久：`timeuntil`

```django
距離截止還有 {{ deadline|timeuntil }}
```

適合：

- 活動倒數
- 排程發佈
- 訂單付款期限

如果要精準倒數到秒，應交給 JavaScript，而不是 template 每秒重算。

---

## Template 裡取得現在時間：`{% now %}`

```django
{% now "Y-m-d H:i" %}
```

也可以存進變數：

```django
{% now "Y" as current_year %}
© {{ current_year }}
```

適合 footer 等簡單呈現。

---

## 更自然的時間：`humanize`

先載入：

```django
{% load humanize %}
```

常用：

```django
{{ article.created_at|naturaltime }}
{{ article.published_at|naturalday }}
```

可能得到：

```text
3 minutes ago
今天
明天
```

實際語言依 i18n 設定。

---

## 大數字：`intcomma` / `intword`

```django
{% load humanize %}
{{ article.view_count|intcomma }}
{{ total_users|intword }}
```

例：

```text
12,345
1.2 million
```

適合 dashboard / analytics 類畫面。

---

## 長文字：`truncatechars`

```django
{{ article.title|truncatechars:40 }}
```

超過 40 characters 時會截斷並加省略符號。

最常用在：

- card title
- table column
- sidebar link
- mobile layout

---

## 長文字：`truncatewords`

```django
{{ article.excerpt|truncatewords:25 }}
```

以「單字數」截斷。

英文文章很好用；中文沒有空白斷詞時，`truncatechars` 通常更直覺。

---

## HTML 截斷版本要小心

Django 也有 HTML-aware variants，例如：

```django
{{ trusted_html|truncatechars_html:120 }}
```

重點：

**HTML-aware 不等於 XSS sanitizer。**

如果內容來自使用者，仍要先有可信的 sanitization policy。

---

## 純文字換行：`linebreaks`

```django
{{ comment.body|linebreaks }}
```

會把換行轉成 `<p>` / `<br>` 結構。

如果只想換行變 `<br>`：

```django
{{ comment.body|linebreaksbr }}
```

很適合簡單 textarea 內容。

---

## 檔案大小：`filesizeformat`

```django
{{ upload.size|filesizeformat }}
```

可能顯示：

```text
2.4 MB
```

比直接顯示 `2516582` bytes 更友善。

LearnMart 圖片上傳教材可以直接使用。

---

## 小數格式：`floatformat`

```django
{{ rating|floatformat:1 }}
{{ completion_ratio|floatformat:2 }}
```

例：

```text
4.6
0.83
```

如果是 money，仍建議 model/backend 使用 `Decimal`，不要把精度責任交給 template。

---

## `length` / `wordcount`

```django
{{ articles|length }}
{{ article.body|wordcount }}
```

適合純呈現。

如果 `articles` 是 QuerySet，而且你只是要 DB count，通常 view/queryset 的 `.count()` 更能表達意圖。

---

## List helpers

```django
{{ tags|first }}
{{ tags|last }}
{{ tags|join:", " }}
{{ articles|slice:":3" }}
```

適合小型 presentation transformation。

不要為了只顯示前三筆而在大量 QuerySet evaluate 後才 slice；能在 ORM 限制就優先在 ORM。

---

## `dictsort`

```django
{% for item in items|dictsort:"name" %}
  {{ item.name }}
{% endfor %}
```

可用於 template 收到的普通 dict/list data。

如果排序是 domain rule 或會影響 pagination，應在 ORM / view 排好。

---

## `yesno`

```django
{{ order.is_paid|yesno:"已付款,未付款" }}
```

也可給 None 第三種：

```django
{{ value|yesno:"是,否,未知" }}
```

適合 Boolean label。

---

## `pluralize`

英文 UI 常用：

```django
{{ count }} comment{{ count|pluralize }}
```

中文通常不需要單複數變化，但看官方教材或國際化專案時很常遇到。

---

## `urlize` / `urlizetrunc`

```django
{{ plain_text|urlize }}
{{ plain_text|urlizetrunc:30 }}
```

把純文字 URL/email 轉成 link。

注意：它不是 Markdown parser，也不是 sanitization 工具。

---

## `{% with %}`：替長 lookup 取名字

```django
{% with total=order.items.count %}
  共 {{ total }} 項
{% endwith %}
```

適合：

- 提升可讀性
- 同一個值在區塊內重複使用

不要拿 `{% with %}` 取代應該在 view 計算的複雜資料。

---

## `{% firstof %}`：多個 fallback

```django
{% firstof user.get_full_name user.username "匿名" %}
```

相當於「第一個 truthy 值」。

比多層 `{% if %}` 簡潔。

---

## `{% cycle %}`：輪流值

```django
{% for row in rows %}
<tr class="{% cycle 'odd' 'even' %}">
```

常用：

- zebra table
- card variant
- alternating alignment

Bootstrap 已能處理很多 styling，但讀舊模板時很常見。

---

## `{% ifchanged %}`：分組顯示

```django
{% for article in articles %}
  {% ifchanged article.category.name %}
    <h2>{{ article.category.name }}</h2>
  {% endifchanged %}
  ...
{% endfor %}
```

資料必須先按 grouping key 排好。

---

## `{% regroup %}`：Template 層分組

```django
{% regroup articles by category as grouped %}

{% for group in grouped %}
  <h2>{{ group.grouper }}</h2>
  {% for article in group.list %}
    {{ article.title }}
  {% endfor %}
{% endfor %}
```

適合「已經排序好的資料」做 presentation grouping。

不是 SQL `GROUP BY` 的替代品。

---

## `{% querystring %}`：分頁超實用

Django 5.1+ 內建：

```django
<a href="{% querystring page=page_obj.next_page_number %}">
  下一頁
</a>
```

如果目前 URL 是：

```text
/?q=django&category=web&page=1
```

它能只改 `page`，保留其他 query parameters。

---

## 搜尋＋分頁的典型寫法

```django
{% if page_obj.has_previous %}
<a href="{% querystring page=page_obj.previous_page_number %}">
  上一頁
</a>
{% endif %}

{% if page_obj.has_next %}
<a href="{% querystring page=page_obj.next_page_number %}">
  下一頁
</a>
{% endif %}
```

比手動：

```django
?q={{ query }}&page=...
```

更不容易漏掉其他 filter。

---

## `url` tag：不要手拼路徑

```django
{% url 'journal:article-update' article.pk %}
```

有 kwargs：

```django
{% url 'journal:category' slug=category.slug %}
```

URL 結構改名時，named URL 能集中變更。

---

## `json_script`：安全把資料交給 JS

```django
{{ chart_data|json_script:"chart-data" }}
```

JavaScript：

```js
const data = JSON.parse(
  document.getElementById("chart-data").textContent
);
```

比直接把 Python data 插進 `<script>` 字串安全，也更符合 CSP。

---

## Autoescape 是預設安全線

```django
{{ comment.body }}
```

Django 預設會 escape HTML 特殊字元。

例如 user 輸入：

```html
<script>alert(1)</script>
```

不應直接成為可執行 script。

---

## `safe` 要非常克制

```django
{{ value|safe }}
```

它的意思不是「幫我清理 HTML」。

它的意思是：

> 我向 template engine 保證，這段內容已可信，可不要 escape。

如果保證錯了，就是 XSS。

---

## `striptags|safe` 不是 sanitizer

不要假設：

```django
{{ user_html|striptags|safe }}
```

就一定安全。

Django 官方文件也明確提醒 `striptags` 的輸出不應再直接標記 safe。

有 user HTML 需求時，用專門 sanitizer policy。

---

## Template 裡不要呼叫帶參數方法

DTL 允許：

```django
{{ article.get_absolute_url }}
```

但不支援像 Python：

```python
article.some_method("x")
```

需要帶參數的 presentation logic：

- 先在 view 計算
- 自訂 filter
- simple_tag / inclusion_tag

---

## 什麼時候做 custom filter？

當你一直重複：

```django
{{ value|...一串處理... }}
```

而且它是純 presentation transformation。

例：LearnJournal 的 `markdownify`。

Custom filter 應盡量是 deterministic、沒有 DB side effect。

---

## 什麼時候做 inclusion tag？

當一小塊 UI 同時需要：

- 自己的 query/context
- 自己的 partial template
- 多頁重用

例：

```django
{% latest_articles 5 %}
{% tag_cloud 20 %}
```

比每個 view 都塞相同 context 更乾淨。

---

## LearnBoard 可以立刻用的補強

留言清單：

```django
{{ message.content|truncatechars:120 }}
{{ message.created_at|naturaltime }}
```

搜尋分頁：

```django
{% querystring page=page_obj.next_page_number %}
```

---

## LearnMart 可以立刻用的補強

```django
{{ product.description|truncatewords:30 }}
{{ product.image.size|filesizeformat }}
{{ product.rating|floatformat:1 }}
{{ order.created_at|date:"Y-m-d H:i" }}
```

數量：

```django
{{ cart_items|length }} 項商品
```

---

## LearnJournal 可以立刻用的補強

```django
{% load humanize %}
{{ article.published_at|naturaltime }}
{{ article.view_count|intcomma }} 次瀏覽
{{ article.excerpt|truncatechars:140 }}
```

Scheduled：

```django
距離發佈還有 {{ article.published_at|timeuntil }}
```

---

## 判斷「該放哪一層」

如果你正在 template 想做：

```text
多次 DB query
複雜排序
permission decision
transaction
API call
多層資料轉換
```

停下來。

大多數情況應該移到 Python 層。

---

## 本章實作題

1. LearnBoard 留言列表加 `naturaltime`。
2. LearnMart 商品卡改用 `truncatechars` / `floatformat`。
3. 任一搜尋分頁改用 `{% querystring %}` 保留 `q`。
4. 做一頁展示 `default` 和 `default_if_none` 對 `0` 的差別。
5. 用 `json_script` 把 5 個文章瀏覽數交給前端 console 印出。

---

## 參考資料

- Django 6.1.1 Template language：<https://docs.djangoproject.com/en/6.1/ref/templates/language/>
- Built-in tags / filters：<https://docs.djangoproject.com/en/6.1/ref/templates/builtins/>
- Humanize：<https://docs.djangoproject.com/en/6.1/ref/contrib/humanize/>
- Time zones in templates：<https://docs.djangoproject.com/en/6.1/topics/i18n/timezones/>

---

## 最後記住三件事

1. **格式化留在 template，business rule 留在 Python。**
2. **autoescape 是預設安全線，不要隨便 `safe`。**
3. **如果同一段 presentation logic 重複出現，就考慮 custom filter/tag。**
