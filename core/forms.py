from django import forms
from .models import Review, Order, Master, Service

RATING_CHOICES = [
    (1, '1 - Ужасно'),
    (2, '2 - Плохо'),
    (3, '3 - Нормально'),
    (4, '4 - Хорошо'),
    (5, '5 - Отлично'),
]

class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = Review
        fields = ['master', 'rating', 'client_name', 'text', 'photo']
        widgets = {
            'master': forms.Select(attrs={'class': 'form-control'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем services необязательным при инициализации
        self.fields['services'].required = False
        # Если передан мастер, фильтруем услуги
        if 'master' in self.data:
            try:
                master_id = int(self.data.get('master'))
                master = Master.objects.get(id=master_id)
                self.fields['services'].queryset = master.services.all()
            except (ValueError, Master.DoesNotExist):
                pass
    
    class Meta:
        model = Order
        fields = ['master', 'services', 'client_name', 'phone', 'comment', 'appointment_date']
        widgets = {
            'master': forms.Select(attrs={'class': 'form-control', 'id': 'master-select'}),
            'services': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'services-select'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'appointment_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        master = cleaned_data.get('master')
        services = cleaned_data.get('services')
        
        if master and services:
            invalid_services = [service for service in services if service not in master.services.all()]
            if invalid_services:
                invalid_names = ", ".join([s.name for s in invalid_services])
                raise forms.ValidationError(
                    f"Мастер {master.name} не предоставляет выбранные услуги: {invalid_names}"
                )
        return cleaned_data