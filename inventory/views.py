from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from datetime import datetime

from store.models import Product, Supplier, Buyer, Order


@login_required(login_url='login')
def dashboard(request):
    total_buyer = Buyer.objects.filter(active=True).count()
    total_product = Product.objects.filter(active=True).count()
    total_supplier = Supplier.objects.filter(active=True).count()
    total_order = Order.objects.filter(created_date=datetime.now().date()).count()
    orders = Order.objects.all().order_by('-id')
    products = Product.objects.filter(active=True)
    active_products_list_price = 0
    active_products_selling_price = 0
    for product in products:
        active_products_list_price = active_products_list_price + (product.stock * product.list_price)
        active_products_selling_price = active_products_selling_price + (product.stock * product.price)
    context = {
        'product': total_product,
        'supplier': total_supplier,
        'buyer': total_buyer,
        'order': total_order,
        'orders': orders,
        'active_products_list_price': active_products_list_price,
        'active_products_selling_price': active_products_selling_price,
    }
    return render(request, 'dashboard.html', context)
