# Generated by Django 4.2 on 2024-05-11 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_reservation_count_quests_reservation_tag_to_place_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='comment',
            field=models.TextField(default='', verbose_name='Комментарий'),
        ),
        migrations.AlterField(
            model_name='orderanddish',
            name='comment',
            field=models.TextField(default='', verbose_name='Комментарий'),
        ),
    ]
