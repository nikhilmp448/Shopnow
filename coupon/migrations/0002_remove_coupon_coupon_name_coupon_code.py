# Generated by Django 4.0.4 on 2022-06-07 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='coupon_name',
        ),
        migrations.AddField(
            model_name='coupon',
            name='code',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
