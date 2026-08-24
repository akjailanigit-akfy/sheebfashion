def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            count = sum(item.quantity for item in request.user.cart.items.all())
        except Exception:
            count = 0
    else:
        count = sum(request.session.get("cart", {}).values())
    return {"cart_count": count}
