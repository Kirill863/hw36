# core/signals.py

import logging
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Order
from .telegram import send_telegram_message

logger = logging.getLogger(__name__)


@receiver(m2m_changed, sender=Order.services.through)
def handle_order_services_change(sender, instance, action, **kwargs):
    """
    Обработчик сигнала m2m_changed для поля services модели Order.
    Отправляет уведомление в Telegram при добавлении нового заказа.
    """

    # Проверяем, что instance — это Order и действие завершено
    if not isinstance(instance, Order) or action != "post_add":
        return

    try:
        # Получаем имя мастера безопасно
        barber_name = getattr(instance.barber, 'get_full_name', lambda: None)()
        if not barber_name:
            barber_name = "Не указан"

        # Формируем список услуг
        services_list = "\n".join([f"- {service.name} ({service.price} ₽)" for service in instance.services.all()])

        # Формируем сообщение
        message = (
            f"* Новый заказ на услуги*\n\n"
            f"*Имя клиента:* {instance.client_name}\n"
            f"*Телефон:* {instance.phone}\n"
            f"*Мастер:* {barber_name}\n"
            f"*Дата записи:* {instance.date.strftime('%d.%m.%Y %H:%M')}\n\n"
            f"*Выбранные услуги:*\n{services_list}\n\n"
            f" [Посмотреть в админке](http://127.0.0.1:8000/admin/core/order/{instance.id}/)"
        )

        # Отправляем уведомление
        send_telegram_message(message)

    except Exception as e:
        logger.error(f"[Telegram] Ошибка при отправке уведомления о заказе #{instance.id}: {e}", exc_info=True)