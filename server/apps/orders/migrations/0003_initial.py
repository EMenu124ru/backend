# Generated by Django 3.2.16 on 2022-12-09 13:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0002_initial'),
        ('users', '0001_initial'),
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='users.client', verbose_name='Клиент'),
        ),
        migrations.AddField(
            model_name='order',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='users.employee', verbose_name='Сотрудник'),
        ),
        migrations.AddField(
            model_name='dishimages',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='orders.dish', verbose_name='Блюдо'),
        ),
        migrations.AddField(
            model_name='dish',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='orders.category', verbose_name='Категория'),
        ),
        migrations.AddField(
            model_name='dish',
            name='reviews',
            field=models.ManyToManyField(related_name='dish', to='reviews.Review', verbose_name='Отзыв'),
        ),
    ]
