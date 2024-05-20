from datetime import *
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager
from django.utils import timezone
# Create your models here.

class Category(models.Model):
    '''this model generate category and add in to database'''
    c_name = models.CharField(max_length = 50)
    def __str__(self):
        return self.c_name
    


class Products(models.Model):
    '''for ading products in existing category in Db.'''
    product_id = models.AutoField
    product_name = models.CharField(max_length = 50)
    c_name = models.ForeignKey(Category, on_delete = models.CASCADE, null = True,blank = True)
    price = models.IntegerField(blank = True, null=True)
    details = models.CharField(max_length = 200)
    img = models.ImageField(upload_to='uploads/')
    
    
    def __str__(self):
        return self.product_name
    
    
class CustomUser(AbstractBaseUser,PermissionsMixin):
    '''creatingb new user with email requirement'''
    email = models.EmailField(_("email"), unique = True)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True)
    date_joined = models.DateTimeField(default = timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
       
    objects = CustomUserManager()
      
    def __str__(self):
        return self.email
    
    
class Cart(models.Model):
    '''adding products and quantity of products on user cart'''
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    product = models.ForeignKey(Products, on_delete= models.CASCADE)
    quantity = models.IntegerField(default = 1) 
    date_added = models.DateTimeField(auto_now_add=True, null = True,blank=True)
    
    def __str__(self):
        return f"{self.user} {self.product.product_name} {self.quantity}"
    
    def get_absolute_url(self):
        return reverse('cart_detail')
    
    
class Contact(models.Model):
    '''this model takes client info and question and store that entry in databse.'''
    messeage_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=12)
    inquiry = models.CharField(max_length= 300)
    
    def __str__(self):
        return self.name
    
    
    
class CheckoutDetails(models.Model):
    '''this model store customer details for shipping order and '''
    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email_address = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)
    address = models.TextField(max_length=500)  
    date_added = models.DateTimeField(auto_now_add=True, null = True,blank=True)  
    
    def __str__(self):
        return self.full_name
    
    
    
class Invoice(models.Model):
    ud = models.ForeignKey(Cart, on_delete = models.CASCADE)
    cd = models.ForeignKey(CheckoutDetails, on_delete = models.CASCADE)



class CartItems(models.Model):
    pass
    