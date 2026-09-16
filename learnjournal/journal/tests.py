from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from journal.forms import ArticleForm
from journal.models import Article, ArticleTag, Category, Comment, Subscription, Tag

User = get_user_model()


class BaseData(TestCase):
    def setUp(self):
        self.amy = User.objects.create_user(username="amy", email="amy@example.com", password="pw-amy-12345")
        self.ben = User.objects.create_user(username="ben", email="ben@example.com", password="pw-ben-12345")
        self.cat = Category.objects.create(name="Django", slug="django")
        self.tag = Tag.objects.create(name="ORM", slug="orm")

    def make_article(self, **kwargs):
        defaults = dict(
            author=self.amy,
            category=self.cat,
            title="測試文章",
            body="內文",
            status=Article.Status.PUBLISHED,
            published_at=timezone.now(),
        )
        defaults.update(kwargs)
        return Article.objects.create(**defaults)


class PublishedManagerTests(BaseData):
    def test_published_excludes_drafts_and_future(self):
        self.make_article(title="已發佈")
        self.make_article(title="草稿", status=Article.Status.DRAFT, published_at=None)
        self.make_article(
            title="未來", status=Article.Status.PUBLISHED, published_at=timezone.now() + timedelta(days=1)
        )
        titles = set(Article.published.values_list("title", flat=True))
        self.assertEqual(titles, {"已發佈"})

    def test_slug_autofilled_and_published_at_set(self):
        article = Article(author=self.amy, category=self.cat, title="Hello World", body="x", status=Article.Status.PUBLISHED)
        article.save()
        self.assertTrue(article.slug)
        self.assertIsNotNone(article.published_at)


class ViewCountTests(BaseData):
    def test_register_view_is_atomic_increment(self):
        article = self.make_article()
        article.register_view()
        article.register_view()
        article.refresh_from_db()
        self.assertEqual(article.view_count, 2)

    def test_detail_page_increments_view(self):
        article = self.make_article()
        self.client.get(article.get_absolute_url())
        article.refresh_from_db()
        self.assertEqual(article.view_count, 1)


class DateUrlTests(BaseData):
    def test_absolute_url_contains_date_and_slug(self):
        article = self.make_article(title="日期網址")
        local = timezone.localtime(article.published_at)
        url = article.get_absolute_url()
        self.assertIn(str(local.year), url)
        self.assertContains(self.client.get(url), "日期網址")

    def test_month_archive_lists_article(self):
        article = self.make_article(title="彙整測試")
        local = timezone.localtime(article.published_at)
        response = self.client.get(f"/{local.year}/{local.month}/")
        self.assertContains(response, "彙整測試")

    def test_scheduled_article_uses_private_preview_url(self):
        article = self.make_article(
            title="排程文章",
            status=Article.Status.SCHEDULED,
            published_at=timezone.now() + timedelta(hours=1),
        )
        self.assertEqual(article.get_absolute_url(), reverse("journal:article-preview", args=[article.pk]))


class TagAndCoauthorTests(BaseData):
    def test_many_to_many_through_and_reverse(self):
        article = self.make_article()
        ArticleTag.objects.create(article=article, tag=self.tag, featured_order=1)
        self.assertIn(self.tag, article.tags.all())
        self.assertIn(article, self.tag.articles.all())

    def test_coauthor_reverse_name_is_separate(self):
        article = self.make_article()
        article.coauthors.add(self.ben)
        self.assertIn(article, self.ben.coauthored_articles.all())
        self.assertNotIn(article, self.ben.articles.all())


