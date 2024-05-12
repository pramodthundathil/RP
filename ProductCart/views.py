from django.shortcuts import render,redirect
from django.contrib import messages
from Home.models import Product,ProfileData
from .models import CartItems,CheckOuts
from django.contrib.auth.decorators import login_required
import json
import pandas as pd
import requests
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest

response1 = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=32d8341ec1da4e57aba06d2b9b004c50")
# print(response1.status_code)
# print(response1.content)
razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


def Products(request):
    response1 = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=32d8341ec1da4e57aba06d2b9b004c50")
    
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
        "item_product":item_product,
        "district":district
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
    response1 = requests.get("https://ipgeolocation.abstractapi.com/v1/?api_key=32d8341ec1da4e57aba06d2b9b004c50")
    
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
    
@login_required(login_url="SignIn")
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
    currency = 'INR'
    amount = total * 100 # Rs. 200
    

  # Create a Razorpay Order Pyament Integration.....
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                          currency=currency,
                          payment_capture='0'))

  # order id of newly created order.
    razorpay_order_id = razorpay_order["id"]
    callback_url = 'paymenthandlercus'

  # we need to pass these details to frontend.
    
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    context['slotid'] = ckout.id,
    # context['amt'] = (product1.Product_price)*float(qty)
       
    return render(request,"Makepayment.html",context)

@csrf_exempt
def paymenthandlercus(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

      # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                amount = 800 * 100 # Rs. 200
                try:
                    print("working 1")
                    razorpay_client.payment.capture(payment_id, amount)
                    return redirect('Success1')
          # render success page on successful caputre of payment
                except:
                    print("working 2")
                    return redirect('Success1')
                    
                    
          # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')
        # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
        
      # if we don't find the required parameters in POST data
    else:
  # if other than POST request is made.
        return HttpResponseBadRequest()
    
def Success1(request):
    return render(request,'Paymentconfirm.html')
        
        
@login_required(login_url="SignIn")
def Myorders(request):
    order = CheckOuts.objects.filter(user = request.user)
    context = {
        'order':order
    }
    return render(request,"myorders.html",context)

@login_required(login_url="SignIn")
def deleteorderedhistory(request,pk):
    CheckOuts.objects.get(id = pk).delete()
    messages.info(request,"Product Deleted")
    return redirect("Myorders")

@login_required(login_url="SignIn")
def Customerorders(request):
    order = CheckOuts.objects.filter(Product__merchant = request.user)
    hub_profile = ProfileData.objects.all()
    context = {
        "order":order,
        "hub_profile":hub_profile
    }
    return render(request,"customerorder.html",context)

@login_required(login_url="SignIn")
def AssignToHub(request,pk):
    cheout = CheckOuts.objects.get(id = pk)
    if request.method == "POST":
        hub = ProfileData.objects.get(id = int(request.POST['hub']))
        cheout.hub = hub 
        cheout.save()
        messages.info(request,"Hub assigened......")
        return redirect("Customerorders")
    return redirect("Customerorders")

@login_required(login_url="SignIn")
def ChangeToDespached(request,pk):
    order = CheckOuts.objects.get(id = pk)
    order.status = "Item Despached"
    order.save()
    return redirect("CustomerordersHub")

@login_required(login_url="SignIn")
def ChangeToAccepetd(request,pk):
    order = CheckOuts.objects.get(id = pk)
    order.status = "Item Accepted By Hub"
    order.save()
    return redirect("CustomerordersHub")

@login_required(login_url="SignIn")
def ChangeToReceivedByHub(request,pk):
    order = CheckOuts.objects.get(id = pk)
    order.status = "Item Received on Hub"
    order.save()
    return redirect("CustomerordersHub")

@login_required(login_url="SignIn")
def ChangeToDelivered(request,pk):
    order = CheckOuts.objects.get(id = pk)
    order.status = "Item Delivered"
    order.save()
    return redirect("CustomerordersHub")

@login_required(login_url="SignIn")
def ChangeToCanceled(request,pk):
    order = CheckOuts.objects.get(id = pk)
    order.status = "Order Cancelled By Merchant"
    order.save()
    return redirect("Customerorders")

@login_required(login_url="SignIn")
def DelateOrderMerchant(request,pk):
    CheckOuts.objects.get(id = pk)
    messages.info(request,"Order Deleted")
    return redirect("Customerorders")

def ViewAddress(request,pk):
    ckout = CheckOuts.objects.get(id = pk)
    prodata = ProfileData.objects.get(user = ckout.user)
    context = {
        "prodata":prodata
    }
    return render(request,'customeraddress.html',context)


def CustomerordersHub(request):
    profile = ProfileData.objects.get(user = request.user)
    print(profile,"------------------------------------------")
    order = CheckOuts.objects.filter(hub = profile)
    hub_profile = ProfileData.objects.all()
    context = {
        "order":order,
        "hub_profile":hub_profile
    }
    return render(request,"customerordershub.html",context)