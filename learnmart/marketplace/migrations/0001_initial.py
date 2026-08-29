# Generated for the LearnMart teaching project using Django 5.2.
import decimal

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("auth", "0012_alter_user_first_name_max_length")]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True, verbose_name="分類名稱")),
                ("slug", models.SlugField(max_length=80, unique=True, verbose_name="網址代稱")),
            ],
            options={"verbose_name": "商品分類", "verbose_name_plural": "商品分類", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("is_superuser", models.BooleanField(default=False, help_text="Designates that this user has all permissions without explicitly assigning them.", verbose_name="superuser status")),
                ("username", models.CharField(error_messages={"unique": "A user with that username already exists."}, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.", max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name="username")),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="email address")),
                ("is_staff", models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.", verbose_name="staff status")),
                ("is_active", models.BooleanField(default=True, help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.", verbose_name="active")),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("role", models.CharField(choices=[("buyer", "買家"), ("seller", "賣家")], default="buyer", max_length=10, verbose_name="身份")),
                ("groups", models.ManyToManyField(blank=True, help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.", related_name="user_set", related_query_name="user", to="auth.group", verbose_name="groups")),
                ("user_permissions", models.ManyToManyField(blank=True, help_text="Specific permissions for this user.", related_name="user_set", related_query_name="user", to="auth.permission", verbose_name="user permissions")),
            ],
            options={"verbose_name": "user", "verbose_name_plural": "users", "abstract": False},
            managers=[("objects", django.contrib.auth.models.UserManager())],
        ),
        migrations.CreateModel(
            name="BoardPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120, verbose_name="主旨")),
                ("content", models.TextField(verbose_name="內容")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="board_posts", to="marketplace.user")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150, verbose_name="商品名稱")),
                ("description", models.TextField(verbose_name="商品說明")),
                ("price", models.DecimalField(decimal_places=0, max_digits=10, verbose_name="售價")),
                ("stock", models.PositiveIntegerField(default=0, verbose_name="庫存")),
                ("image", models.ImageField(blank=True, upload_to="products/%Y/%m/", verbose_name="商品圖片")),
                ("is_active", models.BooleanField(default=True, verbose_name="上架")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="建立時間")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="更新時間")),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="marketplace.category", verbose_name="分類")),
                ("seller", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="products", to="marketplace.user", verbose_name="賣家")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name="數量")),
                ("added_at", models.DateTimeField(auto_now_add=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cart_items", to="marketplace.product")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cart_items", to="marketplace.user")),
            ],
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("recipient_name", models.CharField(max_length=80, verbose_name="收件人")),
                ("address", models.CharField(max_length=255, verbose_name="收件地址")),
                ("phone", models.CharField(max_length=30, verbose_name="聯絡電話")),
                ("status", models.CharField(choices=[("pending", "待出貨"), ("shipped", "已出貨"), ("completed", "已完成"), ("cancelled", "已取消")], default="pending", max_length=12, verbose_name="狀態")),
                ("total", models.DecimalField(decimal_places=0, default=decimal.Decimal("0"), max_digits=12, verbose_name="訂單總額")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="下單時間")),
                ("shipped_at", models.DateTimeField(blank=True, null=True, verbose_name="出貨時間")),
                ("buyer", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orders", to="marketplace.user", verbose_name="買家")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_name", models.CharField(max_length=150, verbose_name="商品名稱快照")),
                ("unit_price", models.DecimalField(decimal_places=0, max_digits=10, verbose_name="購買時單價")),
                ("quantity", models.PositiveIntegerField(verbose_name="數量")),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="marketplace.order")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="order_items", to="marketplace.product")),
                ("seller", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="sold_items", to="marketplace.user")),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name="評分")),
                ("comment", models.TextField(verbose_name="評論")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="marketplace.user")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="marketplace.product")),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddConstraint(model_name="cartitem", constraint=models.UniqueConstraint(fields=("user", "product"), name="unique_cart_product")),
        migrations.AddConstraint(model_name="review", constraint=models.UniqueConstraint(fields=("product", "author"), name="one_review_per_product")),
    ]
