from django.conf import settings
from django.conf import settings
from django.db import models
from django.urls import reverse


class Message(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="messages",
        verbose_name="作者",
    )
    content = models.TextField("留言內容", max_length=500)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        who = self.author.username if self.author else "訪客"
        return f"{who}：{self.content[:20]}"

    def get_absolute_url(self):
        return reverse("board:list")
