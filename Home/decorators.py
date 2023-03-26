from django.shortcuts import redirect

def Admin_Only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.all().exists():
            group = request.user.groups.all()[0].name
        if group == "merchant":
            return redirect('MerchantIndex')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func