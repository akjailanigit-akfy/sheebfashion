from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    brand = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    specifications = models.TextField(blank=True, help_text="One specification per line.")
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="Upload product image")
    image_url = models.URLField(max_length=500, blank=True, help_text="Legacy: Use image field instead")
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0"))])
    discount_percent = models.PositiveIntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    stock = models.PositiveIntegerField(default=0)
    sizes = models.CharField(max_length=200, blank=True, help_text="Example: S,M,L,XL")
    colors = models.CharField(max_length=200, blank=True, help_text="Example: Black,White")
    rating = models.DecimalField(
        max_digits=3, decimal_places=1, default=4.5,
        validators=[MinValueValidator(Decimal("0")), MaxValueValidator(Decimal("5"))]
    )
    is_new = models.BooleanField(default=False)
    is_trending = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=False)
    is_offer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        return self.price * (Decimal("1") - Decimal(self.discount_percent) / Decimal("100"))

    @property
    def savings(self):
        return self.price - self.discounted_price




class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(max_length=500)
    alt_text = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.product.name} image"


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["product", "user"], name="one_review_per_user_product")
        ]

    def __str__(self):
        return f"{self.product.name} - {self.user.username}"


class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "product"], name="unique_wishlist_product")
        ]

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
