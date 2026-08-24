from django.contrib import admin
from .models import Category, Product, ProductImage, Review, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "brand", "price", "discount_percent",
        "discounted_price_display", "stock", "rating", "is_new",
        "is_trending", "is_best_seller", "is_offer"
    )
    list_filter = ("category", "is_new", "is_trending", "is_best_seller", "is_offer")
    search_fields = ("name", "brand", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("stock", "is_new", "is_trending", "is_best_seller", "is_offer")
    inlines = [ProductImageInline]
    fieldsets = (
        ("Product Information", {
            "fields": ("name", "slug", "category", "brand", "description")
        }),
        ("Pricing & Stock", {
            "fields": ("price", "discount_percent", "stock")
        }),
        ("Images", {
            "fields": ("image", "image_url"),
            "description": "Upload a product image or provide a URL (image field takes priority)"
        }),
        ("Variants", {
            "fields": ("sizes", "colors")
        }),
        ("Details", {
            "fields": ("specifications", "rating")
        }),
        ("Status", {
            "fields": ("is_new", "is_trending", "is_best_seller", "is_offer")
        }),
    )

    @admin.display(description="Sale Price")
    def discounted_price_display(self, obj):
        return obj.discounted_price


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__name", "user__username", "comment")


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
    search_fields = ("user__username", "product__name")
