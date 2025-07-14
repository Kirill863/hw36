from django.db import models
import random

# Create your models here.

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена")
    duration = models.IntegerField(null=True, blank=True, verbose_name="Длительность (мин)")
    is_popular = models.BooleanField(default=False, verbose_name="Популярная услуга")
    is_published = models.BooleanField(default=True, verbose_name="Опубликована")
    image = models.ImageField(upload_to='services/', null=True, blank=True) 
    

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"

    def __str__(self):
        return self.name
    
class Master(models.Model):
    name = models.CharField(max_length=150, verbose_name="Имя")
    photo = models.ImageField(upload_to='masters/', blank=True, verbose_name="Фотография")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    experience = models.PositiveIntegerField(null=True, blank=True, verbose_name="Опыт (лет)") 
    services = models.ManyToManyField(Service, related_name='masters', verbose_name="Услуги")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Мастер"
        verbose_name_plural = "Мастера"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.experience is None:
            self.experience = random.randint(0, 10)
        super().save(*args, **kwargs)

STATUS_CHOICES = [
    ('not_approved', 'Не подтверждён'),
    ('approved', 'Подтверждён'),
    ('in_progress', 'В процессе'),
    ('completed', 'Выполнен'),
]

class Order(models.Model):
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='not_approved', verbose_name="Статус")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_updated = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    master = models.ForeignKey(Master, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Мастер")
    services = models.ManyToManyField(Service, related_name='orders', verbose_name="Услуги")
    appointment_date = models.DateTimeField(verbose_name="Дата и время записи")

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"

    def __str__(self):
        return f"{self.client_name} - {self.status}"

# models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import Master  

AI_CHOICES = [
    ("ai_checked_true", "Проверено ИИ"),
    ("ai_cancelled", "Отменено ИИ"),
    ("ai_checked_in_progress", "В процессе проверки"),
    ("ai_checked_false", "Не проверено"),
]

class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    client_name = models.CharField(max_length=100, verbose_name="Имя клиента")
    master = models.ForeignKey(
        Master,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name="Мастер"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    photo = models.ImageField(
        upload_to='reviews/',
        blank=True,
        null=True,
        verbose_name="Фотография"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    # Статус проверки ИИ
    ai_checked_status = models.CharField(
        max_length=30,
        choices=AI_CHOICES,
        default="ai_checked_false",
        verbose_name="Статус проверки ИИ"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв от {self.client_name} о {self.master}"