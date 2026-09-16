from django.core.cache import cache

from journal.models import Category

NAV_CATEGORIES_CACHE_KEY = "journal:nav-categories:v1"
NAV_CATEGORIES_CACHE_SECONDS = 300


def site_nav(request):
    """導覽列共用資料：示範低階 cache API 與失效策略。

    第一次請求會查資料庫，之後五分鐘直接讀 cache。Category 新增、修改或刪除時，
    `journal.signals.invalidate_navigation_cache` 會主動清掉這個 key。
    """
    categories = cache.get(NAV_CATEGORIES_CACHE_KEY)
    if categories is None:
        categories = list(Category.objects.all())
        cache.set(NAV_CATEGORIES_CACHE_KEY, categories, NAV_CATEGORIES_CACHE_SECONDS)

    return {
        "nav_categories": categories,
        "reading_mode": request.COOKIES.get("reading_mode", "comfortable"),
    }
