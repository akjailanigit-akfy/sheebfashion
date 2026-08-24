from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.home, name="home"),
    path("shop/", views.collection, name="collection"),
    path("product/<slug:slug>/", views.product_detail, name="detail"),
    path("wishlist/toggle/<int:product_id>/", views.toggle_wishlist, name="toggle_wishlist"),
    path("profile/", views.profile, name="profile"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]
