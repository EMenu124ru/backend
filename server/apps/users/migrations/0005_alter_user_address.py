# Generated by Django 4.2 on 2024-03-10 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_employee_medical_checkup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.TextField(blank=True, default='', verbose_name='Адрес проживания'),
        ),
    ]