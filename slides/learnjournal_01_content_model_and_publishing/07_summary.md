---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnJournal 01｜內容模型與發佈"
footer: "初學者教材｜觀念 → 語法 → LearnJournal 實作"
---

# Deck 03A 總結
## 你已經能建立有結構的內容站

```text
多對多 / 中介模型 / 自我關聯
  → 自訂 Manager（published）
  → F() 原子更新 + CheckConstraint
  → slug + 日期網址 + 日期型 View（時區一致）
  → 自訂 template tag（Markdown / 標籤雲 GROUP BY）
  → FormMixin + DetailView + signal（巢狀留言）
```

你已經學會：

- 判斷「一對多 vs 多對多」，以及何時需要 `through`
- 用 `RunPython` data migration 搬舊資料
- 把重複查詢收斂到具名 QuerySet 方法
- 用 `F()` 避免 read-modify-write 的 race
- 讓一個 `DetailView` 同時顯示與收 POST

---

## 對照三個專案：同一套骨架，不同深度

| 觀念 | LearnBoard | LearnMart | LearnJournal |
|---|---|---|---|
| 關聯 | 一個 FK（author 可 NULL） | 多個 FK + 中介模型 OrderItem | **M2M + through + 自我關聯** |
| 查詢收斂 | 直接 filter | 直接 filter | **自訂 Manager / QuerySet** |
| 原子更新 | — | `stock -= n`（有 race） | **`F()` 原子遞增** |
| 約束 | — | `UniqueConstraint` | **＋`CheckConstraint`／`indexes`** |
| generic view | ListView | ListView / DetailView / CreateView | **＋日期型 View、FormMixin** |
| 表單收 POST | function view | function view（add_review） | **FormMixin on DetailView** |
| 副作用 | — | context processor | **signal** |

---

## 下一份教材（Deck 03B）會加入什麼？

**傳播、效能與帳號**——目前 `learnjournal/` 程式碼裡以 `# Deck 03B …` 標出掛鉤點：

- Sessions 與 Cookies：匿名「最近瀏覽」
- 快取框架 ＋ 片段快取；用 signal 失效快取；`django-debug-toolbar` 看 SQL 數
- Signals 深入（留言通知寄信、`m2m_changed` 更新計數）＋ 自訂 middleware
- Email 與內建密碼重設；電子報 double opt-in
- 全文檢索：`icontains` → PostgreSQL `SearchVector`／`SearchRank`（換資料庫）
- `contrib.syndication`（RSS）、`contrib.sitemaps`
- Django 權限框架（Group／Permission）取代「任何登入者都能寫」
- 帶參數的 management command ＋ cron（`publish_scheduled`、`send_weekly_digest`）
- `inlineformset_factory`（一篇文章多張圖）

**Deck 04** 則是部署與營運：環境變數、`DEBUG=False`、`collectstatic`、WSGI server、`check --deploy` 收尾。

---

## 驗證你已完成 Deck 03A

```bash
cd learnjournal
uv run python manage.py check
uv run python manage.py makemigrations --check      # No changes detected
uv run python manage.py test                        # 11 passed
```

你應該能不看投影片回答：

1. 「文章 ↔ 標籤」在資料庫裡實際是幾張表？
2. `Article.objects` 與 `Article.published` 差在哪？
3. 為什麼 `get_absolute_url()` 要用 `timezone.localtime()`？
4. `mark_safe` 什麼時候安全、什麼時候是漏洞？
5. `FormMixin` 補了 `DetailView` 缺少的哪些方法？

> 先確定你能用檔案與資料關聯說明「內容站的結構」；Deck 03B 才把「做出內容」推進到「內容被傳播、扛得住流量」。
