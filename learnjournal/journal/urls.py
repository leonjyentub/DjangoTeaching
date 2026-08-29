from django.urls import path, register_converter

from . import views


class UnicodeSlugConverter:
    """Django 內建的 `slug` 只收 ASCII；中文標題產生的 slug 需要這個。"""

    regex = r"[-\w]+"

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(UnicodeSlugConverter, "uslug")

app_name = "journal"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("register/", views.register, name="register"),
    path("subscribe/", views.subscribe, name="subscribe"),

    # 寫作後台
    path("write/", views.ArticleCreateView.as_view(), name="article-create"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("articles/<int:pk>/edit/", views.ArticleUpdateView.as_view(), name="article-update"),
    path("articles/<int:pk>/preview/", views.ArticlePreviewView.as_view(), name="article-preview"),

    # 分類 / 標籤 / 作者
    path("category/<uslug:slug>/", views.CategoryView.as_view(), name="category"),
    path("tag/<uslug:slug>/", views.TagView.as_view(), name="tag"),
    path("author/<str:username>/", views.AuthorView.as_view(), name="author"),

    # 日期彙整與文章頁：/2026/ 、/2026/08/ 、/2026/08/29/<slug>/
    path("<int:year>/", views.ArticleYearArchiveView.as_view(), name="archive-year"),
    path("<int:year>/<int:month>/", views.ArticleMonthArchiveView.as_view(), name="archive-month"),
    path("<int:year>/<int:month>/<int:day>/<uslug:slug>/", views.ArticleDetailView.as_view(), name="article-detail"),
]
