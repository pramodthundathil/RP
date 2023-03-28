from django.shortcuts import redirect,HttpResponse

def Admin_Only(view_func):
    def wrapper_func(request,*args,**kwargs):
        group = None
        if request.user.groups.all().exists():
            group = request.user.groups.all()[0].name
        if group == "merchant":
            return redirect('MerchantIndex')
        if group == "admin":
            return redirect('AdminIndex')
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func