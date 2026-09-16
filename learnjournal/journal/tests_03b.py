from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from journal.models import Article, Category, Subscription
from journal.search import search_published_articles

User = get_user_model()


class Deck03BBase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="writer", email="writer@example.com", password="safe-pass-123"
        )
        self.category = Category.objects.create(name="Django", slug="django")
        self.article = Article.objects.create(
            author=self.user,
            category=self.category,
            title="Cache 與 Session 教學",
            body="這篇文章也談 PostgreSQL 搜尋。",
            status=Article.Status.PUBLISHED,
            published_at=timezone.now(),
        )


class SessionCookieMiddlewareTests(Deck03BBase):
    def test_article_detail_remembers_recent_article_in_session(self):
        self.client.get(self.article.get_absolute_url())
        self.assertEqual(self.client.session["recent_article_ids"], [self.article.pk])

    def test_reading_mode_is_stored_in_cookie(self):
        response = self.client.post(reverse("journal:set-reading-mode"), {"mode": "compact"})
        self.assertEqual(response.cookies["reading_mode"].value, "compact")

    def test_response_time_header_is_added(self):
        response = self.client.get(reverse("journal:home"))
        self.assertIn("X-Response-Time", response)
        self.assertTrue(response["X-Response-Time"].endswith("ms"))


class PermissionTests(Deck03BBase):
    def test_article_create_requires_model_permission(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("journal:article-create"))
        self.assertEqual(response.status_code, 403)

        permission = Permission.objects.get(
            content_type__app_label="journal", codename="add_article"
        )
        self.user.user_permissions.add(permission)
        response = self.client.get(reverse("journal:article-create"))
        self.assertEqual(response.status_code, 200)


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
class EmailFlowTests(Deck03BBase):
    def test_password_reset_sends_mail(self):
        response = self.client.post(reverse("password_reset"), {"email": self.user.email})
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("/accounts/reset/", mail.outbox[0].body)

    def test_subscription_double_opt_in_sends_confirmation(self):
        response = self.client.post(reverse("journal:subscribe"), {"email": "reader@example.com"})
        self.assertRedirects(response, reverse("journal:home"))
        subscription = Subscription.objects.get(email="reader@example.com")
        self.assertFalse(subscription.is_confirmed)
        self.assertEqual(len(mail.outbox), 1)

        response = self.client.get(reverse("journal:subscription-confirm", args=[subscription.token]))
        self.assertRedirects(response, reverse("journal:home"))
        subscription.refresh_from_db()
        self.assertTrue(subscription.is_confirmed)


class FeedSitemapSearchTests(Deck03BBase):
    def test_rss_feed_contains_published_article(self):
        response = self.client.get(reverse("journal:feed"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("xml", response["Content-Type"])
        self.assertContains(response, self.article.title)

    def test_sitemap_contains_article_url(self):
        response = self.client.get(reverse("sitemap"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.get_absolute_url())

    def test_sqlite_search_fallback_searches_body(self):
        results = search_published_articles("PostgreSQL")
        self.assertIn(self.article, results)


class ScheduledPublishingCommandTests(Deck03BBase):
    def setUp(self):
        super().setUp()
        self.scheduled = Article.objects.create(
            author=self.user,
            category=self.category,
            title="排程文章",
            body="稍後公開",
            status=Article.Status.SCHEDULED,
            published_at=timezone.now(),
        )

    def test_dry_run_does_not_publish(self):
        stdout = StringIO()
        call_command("publish_scheduled", "--dry-run", stdout=stdout)
        self.scheduled.refresh_from_db()
        self.assertEqual(self.scheduled.status, Article.Status.SCHEDULED)
        self.assertIn("dry-run", stdout.getvalue())

    def test_command_publishes_due_articles(self):
        call_command("publish_scheduled", stdout=StringIO())
        self.scheduled.refresh_from_db()
        self.assertEqual(self.scheduled.status, Article.Status.PUBLISHED)
