from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import F, Count, Sum

from datetime import date, timedelta
import ast

from .models import (
    Buyer,
    Supplier,
    Product,
    Order,
    OrderProduct,
    CashMovement
)

from .forms import (
    BuyerForm,
    SupplierForm,
    ProductForm,
    OrderForm,
    BillingForm,
    CashMovementForm,
    StatisticsTimeParallel,
    StatisticsBestDay,
    StatisticsBestProduct,
)


# Buyer views
@login_required(login_url='login')
def create_buyer(request):
    forms = BuyerForm(request.POST or None)
    if request.method == 'POST':
        if forms.is_valid():
            forms.save()
            return redirect('buyer-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_buyer.html', context)


@staff_member_required
@login_required(login_url='login')
def edit_buyer(request):
    form = BuyerForm()
    if request.method == 'GET':
        buyer_id = request.GET['buyer']
        buyer = Buyer.objects.filter(id=buyer_id).first()
        form.fields['name'].widget.attrs['value'] = buyer.name
        form.fields['address'].widget.attrs['value'] = buyer.address
        form.fields['phone_number'].widget.attrs['value'] = buyer.phone_number
        context = {
            'form': form, 'buyer_id': buyer_id
        }
        return render(request, 'store/edit_buyer.html', context)
    if request.method == 'POST':
        buyer_id = request.POST['id']
        buyer = get_object_or_404(Buyer, pk=buyer_id)
        form = BuyerForm(request.POST, instance=buyer)
        if form.is_valid():
            buyer.save()
            return redirect('buyer-list')
        context = {'form': form, 'buyer_id': buyer_id}
        return render(request, 'store/edit_buyer.html', context)


@staff_member_required
@login_required(login_url='login')
def delete_buyer(request):
    buyer_id = request.GET['buyer']
    buyer = Buyer.objects.filter(id=buyer_id).first()
    buyer.active = False
    buyer.save()
    return redirect('buyer-list')


class BuyerListView(ListView):
    model = Buyer
    template_name = 'store/buyer_list.html'
    context_object_name = 'buyer'


# Supplier views
@login_required(login_url='login')
def create_supplier(request):
    forms = SupplierForm(request.POST or None)
    if request.method == 'POST':
        if forms.is_valid():
            forms.save()
            return redirect('supplier-list')
    context = {
        'form': forms
    }
    return render(request, 'store/create_supplier.html', context)


@staff_member_required
@login_required(login_url='login')
def edit_supplier(request):
    form = SupplierForm()
    if request.method == 'GET':
        supplier_id = request.GET['supplier']
        supplier = Supplier.objects.filter(id=supplier_id).first()
        form.fields['name'].widget.attrs['value'] = supplier.name
        form.fields['address'].widget.attrs['value'] = supplier.address
        form.fields['phone_number'].widget.attrs['value'] = supplier.phone_number
        if supplier.days:
            form.fields['days'].initial = tuple(ast.literal_eval(supplier.days))
        context = {
            'form': form, 'supplier_id': supplier_id
        }
        return render(request, 'store/edit_supplier.html', context)
    if request.method == 'POST':
        supplier_id = request.POST['id']
        supplier = get_object_or_404(Supplier, pk=supplier_id)
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier.save()
            return redirect('supplier-list')
        context = {'form': form, 'supplier_id': supplier_id}
        return render(request, 'store/edit_supplier.html', context)


@staff_member_required
@login_required(login_url='login')
def delete_supplier(request):
    supplier_id = request.GET['supplier']
    supplier = Supplier.objects.filter(id=supplier_id).first()
    supplier.active = False
    supplier.save()
    return redirect('supplier-list')


class SupplierListView(ListView):
    model = Supplier
    template_name = 'store/supplier_list.html'
    context_object_name = 'supplier'


