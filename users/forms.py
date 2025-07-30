from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('example@example.com'),
            'autocomplete': 'email'
        }),
        error_messages={
            'required': _('Обязательное поле'),
            'invalid': _('Введите корректный email адрес')
        }
    )
    
    first_name = forms.CharField(
        label=_("Имя"),
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Ваше имя')
        })
    )
    
    last_name = forms.CharField(
        label=_("Фамилия"),
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Ваша фамилия')
        })
    )
    
    password1 = forms.CharField(
        label=_("Пароль"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Создайте пароль'),
            'autocomplete': 'new-password'
        }),
        help_text=_(
            "Пароль должен содержать минимум 8 символов, "
            "не состоять только из цифр и не быть слишком простым."
        )
    )
    
    password2 = forms.CharField(
        label=_("Подтверждение пароля"),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Повторите пароль'),
            'autocomplete': 'new-password'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': _('Придумайте логин'),
            'autocomplete': 'username'
        })
        self.fields['username'].help_text = _(
            'Не более 150 символов. Только буквы, цифры и @/./+/-/_'
        )
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise ValidationError(
                _("Пароль должен содержать минимум 8 символов"),
                code='password_too_short'
            )
        
        if password1.isdigit():
            raise ValidationError(
                _("Пароль не может состоять только из цифр"),
                code='password_entirely_numeric'
            )
        
        # Дополнительные проверки сложности пароля
        if password1.lower() == password1:
            raise ValidationError(
                _("Пароль должен содержать хотя бы одну заглавную букву"),
                code='password_no_upper'
            )
        
        return password1
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                _("Пользователь с таким email уже зарегистрирован"),
                code='email_exists'
            )
        return email