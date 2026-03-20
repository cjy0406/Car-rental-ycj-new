from django.contrib import admin
from .models import RentalStat

@admin.register(RentalStat)
class RentalStatAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'car', 'date', 'rentals_count', 'revenue')
    search_fields = ('vendor__name', 'car__name')
    list_filter = ('date', 'vendor', 'car')
