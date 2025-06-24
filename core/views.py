from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Master, Service, Order, Review


def landing(request):
    return render(request, 'barbershop/landing.html')


def index(request):
    masters = Master.objects.all()
    reviews = Review.objects.filter(is_published=True)
    services = Service.objects.all()

    return render(request, 'barbershop/index.html', {
        'masters': masters,
        'reviews': reviews,
        'services': services
    })


@login_required
def orders_list(request):
    query = request.GET.get('q', '')
    search_name = request.GET.get('search_name') == 'on'
    search_phone = request.GET.get('search_phone') == 'on'
    search_comment = request.GET.get('search_comment') == 'on'

    queryset = Order.objects.all().order_by('-date_created')

    if query:
        q_objects = Q()
        if search_name:
            q_objects |= Q(client_name__icontains=query)
        if search_phone:
            q_objects |= Q(phone__icontains=query)
        if search_comment:
            q_objects |= Q(comment__icontains=query)
        queryset = queryset.filter(q_objects)

    return render(request, 'barbershop/orders_list.html', {
        'orders': queryset,
        'query': query,
        'search_name': search_name or True,  # Имя клиента включено по умолчанию
        'search_phone': search_phone,
        'search_comment': search_comment
    })


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related('services'), pk=pk)
    return render(request, 'barbershop/order_detail.html', {'order': order})