class CommentTests(BaseData):
    def test_anonymous_cannot_post_comment(self):
        article = self.make_article()
        response = self.client.post(article.get_absolute_url(), {"body": "匿名留言"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_logged_in_user_can_reply_and_author_gets_email(self):
        article = self.make_article()
        root = Comment.objects.create(article=article, author=self.amy, body="root")
        self.client.login(username="ben", password="pw-ben-12345")
        self.client.post(article.get_absolute_url(), {"body": "回覆", "parent": root.pk})
        reply = Comment.objects.get(body="回覆")
        self.assertEqual(reply.parent, root)
        self.assertEqual(reply.author, self.ben)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("新留言", mail.outbox[0].subject)


class OwnershipTests(BaseData):
    def test_user_cannot_edit_others_article(self):
        article = self.make_article()
        self.client.login(username="ben", password="pw-ben-12345")
        response = self.client.post(
            f"/articles/{article.pk}/edit/",
            {
                "title": "被竄改",
                "slug": article.slug,
                "category": self.cat.pk,
                "body": "x",
                "excerpt": "",
                "status": Article.Status.DRAFT,
                "published_at": "",
            },
        )
        self.assertEqual(response.status_code, 404)
        article.refresh_from_db()
        self.assertEqual(article.title, "測試文章")


class SessionCookieMiddlewareTests(BaseData):
    def test_detail_records_recent_article_in_session(self):
        article = self.make_article()
        response = self.client.get(article.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.session["recent_article_ids"], [article.pk])

    def test_reading_mode_is_stored_in_cookie(self):
        response = self.client.post(
            reverse("journal:set-reading-mode"),
            {"mode": "compact", "next": reverse("journal:home")},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.cookies["reading_mode"].value, "compact")

    def test_response_time_middleware_adds_header(self):
        response = self.client.get(reverse("journal:home"))
        self.assertIn("X-Response-Time", response)
        self.assertTrue(response["X-Response-Time"].endswith("ms"))


class PublishingPermissionTests(BaseData):
    def test_plain_author_cannot_publish_from_form(self):
        form = ArticleForm(
            data={
                "title": "沒有權限",
                "slug": "no-permission",
                "category": self.cat.pk,
                "excerpt": "",
                "body": "body",
                "status": Article.Status.PUBLISHED,
                "published_at": "",
            },
            user=self.amy,
        )
        self.assertFalse(form.is_valid())
        self.assertIn("status", form.errors)

    def test_editor_group_can_publish_from_form(self):
        permission = Permission.objects.get(codename="publish_article", content_type__app_label="journal")
        editors = Group.objects.create(name="Editors")
        editors.permissions.add(permission)
        self.amy.groups.add(editors)
        form = ArticleForm(
            data={
                "title": "可以發佈",
                "slug": "can-publish",
                "category": self.cat.pk,
                "excerpt": "",
                "body": "body",
                "status": Article.Status.PUBLISHED,
                "published_at": "",
            },
            user=self.amy,
        )
        self.assertTrue(form.is_valid(), form.errors)


class SubscriptionAndPasswordResetTests(BaseData):
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_subscription_double_opt_in(self):
        response = self.client.post(reverse("journal:subscribe"), {"email": "reader@example.com"})
        self.assertRedirects(response, reverse("journal:home"))
        sub = Subscription.objects.get(email="reader@example.com")
        self.assertFalse(sub.is_confirmed)
        self.assertEqual(len(mail.outbox), 1)

        response = self.client.get(reverse("journal:confirm-subscription", args=[sub.token]))
        self.assertRedirects(response, reverse("journal:home"))
        sub.refresh_from_db()
        self.assertTrue(sub.is_confirmed)

    @override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend")
    def test_password_reset_sends_email_for_known_address(self):
        response = self.client.post(reverse("password_reset"), {"email": self.amy.email})
        self.assertRedirects(response, reverse("password_reset_done"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("reset", mail.outbox[0].body)


class FeedSitemapAndCommandTests(BaseData):
    def test_feed_and_sitemap_expose_published_article(self):
        article = self.make_article(title="Feed 測試")
        self.assertContains(self.client.get(reverse("feed")), "Feed 測試")
        sitemap_response = self.client.get(reverse("sitemap"))
        self.assertEqual(sitemap_response.status_code, 200)
        self.assertContains(sitemap_response, article.get_absolute_url())

    def test_publish_scheduled_supports_dry_run_and_publish(self):
        article = self.make_article(
            title="到期排程",
            status=Article.Status.SCHEDULED,
            published_at=timezone.now() - timedelta(minutes=5),
        )
        out = StringIO()
        call_command("publish_scheduled", "--dry-run", stdout=out)
        article.refresh_from_db()
        self.assertEqual(article.status, Article.Status.SCHEDULED)
        self.assertIn("dry-run", out.getvalue())

        call_command("publish_scheduled", stdout=StringIO())
        article.refresh_from_db()
        self.assertEqual(article.status, Article.Status.PUBLISHED)
