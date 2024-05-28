from django.db import models
from django.conf import settings
from core.models import TimeStampedModel


class List(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='lists')
    products = models.ManyToManyField('product.Product')

    def __str__(self):
        return self.name


class WiseList(List):
    def save(self, *args, **kwargs):
        if not self.id:  # Only set the default name if the object is new
            self.name = "Wise List"
        super().save(*args, **kwargs)
