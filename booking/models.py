from django.db import models
from django.contrib.auth import get_user_model
from customers.models import Customer
from vendors.models import Car, Vendor
from core.models import BaseModel

User = get_user_model()


class Booking(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    ADMIN_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_status = models.CharField(max_length=20, choices=ADMIN_STATUS_CHOICES, default='pending')
    return_confirmed_at = models.DateTimeField(null=True, blank=True)
    return_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.car} for {self.customer}"


class ReturnRecord(BaseModel):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='return_record')
    confirmed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    confirmed_at = models.DateTimeField(auto_now_add=True)
    condition_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Return for {self.booking_id}"


class Review(BaseModel):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='reviews')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    reply = models.TextField(blank=True)
    replied_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Review {self.rating}/5 for {self.car} by {self.customer}"