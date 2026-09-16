---
marp: true
theme: default
paginate: true
---

# 03B-4 Group / Permission

LearnMart 用 `role` 欄位分買家與賣家；LearnJournal 改用 Django 內建權限系統。

---

# 三個問題要分開

1. 你有登入嗎？→ authentication
2. 你有某個 capability 嗎？→ permission
3. 這一筆資料是你的嗎？→ ownership

不要只寫一個 `if user.role == ...` 把三件事混在一起。

---

# Django 自動建立的 model permissions

每個 model 通常會有：

- `add_article`
- `change_article`
- `delete_article`
- `view_article`

我們另外加：

```python
class Meta:
    permissions = [
        ("publish_article", "Can publish and schedule articles"),
    ]
```

---

# Migration 仍然重要

改 `Meta.permissions` 後：

```bash
uv run python manage.py makemigrations --check
uv run python manage.py migrate
```

本 repo 已保留 `0004_alter_article_options.py`，讓學生看到 permission 也屬於 model state 演進。

---

# Group = 一組 permissions

`seed_demo` 建立：

```text
Editors
 ├─ add_article
 ├─ change_article
 ├─ view_article
 └─ publish_article
```

`editor` 使用者加入 Editors；`amy` / `ben` 沒有 publish capability。

---

# 在程式碼問 capability

```python
user.has_perm("journal.publish_article")
```

不是：

```python
user.username == "editor"
```

也不是：

```python
user.groups.filter(name="Editors").exists()
```

後兩者把政策寫死在名稱，而不是 capability。

---

# 表單層阻止發佈

一般作者可以寫草稿；要排程／發佈才檢查：

```python
if status in {SCHEDULED, PUBLISHED}:
    if not user.has_perm("journal.publish_article"):
        self.add_error("status", "你沒有發佈權限")
```

這比把整個寫作頁鎖死更符合實際 editorial workflow。

---

# Ownership 仍然是另一層

即使有 `change_article`，這個教學版仍示範：

```python
return Article.objects.filter(author=self.request.user)
```

所以「能編文章」不代表「能編別人的文章」。

---

# 操作比較

登入 `amy`：

- 可新增草稿
- 選「已發佈」會看到表單錯誤

登入 `editor`：

- `seed_demo` 已把他放入 Editors
- 可以排程／發佈

---

# 測試 capability

```python
permission = Permission.objects.get(codename="publish_article")
editors.permissions.add(permission)
user.groups.add(editors)
self.assertTrue(user.has_perm("journal.publish_article"))
```

測 permission，不測硬編碼群組名稱。

---

# 常見錯誤

- migration 後找不到 permission：確認有跑 `migrate`
- 測試中加 group 後舊結果不變：注意 permission cache
- 只有 template 隱藏按鈕：後端仍必須驗證
- 把 staff/superuser 當所有 domain role：管理權限和業務權限不是同一件事

---

# 本章檢核

1. Group 和 Permission 的關係？
2. 為什麼 template 隱藏按鈕不算授權？
3. ownership 與 permission 能互相取代嗎？
4. 什麼時候自訂 `role` 欄位反而更簡單？
