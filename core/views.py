

# Create your views here.


from django.shortcuts import render
from .data import masters, services, orders, STATUS_NEW, STATUS_CONFIRMED, STATUS_CANCELLED, STATUS_COMPLETED


def landing(request):
    return render(request, 'landing.html', {
        'masters': masters,
        'services': services,
    })


def thanks(request):
    return render(request, 'core/thanks.html')


def orders_list(request):
    return render(request, 'core/orders_list.html', {
        'orders': orders,
        'statuses': {
            'новая': STATUS_NEW,
            'подтвержденная': STATUS_CONFIRMED,
            'отмененная': STATUS_CANCELLED,
            'выполненная': STATUS_COMPLETED
        }
    })


def order_detail(request, order_id):
    order = next((o for o in orders if o['id'] == order_id), None)
    if not order:
        # Можно добавить обработку ошибки 404
        return render(request, 'core/order_detail.html', {'order': None})
    return render(request, 'core/order_detail.html', {
        'order': order,
        'masters': masters
    })