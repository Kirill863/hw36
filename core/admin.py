from django.contrib import admin
from .models import Service, Master, Order, Review


# Кастомный фильтр по цене
class PriceRangeFilter(admin.SimpleListFilter):
    title = 'Ценовой диапазон'  # Название фильтра в админке
    parameter_name = 'price_range'  # URL-параметр

    def lookups(self, request, model_admin):
        return (
            ('0-500', 'До 500'),
            ('500-1500', 'От 500 до 1500'),
            ('1500+', 'Более 1500'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0-500':
            return queryset.filter(price__lt=500)
        elif self.value() == '500-1500':
            return queryset.filter(price__gte=500, price__lte=1500)
        elif self.value() == '1500+':
            return queryset.filter(price__gt=1500)
        return queryset

# Кастомное действие: Опубликовать
def make_published(modeladmin, request, queryset):
    queryset.update(is_published=True)
make_published.short_description = "Опубликовать выбранные услуги"



# Кастомное действие: Снять с публикации
def make_unpublished(modeladmin, request, queryset):
    queryset.update(is_published=False)
make_unpublished.short_description = "Снять с публикации выбранные услуги"


# Инлайн для отзывов
class ReviewInline(admin.TabularInline):  # или admin.StackedInline для более подробного вида
    model = Review
    extra = 1  # количество дополнительных форм для создания новых записей
    fields = ['client_name', 'text', 'rating', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'is_popular']
    search_fields = ['name', 'description']
    list_filter = [PriceRangeFilter] 
    actions = [make_published, make_unpublished] 
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'duration')
        }),
        ('Дополнительно', {
            'fields': ('is_popular', 'image'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'experience', 'is_active']
    search_fields = ['name', 'address']
    list_filter = ['is_active']
    filter_horizontal = ['services']
    inlines = [ReviewInline]  


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'status', 'appointment_date', 'master']
    search_fields = ['client_name', 'phone']
    list_filter = ['status', 'master', 'appointment_date']
    date_hierarchy = 'appointment_date'
    filter_horizontal = ['services']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'master', 'rating', 'created_at']
    search_fields = ['client_name', 'text']
    list_filter = ['rating', 'created_at']
    readonly_fields = ['created_at']