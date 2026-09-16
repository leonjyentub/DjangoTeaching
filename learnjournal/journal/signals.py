"""Signals used by LearnJournal's publishing pipeline.

Teaching goals:
- post_save can maintain derived data (`body_html`).
- post_save can trigger a decoupled side effect (comment notification email).
- cache invalidation is a concrete reason to react to model changes.

Signals are intentionally kept small. Business rules that a caller must be able
to reason about synchronously should still live in normal functions/services.
"""

import markdown as md
from django.core.cache import cache
from django.core.mail import send_mail
from django.core.cache.utils import make_template_fragment_key
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from journal.context_processors import NAV_CACHE_KEY
from journal.models import Article, Category, Comment

SIDEBAR_CACHE_KEYS = [
    make_template_fragment_key("sidebar_latest"),
    make_template_fragment_key("sidebar_tags"),
]


@receiver(post_save, sender=Article)
def render_markdown(sender, instance, **kwargs):
    html = md.markdown(instance.body or "", extensions=["fenced_code", "tables", "toc"])
    if html != instance.body_html:
        # update() does not emit post_save, which avoids an infinite signal loop.
        Article.objects.filter(pk=instance.pk).update(body_html=html)
    cache.delete_many(SIDEBAR_CACHE_KEYS)


@receiver(post_delete, sender=Article)
def invalidate_article_fragments_on_delete(sender, instance, **kwargs):
    cache.delete_many(SIDEBAR_CACHE_KEYS)


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def invalidate_navigation_cache(sender, instance, **kwargs):
    cache.delete(NAV_CACHE_KEY)


@receiver(post_save, sender=Comment)
def notify_author_on_comment(sender, instance, created, **kwargs):
    if not created:
        return
    author = instance.article.author
    if not author.email or comment_is_by_author(instance, author):
        return
    send_mail(
        subject=f"你的文章有新留言：{instance.article.title}",
        message=f"{instance.author.get_username()} 留言：\n\n{instance.body}\n\n{instance.article.get_absolute_url()}",
        from_email=None,
        recipient_list=[author.email],
        fail_silently=True,
    )


def comment_is_by_author(comment, author):
    """Named helper makes the self-notification rule easy to unit test/read."""

    return comment.author_id == author.pk
