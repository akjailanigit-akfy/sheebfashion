from django.contrib import admin
from .models import Address, Order, OrderItem


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("full_name", "mobile", "city", "state", "pincode", "user")
    search_fields = ("full_name", "mobile", "city", "pincode", "user__username")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "unit_price", "quantity", "line_total")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "payment_method", "total", "created_at")
    list_filter = ("status", "payment_method", "created_at")
    search_fields = ("id", "user__username", "user__email")
    list_editable = ("status",)
    inlines = [OrderItemInline]
    readonly_fields = ("subtotal", "delivery_charge", "total", "created_at")
