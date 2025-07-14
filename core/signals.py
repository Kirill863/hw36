# core/signals.py

from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Order
from .telegram import send_telegram_message


@receiver(m2m_changed, sender=Order.services.through)
def handle_order_services_change(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для поля services модели Order.
    Отправляет уведомление в Telegram при изменении списка услуг.
    """

    if action == "post_add":  # Срабатывает после добавления услуг
        try:
            # Формируем список названий услуг
            services = instance.services.all()
            services_list = "\n".join([f"- {service.name} ({service.price} ₽)" for service in services])

            # Формируем сообщение в Markdown
            message = (
                f"*🆕 Новый заказ на услуги*\n\n"
                f"*Имя клиента:* {instance.client_name}\n"
                f"*Телефон:* {instance.phone}\n"
                f"*Мастер:* {instance.barber.get_full_name() or 'Не указан'}\n"
                f"*Дата записи:* {instance.date.strftime('%d.%m.%Y %H:%M')}\n\n"
                f"*Выбранные услуги:*\n{services_list}\n\n"
                f"Ссылка: [Посмотреть в админке](http://127.0.0.1:8000/admin/core/order/{instance.id}/)"
            )

            # Отправляем сообщение
            send_telegram_message(message)

        except Exception as e:
            print(f"[Ошибка Telegram уведомления] {e}")