---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnMart 02｜表單、身份驗證與商城工作流程"
footer: "Django 初學者課程｜LearnMart"
---

# 全冊整合：一次購買旅程

```text
GET catalog → ORM filter → Template
POST add cart → CSRF/login/stock/ownership
GET checkout → unbound CheckoutForm + cart summary
POST checkout → Form validation → atomic writes → redirect
GET order → buyer-scoped queryset
POST ship → seller role + membership
POST review → purchase/status + validators + constraint
Tests → response + database + failure invariants
```

---

## 你現在應該能回答

- 哪些值由 browser 決定，哪些必須由 server 決定？
- 一個 protected CBV 在哪裡檢查 login、role、ownership？
- atomic 與 row locking 的保證有何不同？
- SQLite 對 `select_for_update()` 有何限制？
- 一項規則應放 Form、View、Model validator、constraint 還是 test？

---

## 建議驗證命令

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

接著使用 workbook 逐章完成 labs；每次只改一個可觀察行為，先跑單一測試，再跑完整 suite。
