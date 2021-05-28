from django.db import models
from django.db.models.expressions import F
from shop.models import Products
from accounts.models import User

# Create your models here.

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.product.Product_Name}'
    
    def get_total_item_price(self):
        return self.quantity * self.product.Price


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_Address = models.ForeignKey('BillingAddress', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.first_name

    def get_total(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()
        return total

    def gst_price(self):
        total = 0
        for i in self.item.all():
            total += i.get_total_item_price()
        gst_amount = (total * 12)/100
        gst = total + gst_amount
        return int(gst)



class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=50)
    Apartment_Address = models.CharField(max_length=50)
    Country = models.CharField(max_length=20)
    State = models.CharField(max_length=30)
    Pin_Code = models.CharField(max_length=6)
    Mobile_No = models.CharField(max_length=10)
    E_mail = models.EmailField()
    same_shiping_address = models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name
