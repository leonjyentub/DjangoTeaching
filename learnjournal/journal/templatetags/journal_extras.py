"""自訂 template tags 與 filters（Deck 03A 第 5 章）。

三種形式：
  - filter：把一個值變成另一個值（`{{ article.body|markdownify }}`）
  - simple_tag：回傳一個值（`{% reading_time article %}`）
  - inclusion_tag：算出 context 再渲染一個小模板（`{% tag_cloud %}`）
"""

import markdown as md
from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe

from journal.models import Article, Tag

register = template.Library()


@register.filter
def markdownify(text):
    # mark_safe 是明確的安全邊界：只有信任來源（已渲染的內文）才這樣輸出。
    # 回扣 Deck 02 第 7 章：使用者輸入若走這條路就是 stored XSS。
    return mark_safe(md.markdown(text or "", extensions=["fenced_code", "tables"]))


@register.simple_tag
def reading_time(article):
    return f"閱讀時間約 {article.reading_minutes} 分鐘"


@register.inclusion_tag("journal/_tag_cloud.html")
def tag_cloud(limit=20):
    # values().annotate() = GROUP BY：每個標籤數它有幾篇已發佈文章。
    tags = (
        Tag.objects.filter(articles__status="published")
        .annotate(count=Count("articles"))
        .order_by("-count")[:limit]
    )
    return {"tags": tags}


@register.inclusion_tag("journal/_latest_articles.html")
def latest_articles(limit=5):
    return {"articles": Article.published.all()[:limit]}
