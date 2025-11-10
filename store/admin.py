from django.contrib import admin

from .models import (
    Address,
    Category,
    Brand,
    Product,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Payment,
    Shipment,
    Review,
)


admin.site.register(Address)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Payment)
admin.site.register(Shipment)
admin.site.register(Review)
