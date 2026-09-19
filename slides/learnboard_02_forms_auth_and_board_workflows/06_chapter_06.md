---
marp: true
theme: django-teal
size: 16:9
paginate: true
header: "LearnBoard 02｜表單、帳號與留言權限"
footer: "Django 初學者課程｜LearnBoard"
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