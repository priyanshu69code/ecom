from django.db import models
from core.models import TimeStampedModel
from django.db.models import JSONField
# Create your models here.


class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        'category.Category', on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(
        upload_to='product_images/', blank=True, null=True)
    attributes = JSONField(default=dict, blank=True, null=True)
    seller = models.ForeignKey(
        'user.SellerProfile', on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    def add_stock(self, quantity):
        self.stock += quantity
        self.save()

    def remove_stock(self, quantity):
        self.stock -= quantity
        self.save()


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product.name
