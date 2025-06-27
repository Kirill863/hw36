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
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})

def thanks(request):
    return render(request, 'barbershop/thanks.html')

def order_list(request):
    query = request.GET.get('q', '')
    search_name = 'search_name' in request.GET
    search_phone = 'search_phone' in request.GET
    search_comment = 'search_comment' in request.GET

    # По умолчанию выбираем всё
    orders = Order.objects.all()

    # Если нет активных фильтров — не применяем фильтрацию
    if query:
        q_objects = Q()

        if search_name:
            q_objects |= Q(client_name__icontains=query)
        if search_phone:
            q_objects |= Q(phone__icontains=query)
        if search_comment:
            q_objects |= Q(comment__icontains=query)

        orders = orders.filter(q_objects)

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'query': query,
        'search_name': search_name,
        'search_phone': search_phone,
        'search_comment': search_comment,
    })