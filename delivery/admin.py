from django.contrib import admin
from .models import DeliveryLocation

@admin.register(DeliveryLocation)
class DeliveryLocationAdmin(admin.ModelAdmin):
    list_display = ('delivery_person', 'latitude', 'longitude', 'updated_at')