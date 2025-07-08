from django.contrib import admin
from .models import Service, Master, Order, Review

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'duration', 'is_popular']
    search_fields = ['name']
    list_filter = ['is_popular']

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address', 'experience', 'is_active']
    list_filter = ['is_active']
    filter_horizontal = ['services']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'status', 'appointment_date', 'master']
    list_filter = ['status', 'master']
    filter_horizontal = ['services']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['client_name', 'rating', 'created_at']
    list_filter = ['rating']
    readonly_fields = ['created_at']