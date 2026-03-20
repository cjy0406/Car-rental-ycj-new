from django.db import models
from django.contrib.auth import get_user_model
import uuid
from core.models import BaseModel
from PIL import Image
import os
from django.utils import timezone

User = get_user_model()

class Vendor(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

def car_image_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    from uuid import uuid4
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('car_images', filename)

class Car(BaseModel):
    CAR_TYPE_CHOICES = [
        ('sedan', '轿车'),
        ('suv', 'SUV'),
        ('hatchback', '掀背车'),
        ('convertible', '敞篷车'),
        ('van', '厢式车'),
        ('truck', '卡车'),
        ('other', '其他'),
    ]
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to=car_image_upload_to, blank=True, null=True)
    car_type = models.CharField(max_length=20, choices=CAR_TYPE_CHOICES)
    model_year = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.model_year})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            img = img.convert('RGB')
            img = img.resize((800, 500), Image.LANCZOS)
            img.save(self.image.path, format='JPEG', quality=80, optimize=True)

class CarImage(BaseModel):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=car_image_upload_to)
    order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Image for {self.car.name}"
    class Meta:
        ordering = ['order', 'created_at']


class WithdrawalRequest(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('paid', 'Paid'),
    ]
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='withdrawals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Withdrawal {self.amount} by {self.vendor}"