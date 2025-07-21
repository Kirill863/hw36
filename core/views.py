from django.contrib import admin
from django.shortcuts import get_object_or_404
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
class OrdersListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_list.html'  # Уточненный путь к шаблону
    context_object_name = 'orders'
    ordering = ['-date_created']
    paginate_by = 10  # Опционально: добавить пагинацию

    def get_queryset(self):
        queryset = super().get_queryset().select_related('master').prefetch_related('services')
        query = self.request.GET.get('q', '')
        
        if query:
            filters = Q()
            search_params = {
                'search_name': 'client_name__icontains',
                'search_phone': 'phone__icontains',
                'search_comment': 'comment__icontains'
            }
            
            for param, field_lookup in search_params.items():
                if param in self.request.GET:
                    filters |= Q(**{field_lookup: query})
            
            queryset = queryset.filter(filters)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        # Добавляем флаги поиска в контекст
        for param in ['search_name', 'search_phone', 'search_comment']:
            context[param] = param in self.request.GET
        return context

# Детали заказа
class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'  # Уточненный путь к шаблону
    context_object_name = 'order'
    pk_url_kwarg = 'pk'  # Параметр URL по умолчанию, можно не указывать явно

    def get_queryset(self):
        """
        Оптимизация запросов к БД с помощью select_related и prefetch_related
        """
        return super().get_queryset().select_related('master').prefetch_related('services')

    def get_object(self, queryset=None):
        """
        Получение объекта с обработкой случая, когда заявка не найдена
        """
        if queryset is None:
            queryset = self.get_queryset()
        
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = queryset.filter(pk=pk)
        
        obj = get_object_or_404(queryset)
        return obj
# Страница благодарности
class ThanksView(TemplateView):
    template_name = 'orders/thanks.html'

# Создание отзыва
class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'orders/review_form.html'
    success_url = reverse_lazy('thanks')  # Редирект после успешного создания

    def form_valid(self, form):
        """Добавляем success-сообщение при успешном создании отзыва"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Ваш отзыв успешно отправлен!'
        )
        return response

# Создание заказа
class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('thanks')

    def form_valid(self, form):
        """Обработка валидной формы и добавление сообщения"""
        response = super().form_valid(form)
        messages.success(
            self.request,
            'Ваша заявка успешно отправлена!'
        )
        return response

    def get_context_data(self, **kwargs):
        """Добавление дополнительного контекста для AJAX-загрузки услуг"""
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.none()  # Пустой queryset по умолчанию
        return context
    
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