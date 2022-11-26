# Generated by Django 3.2.16 on 2022-11-11 02:16

import apps.reviews.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review', models.TextField(verbose_name='Текст отзыва')),
                ('mark', models.DecimalField(decimal_places=2, max_digits=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Оценка')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='ReviewImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=apps.reviews.models.get_directory_path, verbose_name='Картинка')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='reviews.review', verbose_name='Отзыв')),
            ],
            options={
                'verbose_name': 'Картинка',
                'verbose_name_plural': 'Картинки',
            },
        ),
    ]
