from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from vendors.models import Vendor, Car
from customers.models import Customer
from django import forms
from django import template
from django.db.models import Q
from booking.models import Booking
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Create your views here.

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css):
    return field.as_widget(attrs={**field.field.widget.attrs, 'class': css})

class VendorRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    class Meta:
        model = Vendor
        fields = ['name', 'contact_email', 'phone', 'address']

class CustomerRegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    class Meta:
        model = Customer
        fields = ['phone', 'address']

def vendor_register(request):
    if request.method == 'POST':
        form = VendorRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            vendor = form.save(commit=False)
            vendor.user = user
            vendor.is_approved = False
            vendor.save()
            messages.success(request, 'Vendor registered! Await admin approval.')
            return redirect('login')
    else:
        form = VendorRegisterForm()
    return render(request, 'vendor_register.html', {'form': form})

def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email'],
            )
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            messages.success(request, 'Customer registered! You can now log in.')
            return redirect('login')
    else:
        form = CustomerRegisterForm()
    return render(request, 'customer_register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully.')
    return redirect('home')

def home(request):
    return render(request, 'home.html')

def car_list(request):
    cars = Car.objects.filter(is_available=True, is_approved=True)
    car_type = request.GET.get('type')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search = request.GET.get('search')

    if car_type:
        cars = cars.filter(car_type=car_type)
    if min_price:
        cars = cars.filter(price_per_day__gte=min_price)
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    if search:
        cars = cars.filter(Q(name__icontains=search) | Q(description__icontains=search))

    car_types = Car.CAR_TYPE_CHOICES
    context = {
        'cars': cars,
        'car_types': car_types,
        'selected_type': car_type,
        'min_price': min_price,
        'max_price': max_price,
        'search': search,
    }
    return render(request, 'car_list.html', context)

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id, is_approved=True)
    booking_success = False
    booking_error = None
    total_price = None
    if request.method == 'POST':
        if not request.user.is_authenticated:
            booking_error = 'You must be logged in as a customer to book.'
        else:
            try:
                customer = request.user.customer
            except Exception:
                booking_error = 'Only customers can book cars.'
            else:
                start_date = request.POST.get('start_date')
                end_date = request.POST.get('end_date')
                try:
                    start = datetime.strptime(start_date, '%Y-%m-%d').date()
                    end = datetime.strptime(end_date, '%Y-%m-%d').date()
                    if start >= end:
                        raise ValueError('End date must be after start date.')
                except Exception:
                    booking_error = 'Please enter valid start and end dates.'
                else:
                    days = (end - start).days
                    total_price = days * car.price_per_day
                    Booking.objects.create(
                        car=car,
                        customer=customer,
                        start_date=start,
                        end_date=end,
                        total_price=total_price,
                        status='pending',
                        admin_status='pending',
                    )
                    booking_success = True
    return render(request, 'car_detail.html', {
        'car': car,
        'booking_success': booking_success,
        'booking_error': booking_error,
        'total_price': total_price,
    })
