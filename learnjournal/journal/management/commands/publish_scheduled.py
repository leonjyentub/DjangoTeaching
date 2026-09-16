from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from journal.models import Article


class Command(BaseCommand):
    help = "Publish scheduled articles whose publication time has arrived."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Show what would be published without changing data.")
        parser.add_argument("--limit", type=int, default=100, help="Maximum number of articles to process (default: 100).")

    def handle(self, *args, **options):
        now = timezone.now()
        limit = max(1, options["limit"])
        articles = list(
            Article.objects.filter(status=Article.Status.SCHEDULED, published_at__lte=now)
            .order_by("published_at")[:limit]
        )

        if not articles:
            self.stdout.write("沒有到期的排程文章。")
            return

        for article in articles:
            self.stdout.write(f"- {article.pk}: {article.title} ({article.published_at:%Y-%m-%d %H:%M})")

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING(f"dry-run：共 {len(articles)} 篇，不修改資料。"))
            return

        # One transaction makes the command's batch behavior easy to reason about.
        # We still call save() per row so Article post_save signals run.
        with transaction.atomic():
            for article in articles:
                article.status = Article.Status.PUBLISHED
                article.save(update_fields=["status", "updated_at"])

        self.stdout.write(self.style.SUCCESS(f"已發佈 {len(articles)} 篇文章。"))
