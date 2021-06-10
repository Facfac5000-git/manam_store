from django import forms

from .models import Buyer, Supplier, Product, Order, OrderProduct, CashMovement


class BuyerForm(forms.ModelForm):
    class Meta:
        model = Buyer
        fields = ['name', 'address', 'phone_number']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'data-val': 'true',
                'data-val-required': 'Ingresa un nombre',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'address',
                'data-val': 'true',
                'data-val-required': 'Ingresa una dirección',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'phone_number',
                'data-val': 'true',
                'data-val-required': 'Ingresa un número de télefono',
            }),
        }

        error_messages = {
            'name': {
                'required': 'Este campo Nombre es requerido.',
                'unique': 'Ya se encuentra cargado un comprador con este nombre.'
            },
            'address': {
                'required': 'El campo Dirección es requerido.'
            },
            'phone_number': {
                'required': 'El campo Número de Teléfono es requerido.'
            }
        }


class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'address', 'phone_number', 'days']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'data-val': 'true',
                'data-val-required': 'Ingresa un nombre',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'address',
                'data-val': 'true',
                'data-val-required': 'Ingresa una dirección',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'phone_number',
                'data-val': 'true',
                'data-val-required': 'Ingresa un número de télefono',
            }),
            'days': forms.CheckboxSelectMultiple(attrs={
                'id': 'days'
            }, choices=(('l', 'Lunes'),
                        ('m', 'Martes'),
                        ('mi', 'Miércoles'),
                        ('j', 'Jueves'),
                        ('v', 'Viernes'),
                        ('s', 'Sábado'),
                        ('d', 'Domingo')))
        }

        error_messages = {
            'name': {
                'required': 'Este campo Nombre es requerido.',
                'unique': 'Ya se encuentra cargado un proveedor con este nombre.'
            },
            'address': {
                'required': 'El campo Dirección es requerido.'
            },
            'phone_number': {
                'required': 'El campo Número de Teléfono es requerido.'
            }
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['supplier', 'barcode', 'name', 'price', 'profit_porc', 'rounding', 'list_price', 'stock', 'stock_alert', 'expire_date']

        widgets = {
            'supplier': forms.Select(attrs={
                'class': 'form-control', 'id': 'supplier', 'required': 'true', 'value': 1
            }),
            'barcode': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'barcode', 'minlength': '13', 'maxlength': '13', 'required': 'true'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'name', 'required': 'true'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'price', 'min': 0, 'required': 'true', 'readonly': 'true'
            }),
            'list_price': forms.NumberInput(attrs={
                'class': 'form-control make_total', 'id': 'list_price', 'min': 0, 'required': 'true'
            }),
            'profit_porc': forms.NumberInput(attrs={
                'class': 'form-control make_total', 'id': 'profit_porc', 'min': 0, 'required': 'true', 'value': 0
            }),
            'rounding': forms.NumberInput(attrs={
                'class': 'form-control make_total', 'id': 'rounding', 'min': 0, 'required': 'true', 'value': 0
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'stock', 'min': 0, 'required': 'true'
            }),
            'stock_alert': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'alert_stock', 'min': 0, 'required': 'true'
            }),
            'expire_date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control', 'id': 'expire_date', 'required': 'true'
            })
        }

        error_messages = {
            'supplier': {
                'required': 'El proveedor es un campo requerido.'
            },
            'barcode': {
                'required': 'El campo Código de Barras es requerido.',
                'unique': 'Ya se encuentra cargado un producto con este Código de Barras.'
            },
            'name': {
                'required': 'El campo Nombre es requerido.'
            },
            'price': {
                'required': 'El campo Precio de Venta es requerido.'
            },
            'list_price': {
                'required': 'El campo Precio de Lista es requerido.'
            },
            'profit_porc': {
                'required': 'El campo Porcentaje es requerido.'
            },
            'rounding': {
                'required': 'El campo Redondeo es requerido.'
            },
            'stock': {
                'required': 'El campo Stock es requerido.'
            },
            'stock_alert': {
                'required': 'El campo Alerta de Stock es requerido.'
            },
            'expire_date': {
                'required': 'El campo Fecha de Expiración es requerido.'
            },
        }


