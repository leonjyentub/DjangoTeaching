from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.mail import send_mail
from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, ListView, UpdateView
from django.views.generic.dates import MonthArchiveView, YearArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin

from journal.forms import ArticleForm, CommentForm, RegistrationForm, SubscriptionForm
from journal.models import Article, Category, Subscription, Tag, User
from journal.search import search_published_articles


class HomeView(ListView):
    template_name = "journal/home.html"
    context_object_name = "articles"
    paginate_by = 6

    def get_queryset(self):
        return search_published_articles(self.request.GET.get("q", ""))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


class CategoryView(HomeView):
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return super().get_queryset().by_category(self.category.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context


class TagView(HomeView):
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        return super().get_queryset().by_tag(self.tag.slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        return context


class AuthorView(HomeView):
    def get_queryset(self):
        self.author = get_object_or_404(User, username=self.kwargs["username"])
        return super().get_queryset().filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.author
        return context


class ArticleDetailView(FormMixin, DetailView):
    template_name = "journal/article_detail.html"
    context_object_name = "article"
    form_class = CommentForm

    def get_queryset(self):
        return Article.published.prefetch_related("comments__author", "comments__replies", "reactions")

    def get_object(self, queryset=None):
        queryset = queryset or self.get_queryset()
        return get_object_or_404(
            queryset,
            slug=self.kwargs["slug"],
            published_at__year=self.kwargs["year"],
            published_at__month=self.kwargs["month"],
            published_at__day=self.kwargs["day"],
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.register_view()

        # Session 適合保存「伺服器需要知道」的匿名狀態。瀏覽器只拿 session id，
        # 文章 id 清單存在 session backend，而不是直接暴露在 cookie value 中。
        recent_ids = request.session.get("recent_article_ids", [])
        recent_ids = [pk for pk in recent_ids if pk != self.object.pk]
        request.session["recent_article_ids"] = [self.object.pk, *recent_ids][:5]

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("form", self.get_form())
        context["top_comments"] = self.object.comments.filter(parent__isnull=True, is_approved=True)
        context["reaction_counts"] = self.object.reactions.values("kind").annotate(n=Count("id"))

        recent_ids = self.request.session.get("recent_article_ids", [])
        recent_map = Article.published.in_bulk(recent_ids)
        context["recent_articles"] = [recent_map[pk] for pk in recent_ids if pk in recent_map and pk != self.object.pk]
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        form = self.get_form()
        if not form.is_valid():
            return self.render_to_response(self.get_context_data(form=form))
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = request.user
        parent_id = request.POST.get("parent")
        if parent_id:
            comment.parent = self.object.comments.filter(pk=parent_id).first()
        comment.save()
        messages.success(request, "留言已送出。")
        return redirect(self.object.get_absolute_url() + "#comments")


class ArticlePreviewView(LoginRequiredMixin, DetailView):
    template_name = "journal/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        user = self.request.user
        return Article.objects.filter(author=user) | Article.objects.filter(coauthors=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["preview"] = True
        context["top_comments"] = self.object.comments.none()
        context["reaction_counts"] = []
        context["recent_articles"] = []
        return context


class ArticleYearArchiveView(YearArchiveView):
    date_field = "published_at"
    make_object_list = True
    allow_empty = True
    template_name = "journal/archive_year.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.published.all()


class ArticleMonthArchiveView(MonthArchiveView):
    date_field = "published_at"
    month_format = "%m"
    allow_empty = True
    template_name = "journal/archive_month.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.published.all()


def register(request):
    if request.user.is_authenticated:
        return redirect("journal:home")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "註冊成功，歡迎加入 LearnJournal！")
        return redirect("journal:home")
    return render(request, "registration/register.html", {"form": form})


class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = "journal.add_article"
    raise_exception = True
    model = Article
    form_class = ArticleForm
    template_name = "journal/article_form.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["author"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "文章已儲存。")
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = "journal.change_article"
    raise_exception = True
    model = Article
    form_class = ArticleForm
    template_name = "journal/article_form.html"

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["author"] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "文章已更新。")
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "journal.view_article"
    raise_exception = True
    template_name = "journal/dashboard.html"
    context_object_name = "articles"

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user).select_related("category")


@require_POST
def set_reading_mode(request):
    """Cookie 適合保存純 client-side 偏好；這裡不放敏感或授權資訊。"""
    mode = request.POST.get("mode", "comfortable")
    if mode not in {"comfortable", "compact"}:
        raise Http404
    response = redirect("journal:home")
    response.set_cookie(
        "reading_mode",
        mode,
        max_age=60 * 60 * 24 * 365,
        samesite="Lax",
    )
    return response


def subscribe(request):
    import secrets

    form = SubscriptionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        sub = form.save(commit=False)
        sub.token = secrets.token_urlsafe(32)
        sub.is_confirmed = False
        sub.save()
        confirm_url = request.build_absolute_uri(reverse("journal:subscription-confirm", args=[sub.token]))
        send_mail(
            "確認 LearnJournal 電子報訂閱",
            f"請開啟以下網址完成 double opt-in：\n\n{confirm_url}",
            None,
            [sub.email],
            fail_silently=False,
        )
        messages.success(request, "確認信已寄出（開發階段請看終端機）。")
        return redirect("journal:home")
    return render(request, "journal/subscribe.html", {"form": form})


def confirm_subscription(request, token):
    subscription = get_object_or_404(Subscription, token=token)
    if not subscription.is_confirmed:
        subscription.is_confirmed = True
        subscription.save(update_fields=["is_confirmed"])
    messages.success(request, "電子報訂閱已確認。")
    return redirect("journal:home")
