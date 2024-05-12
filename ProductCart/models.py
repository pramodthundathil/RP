from django.db import models
from Home.models import Product,ProfileData
from django.contrib.auth.models import User


# Create your models here.

class CartItems(models.Model):

    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    price = models.FloatField(null=True,blank=True)
    
class CheckOuts(models.Model):
    
    Product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    py_status = models.BooleanField(default=False)
    hub = models.ForeignKey(ProfileData,on_delete=models.SET_NULL,null=True, blank=True)
    
