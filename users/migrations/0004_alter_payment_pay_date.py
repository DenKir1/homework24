# Generated by Django 5.0.1 on 2024-01-26 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_payment_pay_course_alter_payment_pay_lesson'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='pay_date',
            field=models.DateField(auto_now=True, null=True, verbose_name='Дата оплаты'),
        ),
    ]
