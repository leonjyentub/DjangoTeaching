from django.db import connection
from django.db.models import Q

from journal.models import Article


def search_published_articles(term: str):
    """Search published articles with a database-appropriate strategy.

    SQLite keeps the classroom setup dependency-free and falls back to
    `icontains`. PostgreSQL uses weighted full-text search and relevance rank.
    The PostgreSQL imports stay inside the branch so SQLite users don't need a
    PostgreSQL driver just to run the teaching project.
    """
    term = (term or "").strip()
    queryset = Article.published.select_related("author", "category")
    if not term:
        return queryset

    if connection.vendor != "postgresql":
        return queryset.filter(
            Q(title__icontains=term)
            | Q(excerpt__icontains=term)
            | Q(body__icontains=term)
        )

    from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

    vector = (
        SearchVector("title", weight="A")
        + SearchVector("excerpt", weight="B")
        + SearchVector("body", weight="C")
    )
    query = SearchQuery(term)
    return (
        queryset.annotate(search=vector, rank=SearchRank(vector, query))
        .filter(search=query)
        .order_by("-rank", "-published_at")
    )
