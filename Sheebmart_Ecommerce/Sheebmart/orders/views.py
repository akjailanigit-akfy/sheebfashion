from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.models import Cart
from products.models import Product
from .forms import AddressForm
from .models import Address, Order, OrderItem


def _cart_totals(cart):
    items = list(cart.items.select_related("product"))
    subtotal = sum((item.product.discounted_price * item.quantity for item in items), Decimal("0"))
    delivery = Decimal("0") if subtotal >= Decimal("999") or subtotal == 0 else Decimal("49")
    return items, subtotal, delivery, subtotal + delivery


@login_required
def address_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items, subtotal, delivery, total = _cart_totals(cart)
    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("cart:page")

    form = AddressForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        request.session["checkout_address_id"] = address.id
        return redirect("orders:summary")
    return render(
        request,
        "address.html",
        {"form": form, "subtotal": subtotal, "delivery": delivery, "total": total},
    )


@login_required
def summary_view(request):
    address_id = request.session.get("checkout_address_id")
    address = get_object_or_404(Address, id=address_id, user=request.user) if address_id else None
    if address is None:
        return redirect("orders:address")

    cart, _ = Cart.objects.get_or_create(user=request.user)
    items, subtotal, delivery, total = _cart_totals(cart)
    if not items:
        return redirect("cart:page")

    return render(
        request,
        "summary.html",
        {
            "address": address,
            "items": items,
            "subtotal": subtotal,
            "delivery": delivery,
            "total": total,
        },
    )


@login_required
@require_POST
@transaction.atomic
def place_order(request):
    address_id = request.session.get("checkout_address_id")
    address = get_object_or_404(Address, id=address_id, user=request.user) if address_id else None
    if address is None:
        return redirect("orders:address")

    cart, _ = Cart.objects.get_or_create(user=request.user)
    items, subtotal, delivery, total = _cart_totals(cart)
    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart:page")

    payment_method = request.POST.get("payment_method", "cod")
    if payment_method not in {"cod", "online"}:
        payment_method = "cod"

    for item in items:
        if item.quantity > item.product.stock:
            messages.error(request, f"Not enough stock for {item.product.name}.")
            return redirect("cart:page")

    order = Order.objects.create(
        user=request.user,
        address=address,
        payment_method=payment_method,
        subtotal=subtotal,
        delivery_charge=delivery,
        total=total,
    )

    for item in items:
        product = Product.objects.select_for_update().get(pk=item.product.pk)
        product.stock -= item.quantity
        product.save(update_fields=["stock"])
        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.name,
            unit_price=product.discounted_price,
            quantity=item.quantity,
            line_total=product.discounted_price * item.quantity,
        )

    cart.items.all().delete()
    request.session.pop("checkout_address_id", None)
    request.session.pop("cart", None)

    return redirect("orders:success", order_id=order.id)


@login_required
def success_view(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related("items"),
        id=order_id,
        user=request.user,
    )
    return render(request, "order_success.html", {"order": order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items")
    return render(request, "orders.html", {"orders": orders})
