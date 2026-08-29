---
marp: true
theme: default
size: 16:9
paginate: true
header: "LearnMart 02｜表單、身份驗證與商城工作流程"
footer: "Django 初學者課程｜LearnMart"
style: |
  section {
    font-family: 'Noto Sans CJK TC', 'Noto Serif CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', 'Heiti TC', sans-serif;
    font-size: 28px;
    line-height: 1.35;
  }
  h1, h2 {
    font-family: 'Noto Sans CJK TC', 'WenQuanYi Zen Hei',
                 'PingFang TC', 'Microsoft JhengHei', sans-serif;
  }
  h1 { color: #8b1e2d; }
  h2 { color: #17324d; }
  blockquote {
    font-family: 'Noto Serif CJK TC', 'Noto Sans CJK TC', 'WenQuanYi Zen Hei', serif;
  }
  code, kbd {
    font-family: 'Noto Sans Mono CJK TC', 'SF Mono', Consolas,
                 'WenQuanYi Zen Hei Mono', 'Courier New', monospace;
    font-size: 0.82em;
  }
  pre { margin-top: 0.35em; margin-bottom: 0.35em; }
  .label { display: inline-block; padding: 0.15em 0.55em; border-radius: 999px; font-size: 0.72em; font-weight: 700; background: #e8eef5; color: #17324d; }
  .current { background: #e5f4ea; color: #17633a; }
  .warning { background: #fff0d9; color: #8a4b08; }
  .check { background: #f3e8ff; color: #6b21a8; }
  .small { font-size: 0.78em; }
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
