# Generated by Django 5.1.1 on 2024-10-01 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0002_category_product_pricehistory_productimage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
    ]
