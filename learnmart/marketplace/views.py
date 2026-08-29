from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import BoardPostForm, CheckoutForm, ProductForm, RegistrationForm, ReviewForm
from .models import BoardPost, CartItem, Category, Order, OrderItem, Product, Review


class ProductListView(ListView):
    model = Product
    template_name = "marketplace/home.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related("category", "seller")
        query = self.request.GET.get("q", "").strip()
        category = self.request.GET.get("category", "").strip()
        if query:
            queryset = queryset.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["query"] = self.request.GET.get("q", "")
        context["selected_category"] = self.request.GET.get("category", "")
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "marketplace/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related("seller", "category").prefetch_related("reviews__author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["review_form"] = ReviewForm()
        return context


def register(request):
    if request.user.is_authenticated:
        return redirect("marketplace:home")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "註冊成功，歡迎加入學購！")
        return redirect("marketplace:home")
    return render(request, "registration/register.html", {"form": form})


class SellerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_seller


class SellerProductListView(SellerRequiredMixin, ListView):
    model = Product
    template_name = "marketplace/seller_products.html"
    context_object_name = "products"

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).select_related("category")


class ProductCreateView(SellerRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "marketplace/form.html"

    def form_valid(self, form):
        form.instance.seller = self.request.user
        messages.success(self.request, "商品已新增。")
        return super().form_valid(form)


class ProductUpdateView(SellerRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "marketplace/form.html"

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "商品已更新。")
        return super().form_valid(form)


@require_POST
@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    try:
        quantity = max(1, int(request.POST.get("quantity", 1)))
    except ValueError:
        quantity = 1
    if quantity > product.stock:
        messages.error(request, "加入數量超過目前庫存。")
    else:
        item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        item.quantity = quantity if created else min(item.quantity + quantity, product.stock)
        item.save()
        messages.success(request, f"已將「{product.name}」加入購物車。")
    return redirect(product)


@login_required
def cart(request):
    items = request.user.cart_items.select_related("product", "product__seller")
    total = sum(item.subtotal for item in items)
    return render(request, "marketplace/cart.html", {"items": items, "total": total})


@require_POST
@login_required
def update_cart(request, pk):
    item = get_object_or_404(CartItem, pk=pk, user=request.user)
    try:
        quantity = int(request.POST.get("quantity", 1))
    except ValueError:
        quantity = 1
    if quantity <= 0:
        item.delete()
    elif quantity <= item.product.stock:
        item.quantity = quantity
        item.save()
    else:
        messages.error(request, "數量超過庫存。")
    return redirect("marketplace:cart")


@require_POST
@login_required
def remove_from_cart(request, pk):
    get_object_or_404(CartItem, pk=pk, user=request.user).delete()
    return redirect("marketplace:cart")


@login_required
@transaction.atomic
def checkout(request):
    items = list(request.user.cart_items.select_related("product", "product__seller").select_for_update())
    if not items:
        messages.info(request, "購物車目前是空的。")
        return redirect("marketplace:cart")
    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        for item in items:
            if item.quantity > item.product.stock:
                messages.error(request, f"「{item.product.name}」庫存不足，請調整數量。")
                return redirect("marketplace:cart")
        order = form.save(commit=False)
        order.buyer = request.user
        order.total = sum(item.subtotal for item in items)
        order.save()
        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                seller=item.product.seller,
                product_name=item.product.name,
                unit_price=item.product.price,
                quantity=item.quantity,
            )
            item.product.stock -= item.quantity
            item.product.save(update_fields=["stock"])
        request.user.cart_items.all().delete()
        messages.success(request, f"訂單 #{order.pk} 已成立。")
        return redirect("marketplace:order-detail", pk=order.pk)
    return render(request, "marketplace/checkout.html", {"form": form, "items": items})


class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = "marketplace/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).prefetch_related("items")


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "marketplace/order_detail.html"
    context_object_name = "order"

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).prefetch_related("items__product")


class SellerOrderListView(SellerRequiredMixin, ListView):
    model = Order
    template_name = "marketplace/seller_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(items__seller=self.request.user).distinct().prefetch_related("items")


@require_POST
@login_required
def ship_order(request, pk):
    if not request.user.is_seller:
        return HttpResponseForbidden("只有賣家可以確認出貨。")
    order = get_object_or_404(Order.objects.filter(items__seller=request.user).distinct(), pk=pk)
    if order.status == Order.Status.PENDING:
        order.status = Order.Status.SHIPPED
        order.shipped_at = timezone.now()
        order.save(update_fields=["status", "shipped_at"])
        messages.success(request, f"訂單 #{order.pk} 已標記為出貨。")
    return redirect("marketplace:seller-orders")


@require_POST
@login_required
def add_review(request, pk):
    product = get_object_or_404(Product, pk=pk)
    has_purchased = OrderItem.objects.filter(
        order__buyer=request.user, product=product, order__status__in=[Order.Status.SHIPPED, Order.Status.COMPLETED]
    ).exists()
    if not has_purchased:
        messages.error(request, "商品出貨後才能留下評價。")
        return redirect(product)
    form = ReviewForm(request.POST)
    if form.is_valid():
        Review.objects.update_or_create(product=product, author=request.user, defaults=form.cleaned_data)
        messages.success(request, "謝謝你的評價！")
    else:
        messages.error(request, "評價內容有誤，請重新輸入。")
    return redirect(product)


class BoardListView(ListView):
    model = BoardPost
    template_name = "marketplace/board_list.html"
    context_object_name = "posts"
    paginate_by = 10


class BoardPostCreateView(LoginRequiredMixin, CreateView):
    model = BoardPost
    form_class = BoardPostForm
    template_name = "marketplace/form.html"
    success_url = "/board/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "留言已發布。")
        return super().form_valid(form)
