from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm
)
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserLoginForm(AuthenticationForm):
    """Форма входа пользователя с Bootstrap стилями"""
    username = forms.CharField(
        label=_('Имя пользователя'),
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите имя пользователя'),
            'autofocus': True
        })
    )
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите пароль')
        })
    )

    error_messages = {
        'invalid_login': _(
            "Пожалуйста, введите правильные имя пользователя и пароль. "
            "Оба поля могут быть чувствительны к регистру."
        ),
        'inactive': _("Этот аккаунт неактивен."),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = _('Имя пользователя или Email')


class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя с дополнительными полями"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите ваш email')
        }),
        label=_('Email'),
        help_text=_('На этот email будет отправлено письмо для подтверждения')
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': _('Имя пользователя'),
            'password1': _('Пароль'),
            'password2': _('Подтверждение пароля'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Настройка виджетов и удаление help_text
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            self.fields[field_name].help_text = None
            self.fields[field_name].widget.attrs['placeholder'] = self.fields[field_name].label

        # Кастомные placeholder для паролей
        self.fields['password1'].widget.attrs['placeholder'] = _('Введите пароль')
        self.fields['password2'].widget.attrs['placeholder'] = _('Повторите пароль')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Пользователь с таким email уже существует'))
        return email


class UserProfileUpdateForm(forms.ModelForm):
    """Форма обновления профиля пользователя"""
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date', 'class': 'form-control'},
            format='%Y-%m-%d'
        ),
        required=False,
        label=_('Дата рождения')
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'avatar', 'birth_date', 'telegram_id', 'github_id']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telegram_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '@username'
            }),
            'github_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'username'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'telegram_id': _('Telegram username'),
            'github_id': _('GitHub username'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True


class UserPasswordChangeForm(PasswordChangeForm):
    """Форма смены пароля"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })
            self.fields[field].help_text = None


class CustomPasswordResetForm(PasswordResetForm):
    """Кастомная форма сброса пароля"""
    email = forms.EmailField(
        label=_('Email'),
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Введите email, указанный при регистрации'),
            'autocomplete': 'email'
        })
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            raise forms.ValidationError(_('Пользователь с таким email не найден'))
        return email


class CustomSetPasswordForm(SetPasswordForm):
    """Форма установки нового пароля"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })
            self.fields[field].help_text = None