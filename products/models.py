from email.mime import image
from typing import final
from django.db import models
from django.forms import DateTimeField
from shopapp.models import Account, Address
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200,  db_index=True,null=True, blank=True, verbose_name='name')
    slug = models.SlugField(max_length=200, unique=True, db_index=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'category'

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('product_category', args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=100, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=200, db_index=True)
    price = models.FloatField()
    image = models.ImageField(upload_to="image/product")
    image1 = models.ImageField(upload_to="image/product")
    image2 = models.ImageField(upload_to="image/product")
    description = models.TextField(max_length=1000)
    status = models.BooleanField(default=False,help_text="0=default,1=trending")
    available = models.BooleanField(default=True, verbose_name="available")
    stock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['name']
        index_together = [
            ['id', 'slug']
        ]
        verbose_name = 'item'
        verbose_name_plural = 'item'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:ProductDetail', args=[self.id, self.slug])
    


class OrderItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"{self.quantity} - {self.product.name}"

    def get_total_price(self):
        return  self.quantity * self.product.price

    def get_final_price(self):
        return self.get_total_price()


class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name


class Order(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    full_name        =  models.CharField(max_length=100)
    address   =  models.TextField(max_length=100)
    city             =  models.CharField(max_length=100)
    pin_code         =  models.CharField(max_length=10)
    state            =  models.CharField(max_length=50)
    country          =  models.CharField(max_length=50)
    mobile           =  models.CharField(max_length=15)
    landmark         =  models.CharField(max_length=50)
    total_price = models.FloatField(null=False)
    is_paid = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=100,null=False)
    payment_id = models.CharField(max_length=250,null=True)
    order_status = (
        ('pending', 'pending'),
        ('packed', 'packed'),
        ('shipped','shipped'),
        ('delivered','delivered'),
        ('canceled','canceled'),
    )
    status = models.CharField(max_length=150,choices=order_status , default='pending')
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=150,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return (self.tracking_no)


class Myorder(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    price = models.FloatField(null=False)
    quantity = models.IntegerField(null=False)

    def __str__(self):
        return ( self.order.tracking_no)
    
    def order_state(self):
        return ( self.order.status)
  

    


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200, blank=True)
    review = models.TextField(null=True, blank=True)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
