from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Master, Service, Order, Review
from .data import services


def index(request):
    masters = Master.objects.all()
    reviews = Review.objects.select_related('master').all()[:5] 
    services = Service.objects.all()

    return render(request, 'barbershop/index.html', {
        'masters': masters,
        'reviews': reviews,
        'services': services
    })



@login_required
def order_list(request):
    orders = Order.objects.all().order_by('-date_created')
    return render(request, 'orders/order_list.html', {'orders': orders})


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('services'), pk=pk)
    return render(request, 'barbershop/order_detail.html', {'order': order})

def thanks(request):
    return render(request, 'barbershop/thanks.html')