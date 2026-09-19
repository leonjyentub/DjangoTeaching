# LearnBoard 02 配套實作手冊

本手冊在 [Django 課程教材](../README.md) 的 LearnBoard 第二階段配合使用；主教材保留問題與任務，本手冊提供答案、推理、實作步驟與前後程式碼對照。

> 建議先獨立回答，再查看解答。涉及 source code 的練習請在個人練習 branch 進行。每段「修改後」只顯示焦點 excerpt，不代表整個檔案。

## 目錄

1. [第 1 章｜完整表單生命週期](#chapter-1)
2. [第 2 章｜身份驗證：註冊、登入與 session](#chapter-2)
3. [第 3 章｜Model 演進：把留言連回作者](#chapter-3)
4. [第 4 章｜CBV 與物件擁有權](#chapter-4)
5. [第 5 章｜安全三課](#chapter-5)
6. [第 6 章｜測試與回歸防護](#chapter-6)
7. [附錄｜結業總驗收清單](#appendix)

---

<a id="chapter-1"></a>
# 第 1 章｜完整表單生命週期

## 觀念檢核答案

### 1. PRG 模式解決什麼問題？

Post/Redirect/Get 防止「重新整理重複送 POST」。POST 成功後立刻 302 到一個 GET 網址，使用者重新整理時只會重送無害的 GET。

### 2. `request.POST or None` 在 GET 與 POST 時各是什麼？

POST 時 `request.POST` 是 QueryDict（truthy）→ form 帶資料驗證；GET 時是空的（falsy）→ `or None` 讓 form 初始化為空表單。一行同時服務兩個分支。

### 3. Form 與 ModelForm 怎麼選？

資料最終要存進某個 model → ModelForm（驗證規則繼承 model、`save()` 直接入庫）；只是處理輸入（如聯絡我們、純查詢）→ 一般 Form。留言板兩種都示範過：MessageForm 是 ModelForm。

### 4. `{% csrf_token %}` 少了會怎樣？為什麼現在只說現象？

所有 POST 回 403 CSRF verification failed。原理（攻擊情境）刻意留到第 5 章——先讓身體記住「403 = 想到 token」，第 5 章再補上「為什麼要這張票」。

## 實作任務：匿名發文過渡版＋邊界測試

### 影響檔案／符號

```text
board/forms.py        # MessageForm
board/views.py        # create_message function view（過渡版）
board/urls.py         # path("new/", views.create_message, name="create")
templates/board/message_form.html
```

### 焦點前後對照

**修改前：**只有唯讀列表。

**修改後（過渡版 view）：**

```python
def create_message(request):
    form = MessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("board:list")
    return render(request, "board/message_form.html", {"form": form})
```

### 步驟

1. 建立 MessageForm（ModelForm，fields=("content",)）
2. 加入上述 view 與路由
3. 模板放 `<form method="post">{% csrf_token %}{{ form.as_p }}<button>發布</button></form>`
4. 邊界測試：
   - 全空白內容送出 → 表單紅字 "This field is required."
   - 貼上 600 字 → 被 max_length=500 擋下（HTML maxlength 先擋；用工具繞過後伺服器仍擋）

### 驗收

- 發布成功後 redirect 回首頁且出現綠色提示（若已接 messages）
- **重新整理不會重複發文**（PRG 生效）
- 用 curl 直接 POST `/new/` 得 403（CSRF 生效）

---

<a id="chapter-2"></a>
# 第 2 章｜身份驗證：註冊、登入與 session

## 觀念檢核答案

### 1. sessionid cookie 被偷走會發生什麼？

攻擊者可以冒充你（session hijacking），直到 session 過期或被註銷。這正是全站 HTTPS 的理由——HTTP 明文傳輸時 cookie 可能被中間人讀走。

### 2. `authenticate` 回傳 None 代表什麼？

帳號不存在或密碼不符（不區分原因，避免洩漏帳號存在性）。view 必須處理 None 分支，不能假設一定拿到 user。

### 3. `?next=` 的完整流程？

匿名開啟受保護頁 → LoginRequiredMixin 302 到 `LOGIN_URL?next=原網址` → 使用者登入成功 → LoginView 讀 next 參數 → 302 回原網址。若無 next 則去 `LOGIN_REDIRECT_URL`。

### 4. 為什麼登出要用 POST？

GET 的登出連結可能被 `<img src="/accounts/logout/">`、預載入、爬蟲誤觸，造成被動登出甚至 CSRF 式操作。改變狀態的動作一律 POST＋csrf token。

## 實作任務：完整帳號流程演練

### 影響檔案

```text
board/forms.py            # RegistrationForm（UserCreationForm 子類）
board/views.py            # register function view
config/urls.py            # login/logout 路由
templates/registration/login.html、register.html
```

### 步驟

1. 確認 settings 已有四組 AUTH_PASSWORD_VALIDATORS
2. 註冊新帳號 carol：
   - 密碼設 `123` → 觸發強度驗證錯誤（太短／太常見）
   - 兩次密碼不一致 → "The two password fields didn't match"
   - 合法密碼 `strong-pass-99` → 自動登入並回首頁，導覽列顯示嗨，carol
3. 登出 → 再登入
4. 匿名直接開 `/new/` → 302 到 `/accounts/login/?next=/new/`，登入後回到發文頁

### 驗收

```python
>>> from django.contrib.auth.models import User
>>> User.objects.get(username="carol").password.startswith("pbkdf2_sha256")
True
```

雜湊而非明文，即為通關。

---

<a id="chapter-3"></a>
# 第 3 章｜Model 演進：把留言連回作者

## 觀念檢核答案

### 1. 為什麼選 SET_NULL 而不是 CASCADE？

留言板的社群價值在內容本身。作者刪除帳號時，CASCADE 會連環刪掉他的所有留言（甚至波及被回覆的討論脈絡）；SET_NULL 保留內容、標示為訪客，損害最小。

### 2. `null=True` 與 `blank=True` 分別影響哪一層？

`null=True` 是**資料庫層**允許 NULL；`blank=True` 是**表單/驗證層**允許留空。兩者獨立設定；FK 兩個都要才順滑。

### 3. 為什麼用 `settings.AUTH_USER_MODEL` 而不 import User？

它以字串指向專案的使用者 model。未來換成自訂 User（商城的 AbstractUser 做法）時，model 不需要改 import；官方文件也建議可重用 app 一律這樣寫。

### 4. `form.save(commit=False)` 解決什麼問題？

取得尚未寫入 DB 的 instance，讓你在 save 前補上程式決定的欄位（author）。直接 `form.save()` 會因 author 未填而失敗（或存成 NULL）。

## 實作任務：重走一遍加欄位流程

> repository 已含最終結果（models.py 有 author、0002 migration 存在）。請在練習 branch 上把 models.py 的 author 暫時移除體驗反向流程，或直接閱讀既有 migration 回答下列問題。

### 觀察作業

1. 打開 `board/migrations/0002_message_author.py`
2. 回答：

| dependencies 項目 | 代表什麼 |
|---|---|
| `("board", "0001_initial")` | 本表必須先存在（0001 建 Message） |
| `("auth", "0012_...")` | FK 目標 auth.User 的 schema 必須就緒 |

3. 執行：

```bash
uv run python manage.py migrate --plan    # 看執行順序圖
uv run python manage.py sqlmigrate board 0002   # 看轉成的 SQL
```

### 驗收

- 登入 alice 發一篇留言 → 卡片顯示 alice
- seed_demo 的訪客留言仍顯示「訪客」（NULL author 分支正常）
- `alice.messages.all()` 在 shell 可反向查出她的留言

---

<a id="chapter-4"></a>
# 第 4 章｜CBV 與物件擁有權

## 觀念檢核答案

### 1. get_queryset 過濾如何同時做到授權與隱匿存在性？

CBV 的 `get_object()` 只在過濾後的集合裡找。他人之物＝不在你的世界裡＝404。攻擊者連「這個 id 存在」的資訊都拿不到，比 403 更隱匿。

### 2. 為什麼刪除不用 queryset 過濾，而用 test_func？

管理員（staff）要能刪任何人的留言。queryset 過濾會把「他人的留言」整個藏起來，staff 也看不到確認頁。test_func 能表達「找得到，但要看你是不是作者或 staff」的細粒度規則。

### 3. reverse_lazy 解決什麼時序問題？

類別屬性在 urls.py 載入期間就被求值，此時 URLconf 尚未註冊完成，`reverse()` 會炸 NoReverseMatch 或循環匯入。reverse_lazy 把計算延後到真正需要（redirect 當下）。

### 4. 為什麼說模板藏按鈕不算安全措施？

模板只是呈現層；任何人可以直接打網址發請求。真正的授權必須在 view 層（queryset/test_func）——按鈕是給守規矩的人看的便利，不是防線。

## 實作任務：四身份實測矩陣

### 步驟

| 操作 | 匿名 | bob（非作者） | alice（作者） | staff |
|---|---|---|---|---|
| GET /messages/{alice的id}/edit/ | 302→login | **404** | 200 | 200 |
| POST 同網址 | 302→login | **404**（內容不變） | 302→list（已更新） | 302→list |
| GET /messages/{id}/delete/ | 302→login | **403** | 200 | 200 |
| POST 同網址 | 302→login | **403**（仍存在） | 302→list（已刪） | 302→list（已刪） |

逐格驗證並記錄狀態碼；任何一格不符合，回到 views.py 找是哪一層防禦沒生效。

---

<a id="chapter-5"></a>
# 第 5 章｜安全三課

## 觀念檢核答案

### 1. 三種攻擊分別濫用了什麼信任？

| 攻擊 | 濫用的信任 |
|---|---|
| XSS | 瀏覽器信任你網站送出的 HTML（注入腳本混進來） |
| CSRF | 你的伺服器信任「帶著有效 session 的請求＝本人」（借瀏覽器的身份） |
| IDOR | 伺服器只信任「登入」卻沒驗證「歸屬」 |

### 2. 為什麼 csrf token 能防 CSRF 卻防不了 XSS？

Token 阻擋的是「外部站點發起的偽造請求」——攻擊者拿不到 token。但 XSS 已經在你的頁面裡跑腳本，可以讀 DOM、以你的名義發同源請求，token 自然也在它的勢力範圍內。兩者是不同層的威脅，需要各自的防線（跳脫 vs token）。

### 3. 若把留言內容加上 `|safe`，哪一課的防線瓦解了？

XSS。跳脫是 XSS 的唯一主防線，`|safe` 直接關掉它。

### 4. IDOR 與第 4 章哪段程式碼一一對應？

`MessageUpdateView.get_queryset`（404 防線）與 `OwnerOrStaffMixin.test_func`（403 防線）。

## 實作任務：三次親手觸發

1. **XSS 被跳脫：**admin 新增留言 `<script>alert(1)</script>` → 前台看到文字、檢視原始碼確認 `&lt;script&gt;`
2. **CSRF 被擋：**暫時移除 message_form.html 的 `{% csrf_token %}` → 送出得 403 → 還原
3. **IDOR 被擋：**bob 登入打 alice 的 edit/delete 網址 → 404／403（見第 4 章矩陣）

每項截圖存證，寫一句「防線在哪一行」。

---

<a id="chapter-6"></a>
# 第 6 章｜測試與回歸防護

## 觀念檢核答案

### 1. TestCase 如何保證測試互不污染？

每個 test 方法都在全新的測試資料庫（或包在 transaction 中 rollback）執行，setUp 重建所需資料；結束即銷毀，永不碰 db.sqlite3。

### 2. assertRedirects 除了狀態碼還檢查什麼？

還會真的 GET 目標網址並確認其為 200——驗證 redirect 鏈完整可用，不只是數字正確。

### 3. refresh_from_db() 為什麼必要？

ORM 以 identity map 快取 instance；測試中 post 之後手上那個 self.message 仍是舊值。refresh_from_db() 重新 SELECT，斷言才是對資料庫真況的判斷。

### 4. 「每修一 bug 加一測試」累積三年後是什麼？

一套由真實事故轉化的回歸防護網。任何重構只要弄壞曾經的 bug，測試立即變紅——bug 可以復發一次，不會第二次。

## 實作任務：為「已編輯徽章」寫測試

### 影響檔案

```text
board/tests.py    # 新增一個方法到 MessagePermissionTests 或新 class
```

### 焦點前後對照

**修改前：**無此測試。

**修改後：**

```python
def test_edit_updates_timestamp_and_marks_edited(self):
    self.client.login(username="alice", password="safe-pass-123")
    original = self.message.updated_at
    response = self.client.post(
        reverse("board:update", args=[self.message.pk]),
        {"content": "alice 改過的留言"},
    )
    self.assertRedirects(response, reverse("board:list"))
    self.message.refresh_from_db()
    self.assertNotEqual(self.message.updated_at, original)
    page = self.client.get(reverse("board:list"))
    self.assertContains(page, "已編輯")
```

### 步驟

1. 把方法加入 tests.py
2. `uv run python manage.py test board.tests -v 2` 確認綠燈
3. 反向驗證：把 message_list.html 的「已編輯」徽章暫時刪掉 → 測試應變紅 → 還原

### 驗收

- 測試綠燈；步驟 3 的紅燈證明測試真的在守護行為

---

<a id="appendix"></a>
# 附錄｜結業總驗收清單

完成第一階段前，逐項自評：

- [ ] 能從空白機器四步啟動 LearnBoard 並說明每一動影響哪一層
- [ ] 能畫出 GET `/` 與 POST `/new/` 各自的完整旅程（含 middleware 與 session）
- [ ] 說得出 Form 驗證為何必須在伺服器端
- [ ] 能口述 PRG、session 心智模型、密碼雜湊單向性
- [ ] 讀懂 0001→0002 兩支 migration，講出 schema 演進故事
- [ ] 能解釋 404 與 403 兩道防線各自的選擇理由
- [ ] 親手觸發過 XSS 跳脫、CSRF 403、IDOR 404/403 三個現象
- [ ] `uv run python manage.py test` 綠燈，且能說出每支測試守住什麼

全部打勾 → 你已完成個人留言板課程，具備進入 LearnMart 商城教材的全部前置能力。

下一站：[Django 課程教材](../README.md) 的 LearnMart 章節。
