from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product
from .models import Cart, CartItem


def _get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def _session_cart(request):
    return request.session.setdefault("cart", {})


def _merge_session_into_user(request, user):
    session_cart = request.session.get("cart", {})
    if not session_cart:
        return
    cart = _get_or_create_cart(user)
    for product_id, quantity in session_cart.items():
        try:
            product = Product.objects.get(id=int(product_id), stock__gt=0)
        except Product.DoesNotExist:
            continue
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = min(
            product.stock,
            item.quantity + int(quantity) if not created else int(quantity),
        )
        item.save()
    request.session["cart"] = {}


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = max(1, int(request.POST.get("quantity", 1) or 1))
    quantity = min(quantity, product.stock) if product.stock else 0

    if quantity <= 0:
        return JsonResponse({"ok": False, "message": "This product is out of stock."}, status=400)

    if request.user.is_authenticated:
        cart = _get_or_create_cart(request.user)
        item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        item.quantity = min(product.stock, item.quantity + quantity)
        item.save()
        count = sum(i.quantity for i in cart.items.all())
    else:
        cart = _session_cart(request)
        key = str(product.id)
        cart[key] = min(product.stock, int(cart.get(key, 0)) + quantity)
        request.session.modified = True
        count = sum(cart.values())

    return JsonResponse({"ok": True, "message": f"{product.name} added to cart.", "count": count})


def cart_page(request):
    if request.user.is_authenticated:
        _merge_session_into_user(request, request.user)
        cart = _get_or_create_cart(request.user)
        items = list(cart.items.select_related("product", "product__category"))
    else:
        items = []
        for product_id, quantity in _session_cart(request).items():
            try:
                product = Product.objects.select_related("category").get(id=int(product_id))
                items.append({"product": product, "quantity": quantity, "line_total": product.discounted_price * quantity})
            except Product.DoesNotExist:
                pass

    subtotal = sum((item.line_total for item in items), Decimal("0")) if items else Decimal("0")
    discount = sum(
        ((item.product.price - item.product.discounted_price) * item.quantity for item in items),
        Decimal("0"),
    ) if items else Decimal("0")
    delivery = Decimal("0") if subtotal >= Decimal("999") or subtotal == 0 else Decimal("49")
    total = subtotal + delivery

    return render(
        request,
        "cart.html",
        {"items": items, "subtotal": subtotal, "discount": discount, "delivery": delivery, "total": total},
    )


@require_POST
def update_cart(request, product_id):
    quantity = max(0, int(request.POST.get("quantity", 1) or 0))
    product = get_object_or_404(Product, id=product_id)

    if request.user.is_authenticated:
        cart = _get_or_create_cart(request.user)
        item = CartItem.objects.filter(cart=cart, product=product).first()
        if item:
            if quantity == 0:
                item.delete()
            else:
                item.quantity = min(quantity, product.stock)
                item.save()
    else:
        session_cart = _session_cart(request)
        key = str(product.id)
        if quantity == 0:
            session_cart.pop(key, None)
        else:
            session_cart[key] = min(quantity, product.stock)
        request.session.modified = True

    return redirect("cart:page")


@require_POST
def remove_from_cart(request, product_id):
    return update_cart(request, product_id)


@login_required
@require_POST
def sync_local_cart(request):
    _merge_session_into_user(request, request.user)
    return JsonResponse({"ok": True})


def checkout_redirect(request):
    if request.user.is_authenticated:
        return redirect("orders:address")
    messages.info(request, "Please log in to continue to checkout.")
    return redirect(f"/accounts/login/?next=/orders/address/")
