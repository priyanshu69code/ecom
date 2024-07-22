from django.db import models
from core.models import TimeStampedModel
from django.conf import settings
from django.contrib.sessions.models import Session
from product.models import Product
from django.core.validators import MaxValueValidator


class Cart(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ManyToManyField('product.Product', through='CartItem')

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    def add_item(self, product, quantity=1):
        item, created = self.items.get_or_create(
            product=product, defaults={'quantity': quantity})
        if not created:
            item.quantity += quantity
            item.save()

    def remove_item(self, product):
        self.items.filter(product=product).delete()

    def update_item(self, product, quantity):
        item = self.items.get(product=product)
        if quantity == 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items',
                             on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(
        default=1, validators=[MaxValueValidator(4)])

    @property
    def total_price(self):
        return self.quantity * self.product.price
