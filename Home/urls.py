from django.urls import path  
from .import views

urlpatterns = [
    path("",views.Index,name="Index"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignIn",views.SignIn,name="SignIn"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("MerchantIndex",views.MerchantIndex,name="MerchantIndex"),
    path("Inventory",views.Inventory,name="Inventory"),
    path("Profile",views.Profile,name="Profile")
]
