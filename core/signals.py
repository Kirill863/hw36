
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from moderation.utils import check_content_with_mistral


@receiver(post_save, sender=Review)
def moderate_review_on_creation(sender, instance, created, **kwargs):
    """
    При создании отзыва автоматически запускает проверку текста через ИИ.
    """
    if created and instance.ai_checked_status == "ai_checked_false":
        # Меняем статус на "в процессе"
        instance.ai_checked_status = "ai_checked_in_progress"
        instance.save(update_fields=["ai_checked_status"])

        try:
            is_safe = check_content_with_mistral(instance.text)

            if is_safe:
                instance.ai_checked_status = "ai_checked_true"
            else:
                instance.ai_checked_status = "ai_cancelled"
        except Exception as e:
            print(f"Ошибка при проверке контента через Mistral AI: {e}")
            instance.ai_checked_status = "ai_checked_false"

        instance.save(update_fields=["ai_checked_status"])