# Product views
@login_required(login_url='login')
def create_product(request):
    forms = ProductForm()
    if request.method == 'POST':
        forms = ProductForm(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('product-list')
    context = {
        'form': forms,
    }
    return render(request, 'store/create_product.html', context)


@staff_member_required
@login_required(login_url='login')
def edit_product(request):
    form = ProductForm()
    if request.method == 'GET':
        product_id = request.GET['product']
        product = Product.objects.filter(id=product_id).first()
        form.fields['supplier'].initial = product.supplier
        form.fields['barcode'].widget.attrs['value'] = product.barcode
        form.fields['name'].widget.attrs['value'] = product.name
        form.fields['price'].widget.attrs['value'] = product.price
        form.fields['list_price'].widget.attrs['value'] = product.list_price
        form.fields['profit_porc'].widget.attrs['value'] = product.profit_porc
        form.fields['rounding'].widget.attrs['value'] = product.rounding
        form.fields['stock'].widget.attrs['value'] = product.stock
        form.fields['stock_alert'].widget.attrs['value'] = product.stock_alert
        form.fields['expire_date'].widget.attrs['value'] = product.expire_date
        context = {
            'form': form, 'product_id': product_id
        }
        return render(request, 'store/edit_product.html', context)
    if request.method == 'POST':
        product_id = request.POST['id']
        product = get_object_or_404(Product, pk=product_id)
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product.save()
            return redirect('product-list')
        context = {'form': form, 'product_id': product_id}
        return render(request, 'store/edit_product.html', context)


@staff_member_required
@login_required(login_url='login')
def delete_product(request):
    product_id = request.GET['product']
    product = Product.objects.filter(id=product_id).first()
    product.active = False
    product.save()
    return redirect('product-list')


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'


# Order views
@login_required(login_url='login')
def create_order(request):
    extra_products = get_extra_products(request)
    form = OrderForm(request.POST or None, extra=extra_products)
    if request.method == 'POST':
        if form.is_valid():
            order = form.save(user=request.user)
            return redirect('order-list')
    context = {
        'form': form
    }
    return render(request, 'store/create_order.html', context)


class OrderListView(ListView):
    model = Order
    template_name = 'store/order_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = Order.objects.all().order_by('-id')
        return context


def get_extra_products(request):
    extra = int((len(request.POST)-6)/4)
    return extra


def get_product_by_barcode(request):
    barcode = request.GET.get('barcode')
    product = Product.objects.filter(barcode=barcode).first()
    if product:
        data = {'error': 0,
                'product': product.id,
                'price': product.price,
                'list_price': product.list_price,
                'stock': product.stock}
    else:
        data = {'error': 40, 'message': 'No hay un objeto con el código de barras ingresado.'}
    return JsonResponse(data)


def get_product_by_id(request):
    product_id = request.GET.get('product_id')
    product = Product.objects.filter(id=product_id).first()
    if product:
        data = {'error': 0,
                'product': product.id,
                'price': product.price,
                'list_price': product.list_price,
                'stock': product.stock}
    else:
        data = {'error': 40, 'message': 'No hay un objeto con el código de barras ingresado.'}
    return JsonResponse(data)


def get_order_data(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.filter(id=order_id).first()
    order_products = OrderProduct.objects.filter(order=order_id)
    products = dict()
    order_to_trust = ''
    if order.to_trust:
        order_to_trust = order.to_trust.name
    for order_product in order_products:
        products[order_product.product_id] = {
            'product': order_product.product.name,
            'quantity': order_product.quantity,
            'value': order_product.price
        }
    data = {
        'error': 0,
        'id': order.id,
        'total': order.total,
        'list_total': order.list_total,
        'date': order.created_date,
        'by_card': order.by_card,
        'by_trust': order.by_trust,
        'to_trust': order_to_trust,
        'products': products,
        'user': order.user.username
    }
    return JsonResponse(data)


# Alert views
def get_alert_stock_products(request):
    products = Product.objects.filter(active=True).filter(stock__lte=F('stock_alert'))
    data = dict()
    if products.count() > 0:
        data['error'] = 0
        data['count'] = products.count()
        data['products'] = dict()
        for product in products:
            data['products'][product.id] = {
                'name': product.name,
                'stock': product.stock,
                'alert_stock': product.stock_alert
            }
    else:
        data['error'] = 204
        data['message'] = 'No hay ningún producto en alerta de stock.'
    return JsonResponse(data)


def get_alert_expire_products(request):
    products = Product.objects.filter(active=True).filter(expire_date__lte=date.today()+timedelta(days=7))
    data = dict()
    if products.count() > 0:
        data['error'] = 0
        data['count'] = products.count()
        data['products'] = dict()
        for product in products:
            data['products'][product.id] = {
                'name': product.name,
                'expire_date': product.expire_date,
            }
    else:
        data['error'] = 204
        data['message'] = 'No hay ningún producto en alerta de vencimiento.'
    return JsonResponse(data)


# Billing views
@staff_member_required
@login_required(login_url='login')
def billing(request):
    form = BillingForm(request.POST or None)
    context = {
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            data = get_billing_data(request.POST.get('date_from'), request.POST.get('date_to'))
            context['data'] = data
            return render(request, 'store/billing.html', context)
    return render(request, 'store/billing.html', context)


def get_billing_data(date_from, date_to):
    orders = Order.objects.filter(created_date__range=[date_from, date_to])
    data = dict()
    users = dict()
    data['total'] = 0
    data['list_total'] = 0
    data['by_trust_total'] = 0
    data['by_card_total'] = 0
    data['orders_count'] = orders.count()
    if date_from == date_to:
        data['title'] = 'Liquidación del día '+str(date_to)
    else:
        data['title'] = 'Liquidación del '+str(date_from.format("%d-%m-%Y"))+' al '+str(date_to.format("%d-%m-%Y"))
    for order in orders:
        data['total'] = data['total'] + order.total
        data['list_total'] = data['list_total'] + order.list_total
        if order.by_trust:
            data['by_trust_total'] = data['by_trust_total'] + order.total
        if order.by_card:
            data['by_card_total'] = data['by_card_total'] + order.total

        if order.user not in users.keys():
            users[order.user] = dict()
            users[order.user]['total'] = 0
            users[order.user]['list_total'] = 0
            users[order.user]['by_trust_total'] = 0
            users[order.user]['by_card_total'] = 0
            users[order.user]['orders_count'] = 0
            users[order.user]['username'] = order.user.username
        users[order.user]['total'] = users[order.user]['total'] + order.total
        users[order.user]['list_total'] = users[order.user]['list_total'] + order.total
        if order.by_trust:
            users[order.user]['by_trust_total'] = users[order.user]['by_trust_total'] + order.total
        if order.by_card:
            users[order.user]['by_card_total'] = users[order.user]['by_card_total'] + order.total
        users[order.user]['orders_count'] = users[order.user]['orders_count'] + 1
    data['users_data'] = users
    return data


# Cash control views
@staff_member_required
@login_required(login_url='login')
def cash_control(request):
    movements = CashMovement.objects.all().order_by('-id')
    form = CashMovementForm(request.POST or None)
    cash_total = CashMovement.objects.last().total
    form.fields['total'].widget.attrs['value'] = cash_total
    context = {
        'form': form,
        'movements': movements,
        'cash_total': cash_total
    }
    if request.method == 'POST':
        if form.is_valid():
            if form.cleaned_data['type'] == 'i':
                form.instance.total = form.cleaned_data['total'] + form.cleaned_data['amount']
            else:
                form.instance.total = form.cleaned_data['total'] - form.cleaned_data['amount']
            form.save()
            return redirect('cash-control')
    return render(request, 'store/cash_control.html', context)


# Calendar views
@login_required(login_url='login')
def calendar(request):
    suppliers = Supplier.objects.filter(active=True).exclude(days='')
    days_data = dict()
    days_data['l'] = list()
    days_data['m'] = list()
    days_data['mi'] = list()
    days_data['j'] = list()
    days_data['v'] = list()
    days_data['s'] = list()
    days_data['d'] = list()
    for supplier in suppliers:
        days_list = ast.literal_eval(supplier.days)
        for day in days_list:
            days_data[day].append(supplier.name)
    context = {'days_data': days_data}
    return render(request, 'store/calendar.html', context)


# Statistics views
@staff_member_required
@login_required(login_url='login')
def st_time_parallel(request):
    form = StatisticsTimeParallel(request.POST or None)
    context = {'form': form}
    if request.method == 'POST':
        if form.is_valid():
            data1 = get_billing_data(request.POST.get('date_from_1'), request.POST.get('date_to_1'))
            data2 = get_billing_data(request.POST.get('date_from_2'), request.POST.get('date_to_2'))
            context['data1'] = data1
            context['data2'] = data2
            context['chart_labels'] = ['Vendido 1', 'Vendido 2', 'de Lista 1', 'de Lista 2',
                                       'por Tarjeta 1', 'por Tarjeta 2', 'Fiado 1', 'Fiado 2']
            context['chart_data'] = [data1['total'], data2['total'], data1['list_total'],
                                     data2['list_total'], data1['by_card_total'], data2['by_card_total'],
                                     data1['by_trust_total'], data2['by_trust_total']]
            if data1['total'] == 0 and data1['total']:
                context['message'] = "No hay ventas registradas en ninguno de los periodos."
            elif data1['total'] == 0 or data2['total'] == 0:
                context['message'] = "No hay ventas registradas en uno de los periodos."
            elif data1['total'] >= data2['total']:
                aux = round(data1['total']/data2['total']*100, 2)
                context['message'] = f"El periodo 1 vendió un {aux}% en comparación al periodo 2."
            else:
                aux = round(data2['total'] / data1['total']*100, 2)
                context['message'] = f"El periodo 2 vendió un {aux}% en comparación al periodo 1."
            return render(request, 'store/statistics_time_parallel.html', context)
    return render(request, 'store/statistics_time_parallel.html', context)


@staff_member_required
@login_required(login_url='login')
def st_best_day(request):
    form = StatisticsBestDay(request.POST or None)
    context = {'form': form}
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            data = get_best_day(request.POST.get('date_from'), request.POST.get('date_to'))
            chart_labels = []
            chart_data = []
            for row in data:
                chart_labels.append(row['created_date'].strftime('%d/%m/%y'))
                chart_data.append(row['day_total'])
            context['chart_labels'] = chart_labels
            context['chart_data'] = chart_data
            context['data'] = data
            return render(request, 'store/statistics_best_day.html', context)
    return render(request, 'store/statistics_best_day.html', context)


@staff_member_required
@login_required(login_url='login')
def st_best_product(request):
    form = StatisticsBestDay(request.POST or None)
    context = {'form': form}
    data = dict()
    if request.method == 'POST':
        if form.is_valid():
            data = get_best_product(request.POST.get('date_from'), request.POST.get('date_to'))
            chart_labels = []
            chart_data = []
            for row in data:
                chart_labels.append(row['name'])
                chart_data.append(row['product_count'])
            context['chart_labels'] = chart_labels
            context['chart_data'] = chart_data
            context['data'] = data
            return render(request, 'store/statistics_best_product.html', context)
    return render(request, 'store/statistics_best_product.html', context)


def get_best_day(date_from, date_to):
    orders = Order.objects\
        .filter(created_date__range=[date_from, date_to])\
        .values('created_date')\
        .annotate(day_total=Sum('total'), day_list_total=Sum('list_total'), day_count=Count('created_date'))\
        .order_by('-day_total')[:10]
    data = orders
    return data


def get_best_product(date_from, date_to):
    products = OrderProduct.objects\
        .filter(order__created_date__range=[date_from, date_to])\
        .values('product',)\
        .annotate(product_count=Sum('quantity'))\
        .order_by('-product_count')[:10]
    for item in products:
        item['name'] = Product.objects.get(id=item['product']).name
        item['supplier'] = Product.objects.get(id=item['product']).supplier.name
    data = products
    return data
