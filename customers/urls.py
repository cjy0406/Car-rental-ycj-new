from django.urls import path
from .views import customer_dashboard, booking_cancel

urlpatterns = [
    # Customer endpoints will go here
    path('dashboard/', customer_dashboard, name='customer_dashboard'),
    path('bookings/<uuid:booking_id>/cancel/', booking_cancel, name='booking_cancel'),
] 