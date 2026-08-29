from journal.models import Category


def site_nav(request):
    """導覽列每頁都需要分類清單（回扣 LearnMart 的 cart_count context processor）。

    Deck 03B 第 8 章會示範用片段快取或低階快取避免每頁一次查詢。
    """
    return {"nav_categories": Category.objects.all()}
