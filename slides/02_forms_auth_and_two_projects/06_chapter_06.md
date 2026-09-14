---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 02｜表單、身份驗證與工作流程"
footer: "初學者教材｜LearnBoard × LearnMart"
---

<!-- _class: cover -->

# 第 6 章
## 賣家出貨、評價與多方交易限制

<div class="box">把狀態轉換、參與者關係與規則所在層次說清楚</div>

<!--
授課提示：狀態機思維首次登場：PENDING → SHIPPED 的五件事（起點/終點/條件/副作用/誰能觸發）。
-->

---

## Seller 如何找到有自己商品的訂單？

```python
Order.objects.filter(
    items__seller=self.request.user
).distinct().prefetch_related("items")
```

- `items__seller` 沿 reverse FK 篩選
- 一張 order 可能有多個 matching items
- `distinct()` 避免同一 order 重複出現
- Template 再只列出該 seller 的 items

---

## Seller order list 還有一個 N+1 觀察點

Template 顯示：

```django
{{ order.buyer.username }}
```

目前 queryset prefetch items，但沒有 `select_related("buyer")`。列表有多張 order 時可能額外查 buyer。

這是比「order detail prefetch items__product」更貼近實際模板使用的優化練習。

---

## 出貨操作的四層檢查

```python
@require_POST
@login_required
def ship_order(request, pk):
    if not request.user.is_seller:
        return HttpResponseForbidden(...)
    order = get_object_or_404(
        Order.objects.filter(items__seller=request.user).distinct(),
        pk=pk,
    )
```

method → login → seller role → order membership。

<!--
授課提示：逐層回收前面章節編號：POST-only（第1章）、login（第2章）、角色（第3章）、賣家歸屬 query。
-->

---

## 目前只實作 PENDING → SHIPPED

```python
if order.status == Order.Status.PENDING:
    order.status = Order.Status.SHIPPED
    order.shipped_at = timezone.now()
    order.save(update_fields=["status", "shipped_at"])
```

Model 還定義 COMPLETED 與 CANCELLED，但目前沒有對應 endpoint／transition。

「有狀態值」不等於「所有狀態轉換已實作」。

---

## 狀態轉換要定義五件事

1. 誰可以觸發？
2. 從哪些舊狀態允許？
3. 新狀態是什麼？
4. 有哪些副作用？例如時間、庫存、退款
5. 重複 request 是否 idempotent？

依序送出的重複 POST 中，第一個 request 將狀態改為 shipped，後一個不再改時間，所以具有**序列情境下**的冪等效果。

但兩個 concurrent requests 都可能先讀到 pending；正式方向是 conditional update（例如 `filter(pk=..., status=PENDING).update(...)` 並檢查 affected rows）或適當 row lock，而不能只靠 Python `if` 宣稱 concurrency-safe。

---

## 多賣家訂單的核心限制

<span class="label warning">目前教學版設計</span>

一張 Order 可含 seller A 與 seller B 的 items，但 shipping status 在 Order 層級。

結果：只要 A 是其中一項的 seller，A 就能把整張 order 標成 shipped，B 的 item 也被視為已出貨。

<!--
授課提示：說明這是教學簡化：正式多賣家平台需要 per-seller shipment 子模型，期末報告可挑戰。
-->

---

## 限制還會影響 Review

Review eligibility 使用：

```python
order__status__in=[Order.Status.SHIPPED,
                   Order.Status.COMPLETED]
```

若 seller A 把混合訂單整張標為 shipped，買家也可能開始評 seller B 尚未實際出貨的商品。

正式設計應將 shipment/status 拆到 seller group 或 item 層級。

---

## Review 規則要分層描述

LearnMart 有四個不同機制：

1. View query：是否買過且訂單已出貨／完成
2. Form／model validators：rating 是否 1–5
3. Database unique constraint：每個 author/product 一列
4. `update_or_create()`：再次送出時更新原評價

不要籠統說「全部規則都在 View、validator、constraint」。

---

## Eligibility 在 View 查詢

```python
has_purchased = OrderItem.objects.filter(
    order__buyer=request.user,
    product=product,
    order__status__in=[
        Order.Status.SHIPPED,
        Order.Status.COMPLETED,
    ],
).exists()
```

`.exists()` 只需要回答有沒有符合資料，不必載入完整 OrderItem list。

---

## Rating 1–5 由 validators／form 驗證

```python
rating = models.PositiveSmallIntegerField(
    "評分",
    validators=[MinValueValidator(1), MaxValueValidator(5)],
)
```

ModelForm 會使用 model validators。注意：任意程式碼直接 `.save()` 並不等於自動執行 `full_clean()`。

目前 database 沒有 `CheckConstraint` 強制 rating 1–5。

---

## 每人每商品一列由 database unique constraint

```python
models.UniqueConstraint(
    fields=["product", "author"],
    name="one_review_per_product",
)
```

這個 constraint 保護 row uniqueness；它不檢查購買資格，也不檢查 order status。

---

## `update_or_create()` 讓重送變成編輯

```python
Review.objects.update_or_create(
    product=product,
    author=request.user,
    defaults=form.cleaned_data,
)
```

- 找到既有 row：更新 rating/comment
- 找不到：建立新 row

資料庫 unique constraint 與 lookup fields 必須一致，才能避免重複評價。

<!--
授課提示：對照 get_or_create：defaults 只更新指定欄位；unique constraint 是它的前提（回收 Deck 01 5-16A）。
-->

---

## 評價輸出仍需 template escaping

```django
<div>{{ review.comment|linebreaksbr }}</div>
```

Django 先 escape 變數內容，再由 `linebreaksbr` 處理換行。不要對 user comment 加 `|safe`。

這與購買資格無關：authorization 控制誰能寫，escaping 控制內容如何安全輸出。

---

## 出貨與 Review 應有哪些測試？

- buyer POST ship → 403
- seller A 對無關 order → 404
- 正確 seller 對 pending order → shipped + timestamp
- 非購買者 review → 不建立資料
- 未出貨購買者 review → 不建立資料
- 合格買家 review → 建立
- 同人再送 → 更新同一 row
- rating 超範圍 → form invalid

---

## 第 6 章概念檢核

1. 為何 seller order queryset 需要 `distinct()`？
2. Model 有四個 status 是否代表四種 transition 都存在？
3. Whole-order shipping 對多賣家有什麼副作用？
4. Review 的資格、rating 範圍、唯一性各由哪一層負責？
5. `update_or_create()` 與 UniqueConstraint 如何配合？

<span class="label check">答案見配套實作手冊第 6 章</span>

<!--
授課提示：eligibility 查詢條件請學生口述：buyer + product + status in (SHIPPED, COMPLETED)。
-->

---

## 第 6 章 LearnMart 實作

任務：加入 seller shipping ownership 與 review eligibility tests。

驗收重點：

- 不相關 seller 得到 404
- buyer 不可出貨
- non-purchaser／pending order 不可評
- 合格評價建立，再送時更新而非新增

[LearnMart Fixtures、步驟與參考測試](../workbooks/learnmart_02_forms_auth_and_marketplace_workflows_workbook.md#chapter-6)；[LearnBoard 對應練習](../workbooks/learnboard_02_forms_auth_and_board_workflows_workbook.md#chapter-6)
