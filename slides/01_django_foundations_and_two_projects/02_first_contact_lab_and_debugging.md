---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "Django 01｜第一次實作操作導引"
footer: "補充 lab｜指令、成功訊號、錯誤定位"
---

<!-- _class: cover -->

# Django 01 補充 Lab
## 第一次從 Terminal 走到 Django Page

<div class="box">我在哪裡？→ 我跑了什麼？→ 成功長什麼樣？→ 失敗從哪一行看？</div>

---

## 0. 每次先確認「我在哪裡」

macOS/Linux：

```bash
pwd
ls
```

PowerShell：

```powershell
Get-Location
Get-ChildItem
```

你應該看到 `manage.py` 與 `pyproject.toml`。

若看不到，不要繼續輸入 migration/runserver 指令。

---

## 1. `uv sync` 到底做什麼？

```bash
uv sync
```

它依 `pyproject.toml` / `uv.lock` 準備專案 Python 環境與依賴。

成功後不要只看「沒報錯」；再驗證：

```bash
uv run python --version
uv run python -c "import django; print(django.get_version())"
```

---

## 2. `uv run` 的心智模型

```bash
uv run python manage.py check
```

拆開看：

```text
uv run
  └─ 用這個 project 的環境執行
      └─ python manage.py check
```

不要混用「系統 python」與專案環境中的 python。

---

## 3. 第一次先跑 `check`

```bash
uv run python manage.py check
```

理想輸出：

```text
System check identified no issues (0 silenced).
```

如果這一步就失敗，先不要跑 migrate/runserver；先處理 import/settings/URL 等問題。

---

## 4. Migration 三步驟不要背成一團

```text
models.py 改變
   ↓
makemigrations   產生「變更計畫檔」
   ↓
migrate          把 migration 套到 database
```

常用：

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

---

## 5. `makemigrations --check` 是什麼？

```bash
uv run python manage.py makemigrations --check
```

用途：確認 `models.py` 沒有尚未建立 migration 的變更。

它不是「執行 migration」。

---

## 6. 看 migration，不要只相信它

```bash
uv run python manage.py showmigrations
uv run python manage.py migrate --plan
```

某 app 的 SQL：

```bash
uv run python manage.py sqlmigrate board 0002
```

把「Python migration operation」連到「資料庫 schema 真的會怎麼改」。

---

## 7. 啟動 server 後 Terminal 不會回 prompt

```bash
uv run python manage.py runserver
```

Terminal 會被 server process 佔住，這是正常的。

你要：

- 保留它看 request log / traceback
- 開第二個 terminal 跑 shell/test
- 停止 server：`Ctrl+C`

---

## 8. 成功啟動長什麼樣？

你應該看到類似：

```text
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

瀏覽器開：

```text
http://127.0.0.1:8000/
```

不是把 URL 當成 terminal 指令。

---

## 9. Request log 是第一個 debugger

瀏覽一頁後 terminal 會出現：

```text
"GET / HTTP/1.1" 200 ...
```

觀察：

- method：GET / POST
- path
- status code

先從 HTTP 層判斷問題，再進 Python。

---

## 10. 常見 status code 怎麼讀？

- 200：有正常 response
- 302：redirect；不等於失敗
- 403：知道你是誰，但不允許
- 404：URL 或物件找不到
- 405：這個 URL 不接受該 HTTP method
- 500：server-side exception

先看 status，再猜原因。

---

## 11. Traceback 要從哪裡開始？

不要從最上面一路讀到失去方向。

先找 traceback 最下面：

```text
ExceptionType: 最終錯誤訊息
```

再往上找第一個屬於你專案的檔案：

```text
.../board/views.py, line 23
```

先修最靠近 exception 的「自己程式碼」。

---

## 12. `ModuleNotFoundError` 常見原因

```text
ModuleNotFoundError: No module named '...'
```

檢查順序：

1. 有沒有 `uv sync`
2. 是否用 `uv run python ...`
3. app/module 名稱拼對嗎
4. `INSTALLED_APPS` 有嗎
5. import path 正確嗎

---

## 13. `TemplateDoesNotExist`

```text
TemplateDoesNotExist: board/message_list.html
```

檢查：

- template path 拼字
- `templates/` 放哪裡
- `TEMPLATES["DIRS"]`
- app templates convention
- `render()` / CBV `template_name`

---

## 14. `NoReverseMatch`

常見訊息：

```text
NoReverseMatch: Reverse for 'detail' ...
```

問三件事：

1. URL name 對嗎？
2. namespace 對嗎？
3. required args/kwargs 有傳嗎？

可以用 shell 驗證：

```bash
uv run python manage.py shell
```

```python
from django.urls import reverse
reverse("board:list")
```

---

## 15. ORM 先在 shell 小步驗證

```bash
uv run python manage.py shell
```

```python
from board.models import Message
Message.objects.count()
Message.objects.all()[:3]
```

先確認 QuerySet 做得到，再把它放進 view。

---

## 16. 修改 model 後的固定節奏

```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
uv run python manage.py check
uv run python manage.py test
```

不要只 reload browser。

Model schema 改變需要 database 跟著改。

---

## 17. 測試不要一次只會「全部跑」

全部：

```bash
uv run python manage.py test
```

指定 app：

```bash
uv run python manage.py test board
```

指定 class / method：

```bash
uv run python manage.py test board.tests.BoardAccessTests.test_home_shows_message
```

Debug 時縮小範圍，修完再跑全部。

---

## 18. 測試 failure 怎麼讀？

先看：

```text
FAIL: test_xxx (...)
```

再看：

```text
AssertionError: expected != actual
```

最後看 test 裡「Arrange / Act / Assert」哪一段的假設錯了。

不要第一時間把 assertion 改成目前結果。

---

## 19. 每次 lab 的完成條件

不要只寫「做完」。至少留下：

- 執行過哪些 command
- 預期 URL/status
- shell 查到什麼
- test 名稱與結果
- 遇到的錯誤與修法

這份紀錄就是你的 debugging notebook。

---

## 20. 第一次 Django 的固定節奏

```text
確認目錄
→ uv sync
→ check
→ migrate
→ runserver
→ browser 看 request
→ shell 驗證 ORM
→ 修改一小步
→ test
→ 全部 test
```

先把節奏練熟，再追求功能速度。
