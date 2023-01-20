from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    def __str__(self) -> str:
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class Product(models.Model):

    GEN_M = 'M'
    GEN_F = 'F'

    GEN = [
        (GEN_M,'Male'),
        (GEN_F,'Female')
        ]

    name = models.CharField(max_length=200,null=True)
    price = models.DecimalField(max_digits=8,decimal_places=2)
    description = models.TextField()
    size = models.CharField(max_length=2,blank=True,null=True)
    gender = models.CharField(max_length=1,choices=GEN)
    category= models.ForeignKey(Category,on_delete=models.PROTECT)
    brand= models.ForeignKey(Brand,on_delete=models.PROTECT)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url=''
        return url    
        

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_order = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False,null=True,blank=False)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)


        

    @property
    def get_cart_total(self):
        order_items = self.orderitem_set.all()
        total = sum([item.get_total for item in order_items])
        return total
    @property
    def get_cart_items(self):
        order_items = self.orderitem_set.all()
        total = sum([item.qtd for item in order_items])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    qtd = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.qtd
        return total
    
class ShippingAdress(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address = models.CharField(max_length=200,null=True)
    city = models.CharField(max_length=200,null=True)
    state = models.CharField(max_length=200,null=True)
    country = models.CharField(max_length=200,null=True)
    zip_code = models.CharField(max_length=200,null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.address

