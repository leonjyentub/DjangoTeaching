from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from board.models import Message

User = get_user_model()


class Command(BaseCommand):
    help = "建立 LearnBoard 課堂示範帳號與留言（可重複執行）"

    def handle(self, *args, **options):
        users = {}
        for username, email in [("alice", "alice@example.com"), ("bob", "bob@example.com")]:
            user, created = User.objects.get_or_create(username=username, defaults={"email": email})
            if created:
                user.set_password(f"{username}12345")
                user.save()
            users[username] = user

        samples = [
            ("alice", "歡迎來到學言板！這裡是 Django 課程的第一個練習專案。"),
            ("bob", "請問 ListView 的 paginate_by 要寫在哪裡？"),
            (None, "訪客留言：我在還沒有帳號的階段發文，所以作者欄位是空的。"),
            ("alice", "找到答案了：paginate_by 是 ListView 的類別屬性，設 10 就是每頁十筆。"),
        ]
        for username, content in samples:
            Message.objects.get_or_create(
                content=content,
                defaults={"author": users[username] if username else None},
            )
        self.stdout.write(self.style.SUCCESS("示範資料已準備完成。alice/alice12345；bob/bob12345"))
