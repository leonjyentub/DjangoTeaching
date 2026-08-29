from django.urls import path

from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
    path("register/", views.register, name="register"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("products/<int:pk>/cart/", views.add_to_cart, name="add-to-cart"),
    path("products/<int:pk>/review/", views.add_review, name="add-review"),
    path("seller/products/", views.SellerProductListView.as_view(), name="seller-products"),
    path("seller/products/new/", views.ProductCreateView.as_view(), name="product-create"),
    path("seller/products/<int:pk>/edit/", views.ProductUpdateView.as_view(), name="product-update"),
    path("cart/", views.cart, name="cart"),
    path("cart/<int:pk>/update/", views.update_cart, name="update-cart"),
    path("cart/<int:pk>/remove/", views.remove_from_cart, name="remove-from-cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("seller/orders/", views.SellerOrderListView.as_view(), name="seller-orders"),
    path("seller/orders/<int:pk>/ship/", views.ship_order, name="ship-order"),
    path("board/", views.BoardListView.as_view(), name="board-list"),
    path("board/new/", views.BoardPostCreateView.as_view(), name="board-create"),
]
