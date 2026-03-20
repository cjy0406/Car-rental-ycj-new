from django.contrib import admin
from .models import Vendor, Car, CarImage
from django.utils.html import mark_safe

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_email', 'phone', 'is_approved', 'created_at')
    search_fields = ('name', 'contact_email', 'phone')
    list_filter = ('is_approved', 'created_at')

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ('image_tag', 'image',)
    readonly_fields = ('image_tag',)
    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-width: 120px; max-height: 80px; border-radius: 4px;" />')
        return "-"
    image_tag.short_description = 'Preview'

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'car_type', 'model_year', 'price_per_day', 'is_available', 'is_approved', 'created_at', 'image_tag')
    search_fields = ('name', 'vendor__name', 'car_type')
    list_filter = ('car_type', 'is_available', 'is_approved', 'created_at')
    readonly_fields = ('image_tag',)
    fieldsets = (
        (None, {
            'fields': ('is_active', 'vendor', 'name', 'description', 'image_tag', 'image', 'car_type', 'model_year', 'price_per_day', 'is_available', 'is_approved')
        }),
    )
    inlines = [CarImageInline]

    def image_tag(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-width: 300px; max-height: 200px; border-radius: 8px;" />')
        return "-"
    image_tag.short_description = 'Current Image'
