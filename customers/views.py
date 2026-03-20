from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from booking.models import Booking

# Create your views here.

@login_required
def customer_dashboard(request):
    try:
        customer = request.user.customer
    except Exception:
        return redirect('home')
    bookings = Booking.objects.filter(customer=customer).order_by('-created_at')
    return render(request, 'customers/dashboard.html', {
        'customer': customer,
        'bookings': bookings,
    })

@login_required
def booking_cancel(request, booking_id):
    try:
        customer = request.user.customer
    except Exception:
        return redirect('home')
    booking = Booking.objects.filter(id=booking_id, customer=customer).first()
    if not booking or booking.status not in ['pending', 'confirmed']:
        return redirect('customer_dashboard')
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        return redirect('customer_dashboard')
    return render(request, 'customers/booking_cancel.html', {'booking': booking})
