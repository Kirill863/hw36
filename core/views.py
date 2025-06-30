from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from .models import Master, Service, Order, Review
from .forms import ReviewForm, OrderForm

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
    query = request.GET.get('q', '')
    search_name = 'search_name' in request.GET
    search_phone = 'search_phone' in request.GET
    search_comment = 'search_comment' in request.GET

    orders = Order.objects.select_related('master').prefetch_related('services').order_by('-date_created')

    if query:
        q_objects = Q()
        if search_name:
            q_objects |= Q(client_name__icontains=query)
        if search_phone:
            q_objects |= Q(phone__icontains=query)
        if search_comment:
            q_objects |= Q(comment__icontains=query)
        
        if q_objects:
            orders = orders.filter(q_objects)

    return render(request, 'orders/order_list.html', {
        'orders': orders,
        'query': query,
        'search_name': search_name,
        'search_phone': search_phone,
        'search_comment': search_comment,
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related('master').prefetch_related('services'), 
        pk=pk
    )
    return render(request, 'orders/order_detail.html', {'order': order})

def thanks(request):
    return render(request, 'barbershop/thanks.html')

def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = ReviewForm()
    return render(request, 'orders/review_form.html', {'form': form})

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thanks')
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})

def get_services(request):
    master_id = request.GET.get('master_id')
    if not master_id:
        return JsonResponse([], safe=False)
    
    services = Service.objects.filter(masters__id=master_id).values('id', 'name')
    return JsonResponse(list(services), safe=False)