from datetime import timedelta

from django.core.mail import send_mass_mail
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils import timezone

from journal.models import Article, Subscription


class Command(BaseCommand):
    help = "Send a digest of recently published articles to confirmed subscribers."

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=7, help="Look-back window in days (default: 7).")
        parser.add_argument("--dry-run", action="store_true", help="Preview recipients/content without sending mail.")
        parser.add_argument("--limit", type=int, default=20, help="Maximum articles included in the digest.")

    def handle(self, *args, **options):
        days = max(1, options["days"])
        limit = max(1, options["limit"])
        since = timezone.now() - timedelta(days=days)
        articles = list(Article.published.filter(published_at__gte=since)[:limit])
        subscribers = list(Subscription.objects.filter(is_confirmed=True).values_list("email", flat=True))

        if not articles:
            self.stdout.write("指定期間沒有新文章，不寄送摘要。")
            return
        if not subscribers:
            self.stdout.write("沒有已確認訂閱者，不寄送摘要。")
            return

        lines = [f"LearnJournal 最近 {days} 天的新文章：", ""]
        for article in articles:
            # Management commands do not have an HttpRequest, so get_absolute_url()
            # intentionally returns a path rather than inventing a deployment host.
            lines.append(f"- {article.title}: {article.get_absolute_url()}")
        message = "\n".join(lines)

        if options["dry_run"]:
            self.stdout.write(self.style.WARNING(f"dry-run：{len(subscribers)} 位收件者、{len(articles)} 篇文章。"))
            self.stdout.write(message)
            return

        payload = tuple(("LearnJournal 每週精選", message, None, [email]) for email in subscribers)
        sent = send_mass_mail(payload, fail_silently=False)
        self.stdout.write(self.style.SUCCESS(f"已送出 {sent} 封摘要信。"))
