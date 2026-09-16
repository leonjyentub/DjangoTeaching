from django.urls import path, register_converter

from . import views


class UnicodeSlugConverter:
    """Django's built-in slug converter is ASCII-oriented; allow Unicode slugs."""

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
    path("subscribe/confirm/<str:token>/", views.confirm_subscription, name="confirm-subscription"),
    path("preferences/reading-mode/", views.set_reading_mode, name="set-reading-mode"),

    # Writing dashboard
    path("write/", views.ArticleCreateView.as_view(), name="article-create"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path("articles/<int:pk>/edit/", views.ArticleUpdateView.as_view(), name="article-update"),
    path("articles/<int:pk>/preview/", views.ArticlePreviewView.as_view(), name="article-preview"),

    # Category / tag / author
    path("category/<uslug:slug>/", views.CategoryView.as_view(), name="category"),
    path("tag/<uslug:slug>/", views.TagView.as_view(), name="tag"),
    path("author/<str:username>/", views.AuthorView.as_view(), name="author"),

    # Date archives and article URL: /2026/ /2026/08/ /2026/08/29/<slug>/
    path("<int:year>/", views.ArticleYearArchiveView.as_view(), name="archive-year"),
    path("<int:year>/<int:month>/", views.ArticleMonthArchiveView.as_view(), name="archive-month"),
    path("<int:year>/<int:month>/<int:day>/<uslug:slug>/", views.ArticleDetailView.as_view(), name="article-detail"),
]
