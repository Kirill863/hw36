from modeltranslation.translator import translator, TranslationOptions
from .models import User

class UserTranslationOptions(TranslationOptions):
    fields = ('username', 'first_name', 'last_name')  # Поля, которые нужно переводить

translator.register(User, UserTranslationOptions)