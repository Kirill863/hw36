from django.contrib import admin
from django.views.generic import TemplateView, ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Master, Service, Order, Review
from .forms import ReviewForm, OrderForm

# Главная страница
class IndexView(TemplateView):
    template_name = 'barbershop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['masters'] = Master.objects.all()
        context['reviews'] = Review.objects.select_related('master').all()[:5]
        context['services'] = Service.objects.all()
        return context

class ThanksView(TemplateView):
    template_name = 'orders/thanks.html' 

# Список заказов
class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    ordering = ['-date_created']

    def get_queryset(self):
        queryset = super().get_queryset().select_related('master').prefetch_related('services')
        query = self.request.GET.get('q', '')
        
        if query:
            filters = Q()
            if 'search_name' in self.request.GET:
                filters |= Q(client_name__icontains=query)
            if 'search_phone' in self.request.GET:
                filters |= Q(phone__icontains=query)
            if 'search_comment' in self.request.GET:
                filters |= Q(comment__icontains=query)
            
            queryset = queryset.filter(filters)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['search_name'] = 'search_name' in self.request.GET
        context['search_phone'] = 'search_phone' in self.request.GET
        context['search_comment'] = 'search_comment' in self.request.GET
        return context

# Детали заказа
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return super().get_queryset().select_related('master').prefetch_related('services')

# Страница благодарности
class ThanksView(TemplateView):
    template_name = 'orders/thanks.html'

# Создание отзыва
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'orders/review_form.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, 'Ваш отзыв успешно отправлен!')
        return super().form_valid(form)

# Создание заказа
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        messages.success(self.request, 'Ваша заявка успешно отправлена!')
        return super().form_valid(form)

# Получение услуг для мастера (AJAX)
def get_services(request):
    master_id = request.GET.get('master_id')
    
    if master_id:
        try:
            services = Service.objects.filter(masters__id=master_id)
            selected_services = request.GET.getlist('selected_services[]')
            
            html = render_to_string('orders/services_checkboxes.html', {
                'services': services,
                'selected_services': selected_services
            })

            return JsonResponse({'html': html})
        except Exception as e:
            print("Ошибка при загрузке услуг:", str(e))
            return JsonResponse({'error': 'Ошибка при загрузке услуг'}, status=500)
    return JsonResponse({'html': ''})

# Фильтр по рейтингу (для админки)
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