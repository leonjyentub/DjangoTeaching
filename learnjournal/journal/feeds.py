from django.contrib.syndication.views import Feed
from django.urls import reverse

from journal.models import Article


class LatestArticlesFeed(Feed):
    title = "LearnJournal 最新文章"
    description = "LearnJournal 教學專案的最新公開文章"

    def link(self):
        return reverse("journal:home")

    def items(self):
        return Article.published.select_related("author")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.excerpt or item.body[:200]

    def item_pubdate(self, item):
        return item.published_at

    def item_author_name(self, item):
        return item.author.get_username()
