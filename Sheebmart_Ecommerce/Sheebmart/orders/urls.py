from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("address/", views.address_view, name="address"),
    path("summary/", views.summary_view, name="summary"),
    path("place/", views.place_order, name="place"),
    path("success/<int:order_id>/", views.success_view, name="success"),
    path("my-orders/", views.my_orders, name="my_orders"),
]
