from django.contrib import admin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Master, Service, Order, Review
from .forms import ReviewForm, OrderForm
from django.http import JsonResponse
from django.http import JsonResponse
from django.template.loader import render_to_string

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
    return render(request, 'orders/thanks.html')

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
    
    if master_id:
        try:
            # Получаем услуги, связанные с мастером
            services = Service.objects.filter(masters__id=master_id)
            
            # Получаем уже выбранные услуги (для сохранения состояния чекбоксов)
            selected_services = request.GET.getlist('selected_services[]')

            # Рендерим шаблон
            html = render_to_string('orders/services_checkboxes.html', {
                'services': services,
                'selected_services': selected_services
            })

            return JsonResponse({'html': html})
        except Exception as e:
            # Логируем ошибку и возвращаем сообщение
            print("Ошибка при загрузке услуг:", str(e))
            return JsonResponse({'error': 'Ошибка при загрузке услуг'}, status=500)
    else:
        return JsonResponse({'html': ''})
    
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'orders/review_form.html'
    success_url = reverse_lazy('thanks')  # Перенаправление после успешного сохранения

class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('thanks')

class RatingFilter(admin.SimpleListFilter):
    title = 'Рейтинг'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return (
            ('high', 'Высокий (4-5 звезд)'),
            ('medium', 'Средний (2-3 звезды)'),
            ('low', 'Низкий (1 звезда)'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'high':
            return queryset.filter(rating__gte=4)
        elif self.value() == 'medium':
            return queryset.filter(rating__gte=2, rating__lte=3)
        elif self.value() == 'low':
            return queryset.filter(rating=1)
        return queryset