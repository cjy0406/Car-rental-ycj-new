from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from vendors.models import Car, CarImage
from booking.models import Booking
from django import forms
from django.http import HttpResponseForbidden

# Create your views here.

@login_required
def vendor_dashboard(request):
    try:
        vendor = request.user.vendor
    except Exception:
        return redirect('home')
    cars = Car.objects.filter(vendor=vendor)
    bookings = Booking.objects.filter(car__vendor=vendor).order_by('-created_at')[:10]
    return render(request, 'vendors/dashboard.html', {
        'vendor': vendor,
        'cars': cars,
        'bookings': bookings,
    })

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['name', 'description', 'image', 'car_type', 'model_year', 'price_per_day']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

@login_required
def add_car(request):
    try:
        vendor = request.user.vendor
    except Exception:
        return redirect('home')
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.vendor = vendor
            car.is_approved = False
            car.save()
            return redirect('vendor_dashboard')
    else:
        form = CarForm()
    return render(request, 'vendors/add_car.html', {'form': form})

@login_required
def edit_car(request, car_id):
    try:
        vendor = request.user.vendor
    except Exception:
        return redirect('home')
    car = Car.objects.filter(id=car_id, vendor=vendor).first()
    if not car:
        return redirect('vendor_dashboard')
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            car = form.save(commit=False)
            car.is_approved = False  # Require re-approval after edit
            car.save()
            return redirect('vendor_dashboard')
    else:
        form = CarForm(instance=car)
    return render(request, 'vendors/edit_car.html', {'form': form, 'car': car})

@login_required
def delete_car(request, car_id):
    try:
        vendor = request.user.vendor
    except Exception:
        return redirect('home')
    car = Car.objects.filter(id=car_id, vendor=vendor).first()
    if not car:
        return redirect('vendor_dashboard')
    if request.method == 'POST':
        car.delete()
        return redirect('vendor_dashboard')
    return render(request, 'vendors/delete_car.html', {'car': car})

@login_required
def car_bookings(request, car_id):
    try:
        vendor = request.user.vendor
    except Exception:
        return redirect('home')
    car = Car.objects.filter(id=car_id, vendor=vendor).first()
    if not car:
        return redirect('vendor_dashboard')
    bookings = car.bookings.all().order_by('-created_at')
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        action = request.POST.get('action')
        booking = car.bookings.filter(id=booking_id).first()
        if booking and booking.status == 'pending':
            if action == 'approve':
                if booking.admin_status == 'approved':
                    booking.status = 'confirmed'
                else:
                    booking.status = 'pending'
                booking.save()
            elif action == 'reject':
                booking.status = 'cancelled'
                booking.save()
        return redirect('car_bookings', car_id=car.id)
    return render(request, 'vendors/car_bookings.html', {'car': car, 'bookings': bookings})

@login_required
def car_image_management(request, car_id):
    try:
        vendor = request.user.vendor
    except Exception:
        return redirect('home')
    car = Car.objects.filter(id=car_id, vendor=vendor).first()
    if not car:
        return HttpResponseForbidden()
    if request.method == 'POST':
        if 'upload' in request.POST and request.FILES.getlist('image'):
            for f in request.FILES.getlist('image'):
                CarImage.objects.create(car=car, image=f)
        elif 'delete' in request.POST:
            img_id = request.POST.get('img_id')
            img = CarImage.objects.filter(id=img_id, car=car).first()
            if img:
                img.delete()
        elif 'reorder' in request.POST:
            order_list = request.POST.get('order', '').split(',')
            for idx, img_id in enumerate(order_list):
                CarImage.objects.filter(id=img_id, car=car).update(order=idx)
        return redirect('car_image_management', car_id=car.id)
    images = car.images.all()
    return render(request, 'vendors/car_image_management.html', {'car': car, 'images': images})
