from django.core.cache import cache

from journal.models import Category


NAV_CACHE_KEY = "learnjournal:nav-categories:v1"


def site_nav(request):
    """Provide site-wide navigation with a small low-level cache example.

    A tuple of plain dictionaries is cached rather than a lazy QuerySet. This
    makes the cache boundary visible to students: the database query happens
    only on a miss, and the template receives already-materialized values.
    """

    categories = cache.get(NAV_CACHE_KEY)
    if categories is None:
        categories = tuple(Category.objects.order_by("name").values("name", "slug"))
        cache.set(NAV_CACHE_KEY, categories, timeout=300)
    return {"nav_categories": categories}


def reader_preferences(request):
    """Expose a harmless cookie preference to every template.

    Cookies are client-side state; sessions are server-side state. Deck 03B
    contrasts this preference cookie with the recently-viewed session list.
    """

    mode = request.COOKIES.get("reading_mode", "comfortable")
    if mode not in {"comfortable", "compact"}:
        mode = "comfortable"
    return {"reading_mode": mode}
