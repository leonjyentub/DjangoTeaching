"""Custom Manager and QuerySet examples used across LearnJournal."""

from django.db import connection, models
from django.utils import timezone


class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status="published", published_at__lte=timezone.now())

    def scheduled(self):
        return self.filter(status="scheduled")

    def by_tag(self, slug):
        return self.filter(tags__slug=slug)

    def by_category(self, slug):
        return self.filter(category__slug=slug)

    def search(self, term):
        """Use PostgreSQL ranking when available; keep SQLite zero-setup.

        The lazy import is deliberate: students can run the project on SQLite
        without installing a PostgreSQL driver. When the configured backend is
        PostgreSQL, Django's SearchVector/SearchQuery/SearchRank path is used.
        """

        term = (term or "").strip()
        if not term:
            return self.none()

        if connection.vendor == "postgresql":
            from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

            vector = SearchVector("title", weight="A", config="simple") + SearchVector(
                "body", weight="B", config="simple"
            )
            query = SearchQuery(term, search_type="websearch", config="simple")
            return (
                self.annotate(search_rank=SearchRank(vector, query))
                .filter(search_rank__gte=0.05)
                .order_by("-search_rank", "-published_at")
            )

        # SQLite fallback keeps the first-contact setup simple and makes the
        # behavioral difference between substring search and FTS easy to compare.
        return self.filter(models.Q(title__icontains=term) | models.Q(body__icontains=term))

    def with_feed_fields(self):
        return self.select_related("author", "category").prefetch_related("tags")


class PublishedManager(models.Manager):
    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db).published().with_feed_fields()
