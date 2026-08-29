from django.test import TestCase
from django.urls import reverse

from .models import CartItem, Category, Order, Product, User


class MarketplaceFlowTests(TestCase):
    def setUp(self):
        self.seller = User.objects.create_user(username="seller", password="safe-pass-123", role=User.Role.SELLER)
        self.buyer = User.objects.create_user(username="buyer", password="safe-pass-123")
        category = Category.objects.create(name="3C", slug="3c")
        self.product = Product.objects.create(
            seller=self.seller, category=category, name="教學鍵盤", description="適合練習", price=990, stock=5
        )

    def test_search_finds_product(self):
        response = self.client.get(reverse("marketplace:home"), {"q": "鍵盤"})
        self.assertContains(response, "教學鍵盤")

    def test_anonymous_user_cannot_add_cart(self):
        response = self.client.post(reverse("marketplace:add-to-cart", args=[self.product.pk]))
        self.assertRedirects(response, f"/accounts/login/?next=/products/{self.product.pk}/cart/")

    def test_buyer_can_add_cart(self):
        self.client.login(username="buyer", password="safe-pass-123")
        self.client.post(reverse("marketplace:add-to-cart", args=[self.product.pk]), {"quantity": 2})
        self.assertEqual(CartItem.objects.get(user=self.buyer).quantity, 2)

    def test_buyer_cannot_open_seller_dashboard(self):
        self.client.login(username="buyer", password="safe-pass-123")
        response = self.client.get(reverse("marketplace:seller-products"))
        self.assertEqual(response.status_code, 403)

    def test_checkout_creates_order_and_reduces_stock(self):
        self.client.login(username="buyer", password="safe-pass-123")
        CartItem.objects.create(user=self.buyer, product=self.product, quantity=2)
        response = self.client.post(
            reverse("marketplace:checkout"),
            {"recipient_name": "王小明", "phone": "0912345678", "address": "台北市教學路 1 號"},
        )
        order = Order.objects.get(buyer=self.buyer)
        self.assertRedirects(response, reverse("marketplace:order-detail", args=[order.pk]))
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)
        self.assertEqual(order.total, 1980)

    def test_user_cannot_read_another_users_order(self):
        other = User.objects.create_user(username="other", password="safe-pass-123")
        order = Order.objects.create(
            buyer=other, recipient_name="他人", phone="0900000000", address="秘密地址", total=0
        )
        self.client.login(username="buyer", password="safe-pass-123")
        response = self.client.get(reverse("marketplace:order-detail", args=[order.pk]))
        self.assertEqual(response.status_code, 404)
