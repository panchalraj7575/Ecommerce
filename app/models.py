from django.db import models
from django.db.models import Model
from django.utils import timezone
# Create your models here.


class CustomerRegister(models.Model):
    Customer_id = models.AutoField(primary_key=True)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    Email = models.EmailField(max_length=100)
    Password = models.CharField(max_length=20)

    def __str__(self):
        return self.First_Name


class Category(models.Model):
    Category_id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class Product(models.Model):
    Product_id = models.AutoField(primary_key=True)
    Category_id = models.ForeignKey(
        Category, on_delete=models.CASCADE, default=1)
    Name = models.CharField(max_length=100)
    Price = models.IntegerField(default=0)
    Description = models.CharField(max_length=20)
    Image = models.ImageField(upload_to="uploads/products", default="")

    def __str__(self):
        return self.Name


class Order(models.Model):
    Order_id = models.AutoField(primary_key=True)
    Customer_id = models.ForeignKey(
        CustomerRegister, on_delete=models.SET_NULL, default=1, null=True)
    Date_ordered = models.DateTimeField(auto_now_add=True)

    Complete = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return str(self.Order_id)

    @property
    def get_cart_total(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitem])
        return total

    @property
    def get_cart_item(self):
        orderitem = self.orderitem_set.all()
        total = sum([item.Qty for item in orderitem])
        return total


class OrderItem(models.Model):
    OrderItem = models.AutoField(primary_key=True)
    Customer_id = models.ForeignKey(
        CustomerRegister, on_delete=models.SET_NULL, default=1, null=True)
    Order_id = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True)
    Product_id = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    Qty = models.IntegerField(default=0)
    Date_Added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.Product_id.Price * self.Qty
        return total


class ShippingAddress(models.Model):
    ShippingAddress_id = models.AutoField(primary_key=True)
    Customer_id = models.ForeignKey(
        CustomerRegister, on_delete=models.SET_NULL, default=1, null=True)
    OrderItem_id = models.ForeignKey(
        OrderItem, on_delete=models.SET_NULL, null=True)
    First_Name = models.CharField(max_length=100)
    Last_Name = models.CharField(max_length=100)
    num = models.EmailField(max_length=100)
    address = models.CharField(max_length=100)
    @property
    def get_total_after_checkout(self):
        total = 0
        return total