class OrderForm(forms.ModelForm):
    barcode_0 = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control add_new_product', 'id': 'barcode_0', 'maxlength': '13'
            }))
    product_0 = forms.CharField(required=False, widget=forms.Select(attrs={
                'class': 'form-control product-control', 'id': 'product_0'
            }))
    quantity_0 = forms.CharField(required=False, widget=forms.NumberInput(attrs={
                'class': 'form-control quantity-control', 'id': 'quantity_0', 'value': 1, 'min': 0, 'step': 1
            }))
    price_0 = forms.CharField(required=False, widget=forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'price_0', 'min': 0, 'value': 0, 'readonly': 'true'
            }))
    unit_price_0 = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control d-none', 'id': f'unit_price_0', 'min': 0, 'value': 0, 'readonly': 'true'
    }))
    list_price_0 = forms.CharField(required=False, widget=forms.NumberInput(attrs={
        'class': 'form-control d-none', 'id': f'list_price_0', 'min': 0, 'value': 0, 'readonly': 'true'
    }))
    to_trust = forms.CharField(required=False, widget=forms.Select(attrs={
                'class': 'form-control', 'id': 'to_trust', 'disabled': True
            }))

    def __init__(self, *args, **kwargs):
        extra = kwargs.pop('extra')
        super(OrderForm, self).__init__(*args, **kwargs)

        PRODUCT_CHOICES = list()
        product_choices = Product.objects.all().filter(stock__gte='1').filter(active=True).order_by('id')
        PRODUCT_CHOICES.append((0, '-----'))
        for choice in product_choices:
            PRODUCT_CHOICES.append((choice.id, choice.name))
        PRODUCT_CHOICES = tuple(PRODUCT_CHOICES)

        self.fields['product_0'].widget.choices = PRODUCT_CHOICES

        BUYER_CHOICES = list()
        buyer_choices = Buyer.objects.all().filter(active=True).order_by('id')
        BUYER_CHOICES.append((0, '-----'))
        for choice in buyer_choices:
            BUYER_CHOICES.append((choice.id, choice.name))
        BUYER_CHOICES = tuple(BUYER_CHOICES)

        self.fields['to_trust'].widget.choices = BUYER_CHOICES

        for i in range(extra):
            barcode = f'barcode_{i+1}'
            self.fields[barcode] = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control add_new_product', 'id': f'barcode_{i+1}', 'maxlength': '13',
            }))
            product = f'product_{i+1}'
            self.fields[product] = forms.CharField(required=False, widget=forms.Select(attrs={
                'class': 'form-control', 'id': f'product_{i+1}'
            }, choices=PRODUCT_CHOICES))
            quantity = f'quantity_{i+1}'
            self.fields[quantity] = forms.CharField(required=False, widget=forms.NumberInput(attrs={
                'class': 'form-control quantity-control', 'id': f'quantity_{i+1}', 'value': 1, 'min': 0, 'step': 1
            }))
            price = f'price_{i+1}'
            self.fields[price] = forms.CharField(required=False, widget=forms.NumberInput(attrs={
                'class': 'form-control', 'id': f'price_{i+1}', 'min': 0, 'value': 0, 'readonly': 'true'
            }))
            unit_price = f'unit_price_{i+1}'
            self.fields[unit_price] = forms.CharField(required=False, widget=forms.NumberInput(attrs={
                'class': 'form-control d-none', 'id': f'unit_price_{i+1}', 'min': 0, 'value': 0, 'readonly': 'true'
            }))
            list_price = f'list_price_{i+1}'
            self.fields[list_price] = forms.CharField(required=False, widget=forms.NumberInput(attrs={
                'class': 'form-control d-none', 'id': f'list_price_{i+1}', 'min': 0, 'value': 0, 'readonly': 'true'
            }))

    def clean(self):
        products = dict()
        i = 0
        product_field = f'product_{i}'
        quantity_field = f'quantity_{i}'
        price_field = f'price_{i}'
        while self.cleaned_data.get(product_field) and self.cleaned_data.get(quantity_field) and self.cleaned_data.get(price_field):
            product = self.cleaned_data[product_field]
            quantity = self.cleaned_data[quantity_field]
            price = self.cleaned_data[price_field]
            already_there = 0
            for item in products.values():
                if product == item['product']:
                    already_there = 1
                    item['quantity'] = int(item['quantity']) + int(quantity)
                    item['price'] = int(item['price']) + int(price)
            if already_there != 1:
                products[i] = {'product': product, 'quantity': quantity, 'price': price}
            i += 1
            product_field = f'product_{i}'
            quantity_field = f'quantity_{i}'
            price_field = f'price_{i}'
        self.cleaned_data['products'] = products

    def save(self, user):
        order = self.instance
        if order.total != 0:
            order.user = user
            order.total = self.cleaned_data['total']
            order.list_total = self.cleaned_data['list_total']
            if self.cleaned_data['to_trust']:
                order.to_trust = Buyer.objects.get(id=self.cleaned_data['to_trust'])
            order.save()
            for item in self.cleaned_data['products'].values():
                if item['product'] != '0' and item['quantity'] != '0':
                    product = Product.objects.get(id=item['product'])
                    product.stock = product.stock - int(item['quantity'])
                    product.save()
                    OrderProduct.objects.create(
                        order=order,
                        product=product,
                        quantity=item['quantity'],
                        price=item['price']
                    )

    def get_choices(self):
        product_list = list()
        product_choices = Product.objects.all().filter(stock__gte='1').filter(active=True).order_by('id')
        product_list.append((0, '-----'))
        for choice in product_choices:
            product_list.append((choice.id, choice.name))
        product_tuple = tuple(product_list)
        return product_tuple

    def get_product_fields(self):
        count = 0
        for field_name in self.fields:
            if field_name.startswith('product_'):
                count = count+1
        return range(count)



    class Meta:
        model = Order
        fields = [
            'total', 'list_total', 'by_card', 'by_trust'
        ]

        widgets = {
            'total': forms.NumberInput(attrs={
                'class': 'form-control', 'readonly': 'true', 'id': 'total', 'value': 0, 'required': 'true'
            }),
            'list_total': forms.NumberInput(attrs={
                'class': 'form-control d-none', 'readonly': 'true', 'id': 'list_total', 'value': 0, 'required': 'true'
            }),
            'by_card': forms.CheckboxInput(attrs={
                'class': 'form-control', 'id': 'by_card'
            }),
            'by_trust': forms.CheckboxInput(attrs={
                'class': 'form-control', 'id': 'by_trust'
            })
        }


class BillingForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control', 'id': 'date_from', 'required': 'true'
    }))
    date_to = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control', 'id': 'date_to', 'required': 'true'
    }))


class CashMovementForm(forms.ModelForm):
    class Meta:
        model = CashMovement
        fields = ['date', 'detail', 'amount', 'type', 'total']

        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date', 'class': 'form-control', 'id': 'date', 'required': 'true'
            }),
            'detail': forms.TextInput(attrs={
                'class': 'form-control', 'id': 'detail', 'required': 'true'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control cash_total_control', 'id': 'amount', 'min': 0, 'required': 'true'
            }),
            'type': forms.Select(attrs={
                'class': 'form-control', 'id': 'type'
            }, choices=(('i', 'Ingreso'), ('e', 'Egreso'))),
            'total': forms.NumberInput(attrs={
                'class': 'form-control', 'id': 'cash_total', 'required': 'true', 'readonly': 'true'
            })
        }

        error_messages = {
            'date': {
                'required': 'El campo Fecha es requerido.'
            },
            'detail': {
                'required': 'El campo Detalle es requerido.'
            },
            'amount': {
                'required': 'El campo Monto es requerido.'
            },
            'type': {
                'required': 'Debe seleccionar un tipo de movimiento.'
            },
            'total': {
                'required': 'El campo Total es requerido.'
            },
        }


class StatisticsTimeParallel(forms.Form):
    date_from_1 = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control', 'id': 'date_from_1', 'required': 'true'
    }))
    date_to_1 = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control', 'id': 'date_to_1', 'required': 'true'
    }))
    date_from_2 = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control', 'id': 'date_from_2', 'required': 'true'
    }))
    date_to_2 = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control', 'id': 'date_to_2', 'required': 'true'
    }))


class StatisticsBestDay(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control', 'id': 'date_from', 'required': 'true'
    }))
    date_to = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control', 'id': 'date_to', 'required': 'true'
    }))


class StatisticsBestProduct(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control', 'id': 'date_from', 'required': 'true'
    }))
    date_to = forms.DateField(widget=forms.DateInput(attrs={
        'type': 'date', 'class': 'form-control', 'id': 'date_to', 'required': 'true'
    }))
