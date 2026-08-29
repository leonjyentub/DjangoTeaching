"""自訂 Manager 與 QuerySet。

Deck 03A 第 3 章：LearnBoard 與 LearnMart 到處寫 `filter(is_active=True)`、
`filter(status="published")`。把這些規則收斂成一個具名、可鏈式的 QuerySet 方法，
呼叫端就只需要說「我要已發佈的文章」，不必重複條件。
"""

from django.db import models
from django.utils import timezone


class ArticleQuerySet(models.QuerySet):
    def published(self):
        """狀態為 published 且發佈時間已到。"""
        return self.filter(status="published", published_at__lte=timezone.now())

    def scheduled(self):
        """已排程但時間未到——`publish_scheduled` 指令的目標。"""
        return self.filter(status="scheduled")

    def by_tag(self, slug):
        return self.filter(tags__slug=slug)

    def by_category(self, slug):
        return self.filter(category__slug=slug)

    def search(self, term):
        """Deck 03B 第 11 章會把這裡換成 PostgreSQL 的 SearchVector。"""
        term = (term or "").strip()
        if not term:
            return self.none()
        return self.filter(models.Q(title__icontains=term) | models.Q(body__icontains=term))

    def with_feed_fields(self):
        """清單頁一次載入作者與分類，避免 N+1（回扣 Deck 01 第 5 章）。"""
        return self.select_related("author", "category").prefetch_related("tags")


class PublishedManager(models.Manager):
    """`Article.published` 只看得到公開文章；`Article.objects` 仍是全部。"""

    def get_queryset(self):
        return ArticleQuerySet(self.model, using=self._db).published().with_feed_fields()
