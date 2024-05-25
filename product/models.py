from django.db import models
from core.models import TimeStampedModel
from django.contrib.postgres.fields import JSONField
# Create your models here.


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(
        upload_to='product_images/', blank=True, null=True)
    attributes = JSONField(default=dict)

    def __str__(self):
        return self.name
