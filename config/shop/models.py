from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120,unique=True)
    is_active = models.BooleanField(default = True)
    def __str__(self):
        return f"{self.name}"
class Product(models.Model):
    category = models.ForeignKey(to=Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120,unique=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.name}'
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Cart for {self.user}"

class CartItem(models.Model):
    cart = models.ForeignKey(to=Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(to=Product,on_delete=models.CASCADE,related_name='in_cart_items')
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"ID:{self.cart} for {self.product}"
class Order(models.Model):
    class Status(models.TextChoices):
            NEW = 'NEW', 'New'
            PAID = 'PAID', 'Paid'
            CANCELLED = 'CANCELLED', 'Cancelled'


    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 10,choices=Status.choices,default=Status.NEW)
    def __str__(self):
        return f"Order for {self.user}"
class OrderItem(models.Model):
    order = models.ForeignKey(to=Order,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(to=Product,on_delete=models.CASCADE,related_name='in_order_items')
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    def __str__(self):
        return f"ID:{self.order} for {self.product} price is {self.quantity * self.price}"
