from django.shortcuts import render

# Create your views here.


def landing(request):
    return render(request, 'landing.html')

def thanks(request):
    return render(request, 'core/thanks.html')

def orders_list(request):
    
    return render(request, 'core/orders_list.html')

def order_detail(request, order_id):
    
    return render(request, 'core/order_detail.html')