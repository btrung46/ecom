from django.db import models
from django.contrib.auth.models import User
# Create your models here.
CATEGORY_CHOICES=(
    ('CR','Curd'),
    ('ML','Milk'),
    ('LS','lassi'),
    ('MS',',milkshake'),
)
class Product(models.Model):
    title = models.CharField(max_length = 100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices = CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')

    def __str__(self):
        return self.title
    
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)
    city = models.CharField(max_length = 200)
    mobile = models.IntegerField(default = 0)
    zipcode =  models.IntegerField()
    address = models.CharField(max_length = 255)
    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    quantity = models.PositiveBigIntegerField(default= 1)
     
    @property
    #cho phép truy cập như thuộc tính của 1 mô hình mà k cần dấu ngoặc đơn
    def total_cost(self):
        return self.quantity*self.product.discounted_price
    def __str__(self):
        return self.product.title
    
    
    
STATUS_CHOICE = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
    ('Pending','Pending'),
)
   
class Order(models.Model):
     user = models.ForeignKey(User, on_delete = models.CASCADE)
     customer = models.ForeignKey(Customer,on_delete = models.CASCADE)
     product = models.ForeignKey(Product,on_delete = models.CASCADE)
     quantity = models.PositiveBigIntegerField(default= 1)
     ordered_date = models.DateTimeField(auto_now_add = True)
     status = models.CharField(max_length= 100, choices = STATUS_CHOICE, default = 'Pending')
     @property
     def total_cost(self):
        return self.quantity*self.product.discounted_price
     def __str__(self):
        return self.product.title
    
