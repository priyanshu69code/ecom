# Generated by Django 5.0.6 on 2024-07-20 02:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
        ('product', '0003_product_seller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='attributes',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='category.category'),
        ),
    ]