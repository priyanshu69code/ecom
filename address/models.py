from django.db import models
from core.models import TimeStampedModel
from django.conf import settings
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
# Create your models here.


class Address(TimeStampedModel):
    ADDRESS_TYPE = (
        ('home', 'Home'),
        ('office', 'Office'),
        ('other', 'Other'),
    )

    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    phone1 = models.CharField(max_length=10, validators=[
                              RegexValidator(r'^[0-9]+$')])
    phone2 = models.CharField(max_length=10, validators=[
                              RegexValidator(r'^[0-9]+$')])
    type = models.CharField(max_length=10, choices=ADDRESS_TYPE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    country = CountryField(default='IN')

    def __str__(self):
        return self.address
