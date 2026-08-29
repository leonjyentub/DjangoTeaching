---
marp: true
theme: default
size: 16:9
paginate: true
header: "LearnBoard 02｜表單、帳號與留言權限"
footer: "Django 初學者課程｜LearnBoard"
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
  h1 { color: #1e3a8a; }
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

# 第 6 章
## 測試與回歸防護

目標：把前面所有行為規格化成 TestCase，讓未來的重構有安全網。

<!--
授課提示：測試不是額外作業，是把「手動實測」變成「機器代跑」。第 4 章的四身份實測就是現成的測試藍圖。
-->

---

## TestCase：每次都是全新資料庫

```python
from django.test import TestCase


class MyTest(TestCase):
    def setUp(self):          # 每個測試方法執行前都跑一次
        ...

    def test_something(self): # 一個方法 = 一個獨立案例
        ...
```

- 每個測試方法都從乾淨的測試資料庫開始，互不污染
- 測試結束自動銷毀，不碰真正的 db.sqlite3
- 斷言失敗 → 詳細 diff

---

## 測試用 client：模擬瀏覽器

```python
response = self.client.get(reverse("board:list"))
self.assertEqual(response.status_code, 200)

self.client.login(username="alice", password="safe-pass-123")
response = self.client.post(reverse("board:create"), {"content": "hi"})
self.assertRedirects(response, reverse("board:list"))

self.assertContains(response, "hi")     # 內容斷言
```

`reverse()` 取網址（路由改名測試不必跟著改）；client 能 GET/POST/login/logout。

---

## 我們的測試長什麼樣：公開讀取

```python
# board/tests.py（目前 LearnBoard 實作｜節錄）
class BoardAccessTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="safe-pass-123")
        Message.objects.create(author=self.alice, content="今天天氣很好")

    def test_home_shows_message(self):
        response = self.client.get(reverse("board:list"))
        self.assertContains(response, "今天天氣很好")

    def test_search_filters_messages(self):
        Message.objects.create(author=self.alice, content="Django 真好玩")
        response = self.client.get(reverse("board:list"), {"q": "Django"})
        self.assertContains(response, "Django 真好玩")
        self.assertNotContains(response, "今天天氣很好")
```

setUp 建舞台 → 測試方法演出一幕 → 斷言結果。命名即規格。

---

## 身份與擁有權的自動化

```python
class MessagePermissionTests(TestCase):
    def setUp(self):
        self.alice = ...; self.bob = ...
        self.staff = User.objects.create_user(username="staffer",
                                              password="safe-pass-123", is_staff=True)
        self.message = Message.objects.create(author=self.alice, content="alice 的留言")

    def test_anonymous_cannot_open_create_form(self):
        response = self.client.get(reverse("board:create"))
        self.assertRedirects(response, f"/accounts/login/?next={reverse('board:create')}")

    def test_create_assigns_logged_in_author(self):
        self.client.login(username="bob", password="safe-pass-123")
        self.client.post(reverse("board:create"), {"content": "bob 的新留言"})
        self.assertEqual(Message.objects.get(content="bob 的新留言").author, self.bob)

    def test_user_cannot_edit_anothers_message(self):
        self.client.login(username="bob", password="safe-pass-123")
        response = self.client.post(reverse("board:update", args=[self.message.pk]),
                                    {"content": "被竄改"})
        self.assertEqual(response.status_code, 404)   # queryset 過濾生效
        self.message.refresh_from_db()
        self.assertEqual(self.message.content, "alice 的留言")   # 內容未被動
```

---

## 403 與管理員放行

```python
    def test_non_owner_cannot_delete_but_staff_can(self):
        self.client.login(username="bob", password="safe-pass-123")
        response = self.client.post(reverse("board:delete", args=[self.message.pk]))
        self.assertEqual(response.status_code, 403)              # OwnerOrStaffMixin
        self.assertTrue(Message.objects.filter(pk=self.message.pk).exists())

        self.client.login(username="staffer", password="safe-pass-123")
        response = self.client.post(reverse("board:delete", args=[self.message.pk]))
        self.assertRedirects(response, reverse("board:list"))    # staff 放行
        self.assertFalse(Message.objects.filter(pk=self.message.pk).exists())
```

第 4 章的手動實測，現在 0.5 秒跑完——而且永遠不會被忘記。

---

## 執行與閱讀測試結果

```bash
uv run python manage.py test
```

```text
Ran 9 tests in 3.459s

OK
```

失敗時輸出會指出：哪個測試、哪一行、期望 vs 實際。

**開發節奏：**改程式 → 跑測試 → 綠燈才 commit。紅燈訊息本身就是除錯線索。

> **補充／進階：**`coverage run manage.py test && coverage report` 可以量化哪些行沒被測到。

---

## 測試清單：哪些行為值得固守？

| 類別 | 案例 |
|---|---|
| 公開讀取 | 首頁顯示留言；搜尋過濾正確 |
| 註冊登入 | 註冊後自動登入；登出清除 session |
| 門禁 | 匿名打 create 被 302 到登入頁 |
| 授權 | 改他人留言得 404；刪他人留言得 403；staff 可刪 |
| CRUD | 編輯後內容更新；刪除後消失 |

**心法：**每修一個 bug 就加一個測試，防止它回來（regression 的字面意義）。

---

## 第 6 章｜觀念檢核與實作

**觀念檢核：**

1. TestCase 如何保證測試互不污染？
2. `assertRedirects` 除了狀態碼還檢查什麼？
3. `refresh_from_db()` 為什麼必要？（提示：ORM 的 identity map）
4. 「每修一 bug 加一測試」累積三年後，這套測試變成什麼？

**實作任務：**為「編輯後 updated_at 變動、畫面出現『已編輯』徽章」寫一支測試。

→ 步驟與解答在配套手冊第 6 章。

---

## 總結：你現在擁有一個完整的個人留言板

```text
Deck 01（唯讀牆）           本冊補完
─────────────────          ─────────────────
列表＋搜尋                  ＋ 發文表單（POST/PRG/messages）
                            ＋ 註冊／登入／session
                            ＋ author FK（migration 演進）
                            ＋ 編輯／刪除（擁有權 403/404）
                            ＋ CSRF/XSS/IDOR 防線
                            ＋ 9 支自動化測試
```

**下一站 LearnMart 商城**：同一套功夫，加上角色（買家/賣家）、購物車、transaction 交易一致性——所有概念都能在這個小專案找到原型。

<!--
授課提示：結業前請每位學生完成總驗收清單（workbook 附錄），並保留 learnboard 專案供商城階段對照。
-->
