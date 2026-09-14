---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 02｜表單、身份驗證與工作流程"
footer: "初學者教材｜LearnBoard × LearnMart"
---

<!-- _class: cover -->

# 第 7 章
## 安全與回歸測試整合

<div class="box">把每個防線放回它保護的 trust boundary，並用測試防止日後退步</div>

<!--
授課提示：安全章不是附加品，是把前面各章的防線串成地圖；trust_boundary.svg 務必配合使用。
-->

---

## 安全不是最後才加的一頁

本冊已經在功能旁使用：

- Template autoescaping：輸出 user content
- CSRF：token 與 Origin／Referer policy 防跨站 mutation
- Form validation：輸入型別與規則
- Authentication：確認身份
- Role／ownership：限制操作範圍
- Server-owned fields：價格、seller、buyer、status
- Transaction：多筆寫入一致性
- Tests：把預期行為固定下來

---

## Trust boundary 地圖

```text
Browser-controlled
URL pk / query string / POST / hidden input / uploaded file
        ↓ validate + authorize
Django View / Form / QuerySet scope
        ↓ server-owned decisions
Models / Database / Transaction
        ↓ encode output
Template / Response
```

每跨一條邊界，都要問：「這個值從哪來？誰有權決定？」

---

## 圖解：信任邊界與五層伺服器防線

![w:1000](../assets/trust_boundary.svg)

<!--
授課提示：左側四張卡片可各配實演（devtools 改 required、改 hidden input、curl 送 POST）。右側五層對應回收：② 第 3 章、③ 第 1 章、④⑤ 第 5 章。收尾提問：「哪一層可以省？」（都不能）
-->

---

## XSS：Template autoescaping 的邊界

安全預設：

```django
{{ post.content }}
{{ post.content|linebreaksbr }}
```

危險：

```django
{{ post.content|safe }}
```

`safe` 告訴 Django 不要 escape；若資料來自使用者，就可能形成 stored XSS。

<!--
授課提示：demo 回收 Deck 01 3-6：留言板輸入 <b>粗體</b> 與 <script>，觀察 escape 差異與 |safe 的危險。
-->

---

## Raw HttpResponse 不會套 Template autoescaping

```python
return HttpResponse(f"歡迎 {name}")
```

若 `name` 是 user-controlled HTML，這個字串會直接成為 response body。

更好的教學方向：

```python
return render(request, "hello.html", {"name": name})
```

或在確實需要時使用明確 escaping utility。不要把「Django 預設安全」誤解成所有字串都自動 escape。

---

## BoardPost 是 stored XSS 的實際觀察點

Board create 儲存 user content；list template 顯示：

```django
<div>{{ post.content|linebreaksbr }}</div>
```

測試可建立 `<script>alert(1)</script>` 文字，再 assert response 包含 escaped 版本而非 raw executable markup。

安全測試要針對輸出，不只看「建立成功」。

---

## SQL injection：ORM value 會參數化

```python
Product.objects.filter(name__icontains=query)
```

`query` 當參數傳給 database driver，不要用字串拼 SQL：

```python
# 危險示意，不要用 f-string 拼接 user input
Product.objects.raw(
    f"SELECT * FROM marketplace_product "
    f"WHERE name LIKE '%{query}%'"
)
```

ORM 防 SQL injection 不代表自動做 authorization。

<!--
授課提示：f-string 拼 SQL 的反例只看不跑；強調 ORM 參數化是預設，raw SQL 才需要警戒。
-->

---

## Dynamic field name 仍需要 allowlist

即使 filter value 安全，使用者控制排序欄位也要限制：

```python
allowed = {"price", "-price", "created_at"}
ordering = request.GET.get("ordering", "-created_at")
if ordering not in allowed:
    ordering = "-created_at"
queryset = queryset.order_by(ordering)
```

不要把任意 query string 直接當 field/expression。

---

## CSRF、Login、Role、Ownership 不可互相替代

以 ship_order 為例：

- CSRF：token 與 Origin／Referer policy 是否通過；不判斷 user 是否有權
- login：是誰
- role：是不是 seller
- ownership/membership：是否參與這張 order
- POST：method 語意與 405 enforcement

只通過其中一層不代表操作安全。

<!--
授課提示：表格快問快答：只做其中一項時，攻擊腳本會長怎樣？
-->

---

## Upload：ImageField 不是完整安全策略

目前已有：

- `ImageField`
- Pillow 支援基本 image 驗證
- `upload_to="products/%Y/%m/"`
- local media storage

尚未完整處理：

- 明確 file size policy
- 內容重新編碼／metadata 移除
- 隨機命名與隔離
- malware scanning
- production object storage／CDN

---

## 開發 settings 不等於 production baseline

<span class="label warning">目前 LearnMart 刻意是 classroom config</span>

```python
SECRET_KEY = "django-insecure-..."
DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
```

正式部署還需環境變數、HTTPS、secure cookies、HSTS、logging、production database、media strategy 等。

