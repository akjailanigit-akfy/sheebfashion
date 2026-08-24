from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path("", views.cart_page, name="page"),
    path("add/<int:product_id>/", views.add_to_cart, name="add"),
    path("update/<int:product_id>/", views.update_cart, name="update"),
    path("remove/<int:product_id>/", views.remove_from_cart, name="remove"),
    path("sync/", views.sync_local_cart, name="sync"),
    path("checkout/", views.checkout_redirect, name="checkout"),
]
