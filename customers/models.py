from django.db import models
from django.contrib.auth import get_user_model
import uuid
from core.models import BaseModel

User = get_user_model()

class Customer(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.get_username()
