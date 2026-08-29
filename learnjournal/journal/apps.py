from django.apps import AppConfig


class JournalConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "journal"

    def ready(self):
        # 匯入 signal handler；沒有這行，@receiver 不會被註冊。
        from journal import signals  # noqa: F401
