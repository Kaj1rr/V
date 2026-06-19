from django.contrib import admin
from .models import TransportType, Application

@admin.register(TransportType)
class TransportTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'icon']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'transport_type', 'start_date', 'status', 'created_at']
    list_filter = ['status', 'transport_type']
    search_fields = ['user__username', 'user__first_name']

# Register your models here.
