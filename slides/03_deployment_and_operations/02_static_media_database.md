---
marp: true
theme: default
paginate: true
---

# P2-2 Static / Media / Database

三種資料不要混：

- static：開發者提供的 CSS/JS/image
- media：使用者上傳
- database：結構化資料

---

# `runserver` 幫你做了很多事

開發環境 `DEBUG=True` 時 static 看起來「自己就能用」。

production 不應依賴 `runserver`。

---

# `collectstatic`

```bash
uv run python manage.py collectstatic --noinput
```

它把各 app / `STATICFILES_DIRS` 的 static 收集到：

```python
STATIC_ROOT
```

再交給 web server / CDN / storage backend 提供。

---

# Media 不等於 Static

LearnMart 的商品圖片是 media。

不要把使用者上傳檔跟程式版本綁在 container image 裡。

production 常見做法：

- persistent disk
- object storage
- CDN 前置

---

# 上傳安全

至少思考：

- content type / extension 不能完全相信 client
- 檔案大小限制
- image decode / malware scanning
- private vs public media
- 不讓 upload path 直接執行程式碼

---

# SQLite 到 PostgreSQL

SQLite 非常適合教學與單機 demo。

production 多使用者服務通常需要：

- concurrent writes
- server DB
- backup / replication
- 權限隔離
- richer indexing / FTS

LearnJournal 03B 已示範用環境變數切 PostgreSQL。

---

# 切 DB 不等於搬資料

改設定後：

```bash
uv run python manage.py migrate
```

只建立 schema；舊 SQLite 資料不會自動出現在 PostgreSQL。

資料搬遷是另一個 migration/import 工作。

---

# `dumpdata` / `loaddata` 的定位

教學小資料可示範：

```bash
uv run python manage.py dumpdata --indent 2 > data.json
uv run python manage.py loaddata data.json
```

但大型 production DB backup 應使用資料庫原生工具與 managed backup。

---

# 本章檢核

1. static / media 的來源與生命週期差在哪？
2. `collectstatic` 會搬使用者上傳檔嗎？
3. 切換 PostgreSQL 後為什麼資料是空的？
4. production backup 為什麼不能只靠 `dumpdata`？
