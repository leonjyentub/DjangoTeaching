"""Create repeatable LearnJournal classroom demo data."""

import textwrap

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from journal.models import Article, ArticleTag, Category, Comment, Tag

User = get_user_model()


class Command(BaseCommand):
    help = "建立 LearnJournal 課堂示範帳號、群組、分類、標籤與文章（可重複執行）"

    def handle(self, *args, **options):
        users = {}
        for name in ["editor", "amy", "ben"]:
            user, created = User.objects.get_or_create(
                username=name, defaults={"email": f"{name}@example.com"}
            )
            if created:
                user.set_password(f"{name}12345")
                user.save()
            users[name] = user

        # Group/Permission example: capabilities are assigned to a group rather
        # than encoded as a custom `role` string on User.
        editors, _ = Group.objects.get_or_create(name="Editors")
        permissions = Permission.objects.filter(
            content_type__app_label="journal",
            content_type__model="article",
            codename__in=["add_article", "change_article", "view_article", "publish_article"],
        )
        editors.permissions.set(permissions)
        users["editor"].groups.add(editors)

        categories = {}
        for name, slug in [("Django", "django"), ("Python", "python"), ("前端", "frontend")]:
            categories[slug] = Category.objects.get_or_create(slug=slug, defaults={"name": name})[0]

        tags = {}
        for name in ["ORM", "測試", "部署", "表單", "教學筆記"]:
            tags[name] = Tag.objects.get_or_create(slug=slugify(name, allow_unicode=True), defaults={"name": name})[0]

        seed = [
            {
                "author": "amy",
                "title": "從 LearnMart 到 LearnJournal：這個專案想補的洞",
                "category": "django",
                "tags": ["教學筆記", "ORM"],
                "body": textwrap.dedent(
                    """
                    ## 為什麼還要第三個專案

                    留言板教會了帳號與擁有權，商城教會了交易與一致性。
                    這一個專案的主題是**內容的發佈與傳播**。

                    - 多對多：一篇文章多個標籤
                    - 自訂 manager：`Article.published.all()`
                    - `F()` 原子遞增瀏覽數

                    ```python
                    Article.objects.filter(pk=self.pk).update(view_count=F("view_count") + 1)
                    ```
                    """
                ).strip(),
                "coauthors": ["ben"],
            },
            {
                "author": "ben",
                "title": "自訂 template tag：把側欄邏輯搬出 view",
                "category": "frontend",
                "tags": ["表單", "教學筆記"],
                "body": "標籤雲、最新文章、閱讀時間都不該塞進每個 view 的 context。\n\n用 `inclusion_tag` 把它們變成 `{% tag_cloud %}`。",
            },
            {
                "author": "amy",
                "title": "巢狀留言：一個自我關聯 ForeignKey 就夠了",
                "category": "python",
                "tags": ["ORM"],
                "body": "`parent = models.ForeignKey('self', null=True, related_name='replies')`\n\n就這樣。剩下的是模板怎麼遞迴顯示。",
            },
        ]

        now = timezone.now()
        for item in seed:
            article, created = Article.objects.get_or_create(
                title=item["title"],
                defaults={
                    "author": users[item["author"]],
                    "category": categories[item["category"]],
                    "body": item["body"],
                    "status": Article.Status.PUBLISHED,
                    "published_at": now,
                },
            )
            if created:
                for order, tag_name in enumerate(item["tags"]):
                    ArticleTag.objects.get_or_create(
                        article=article, tag=tags[tag_name], defaults={"featured_order": order}
                    )
                for co in item.get("coauthors", []):
                    article.coauthors.add(users[co])

        first = Article.objects.filter(title__startswith="從 LearnMart").first()
        if first and not first.comments.exists():
            root = Comment.objects.create(article=first, author=users["ben"], body="這個對照表很有用。")
            Comment.objects.create(article=first, author=users["amy"], parent=root, body="謝謝，第 6 章還會再擴充。")

        self.stdout.write(
            self.style.SUCCESS(
                "示範資料完成。editor/editor12345（Editors，可發佈）、amy/amy12345、ben/ben12345"
            )
        )
