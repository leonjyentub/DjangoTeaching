---
marp: true
theme: default
paginate: true
---

# P2-5 Migrations / Backup / Recovery

部署最危險的時刻，常常不是 code 上線，而是 schema / data 改動。

---

# 先備回顧：資料模型與檔案

[01B 資料模型、ORM 與 Django Admin](../01b_models_orm_and_admin/01b_models_orm_and_admin.md) 已建立本章需要的觀念：

- Model 描述資料；migration 記錄結構的變更。
- unique／constraint 加入前，既有資料也必須符合規則。
- ImageField 保存 storage 路徑參照；DB 備份不包含圖片內容。
- Admin 改資料與修改 schema 不同；後台操作也需權限與紀錄。

本章接著處理正式部署順序、備份及復原。

---

# Migration 是版本化 schema 變更

部署前先確認：

```bash
uv run python manage.py makemigrations --check
uv run python manage.py showmigrations
```

不要在 production 現場才臨時產生 migration。

---

# Deploy 順序要能相容

理想的 migration：

1. 新舊 code 短時間可以共存
2. 先新增 nullable/default 欄位
3. backfill data
4. code 切換讀新欄位
5. 最後再移除舊欄位

這是 expand → migrate → contract 思路。

---

# Data migration 也會失敗

LearnJournal 03A 已有 `RunPython`。

Production 額外要想：

- 資料量多大？
- transaction 多久？
- 會鎖表嗎？
- 可以重跑嗎？
- rollback 真的可逆嗎？

---

# Backup 的最低標準

你要能回答：

- 備份什麼？DB / media / config
- 多久一次？
- 保留多久？
- 放在哪裡？
- 誰能讀？
- 有沒有測過 restore？

「有 backup job」不等於「能恢復」。

---

# RPO / RTO

兩個常用概念：

- RPO：最多能接受遺失多少時間的資料？
- RTO：服務最多能停多久？

這兩個答案決定 backup 頻率與 recovery 設計。

---

# Rollback 不只是 git revert

Code rollback 容易；database rollback 可能困難。

例如：

- 新 code 已寫入新 schema
- migration 已刪欄位
- data migration 不可逆

所以 schema change 要設計向前/向後相容窗口。

---

# Classroom recovery drill

SQLite 可以做最小演練：

```bash
cp db.sqlite3 db.sqlite3.backup
# 做一個破壞性操作
cp db.sqlite3.backup db.sqlite3
```

這只是概念演練；production PostgreSQL 應使用原生/managed backup 與 restore 流程。

---

# 本章檢核

1. `makemigrations` 應該在 production server 臨時跑嗎？
2. backup 成功紀錄為什麼不等於 restore 可用？
3. RPO / RTO 分別回答什麼？
4. 為什麼 database rollback 比 code rollback 難？
