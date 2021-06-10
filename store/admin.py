from django.contrib import admin

from .models import (
    Supplier,
    Product,
    Order,
)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone_number', 'created_date']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'barcode', 'supplier', 'price', 'list_price', 'stock', 'stock_alert']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'total', 'list_total', 'by_card', 'by_trust', 'to_trust', 'user']


admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
