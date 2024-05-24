from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel

# Create your models here.


class User(AbstractUser, TimeStampedModel):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    phone_number = models.CharField(max_length=10, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
