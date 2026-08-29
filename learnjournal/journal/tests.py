from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from journal.models import Article, ArticleTag, Category, Comment, Tag

User = get_user_model()


class BaseData(TestCase):
    def setUp(self):
        self.amy = User.objects.create_user(username="amy", password="pw-amy-12345")
        self.ben = User.objects.create_user(username="ben", password="pw-ben-12345")
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

    def test_logged_in_user_can_reply(self):
        article = self.make_article()
        root = Comment.objects.create(article=article, author=self.amy, body="root")
        self.client.login(username="ben", password="pw-ben-12345")
        self.client.post(article.get_absolute_url(), {"body": "回覆", "parent": root.pk})
        reply = Comment.objects.get(body="回覆")
        self.assertEqual(reply.parent, root)
        self.assertEqual(reply.author, self.ben)


class OwnershipTests(BaseData):
    def test_user_cannot_edit_others_article(self):
        article = self.make_article()
        self.client.login(username="ben", password="pw-ben-12345")
        response = self.client.post(
            f"/articles/{article.pk}/edit/", {"title": "被竄改", "category": self.cat.pk, "body": "x", "status": "draft"}
        )
        self.assertEqual(response.status_code, 404)
        article.refresh_from_db()
        self.assertEqual(article.title, "測試文章")
