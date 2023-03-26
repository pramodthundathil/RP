from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product
from django.forms import ModelForm,TextInput

class UserAddForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name","email","username","password1","password2"]
        
class ProductAddForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name","price","stock","category","image"]
        
    widgets = {
        "pincode": TextInput(attrs={"list":"items"})
    }