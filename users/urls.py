from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users' 

urlpatterns = [
    # Регистрация и аутентификация
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    
    # Профиль пользователя
    path('profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', views.UserProfileUpdateView.as_view(), name='profile_edit'),
    
    # Смена пароля
    path('password-change/', views.UserPasswordChangeView.as_view(), name='password_change'),
    
    # Восстановление пароля
    path('password-reset/', 
        views.CustomPasswordResetView.as_view(
            template_name='users/password_reset_form.html',
            email_template_name='users/password_reset_email.html',
            subject_template_name='users/password_reset_subject.txt'
        ), 
        name='password_reset'),
    
    path('password-reset/done/', 
        views.CustomPasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ), 
        name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
        views.CustomPasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ), 
        name='password_reset_confirm'),
    
    path('reset/done/', 
        views.CustomPasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ), 
        name='password_reset_complete'),
    
    # Включение URL-адресов аутентификации по умолчанию (резервный вариант)
    # path('', include('django.contrib.auth.urls')),
]

# Настройка для медиа-файлов в режиме разработки
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)