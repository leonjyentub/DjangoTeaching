"""教學用 data migration（Deck 03A 第 2 章）。

情境：`excerpt`（摘要）是後來才加的欄位，早期文章沒有填。
用 RunPython 從內文前 140 字補一份，讓清單頁不會空白。

重點：
  - data migration 用 `apps.get_model()` 取「當下版本」的 model，不要 import 真的 model。
  - 一定要提供 reverse（這裡是安全的 no-op），否則不能往回 migrate。
  - 大表要分批；這裡資料量小，直接一次跑完。
"""

from django.db import migrations


def fill_excerpt(apps, schema_editor):
    Article = apps.get_model("journal", "Article")
    for article in Article.objects.filter(excerpt=""):
        text = " ".join((article.body or "").split())
        article.excerpt = text[:140]
        article.save(update_fields=["excerpt"])


def noop(apps, schema_editor):
    # 反向不刪除摘要：把手動填好的內容清掉風險太大。
    pass


class Migration(migrations.Migration):
    dependencies = [("journal", "0002_alter_article_slug_alter_category_slug_and_more")]
    operations = [migrations.RunPython(fill_excerpt, noop)]
