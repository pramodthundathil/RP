from django.shortcuts import render,redirect
from django.contrib import messages
from Home.models import Product
from .models import CartItems,CheckOuts
from django.contrib.auth.decorators import login_required
import json
import pandas as pd
import requests

response1 = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=32d8341ec1da4e57aba06d2b9b004c50")
print(response1.status_code)
print(response1.content)



def Products(request):
    product = Product.objects.all()
    val = json.loads(response1.content)
    pincode = val["postal_code"]
    data = pd.read_csv('ProductCart/pincode.csv',sep = ",")
    array = data.values
    listdata = data[data["Pincode"] == int(pincode)]
    district = listdata.values[0][-3]
    item_product = Product.objects.filter(district__contains = district)
    context = {
        "product":product,
        "item_product":item_product
    }
    return render(request,"products.html",context)

def SearchProducts(request):
    if request.method == "POST":
        search = request.POST["search"]
        product = Product.objects.filter(name__contains = search)
        
        return render(request, "search.html",{"search":search,"product":product})
    else:
        return render(request, "search.html")
    
def SearchByLocation(request):
    val = json.loads(response1.content)
    return render(request,'searchbylocation.html',{"postal":val["postal_code"],"place":val["city"],"png":val['flag']["png"]})

def searchBypincode(request):
    
    if request.method == "POST":
        pincode = request.POST["pincode"]
        data = pd.read_csv('ProductCart/pincode.csv',sep = ",")
        array = data.values
        listdata = data[data["Pincode"] == int(pincode)]
        district = listdata.values[0][-3]
        product = Product.objects.filter(district__contains = district)
        return render(request, "search.html",{"search":pincode,"product":product})
    
    
def SearchByDistrict(request):
    if request.method == "POST":
        district = request.POST["city"]
        product = Product.objects.filter(district__contains = district)
        return render(request, "search.html",{"search":district,"product":product})
        
        
        
        
def ProductSigleViewMerchant(request,pk):
    product = Product.objects.get(id = pk)
    if request.method == "POST":
        pname = request.POST['pname']
        cat = request.POST['cat']
        price = request.POST['price']
        stock = request.POST['stock']
        img = request.FILES['img']
        
        product.name = pname
        product.category = cat
        product.price = float(price)
        product.stock = int(stock)
        product.image.delete()
        product.image = img
        product.save()
        messages.info(request,"Product Updated")
        return redirect("ProductSigleViewMerchant", pk = pk)
        
    context = {
        'product':product
    }
    return render(request,'productviewmerchant.html',context)


def DeleteProduct(request,pk):
    product = Product.objects.get(id = pk)
    product.image.delete()
    product.delete()
    messages.info(request,"Product Deleted")
    return redirect("Inventory")

def ViewProduct(request,pk):
    product = Product.objects.get(id= pk)
    context = {
        "product":product
    }
    return render(request,"productview.html",context)

@login_required(login_url="SignIn")
def AddTocart(request,pk):
    product = Product.objects.get(id = pk)
    if CartItems.objects.filter(product = product,user = request.user).exists():
        cart = CartItems.objects.get(product = product,user = request.user)
        cart.quantity = cart.quantity + 1
        cart.price = cart.price + cart.price
        cart.save()
    else:
        cart = CartItems.objects.create(product = product,quantity = 1,user = request.user,price = product.price)
        cart.save()
    return redirect("Cart")

@login_required(login_url="SignIn")
def Cart(request):
    cartitems = CartItems.objects.filter(user = request.user)
    price = 0
    for item in cartitems:
        price = price + item.price
    context = {
        'cart':cartitems,
        'cartlen':len(cartitems),
        'price':price
    }
    return render(request,"cart.html",context)

@login_required(login_url="SignIn")
def IncreaseCartQunty(request,pk):
    cart = CartItems.objects.get(id = pk)
    cart.quantity = cart.quantity + 1
    cart.price = cart.price + cart.product.price 
    cart.save()
    return redirect('Cart')

@login_required(login_url="SignIn")
def DecreaseCartQunty(request,pk):
    cart = CartItems.objects.get(id = pk)
    if cart.quantity == 1:
        cart.delete()
    else:
        cart.quantity = cart.quantity - 1
        cart.price = cart.price - cart.product.price 
        cart.save()
    return redirect('Cart')

@login_required(login_url="SignIn")
def DeleteCart(request,pk):
    CartItems.objects.get(id = pk).delete()
    return redirect('Cart')
    
def CheckOut(request):
    cart = CartItems.objects.filter(user = request.user)
    total = 0
    for items in cart:
        ckout = CheckOuts.objects.create(Product = items.product,quantity = items.quantity,price = items.price,user = request.user, status = "Item Ordered")
        ckout.save()
        total = total + float(items.price)
        items.delete()
    
    context = {
        
        "total":total
    }   
    return render(request,"Makepayment.html",context)
    
    
def Myorders(request):
    order = CheckOuts.objects.filter(user = request.user)
    context = {
        'order':order
    }
    return render(request,"myorders.html",context)

def deleteorderedhistory(request,pk):
    CheckOuts.objects.get(id = pk).delete()
    messages.info(request,"Product Deleted")
    return redirect("Myorders")

def Customerorders(request):
    order = CheckOuts.objects.all()
    context = {
        "order":order
    }
    return render(request,"customerorder.html",context)