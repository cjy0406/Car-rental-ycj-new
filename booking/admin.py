from django.contrib import admin

# Register your models here.
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('car', 'customer', 'start_date', 'end_date', 'total_price', 'status', 'admin_status', 'created_at')
    search_fields = ('car__name', 'customer__user__username', 'status')
    list_filter = ('status', 'admin_status', 'created_at', 'start_date', 'end_date')
