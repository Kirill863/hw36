from django.shortcuts import render

# Create your views here.
# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm, UserLoginForm


from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import UserRegisterForm
from django.contrib import messages

class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')  # Используем пространство имен
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация прошла успешно! Теперь вы можете войти.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return super().form_invalid(form)


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')