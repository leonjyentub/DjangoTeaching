"""Signals：把「儲存文章」的副作用集中在一處。

Deck 03A 第 6 章先示範一個 signal：文章存檔時把 Markdown 渲染成 HTML 快取。
Deck 03B 第 9 章再擴充：留言通知寄信、清首頁快取、`m2m_changed` 更新標籤計數。

課堂討論點：這段邏輯也可以直接寫在 `Article.save()`。signal 的好處是「發訊者不需要
知道有誰在聽」，壞處是「副作用藏在別的檔案，難追蹤」。不是所有東西都該用 signal。
"""

import markdown as md
from django.db.models.signals import post_save
from django.dispatch import receiver

from journal.models import Article, Comment


@receiver(post_save, sender=Article)
def render_markdown(sender, instance, **kwargs):
    html = md.markdown(instance.body or "", extensions=["fenced_code", "tables", "toc"])
    if html != instance.body_html:
        # update() 不會再觸發 post_save，避免無限迴圈。
        Article.objects.filter(pk=instance.pk).update(body_html=html)


@receiver(post_save, sender=Comment)
def notify_author_on_comment(sender, instance, created, **kwargs):
    if not created:
        return
    # Deck 03B 第 10 章會在這裡呼叫 send_mail 通知文章作者。
    # 目前只留掛鉤，避免測試期間送出真的信。
    return
