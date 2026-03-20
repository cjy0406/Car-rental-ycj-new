from django.contrib import admin
from .models import Booking, ReturnRecord, Review


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'car', 'customer', 'start_date', 'end_date', 'total_price',
        'status', 'admin_status', 'return_confirmed_at', 'created_at'
    )
    search_fields = ('car__name', 'customer__user__username', 'status')
    list_filter = ('status', 'admin_status', 'created_at', 'start_date', 'end_date')


@admin.register(ReturnRecord)
class ReturnRecordAdmin(admin.ModelAdmin):
    list_display = ('booking', 'confirmed_by', 'confirmed_at', 'created_at')
    search_fields = ('booking__id', 'confirmed_by__username')
    list_filter = ('confirmed_at', 'created_at')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('booking', 'customer', 'vendor', 'car', 'rating', 'replied_at', 'created_at')
    search_fields = ('customer__user__username', 'vendor__name', 'car__name')
    list_filter = ('rating', 'replied_at', 'created_at')