from django.db import models
from vendors.models import Vendor, Car
from core.models import BaseModel


class RentalStat(BaseModel):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='rental_stats')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='rental_stats', null=True, blank=True)
    date = models.DateField()
    rentals_count = models.PositiveIntegerField(default=0)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        car_str = f" - {self.car}" if self.car else ""
        return f"Stats for {self.vendor}{car_str} on {self.date}"
