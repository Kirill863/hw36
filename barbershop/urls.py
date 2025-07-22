from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import (
    IndexView,
    OrderCreateView,
    OrdersListView,
    OrderDetailView,
    ReviewCreateView,
    ThanksView,
    get_services
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Главная страница
    path('', IndexView.as_view(), name='index'),  
    
    # Заказы
    path('order/create/', OrderCreateView.as_view(), name='create_order'),
    path('orders/', OrdersListView.as_view(), name='order_list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    
    # Отзывы
    path('orders/review_form/', ReviewCreateView.as_view(), name='review_create'),
    
    # Страницы
    path('thanks/', ThanksView.as_view(), name='thanks'),
    
    # AJAX
    path('get-services/', get_services, name='get_services'),
    
    # Аутентификация
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)