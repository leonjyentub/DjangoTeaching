from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from journal.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.published.all()

    def lastmod(self, obj):
        return obj.updated_at


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.4

    def items(self):
        return ["journal:home", "journal:subscribe"]

    def location(self, item):
        return reverse(item)
