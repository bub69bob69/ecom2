# Generated by Django 5.0.3 on 2024-06-27 09:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paymentapp', '0003_alter_shippingaddress_shipping_address2_order_and_more'),
        ('storeapp', '0004_profile_old_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrdetItem',
            new_name='OrderItem',
        ),
    ]
