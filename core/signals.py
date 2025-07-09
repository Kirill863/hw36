# reviews/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Review
from moderation.mistral import is_bad_review
from django.conf import settings


@receiver(post_save, sender=Review)
def moderate_review_on_creation(sender, instance, created, **kwargs):
    if created and instance.ai_checked_status == "ai_checked_false":
        instance.ai_checked_status = "ai_checked_in_progress"
        instance.save(update_fields=["ai_checked_status"])

        try:
            contains_bad_content = is_bad_review(
                review_text=instance.text,
                api_key=settings.MISTRAL_API_KEY,
                grades=settings.MISTRAL_MODERATIONS_GRADES
            )

            if contains_bad_content:
                instance.ai_checked_status = "ai_cancelled"
            else:
                instance.ai_checked_status = "ai_checked_true"

        except Exception as e:
            print(f"Ошибка при проверке контента: {e}")
            instance.ai_checked_status = "ai_checked_false"

        instance.save(update_fields=["ai_checked_status"])