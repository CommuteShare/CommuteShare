# Generated by Django 4.2.1 on 2023-06-07 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commute_share', '0003_remove_drivermodel_car_remove_drivermodel_company_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='available_seats',
        ),
        migrations.RemoveField(
            model_name='books',
            name='departure_location',
        ),
        migrations.RemoveField(
            model_name='books',
            name='departure_time',
        ),
        migrations.RemoveField(
            model_name='books',
            name='destination_location',
        ),
        migrations.RemoveField(
            model_name='books',
            name='driver',
        ),
        migrations.RemoveField(
            model_name='books',
            name='price',
        ),
        migrations.AddField(
            model_name='books',
            name='create_ride',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='commute_share.createride'),
            preserve_default=False,
        ),
    ]
