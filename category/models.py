from django.db import models
from core.models import TimeStampedModel

# Create your models here.


class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='category', blank=True, null=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')

    def __str__(self):
        return self.name

    def get_full_path(self):
        if self.parent:
            return f'{self.parent.get_full_path()} > {self.name}'
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ('name', 'parent')
