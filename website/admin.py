from django.contrib import admin
from .models import Product,Customer,Cart,Order
# Register your models here.
admin.site.register(Product)
admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(Order)