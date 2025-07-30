from django.urls import path
from django.contrib.auth.views import (
    LoginView, LogoutView, 
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from .views import RegisterView, ProfileDetailView, ProfileUpdateView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        redirect_authenticated_user=True,
        extra_context={'title': 'Авторизация'}
    ), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='users/logout.html',
        next_page='/'
    ), name='logout'),
    
    # Профиль
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    
    # Смена пароля
    path('password-change/', PasswordChangeView.as_view(
        template_name='users/password_change_form.html',
        success_url='/users/password-change/done/'
    ), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(
        template_name='users/password_change_done.html'
    ), name='password_change_done'),
    
    # Восстановление пароля
    path('password-reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.html',
        success_url='/users/password-reset/done/'
    ), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url='/users/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]