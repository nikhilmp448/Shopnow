# Generated by Django 4.0.4 on 2022-06-19 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0002_remove_coupon_coupon_name_coupon_code'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Coupon',
        ),
    ]
