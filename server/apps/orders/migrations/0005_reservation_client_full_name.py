# Generated by Django 4.2 on 2024-06-02 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_rename_count_quests_reservation_count_guests'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='client_full_name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='ФИО клиента'),
        ),
    ]