# Generated by Django 5.0.1 on 2024-02-24 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0007_alter_subscribe_options_payment_pay_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price_course',
            field=models.FloatField(blank=True, null=True, verbose_name='Цена'),
        ),
    ]
