from django.db import models
from django.contrib.auth.models import User
import pandas as pd



data = pd.read_csv('Home/pincode.csv')
array = data.values
pincode=[]
for i in array:
    dataval=[]
    dataval.append(i[-1])
    dataval.append(i[-1])
    val = tuple(dataval)
    pincode.append(val)

pincode.sort()
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255,null=True,blank=True)
    pincode = models.CharField(max_length=255,null=True,blank=True)
    place = models.CharField(max_length=255,null=True,blank=True)
    district = models.CharField(max_length=255,null=True,blank=True)
    state = models.CharField(max_length=255,null = True,blank=True)
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.FileField(upload_to='product_image')
    merchant = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    
class ProfileData(models.Model):
    name = models.CharField(max_length=20)
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    pincode = models.IntegerField()
    House = models.CharField(max_length=20)
    district = models.CharField(max_length=20,null=True,blank=True)
    city = models.CharField(max_length=20,null=True,blank=True)
    place = models.CharField(max_length=20,null=True,blank=True)
    phone = models.CharField(max_length=20,null=True,blank=True)
    state = models.CharField(max_length=20,null=True,blank=True)
    
     
