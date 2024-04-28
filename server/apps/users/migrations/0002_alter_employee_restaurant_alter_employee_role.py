# Generated by Django 4.2 on 2024-04-28 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='restaurants.restaurant', verbose_name='Ресторан'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(choices=[('WAITER', 'Официант'), ('COOK', 'Повар'), ('CHEF', 'Шеф-повар'), ('SOUS_CHEF', 'Су-Шеф'), ('MANAGER', 'Управляющий'), ('HOSTESS', 'Хостес')], max_length=64, verbose_name='Роль'),
        ),
    ]
