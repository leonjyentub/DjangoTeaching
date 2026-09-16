from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import F, Q
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from journal.managers import ArticleQuerySet, PublishedManager


class User(AbstractUser):
    """Custom user chosen before the first migration (recap from LearnMart).

    LearnMart used a role field. LearnJournal deliberately uses Django Groups
    and Permissions for editorial capabilities instead.
    """

    bio = models.CharField("個人簡介", max_length=200, blank=True)

    def get_absolute_url(self):
        return reverse("journal:author", kwargs={"username": self.username})


class Category(models.Model):
    name = models.CharField("分類名稱", max_length=80, unique=True)
    slug = models.SlugField("網址代稱", max_length=80, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "分類"
        verbose_name_plural = "分類"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("journal:category", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField("標籤", max_length=40, unique=True)
    slug = models.SlugField("網址代稱", max_length=40, unique=True, allow_unicode=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("journal:tag", kwargs={"slug": self.slug})


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "草稿"
        SCHEDULED = "scheduled", "已排程"
        PUBLISHED = "published", "已發佈"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="articles",
        verbose_name="主要作者",
    )
    coauthors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="coauthored_articles",
        blank=True,
        verbose_name="共同作者",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="articles",
        verbose_name="分類",
    )
    tags = models.ManyToManyField(Tag, through="ArticleTag", related_name="articles", blank=True, verbose_name="標籤")

    title = models.CharField("標題", max_length=160)
    slug = models.SlugField("網址代稱", max_length=160, unique_for_date="published_at", allow_unicode=True)
    excerpt = models.CharField("摘要", max_length=300, blank=True)
    body = models.TextField("內文（Markdown）")
    body_html = models.TextField("內文（已渲染）", blank=True, editable=False)

    status = models.CharField("狀態", max_length=12, choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField("發佈時間", null=True, blank=True)
    view_count = models.PositiveIntegerField("瀏覽次數", default=0, editable=False)

    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    objects = ArticleQuerySet.as_manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["slug"]),
        ]
        constraints = [
            models.CheckConstraint(
                name="published_article_has_timestamp",
                condition=~Q(status="published") | Q(published_at__isnull=False),
            ),
        ]
        permissions = [
            ("publish_article", "Can publish and schedule articles"),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True) or "article"
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.published_at:
            local = timezone.localtime(self.published_at)
            return reverse(
                "journal:article-detail",
                kwargs={"year": local.year, "month": local.month, "day": local.day, "slug": self.slug},
            )
        return reverse("journal:article-preview", kwargs={"pk": self.pk})

    @property
    def is_live(self):
        return self.status == self.Status.PUBLISHED and self.published_at and self.published_at <= timezone.now()

    def register_view(self):
        """Atomic increment avoids the read-modify-write race shown in LearnMart."""
        Article.objects.filter(pk=self.pk).update(view_count=F("view_count") + 1)

    @property
    def reading_minutes(self):
        words = max(len(self.body.split()), len(self.body))
        return max(1, round(words / 400))


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    featured_order = models.PositiveSmallIntegerField("精選排序", default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["article", "tag"], name="unique_article_tag")]
        ordering = ["featured_order"]


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="replies", verbose_name="回覆對象"
    )
    body = models.TextField("留言內容", max_length=1000)
    is_approved = models.BooleanField("已核准", default=True)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.author}：{self.body[:20]}"


class Reaction(models.Model):
    class Kind(models.TextChoices):
        LIKE = "like", "讚"
        INSIGHTFUL = "insightful", "有收穫"
        CURIOUS = "curious", "想知道更多"

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reactions")
    kind = models.CharField("反應", max_length=12, choices=Kind.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["article", "user", "kind"], name="unique_reaction")]


class Subscription(models.Model):
    """Newsletter subscription with a double opt-in confirmation token."""

    email = models.EmailField("電子郵件", unique=True)
    is_confirmed = models.BooleanField("已確認", default=False)
    token = models.CharField("確認碼", max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
