from django.urls import path
from .views import vendor_dashboard, add_car, edit_car, delete_car, car_bookings, car_image_management

urlpatterns = [
    path('dashboard/', vendor_dashboard, name='vendor_dashboard'),
    path('cars/add/', add_car, name='add_car'),
    path('cars/<uuid:car_id>/edit/', edit_car, name='edit_car'),
    path('cars/<uuid:car_id>/delete/', delete_car, name='delete_car'),
    path('cars/<uuid:car_id>/bookings/', car_bookings, name='car_bookings'),
    path('cars/<uuid:car_id>/images/', car_image_management, name='car_image_management'),
    # Vendor endpoints will go here
] 