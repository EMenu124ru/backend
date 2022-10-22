# Generated by Django 3.2.16 on 2022-10-22 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reviews', '0001_initial'),
        ('restaurants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='reviews',
            field=models.ManyToManyField(related_name='restaurant', to='reviews.Review', verbose_name='Отзыв'),
        ),
    ]
