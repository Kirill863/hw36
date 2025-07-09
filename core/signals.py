# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

from .models import Review
from moderation.mistral import is_bad_review


@receiver(post_save, sender=Review)
def check_review(sender, instance, created, **kwargs):
    """
    Обработчик сигнала, который срабатывает после сохранения нового отзыва.
    Проверяет текст отзыва на наличие нежелательного контента с помощью Mistral AI.
    Обновляет статус проверки и флаг публикации.
    """

    if created:
        # Устанавливаем статус "в процессе проверки"
        instance.ai_checked_status = "ai_checked_in_progress"
        instance.save(update_fields=["ai_checked_status"])

        try:
            # Вызываем функцию модерации
            contains_bad_content = is_bad_review(
                review_text=instance.text,
                api_key=settings.MISTRAL_API_KEY,
                grades=settings.MISTRAL_MODERATIONS_GRADES
            )

            # Обновляем статус и флаг публикации
            if contains_bad_content:
                instance.ai_checked_status = "ai_cancelled"
                instance.is_published = False
            else:
                instance.ai_checked_status = "ai_checked_true"
                instance.is_published = True

        except Exception as e:
            # В случае ошибки помечаем как "Не проверено" и не публикуем
            print(f"[Ошибка модерации] {e}")
            instance.ai_checked_status = "ai_checked_false"
            instance.is_published = False

        # Сохраняем обновлённые поля
        instance.save(update_fields=["ai_checked_status", "is_published"])