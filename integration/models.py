from django.db import models
from utils.models import BaseModel
from phonenumber_field.modelfields import PhoneNumberField


class Employee(BaseModel):
    id = models.UUIDField(editable=False, primary_key=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone = PhoneNumberField(unique=True)
    avatar = models.ImageField(upload_to="employee/", null=True, blank=True)

    def __str__(self):
        return self.first_name
