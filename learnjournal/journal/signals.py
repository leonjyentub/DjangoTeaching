"""Signals：把「儲存後的副作用」集中在一處。

03A 先示範文章存檔後渲染 Markdown；03B 再加入 cache invalidation 與留言通知。
教學重點不是「signal 越多越好」，而是辨認低耦合事件通知與隱藏副作用的取捨。
"""

import markdown as md
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from journal.context_processors import NAV_CATEGORIES_CACHE_KEY
from journal.models import Article, Category, Comment


@receiver(post_save, sender=Article)
def render_markdown(sender, instance, **kwargs):
    html = md.markdown(instance.body or "", extensions=["fenced_code", "tables", "toc"])
    if html != instance.body_html:
        # update() 不會再次觸發 post_save，可避免無限迴圈。
        Article.objects.filter(pk=instance.pk).update(body_html=html)


@receiver([post_save, post_delete], sender=Category)
def invalidate_navigation_cache(sender, **kwargs):
    """資料改變時主動清 cache，示範 cache invalidation。"""
    cache.delete(NAV_CATEGORIES_CACHE_KEY)


@receiver(post_save, sender=Comment)
def notify_author_on_comment(sender, instance, created, **kwargs):
    """新留言以 email 通知作者；開發環境會輸出到 console backend。"""
    if not created:
        return
    author = instance.article.author
    if not author.email or author.pk == instance.author_id:
        return

    send_mail(
        subject=f"[LearnJournal] {instance.author} 留言了：{instance.article.title}",
        message=(
            f"{instance.author} 在〈{instance.article.title}〉留下留言：\n\n"
            f"{instance.body}\n\n"
            "這是教學專案的 console email 示範。"
        ),
        from_email=None,
        recipient_list=[author.email],
        fail_silently=False,
    )
