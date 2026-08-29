from django.core.management.base import BaseCommand

from marketplace.models import BoardPost, Category, Product, User


class Command(BaseCommand):
    help = "建立 LearnMart 課堂示範帳號與商品（可重複執行）"

    def handle(self, *args, **options):
        seller, created = User.objects.get_or_create(
            username="seller",
            defaults={"email": "seller@example.com", "role": User.Role.SELLER},
        )
        if created:
            seller.set_password("seller12345")
            seller.save()

        buyer, created = User.objects.get_or_create(
            username="buyer",
            defaults={"email": "buyer@example.com", "role": User.Role.BUYER},
        )
        if created:
            buyer.set_password("buyer12345")
            buyer.save()

        categories = {}
        for name, slug in [("3C 科技", "tech"), ("生活家電", "home"), ("書籍文具", "books")]:
            categories[slug], _ = Category.objects.get_or_create(name=name, slug=slug)

        products = [
            ("教學用機械鍵盤", "tech", 1590, 20, "練習商品詳情頁與購物車流程的示範鍵盤。"),
            ("RWD 隨行杯", "home", 450, 35, "提醒我們：版面像杯子一樣，也要適應不同尺寸。"),
            ("Django 學習筆記本", "books", 180, 50, "記錄 URL、View、Template 與 ORM 的課堂重點。"),
            ("Python 桌墊", "tech", 690, 12, "印有 Python 與 HTTP request flow 的大型桌墊。"),
            ("SQLite 收納盒", "home", 320, 8, "單檔、輕巧，適合裝入課程前半段的練習資料。"),
            ("Git 版本控制貼紙組", "books", 120, 100, "commit 小、訊息清楚，讓每一次學習都有歷史。"),
        ]
        for name, slug, price, stock, description in products:
            Product.objects.get_or_create(
                seller=seller,
                name=name,
                defaults={
                    "category": categories[slug],
                    "price": price,
                    "stock": stock,
                    "description": description,
                },
            )

        BoardPost.objects.get_or_create(
            author=buyer,
            title="歡迎來到 LearnMart",
            defaults={"content": "這裡可以提出 Django 問題，也可以練習安全顯示使用者輸入。"},
        )
        self.stdout.write(self.style.SUCCESS("示範資料已準備完成。seller/seller12345；buyer/buyer12345"))
