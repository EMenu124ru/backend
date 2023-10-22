# Generated by Django 3.2.16 on 2023-10-22 08:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_initial'),
        ('orders', '0003_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='reservation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='orders.reservation', verbose_name='Бронирование'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='place',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation', to='restaurants.place', verbose_name='Номер места'),
        ),
    ]
