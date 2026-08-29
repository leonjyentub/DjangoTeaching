def cart_count(request):
    if request.user.is_authenticated:
        return {"cart_count": sum(item.quantity for item in request.user.cart_items.all())}
    return {"cart_count": 0}
