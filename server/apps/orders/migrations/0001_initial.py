# Generated by Django 3.2.16 on 2023-03-10 06:18

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import apps.orders.models.dish_image
import apps.orders.models.restaurant_and_order


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Полное описание')),
                ('short_description', models.TextField(verbose_name='Краткое описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('compound', models.TextField(verbose_name='Состав')),
                ('weight', models.DecimalField(decimal_places=3, max_digits=11, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Вес блюда')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
        migrations.CreateModel(
            name='DishImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.orders.models.dish_image.get_directory_path, verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Картинка блюда',
                'verbose_name_plural': 'Картинки блюд',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(choices=[('WAITING_FOR_COOKING', 'Передано на кухню'), ('COOKING', 'Готовится'), ('WAITING_FOR_DELIVERY', 'Ожидает доставки/готово к выдаче'), ('IN_PROCESS_DELIVERY', 'В процессе доставки'), ('DELIVERED', 'Доставлен'), ('FINISHED', 'Закрыт'), ('CANCELED', 'Отменен'), ('PAID', 'Оплачен')], default='WAITING_FOR_COOKING', verbose_name='Статус заказа')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('comment', models.TextField(default='', verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderAndDish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(choices=[('WAITING_FOR_COOKING', 'Ожидает готовки'), ('COOKING', 'Готовится'), ('DONE', 'Готово'), ('CANCELED', 'Отменен'), ('DELIVERED', 'Выдано')], default='WAITING_FOR_COOKING', verbose_name='Статус блюда')),
                ('comment', models.TextField(default='', verbose_name='Комментарий')),
            ],
            options={
                'verbose_name': 'Заказ и блюдо',
                'verbose_name_plural': 'Заказы и блюда',
            },
        ),
        migrations.CreateModel(
            name='RestaurantAndOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.DateTimeField(validators=[apps.orders.models.restaurant_and_order.validate_arrival_time], verbose_name='Время прибытия')),
                ('place_number', models.PositiveIntegerField(verbose_name='Номер места')),
            ],
            options={
                'verbose_name': 'Ресторан и заказ',
                'verbose_name_plural': 'Ресторан и заказы',
            },
        ),
        migrations.CreateModel(
            name='StopList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stop_list', to='orders.dish', verbose_name='Блюда')),
            ],
            options={
                'verbose_name': 'Стоп лист ресторана',
                'verbose_name_plural': 'Стоп листы ресторанов',
            },
        ),
    ]
