from django.urls import path  
from .import views 

urlpatterns = [
    path("ProductSigleViewMerchant/<int:pk>",views.ProductSigleViewMerchant,name="ProductSigleViewMerchant"),
    path("DeleteProduct/<int:pk>",views.DeleteProduct,name="DeleteProduct"),
    path("ViewProduct/<int:pk>",views.ViewProduct,name="ViewProduct"),
    path("Cart",views.Cart,name="Cart"),
    path("AddTocart/<int:pk>",views.AddTocart,name="AddTocart"),
    path("IncreaseCartQunty/<int:pk>",views.IncreaseCartQunty,name="IncreaseCartQunty"),
    path("DecreaseCartQunty/<int:pk>",views.DecreaseCartQunty,name="DecreaseCartQunty"),
    path("DeleteCart/<int:pk>",views.DeleteCart,name="DeleteCart"),
    path("Products",views.Products,name="Products"),
    path("SearchProducts",views.SearchProducts,name="SearchProducts"),
    path("SearchByLocation",views.SearchByLocation,name="SearchByLocation"),
    path("searchBypincode",views.searchBypincode,name="searchBypincode"),
    path("SearchByDistrict",views.SearchByDistrict,name="SearchByDistrict"),
    path("CheckOut",views.CheckOut,name="CheckOut"),
    path("Myorders",views.Myorders,name="Myorders"),
    path("deleteorderedhistory/<int:pk>",views.deleteorderedhistory,name="deleteorderedhistory"),
    path("Customerorders",views.Customerorders,name="Customerorders"),
    path("ChangeToDespached/<int:pk>",views.ChangeToDespached,name="ChangeToDespached"),
    path("ChangeToAccepetd/<int:pk>",views.ChangeToAccepetd,name="ChangeToAccepetd"),
    path("ChangeToReceivedByHub/<int:pk>",views.ChangeToReceivedByHub,name="ChangeToReceivedByHub"),
    path("ChangeToDelivered/<int:pk>",views.ChangeToDelivered,name="ChangeToDelivered"),
    path("ChangeToCanceled/<int:pk>",views.ChangeToCanceled,name="ChangeToCanceled"),
    path("DelateOrderMerchant/<int:pk>",views.DelateOrderMerchant,name="DelateOrderMerchant"),
    path("ViewAddress/<int:pk>",views.ViewAddress,name="ViewAddress"),
    path("paymenthandlercus",views.paymenthandlercus,name="paymenthandlercus"),
    path("AssignToHub/<int:pk>",views.AssignToHub,name="AssignToHub"),
    path("CustomerordersHub",views.CustomerordersHub,name="CustomerordersHub"),
    
    
]
