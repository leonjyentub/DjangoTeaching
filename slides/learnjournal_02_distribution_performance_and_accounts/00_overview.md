---
marp: true
theme: default
paginate: true
---

# LearnJournal 03B
## 傳播、效能、帳號與排程

這一組教材承接 03A 的內容模型與發佈流程，把「文章做出來」推進到：

**記住讀者 → 降低重複工作 → 擴充 request pipeline → 寄信 → 控制權限 → 被搜尋與訂閱 → 自動排程**

---

# 學習地圖

1. Sessions / Cookies / Cache
2. Custom Middleware
3. Email / Password Reset / Double Opt-in
4. Group / Permission
5. RSS / Sitemap
6. Management Commands / Scheduling
7. PostgreSQL Full-text Search

每章都對應 `learnjournal/` 內可執行程式碼與測試。

---

# 開始前

```bash
cd learnjournal
uv sync
uv run python manage.py migrate
uv run python manage.py seed_demo
uv run python manage.py runserver
```

另開一個終端機執行驗證：

```bash
uv run python manage.py check
uv run python manage.py makemigrations --check
uv run python manage.py test
```

---

# 三種狀態放在哪裡？

| 類型 | 放哪裡 | 本 deck 範例 |
|---|---|---|
| 每次 request 都重新算 | request / DB | 搜尋結果 |
| 同一瀏覽器要記住 | session / cookie | 最近看過、閱讀密度 |
| 多個 request 共用結果 | cache | 導覽分類、側欄片段 |

先問「狀態屬於誰、要活多久、可不可以過期」，再選工具。

---

# 完成里程碑

完成 03B 後，你應能解釋並實作：

- session 與 cookie 的信任邊界
- cache hit / miss / invalidation
- middleware 的呼叫順序
- email token flow
- Group 與 Permission 的差別
- feed / sitemap 的用途
- 可重跑的 management command 與 `--dry-run`
- SQLite 搜尋與 PostgreSQL FTS 的差異

---

# 配套手冊

詳細操作、觀察點與練習：

[`../workbooks/learnjournal_02_distribution_performance_and_accounts_workbook.md`](../workbooks/learnjournal_02_distribution_performance_and_accounts_workbook.md)
