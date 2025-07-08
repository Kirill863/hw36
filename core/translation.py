from modeltranslation.translator import register, TranslationOptions
from .models import Service, Master, Review


@register(Service)
class ServiceTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Master)
class MasterTranslationOptions(TranslationOptions):
    fields = ('name',)  # если есть поле bio у Master


@register(Review)
class ReviewTranslationOptions(TranslationOptions):
    fields = ('text',)