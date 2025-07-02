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
    class Meta:
        model = Order
        fields = ['master', 'services', 'client_name', 'phone', 'comment', 'appointment_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['services'].queryset = Service.objects.none()  # Изначально пустой queryset

        if 'master' in self.data:
            try:
                master_id = int(self.data.get('master'))
                self.fields['services'].queryset = Service.objects.filter(master_id=master_id)
            except (ValueError, TypeError):
                pass  # Если мастер не выбран или ошибка
        elif self.instance.pk:
            self.fields['services'].queryset = self.instance.master.services.all()

    def clean(self):
        cleaned_data = super().clean()
        master = cleaned_data.get("master")
        services = cleaned_data.get("services")

        if master and services:
            valid_services = master.services.values_list('id', flat=True)
            for service in services:
                if service.id not in valid_services:
                    raise forms.ValidationError(
                        f"Услуга '{service.name}' недоступна для мастера {master}."
                    )
        return cleaned_data