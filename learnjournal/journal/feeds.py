from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.html import strip_tags

from journal.models import Article


class LatestArticlesFeed(Feed):
    title = "學誌 LearnJournal"
    description = "LearnJournal 最新公開文章"

    def link(self):
        return reverse("journal:home")

    def items(self):
        return Article.published.all()[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return strip_tags(item.excerpt or item.body)[:300]

    def item_pubdate(self, item):
        return item.published_at

    def item_author_name(self, item):
        return item.author.get_username()
