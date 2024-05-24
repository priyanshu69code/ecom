from django.db import models
from core.models import TimeStampedModel

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
    phone1 = models.CharField(max_length=10)
    phone2 = models.CharField(max_length=10)
    type = models.CharField(max_length=10, choices=ADDRESS_TYPE)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.address
