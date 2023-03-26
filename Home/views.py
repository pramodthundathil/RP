from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User,Group
from .forms import UserAddForm,ProductAddForm 
from .decorators import Admin_Only
import pandas as pd
from .models import Product,ProfileData



@Admin_Only
def Index(request):
    product = Product.objects.all()
    context = {
        "product":product
    }
    return render(request,"index.html",context)

def MerchantIndex(request):
    return render(request,'merchant_Index.html')

def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request,'User Registered Successfully')
            return redirect('SignIn')
    return render(request,"register.html",{"form":form})

def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('Index')
        else:
            messages.info(request,"Username or password incorrect")
            return redirect('SignIn')
    return render(request,"login.html")

def SignOut(request):
    logout(request)
    return redirect('Index')



# inventory Managemnet--------------------------------------------


def Inventory(request):
    form = ProductAddForm()
    products = Product.objects.all()
    import pandas as pd
    
    data = pd.read_csv('Home/pincode.csv')
    array = data.values
    pincode=[]
    for i in array:
        pincode.append(i[-1])
    pincode.sort()
     
    if request.method == "POST":
        form = ProductAddForm(request.POST,request.FILES)
        pinc = request.POST['pin']
        x = None
        for area in array:
            if str(area[-1]) == str(pinc):
                x = area
                break
        if x is None:
            messages.info(request,"Pincode Not Found Product Not Added")
            return redirect('Inventory') 
        if form.is_valid():
            product = form.save()
            product.save()
            product.pincode = pinc
            product.place = x[0] +" "+ x[1]
            product.district = x[2]
            product.state = x[3]
            product.merchant = request.user
            product.save()
            messages.info(request,"Product Saved {}".format(x))
            return redirect('Inventory')
            
        return redirect('Inventory')
               
    context = {
        "form":form,
        "pincode":pincode,
        "products":products
    }
    return render(request,'inventory.html',context)

def Profile(request):
    try:
        prodata = ProfileData.objects.get(user = request.user)
    except:
        prodata = None
        pass
    data = pd.read_csv('Home/pincode.csv')
    pincode = []
    for i in data.values:
        pincode.append(i[-1])
    pincode.sort()
    if request.method == "POST":
        name = request.POST['name']
        house = request.POST['house']
        phone = request.POST["phone"]
        pin = request.POST['pin']
        
        try:
            listdata = data[data["Pincode"] == int(pin)]
            district = listdata.values[0][-3]
            city = listdata.values[0][1]
            place = listdata.values[0][0]
            state = listdata.values[0][-2]
        except:
            messages.info(request,"Invalid pincode")
            return redirect("Profile")
            
        
        if ProfileData.objects.filter(user = request.user).exists():
            pdata = ProfileData.objects.get(user = request.user)
            pdata.name = name
            pdata.pincode = pin 
            pdata.House = house
            pdata.district = district
            pdata.city = city
            pdata.place = place
            pdata.phone = phone
            pdata.state = state
            pdata.save()
            return redirect("Profile")
            
        else:
            pdata = ProfileData.objects.create(name = name,pincode = pin,House = house,district = district,place = place,phone = phone,state = state,user = request.user)
            pdata.save()
            return redirect("Profile")
    context = {
        "pincode":pincode,
        "prodata":prodata
    }
    return render(request,'profile.html',context)

