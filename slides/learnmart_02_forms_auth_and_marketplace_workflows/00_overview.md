---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnMart 02｜表單、身份驗證與商城工作流程"
footer: "Django 初學者課程｜LearnMart"
---

# LearnMart 02
## 表單、身份驗證與商城工作流程

從「能查詢商品」前進到「能安全地改變資料，並用測試守住規則」。

---

## 承接 LearnBoard 02：從留言板到商城

留言板課程已經讓你寫過這些原型（見 `../learnboard_02_forms_auth_and_board_workflows/`）：

| 你在留言板做過 | 本冊商城版本 |
|---|---|
| MessageForm 發文＋PRG | ProductForm 上架（多欄位＋圖片） |
| 註冊／登入／session | 相同機制＋買家／賣家角色 |
| author FK 的 migration 演進 | 訂單快照、constraint 與交易 |
| 擁有權 mixin（403/404） | SellerRequiredMixin、多方限制 |
| CSRF／XSS／IDOR 三課 | 同三課＋transaction 一致性 |
| 9 支 TestCase | 流程測試與回歸防護 |

**本冊所有新主題都建立在留言板的原型之上——遇到困難時，先回想小專案的對應段落。**

<!--
授課提示：這頁當全冊的索引卡。每章開場都回指一次：購物車章對照「發文表單」、訂單章對照「author migration」、出貨評價章對照「擁有權 mixin」。
-->

---

## 這份教材接續什麼？

你已經能追蹤：

```text
Browser → URLconf → View → ORM → Template → Response
```

這一份要加入三個新問題：

1. 使用者送來的資料可信嗎？
2. 已登入的人可以操作哪些物件？
3. 多筆資料要一起成功或一起失敗，怎麼保證？

<!--
授課提示：開場先花 3 分鐘複習 Deck 01 的 6-17A 完整資料流圖；本冊所有 POST 流程都建立在那張圖上。
-->

---

## 本冊最終成果

完成後，你能解釋並追蹤：

- 商品新增／編輯與圖片上傳
- 註冊、登入、session、角色與物件權限
- Generic Class-based View 與 `.as_view()`
- 購物車、結帳、訂單快照、出貨與評價
- CSRF、XSS、IDOR、SQL injection 的防線
- Django `TestCase` 如何保護重要流程

---

## 閱讀標籤

<span class="label">教學用最小範例</span>：省略最終專案細節，只聚焦一個新概念。

<span class="label current">目前 LearnMart｜逐字摘錄</span>：未改寫的 source 片段。<br>
<span class="label current">目前 LearnMart｜節錄／重排</span>：省略無關行、重排換行或加入 `...`；語意對齊，但不是逐字 source。

<span class="label warning">常見錯誤／限制</span>：初學者容易誤解，或教學版尚未處理的情況。

<span class="label check">配套實作手冊</span>：答案、修改步驟與前後程式碼放在另一份 Markdown。

---

## 本冊章節地圖

1. 完整表單生命週期
2. 身份驗證、session 與帳號流程
3. Class-based View、Mixin 與物件權限
4. 購物車、POST 操作與第一批流程測試
5. 訂單、結帳、transaction 與鎖定
6. 賣家出貨、評價與多方交易限制
7. 安全與回歸測試整合

<!--
授課提示：建議每章配一次 lab。第 5 章最重，務必預留完整一堂課。
-->
