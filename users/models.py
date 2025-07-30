from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class User(AbstractUser):
    """Кастомная модель пользователя с дополнительными полями"""
    
    # Базовые поля (уже есть в AbstractUser)
    # username, password, email, first_name, last_name, is_active, is_staff, is_superuser
    # last_login, date_joined
    
    # Дополнительные поля
    avatar = models.ImageField(
        verbose_name=_('Аватар'),
        upload_to='users/avatars/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text=_('Загрузите ваш аватар')
    )
    
    birth_date = models.DateField(
        verbose_name=_('Дата рождения'),
        blank=True,
        null=True
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("Номер телефона должен быть в формате: '+799999999'. До 15 цифр.")
    )
    phone_number = models.CharField(
        verbose_name=_('Телефон'),
        validators=[phone_regex],
        max_length=17,
        blank=True,
        null=True
    )
    
    telegram_id = models.CharField(
        verbose_name=_('Telegram ID'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Ваш ID в Telegram')
    )
    
    github_id = models.CharField(
        verbose_name=_('GitHub ID'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_('Ваш профиль на GitHub')
    )
    
    email_verified = models.BooleanField(
        verbose_name=_('Email подтвержден'),
        default=False
    )
    
    # Настройки модели
    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return self.username
    
    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
    def get_short_name(self):
        """Возвращает короткое имя пользователя"""
        return self.first_name
    
    @property
    def avatar_url(self):
        """Возвращает URL аватара или дефолтный"""
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/images/default_avatar.png'


# Сигналы для обработки действий с пользователем
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля при создании пользователя"""
    if created:
        # Здесь можно добавить дополнительные действия
        pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранение профиля при сохранении пользователя"""
    instance.save()