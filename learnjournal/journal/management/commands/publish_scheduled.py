from django.core.management.base import BaseCommand
from django.utils import timezone

from journal.models import Article


class Command(BaseCommand):
    help = "Publish scheduled articles whose published_at time has arrived."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show which articles would be published without changing the database.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            default=100,
            help="Maximum number of articles to publish in one run (default: 100).",
        )

    def handle(self, *args, **options):
        limit = max(1, options["limit"])
        due = Article.objects.filter(
            status=Article.Status.SCHEDULED,
            published_at__isnull=False,
            published_at__lte=timezone.now(),
        ).order_by("published_at")[:limit]
        article_ids = list(due.values_list("pk", flat=True))

        if options["dry_run"]:
            self.stdout.write(f"dry-run: {len(article_ids)} article(s) would be published: {article_ids}")
            return

        updated = Article.objects.filter(pk__in=article_ids).update(status=Article.Status.PUBLISHED)
        self.stdout.write(self.style.SUCCESS(f"published {updated} article(s)"))
