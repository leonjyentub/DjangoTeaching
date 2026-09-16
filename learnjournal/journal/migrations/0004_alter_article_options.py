from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("journal", "0003_backfill_excerpt"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="article",
            options={
                "ordering": ["-published_at", "-created_at"],
                "permissions": [("publish_article", "Can publish and schedule articles")],
            },
        ),
    ]
