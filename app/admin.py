from django.contrib import admin
from . models import CustomerRegister, Product, Category, Order, OrderItem,ShippingAddress
# Register your models here.


class AdminProduct(admin.ModelAdmin):
    list_display = ['Name', 'Price', 'Category_id']


admin.site.register(CustomerRegister)
admin.site.register(Product, AdminProduct)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
