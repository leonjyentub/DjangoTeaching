---
marp: true
theme: default
paginate: true
---

# P2-1 Settings / Environment Variables

第一條 production 規則：**部署差異不要靠改 Git 裡的秘密字串。**

---

# 哪些值不該硬編碼？

- `SECRET_KEY`
- database password
- SMTP password
- object-storage credentials
- API keys
- production host names

這些值屬於部署環境，不屬於教材 repository。

---

# Classroom default vs production override

LearnJournal 現在示範：

```python
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-...classroom-only...",
)
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
```

本機 clone 可直接跑；production 必須 override。

---

# 讀環境變數

macOS/Linux：

```bash
export DJANGO_DEBUG=0
export DJANGO_SECRET_KEY='replace-me'
```

PowerShell：

```powershell
$env:DJANGO_DEBUG="0"
$env:DJANGO_SECRET_KEY="replace-me"
```

驗證：

```bash
uv run python manage.py shell -c "from django.conf import settings; print(settings.DEBUG)"
```

---

# 不要提交 `.env`

`.env` 可以是本機便利工具，但它通常包含 secrets。

Git 原則：

```text
.env            → ignore
.env.example    → 可提交，只放欄位名稱與假值
```

真正 production secrets 交給平台 secret manager / environment config。

---

# ALLOWED_HOSTS

`DEBUG=False` 時要明確列允許 host：

```text
DJANGO_ALLOWED_HOSTS=example.com,www.example.com
```

這不是 CORS；它是 Host header 防護的一部分。

---

# Settings split 要不要做？

小專案可以先用 environment variables。

專案變大後可拆：

```text
settings/
  base.py
  dev.py
  production.py
```

重點不是檔案數，而是避免 dev/prod 差異散落在程式碼各處。

---

# 本章檢核

1. SECRET_KEY 為什麼不能提交？
2. `.env.example` 可以放真密碼嗎？
3. ALLOWED_HOSTS 和 CORS 是同一件事嗎？
4. 何時值得拆 settings module？
