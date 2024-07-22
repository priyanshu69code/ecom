from django.conf import settings
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
    is_seller = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


class SellerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    business_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=20)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return self.business_name


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.otp} for {self.user.email}'
