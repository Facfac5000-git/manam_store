from django.db import models
import datetime

from users.models import User


class Buyer(models.Model):
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    phone_number = models.CharField(max_length=30)
    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=220)
    phone_number = models.CharField(max_length=30)
    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    days = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=13, unique=True)
    name = models.CharField(max_length=120, unique=True)
    list_price = models.FloatField()
    profit_porc = models.FloatField()
    rounding = models.FloatField()
    price = models.FloatField()
    stock = models.PositiveIntegerField()
    stock_alert = models.PositiveIntegerField()
    expire_date = models.DateField()
    created_date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    total = models.FloatField()
    list_total = models.FloatField()
    by_trust = models.BooleanField()
    to_trust = models.ForeignKey(Buyer, null=True, on_delete=models.CASCADE)
    by_card = models.BooleanField()
    created_date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Order'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()

    def __str__(self):
        return self.product.name


class CashMovement(models.Model):
    date = models.DateField()
    detail = models.TextField(max_length=500)
    amount = models.FloatField()
    type = models.CharField(max_length=10)
    total = models.FloatField()

    def __str__(self):
        return self.detail
