# Generated by Django 4.2.1 on 2023-06-27 10:26

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0003_alter_slider_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='discountcode',
            name='used_by',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL, verbose_name='استفاده شده توسط'),
        ),
    ]
