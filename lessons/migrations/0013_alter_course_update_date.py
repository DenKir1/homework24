# Generated by Django 4.2.10 on 2024-02-29 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lessons', '0012_course_update_date_alter_course_public_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='update_date',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления'),
        ),
    ]