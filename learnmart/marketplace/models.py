from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    class Role(models.TextChoices):
        BUYER = "buyer", "買家"
        SELLER = "seller", "賣家"

    role = models.CharField("身份", max_length=10, choices=Role.choices, default=Role.BUYER)

    @property
    def is_seller(self):
        return self.role == self.Role.SELLER


class Category(models.Model):
    name = models.CharField("分類名稱", max_length=80, unique=True)
    slug = models.SlugField("網址代稱", max_length=80, unique=True)

    class Meta:
        verbose_name = "商品分類"
        verbose_name_plural = "商品分類"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products", verbose_name="賣家")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products", verbose_name="分類")
    name = models.CharField("商品名稱", max_length=150)
    description = models.TextField("商品說明")
    price = models.DecimalField("售價", max_digits=10, decimal_places=0)
    stock = models.PositiveIntegerField("庫存", default=0)
    image = models.ImageField("商品圖片", upload_to="products/%Y/%m/", blank=True)
    is_active = models.BooleanField("上架", default=True)
    created_at = models.DateTimeField("建立時間", auto_now_add=True)
    updated_at = models.DateTimeField("更新時間", auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("marketplace:product-detail", kwargs={"pk": self.pk})

    @property
    def average_rating(self):
        result = self.reviews.aggregate(avg=models.Avg("rating"))["avg"]
        return round(result, 1) if result else None


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField("數量", default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "product"], name="unique_cart_product")]

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "待出貨"
        SHIPPED = "shipped", "已出貨"
        COMPLETED = "completed", "已完成"
        CANCELLED = "cancelled", "已取消"

    buyer = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders", verbose_name="買家")
    recipient_name = models.CharField("收件人", max_length=80)
    address = models.CharField("收件地址", max_length=255)
    phone = models.CharField("聯絡電話", max_length=30)
    status = models.CharField("狀態", max_length=12, choices=Status.choices, default=Status.PENDING)
    total = models.DecimalField("訂單總額", max_digits=12, decimal_places=0, default=Decimal("0"))
    created_at = models.DateTimeField("下單時間", auto_now_add=True)
    shipped_at = models.DateTimeField("出貨時間", null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"訂單 #{self.pk} - {self.buyer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name="sold_items")
    product_name = models.CharField("商品名稱快照", max_length=150)
    unit_price = models.DecimalField("購買時單價", max_digits=10, decimal_places=0)
    quantity = models.PositiveIntegerField("數量")

    @property
    def subtotal(self):
        return self.unit_price * self.quantity


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField("評分", validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField("評論")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["product", "author"], name="one_review_per_product")]


class BoardPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="board_posts")
    title = models.CharField("主旨", max_length=120)
    content = models.TextField("內容")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
