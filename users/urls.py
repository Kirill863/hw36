from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', 
        LoginView.as_view(
            template_name='users/login.html',
            redirect_authenticated_user=True,
            extra_context={'title': 'Авторизация'}
        ), 
        name='login'),
    
    path('logout/', 
        LogoutView.as_view(
            template_name='users/logout.html',
            next_page='/'
        ), 
        name='logout'),
    # другие URL...
]