---

## `check` 與 `check --deploy` 不同

```bash
uv run python manage.py check
```

檢查一般 project configuration。

```bash
uv run python manage.py check --deploy
```

會對 production security settings 提出警告；教學版預期會出現多項警告，不代表要在本地課堂設定盲目消除所有項目。

---

## 現有六個測試保護什麼？

1. 搜尋找到商品
2. 匿名 add-to-cart redirect
3. buyer 可加入 cart
4. buyer 進 seller dashboard 得到 403
5. checkout 建 order、扣 stock、算 total
6. 不能讀別人的 order（404）

不要把「教材列出的測試主題」誤說成「目前都已實作」。

---

## 測試矩陣：一個 workflow 至少看五面

| 面向 | 問題 |
|---|---|
| 正常路徑 | 合法使用者能完成嗎？ |
| Invalid input | 邊界值會被拒絕且資料不變嗎？ |
| Authorization | 匿名、錯角色、錯 owner 的結果？ |
| Side effects | 相關 rows、stock、status、message 都正確嗎？ |
| Failure integrity | 中途失敗是否留下半套資料？ |

---

## Response 與 database assertion 都重要

```python
response = self.client.post(url, data)
self.assertRedirects(response, expected_url)

order = Order.objects.get(buyer=self.buyer)
self.assertEqual(order.total, 1980)
self.product.refresh_from_db()
self.assertEqual(self.product.stock, 3)
```

HTTP 正確但資料錯，或資料正確但洩漏 URL，都算 workflow bug。

---

## `refresh_from_db()` 避免看舊 object

測試中的 `self.product` 是記憶體 object；View 在另一段 code 修改 database 後，原 object 不會自動更新。

```python
self.product.refresh_from_db()
```

再 assert stock，才能讀到 database 最新值。

---

## Rollback test 要讓失敗發生在寫入之後

針對目前 checkout，可 patch `Product.save()` 在第一次庫存儲存時拋 exception。此時程式已建立 Order 與至少一個 OrderItem，才真正挑戰 view-level `@transaction.atomic`。

Exception 離開 atomic 後要檢查：

- Order 與 OrderItem 都 rollback
- database stock 不變
- CartItem 仍存在

這是同一 request／connection 的 view-level atomic rollback invariant；不是 row-lock 或 concurrent commit test。

<!--
授課提示：TestCase 包 transaction 的陷阱一句話帶過；細節在 workbook 第 5 章。
-->

---

## 一次跑完整與單一測試

```bash
uv run python manage.py test
```

單一 method：

```bash
uv run python manage.py test \
  marketplace.tests.MarketplaceFlowTests.test_checkout_creates_order_and_reduces_stock
```

Dotted label 可指定 app、module、class 或 method，適合快速迭代。

---

## Migration drift 不是 behavior test

```bash
uv run python manage.py makemigrations --check
```

它檢查 models 是否有尚未建立 migration 的變更。

它不會測試：

- View 權限
- Template 輸出
- checkout transaction
- status transition

三種命令目的不同，要一起使用而不是互相取代。

---

## Security regression 的優先順序

先為高風險、容易退步的規則加測試：

1. ownership-scoped update/detail
2. server-calculated total
3. checkout failure integrity
4. seller order membership
5. review eligibility
6. POST-only state changes
7. user content output escaping

測試不能證明完全安全，但能阻止已知規則被後續修改破壞。

---

## 課堂版與正式商城的界線

目前適合學習：

- Django MVT 與 ORM
- 表單、auth、permissions
- transaction 與測試思維

正式營運仍缺：

- payment、tax、refund
- seller onboarding
- shipment grouping
- production concurrency
- object storage、monitoring、audit log
- 更完整 threat model 與 test coverage

<!--
授課提示：念一遍缺漏清單並宣佈：期末考觀念不考部署；想挑戰的同學指向 check --deploy。
-->

---

## 第 7 章概念檢核

1. Template autoescaping 與 raw HttpResponse 的邊界在哪？
2. ORM 防 injection 是否同時保證 ownership？
3. 為何 CSRF、login、role、ownership 都要存在？
4. 一個 workflow test 為何要同時 assert response 與 side effects？
5. `check`、`makemigrations --check`、`test` 各自檢查什麼？

<span class="label check">答案見配套實作手冊第 7 章</span>

<!--
授課提示：測試矩陣五面（匿名/身份/角色/資料/併發）讓學生對照自己的 lab 補洞。
-->

---

## 第 7 章 LearnMart 實作

任務：新增一個 ownership regression test 與一個失敗完整性 test。

驗收重點：

- 非 owner 得到預期 403／404
- forbidden object 不被修改
- 失敗 checkout 不留下 Order 或 stock/cart 半套狀態
- 完整 test suite 與 migration check 都通過

[LearnMart 安全測試手冊](../workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md#chapter-7)；LearnBoard 安全與測試對應見本冊前段的 `board/tests.py` 對照。

---
