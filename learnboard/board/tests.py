from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Message

User = get_user_model()


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


class AuthFlowTests(TestCase):
    def test_register_logs_in_and_redirects(self):
        response = self.client.post(
            reverse("board:register"),
            {"username": "carol", "password1": "strong-pass-99", "password2": "strong-pass-99"},
        )
        self.assertRedirects(response, reverse("board:list"))
        self.assertTrue(User.objects.filter(username="carol").exists())

    def test_login_then_logout_clears_session(self):
        User.objects.create_user(username="alice", password="safe-pass-123")
        response = self.client.post(reverse("login"), {"username": "alice", "password": "safe-pass-123"})
        self.assertRedirects(response, reverse("board:list"))
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("board:list"))


class MessagePermissionTests(TestCase):
    def setUp(self):
        self.alice = User.objects.create_user(username="alice", password="safe-pass-123")
        self.bob = User.objects.create_user(username="bob", password="safe-pass-123")
        self.staff = User.objects.create_user(username="staffer", password="safe-pass-123", is_staff=True)
        self.message = Message.objects.create(author=self.alice, content="alice 的留言")

    def test_anonymous_cannot_open_create_form(self):
        response = self.client.get(reverse("board:create"))
        self.assertRedirects(response, f"/accounts/login/?next={reverse('board:create')}")

    def test_create_assigns_logged_in_author(self):
        self.client.login(username="bob", password="safe-pass-123")
        self.client.post(reverse("board:create"), {"content": "bob 的新留言"})
        message = Message.objects.get(content="bob 的新留言")
        self.assertEqual(message.author, self.bob)

    def test_user_cannot_edit_anothers_message(self):
        self.client.login(username="bob", password="safe-pass-123")
        response = self.client.post(reverse("board:update", args=[self.message.pk]), {"content": "被竄改"})
        self.assertEqual(response.status_code, 404)
        self.message.refresh_from_db()
        self.assertEqual(self.message.content, "alice 的留言")

    def test_owner_can_edit_own_message(self):
        self.client.login(username="alice", password="safe-pass-123")
        response = self.client.post(reverse("board:update", args=[self.message.pk]), {"content": "alice 改過的留言"})
        self.assertRedirects(response, reverse("board:list"))
        self.message.refresh_from_db()
        self.assertEqual(self.message.content, "alice 改過的留言")

    def test_non_owner_cannot_delete_but_staff_can(self):
        self.client.login(username="bob", password="safe-pass-123")
        response = self.client.post(reverse("board:delete", args=[self.message.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Message.objects.filter(pk=self.message.pk).exists())

        self.client.login(username="staffer", password="safe-pass-123")
        response = self.client.post(reverse("board:delete", args=[self.message.pk]))
        self.assertRedirects(response, reverse("board:list"))
        self.assertFalse(Message.objects.filter(pk=self.message.pk).exists())
