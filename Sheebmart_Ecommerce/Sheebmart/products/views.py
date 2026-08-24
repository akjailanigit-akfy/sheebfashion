from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Category, Product, Review, Wishlist


def home(request):
    context = {
        "new_products": Product.objects.filter(is_new=True, stock__gt=0)[:8],
        "trending_products": Product.objects.filter(is_trending=True, stock__gt=0)[:8],
        "best_sellers": Product.objects.filter(is_best_seller=True, stock__gt=0)[:8],
        "offer_products": Product.objects.filter(is_offer=True, stock__gt=0)[:8],
        "categories": Category.objects.all(),
    }
    return render(request, "home.html", context)


def collection(request):
    products = Product.objects.select_related("category").all()
    category_slug = request.GET.get("category", "").strip()
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "")

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(category__name__icontains=query)
            | Q(brand__icontains=query)
            | Q(description__icontains=query)
        )

    if sort == "price_low":
        products = products.order_by("price")
    elif sort == "price_high":
        products = products.order_by("-price")
    elif sort == "rating":
        products = products.order_by("-rating")
    elif sort == "newest":
        products = products.order_by("-created_at")

    context = {
        "products": products,
        "categories": Category.objects.all(),
        "selected_category": category_slug,
        "query": query,
        "sort": sort,
    }
    return render(request, "collection.html", context)


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("reviews__user", "images"),
        slug=slug,
    )
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(avg=Avg("rating"))["avg"] or product.rating
    wishlist_ids = set()
    if request.user.is_authenticated:
        wishlist_ids = set(
            Wishlist.objects.filter(user=request.user).values_list("product_id", flat=True)
        )

    if request.method == "POST" and request.user.is_authenticated:
        rating = int(request.POST.get("rating", 5))
        comment = request.POST.get("comment", "").strip()
        if comment:
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={"rating": max(1, min(5, rating)), "comment": comment},
            )
            messages.success(request, "Your review has been saved.")
            return redirect("products:detail", slug=product.slug)

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "average_rating": average_rating,
            "in_wishlist": product.id in wishlist_ids,
            "size_list": [s.strip() for s in product.sizes.split(",") if s.strip()],
            "color_list": [c.strip() for c in product.colors.split(",") if c.strip()],
        },
    )


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        wishlist.delete()
        messages.info(request, "Removed from wishlist.")
    else:
        messages.success(request, "Added to wishlist.")
    return redirect(request.META.get("HTTP_REFERER") or "home")


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def wishlist(request):
    items = Wishlist.objects.filter(user=request.user).select_related("product", "product__category")
    return render(request, "wishlist.html", {"items": items})


def about(request):
    return render(request, "about.html")


def contact(request):
    if request.method == "POST":
        messages.success(request, "Thanks! Your message has been received.")
        return redirect("products:contact")
    return render(request, "contact.html")
