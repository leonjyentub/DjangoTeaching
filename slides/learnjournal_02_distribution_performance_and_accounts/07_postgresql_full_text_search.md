---
marp: true
theme: default
paginate: true
---

# 03B-7 PostgreSQL Full-text Search

SQLite 版本先用 `icontains`；PostgreSQL 版本再加入真正的全文搜尋與 rank。

---

# 先理解目前的 fallback

```python
return self.filter(
    Q(title__icontains=term) |
    Q(body__icontains=term)
)
```

優點：簡單、零設定。

限制：沒有 relevance ranking，也不是為大量全文檢索設計。

---

# PostgreSQL 路徑

```python
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
)
```

- SearchVector：哪些欄位要建立 searchable document
- SearchQuery：使用者查詢
- SearchRank：相關度

---

# 欄位權重

```python
vector = (
    SearchVector("title", weight="A", config="simple")
    + SearchVector("body", weight="B", config="simple")
)
```

標題比內文更重要，所以 title 權重高。

---

# Rank

```python
query = SearchQuery(
    term,
    search_type="websearch",
    config="simple",
)

qs.annotate(
    search_rank=SearchRank(vector, query)
).filter(
    search_rank__gte=0.05
).order_by("-search_rank")
```

這不只是「有沒有包含」，還能排序相關度。

---

# 安裝 PostgreSQL driver

本專案把 driver 放在 optional dependency：

```bash
uv sync --extra postgres
```

如果 `uv.lock` 因 pyproject 更新需要重算，uv 會在本機解析並更新 lock。

---

# 切換資料庫

macOS/Linux 範例：

```bash
export DJANGO_DB_ENGINE=postgresql
export DJANGO_DB_NAME=learnjournal
export DJANGO_DB_USER=learnjournal
export DJANGO_DB_PASSWORD=your-password
export DJANGO_DB_HOST=127.0.0.1
uv run python manage.py migrate
```

PowerShell 用 `$env:...` 設定同名變數。

---

# 確認真的連到 PostgreSQL

```bash
uv run python manage.py shell -c \
  "from django.db import connection; print(connection.vendor)"
```

應輸出：

```text
postgresql
```

不要只因為環境變數有設定就假設切換成功。

---

# 同一個 `.search()`，兩條 backend

```python
if connection.vendor == "postgresql":
    # SearchVector / SearchRank
else:
    # icontains fallback
```

這個設計讓教材能先教 ORM API，再比較資料庫能力差異。

---

# 中文全文檢索的現實

PostgreSQL `simple` configuration 不會替你解決所有中文斷詞需求。

正式中文搜尋可能還要評估：

- `pg_trgm`
- n-gram / tokenizer extension
- 專門搜尋服務
- domain-specific normalization

本章重點是 Django/PostgreSQL FTS 心智模型，不宣稱 `simple` 是中文搜尋最終方案。

---

# Query plan 與 index 是下一層

資料量變大後再談：

- `SearchVectorField`
- GIN index
- materialized vector
- `EXPLAIN ANALYZE`

不要在 20 筆 demo data 就先做過度最佳化。

---

# 常見錯誤

- `psycopg` import error：`uv sync --extra postgres`
- connection refused：DB server/port/host
- authentication failed：帳密/pg_hba
- migrate 後資料是空的：SQLite 與 PostgreSQL 是不同 database
- 中文結果不理想：tokenization 問題，不是 ORM 壞掉

---

# 本章檢核

1. `icontains` 和 full-text search 的核心差異？
2. SearchVector / SearchQuery / SearchRank 各做什麼？
3. 為什麼 title 可以給較高權重？
4. 為什麼切 DB 後要重新 migrate/seed？
