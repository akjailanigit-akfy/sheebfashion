from django.core.management.base import BaseCommand
from products.models import Category, Product


CATEGORIES = [
    ("Men's Fashion", "men"),
    ("Women's Fashion", "women"),
    ("Kids", "kids"),
    ("Shoes", "shoes"),
    ("Bags", "bags"),
    ("Watches", "watches"),
    ("Accessories", "accessories"),
    ("Electronics / Gadgets", "electronics"),
]

PRODUCTS = [
    {
        "category": "men", "name": "Relaxed Cotton Overshirt", "slug": "relaxed-cotton-overshirt",
        "brand": "Sheebmart Studio", "price": 1899, "discount_percent": 20, "stock": 25,
        "rating": 4.7, "is_new": True, "is_trending": True,
        "image_url": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?auto=format&fit=crop&w=900&q=80",
        "description": "A versatile cotton overshirt with a relaxed fit for effortless everyday styling.",
        "specifications": "100% cotton\nRelaxed fit\nMachine washable\nLightweight fabric",
        "sizes": "S,M,L,XL", "colors": "Black,Olive,Cream",
    },
    {
        "category": "women", "name": "Minimal Linen Midi Dress", "slug": "minimal-linen-midi-dress",
        "brand": "Sheebmart Studio", "price": 2499, "discount_percent": 25, "stock": 18,
        "rating": 4.8, "is_new": True, "is_offer": True,
        "image_url": "https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?auto=format&fit=crop&w=900&q=80",
        "description": "A clean linen midi dress designed for breathable comfort and polished days.",
        "specifications": "Linen blend\nMidi length\nSide pockets\nRegular fit",
        "sizes": "XS,S,M,L,XL", "colors": "Beige,Black,White",
    },
    {
        "category": "shoes", "name": "Everyday Street Sneakers", "slug": "everyday-street-sneakers",
        "brand": "Urban Step", "price": 2999, "discount_percent": 15, "stock": 30,
        "rating": 4.6, "is_trending": True, "is_best_seller": True,
        "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80",
        "description": "Cushioned everyday sneakers with a clean silhouette that works with any casual look.",
        "specifications": "Rubber outsole\nCushioned footbed\nLace-up closure\nEveryday use",
        "sizes": "6,7,8,9,10", "colors": "White,Black",
    },
    {
        "category": "bags", "name": "Structured Everyday Tote", "slug": "structured-everyday-tote",
        "brand": "Sheebmart", "price": 1599, "discount_percent": 10, "stock": 22,
        "rating": 4.5, "is_best_seller": True,
        "image_url": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?auto=format&fit=crop&w=900&q=80",
        "description": "A structured tote with enough room for daily essentials and a timeless finish.",
        "specifications": "Top handles\nInner pocket\nZip closure\nPolyurethane finish",
        "colors": "Tan,Black,Cream",
    },
    {
        "category": "watches", "name": "Classic Minimal Watch", "slug": "classic-minimal-watch",
        "brand": "Timecraft", "price": 2199, "discount_percent": 30, "stock": 12,
        "rating": 4.8, "is_offer": True, "is_best_seller": True,
        "image_url": "https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=900&q=80",
        "description": "A minimal dial and comfortable strap make this watch an easy everyday choice.",
        "specifications": "Quartz movement\nMineral glass\nWater resistant\nAdjustable strap",
        "colors": "Black,Silver,Brown",
    },
    {
        "category": "accessories", "name": "Everyday Metal Sunglasses", "slug": "everyday-metal-sunglasses",
        "brand": "Vision Edit", "price": 999, "discount_percent": 10, "stock": 35,
        "rating": 4.4, "is_trending": True,
        "image_url": "https://images.unsplash.com/photo-1511499767150-a48a237f0083?auto=format&fit=crop&w=900&q=80",
        "description": "Lightweight metal sunglasses with a clean frame for everyday wear.",
        "specifications": "UV400 lenses\nMetal frame\nLightweight design\nUnisex",
        "colors": "Gold,Black,Silver",
    },
    {
        "category": "kids", "name": "Soft Cotton Kids Set", "slug": "soft-cotton-kids-set",
        "brand": "Little Edit", "price": 799, "discount_percent": 20, "stock": 20,
        "rating": 4.7, "is_new": True,
        "image_url": "https://images.unsplash.com/photo-1503919545889-aef636e10ad4?auto=format&fit=crop&w=900&q=80",
        "description": "A soft cotton co-ord set made for comfortable play and easy movement.",
        "specifications": "Soft cotton\nComfort fit\nEasy wash\nTwo-piece set",
        "sizes": "2Y,4Y,6Y,8Y,10Y", "colors": "Blue,Beige,Pink",
    },
    {
        "category": "electronics", "name": "Compact Wireless Earbuds", "slug": "compact-wireless-earbuds",
        "brand": "Soundloop", "price": 1999, "discount_percent": 18, "stock": 28,
        "rating": 4.5, "is_offer": True,
        "image_url": "https://images.unsplash.com/photo-1606220945770-b5b6c2c55bf1?auto=format&fit=crop&w=900&q=80",
        "description": "Compact wireless earbuds with a pocket-friendly charging case for daily listening.",
        "specifications": "Bluetooth wireless\nCharging case\nTouch controls\nUSB-C charging",
        "colors": "White,Black",
    },
]


class Command(BaseCommand):
    help = "Create Sheebmart demo categories and products."

    def handle(self, *args, **options):
        category_map = {}
        for name, slug in CATEGORIES:
            category, _ = Category.objects.get_or_create(slug=slug, defaults={"name": name})
            if category.name != name:
                category.name = name
                category.save(update_fields=["name"])
            category_map[slug] = category

        for data in PRODUCTS:
            payload = data.copy()
            category_slug = payload.pop("category")
            Product.objects.update_or_create(
                slug=payload["slug"],
                defaults={**payload, "category": category_map[category_slug]},
            )

        self.stdout.write(self.style.SUCCESS("Sheebmart demo data created successfully."))
