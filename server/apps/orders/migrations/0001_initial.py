# Generated by Django 3.2.16 on 2022-11-11 02:24

import apps.orders.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reviews', '0002_review_client'),
        ('users', '0001_initial'),
        ('restaurants', '0002_restaurant_reviews'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Название')),
                ('description', models.TextField(verbose_name='Полное описание')),
                ('short_description', models.TextField(verbose_name='Краткое описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('compound', models.TextField(verbose_name='Состав')),
                ('weight', models.DecimalField(decimal_places=3, max_digits=11, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Вес блюда')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='orders.category', verbose_name='Категория')),
                ('reviews', models.ManyToManyField(related_name='dish', to='reviews.Review', verbose_name='Отзыв')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.TextField(choices=[('WAITING_FOR_COOKING', 'Ожидает готовки'), ('COOKING', 'Готовится'), ('WAITING_FOR_DELIVERY', 'Ожидает доставки'), ('IN_PROCESS_DELIVERY', 'В процессе доставки'), ('DELIVERED', 'Доставлен')], verbose_name='Статус заказа')),
                ('price', models.DecimalField(decimal_places=2, max_digits=11, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Цена')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('place_number', models.PositiveIntegerField(verbose_name='Номер места')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='users.client', verbose_name='Клиент')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='users.employee', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='RestaurantAndOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arrival_time', models.DateTimeField(validators=[apps.orders.models.validate_arrival_time], verbose_name='Время прибытия')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='restaurant_and_order', to='orders.order', verbose_name='Заказ')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='restaurant_and_order', to='restaurants.restaurant', verbose_name='Ресторан')),
            ],
            options={
                'verbose_name': 'Ресторан и заказ',
                'verbose_name_plural': 'Ресторан и заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderAndDishes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='orders.dish', verbose_name='Блюдо')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dishes', to='orders.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Заказ и блюдо',
                'verbose_name_plural': 'Заказы и блюда',
            },
        ),
        migrations.CreateModel(
            name='DishImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.orders.models.get_directory_path, verbose_name='Картинка')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='orders.dish', verbose_name='Блюдо')),
            ],
            options={
                'verbose_name': 'Картинка блюда',
                'verbose_name_plural': 'Картинки блюд',
            },
        ),
    ]
