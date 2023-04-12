# Generated by Django 3.2.16 on 2023-04-12 12:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0002_restaurant_reviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.TextField(verbose_name='План ресторана')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='restaurants.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'План ресторана',
                'verbose_name_plural': 'Планы ресторанов',
            },
        ),
    ]