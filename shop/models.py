from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
    ]
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='product_images/', default='product_images/default.jpg')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='men')
    description = models.TextField(blank=True)
    def __str__(self):
        return f"{self.name} ({self.gender})"
# Product Model
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True) 
    quantity = models.IntegerField(null=False,blank=False)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    is_trending = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/', default='product_images/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    brand = models.CharField(max_length=100, blank=True) 
    

    @property
    def subtotal(self):
        return self.product.price * self.product_qty
    


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlists')

    def __str__(self):
        return f"{self.user.username}'s Wishlist"