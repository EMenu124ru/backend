# Generated by Django 3.2.16 on 2023-10-22 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='surname',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество'),
        ),
    ]
