from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import BoardPost, CartItem, Category, Order, OrderItem, Product, Review, User


@admin.register(User)
class MarketplaceUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("市集身份", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("市集身份", {"fields": ("role", "email")}),)
    list_display = ("username", "email", "role", "is_staff", "is_active")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "seller", "price", "stock", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "unit_price", "quantity", "seller")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "buyer", "status", "total", "created_at")
    list_filter = ("status", "created_at")
    inlines = [OrderItemInline]


admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(Review)
admin.site.register(BoardPost)
