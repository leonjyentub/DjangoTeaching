from django.contrib.sitemaps import Sitemap

from journal.models import Article


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Article.published.all()

    def lastmod(self, item):
        return item.updated_at
