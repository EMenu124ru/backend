# Generated by Django 4.2 on 2024-03-10 17:09

import apps.core.models.file
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ObjectFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to=apps.core.models.file.get_directory_path, verbose_name='Файл')),
                ('filename', models.TextField(default='unnamed_file', verbose_name='Название файла')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
    ]
