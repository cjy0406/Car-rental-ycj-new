from django.urls import path
from .views import home, vendor_register, customer_register, login_view, logout_view, car_list, car_detail


urlpatterns = [
    path('', home, name='home'),
    path('register/vendor/', vendor_register, name='vendor_register'),
    path('register/customer/', customer_register, name='customer_register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('cars/', car_list, name='car_list'),
    path('cars/<uuid:car_id>/', car_detail, name='car_detail'),
] 