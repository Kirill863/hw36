

# Create your views here.


from django.shortcuts import render
from .data import masters, services, orders, STATUS_NEW, STATUS_CONFIRMED, STATUS_CANCELLED, STATUS_COMPLETED
from django.contrib.admin.views.decorators import staff_member_required

def landing(request):
    return render(request, 'landing.html', {
        'masters': masters,
        'services': services,
    })


def thanks(request):
    return render(request, 'core/thanks.html')

@staff_member_required
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
        return render(request, 'core/order_detail.html', {'order': None})

    # Найдём мастера по ID
    master = next((m for m in masters if m['id'] == order['master_id']), None)

    return render(request, 'core/order_detail.html', {
        'order': order,
        'master': master
    })

STATUS_COLORS = {
    STATUS_NEW: 'warning',
    STATUS_CONFIRMED: 'primary',
    STATUS_CANCELLED: 'secondary',
    STATUS_COMPLETED: 'success'
}

def orders_list(request):
    for order in orders:
        order['status_color'] = STATUS_COLORS.get(order['status'], 'light')
    return render(request, 'core/orders_list.html', {'orders': orders})