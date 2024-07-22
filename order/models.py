from django.db import models
from core.models import TimeStampedModel
from django.conf import settings
from django.contrib.sessions.models import Session
# Create your models here.


class Order(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField('product.Product', through='OrderItem')
    status = models.CharField(max_length=255, default='pending')
    address = models.ForeignKey(
        'address.Address', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Order {self.id}'

    @property
    def calculate_total(self):
        total = 0
        for item in self.items.all():
            total += item.total_price
        return total

    def cancel(self):
        self.status = 'cancelled'
        for item in self.items.all():
            item.product.add_stock(item.quantity)
        self.items.all().delete()

        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price
