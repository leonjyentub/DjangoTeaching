---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnBoard 02｜表單、帳號與留言權限"
footer: "Django 初學者課程｜LearnBoard"
---

# LearnBoard 02
## 表單、帳號與留言權限

從「能查詢留言」前進到「能安全地改變資料，並用測試守住規則」。

---

## 這份教材接續什麼？

你已經能追蹤：

```text
Browser → URLconf → ListView → ORM → Template → Response
```

這一份要加入三個新問題：

1. 使用者送來的資料可信嗎？
2. 送資料的人是誰？
3. 已登入的人可以操作哪些物件？

<!--
授課提示：開場先花 3 分鐘複習 Deck 01 的 request flow 圖；本冊所有 POST 流程都建立在那張圖上。
-->

---

## 從留言板到商城：本冊學的就是未來的骨架

| 本冊（LearnBoard） | 未來（LearnMart 商城） |
|---|---|
| MessageForm 發表留言 | ProductForm 上架商品 |
| 註冊／登入／session | 相同機制＋買賣家角色 |
| 加 author 欄位的 migration | 更多關聯欄位演進 |
| 只能編輯自己的留言 | 賣家只能管理自己的商品 |
| CSRF／XSS／IDOR | 同三課＋交易安全 |

**先把小而完整的流程走通，商城只是同樣循環的加強版。**

---

## 本冊最終成果

完成後，你能解釋並追蹤：

- 表單送出 → 驗證 → 儲存 → redirect 的完整生命週期
- 註冊、登入、session、密碼雜湊
- 「加一個 FK 欄位」的 migration 演進
- 編輯／刪除的物件擁有權檢查（403 vs 404）
- CSRF、XSS、IDOR 的防線在哪一行程式碼
- Django `TestCase` 如何保護以上一切

---

## 閱讀標籤

<span class="label">教學用最小範例</span>：省略最終專案細節，只聚焦一個新概念。

<span class="label current">目前 LearnBoard｜逐字摘錄</span>：未改寫的 source 片段。<br>
<span class="label current">目前 LearnBoard｜節錄／重排</span>：省略無關行或重排換行。

<span class="label warning">常見錯誤／限制</span>：初學者容易誤解，或教學版尚未處理的情況。

<span class="label check">配套實作手冊</span>：答案、修改步驟與前後程式碼放在另一份 Markdown。

---

## 本冊章節地圖

1. 完整表單生命週期：GET 與 POST 的分水嶺
2. 身份驗證：註冊、登入與 session
3. Model 演進：把留言連回作者
4. CBV 與物件擁有權：編輯／刪除自己的留言
5. 安全三課：CSRF、XSS、IDOR
6. 測試與回歸防護

<!--
授課提示：建議每章配一次實作。第 3、4 章是本冊核心，務必預留完整課時。
-->
