# Generated by Django 4.2.1 on 2023-05-30 12:31

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('commute_share', '0002_createride_driver'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckDrivers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_color', models.CharField(max_length=10)),
                ('car_plate_number', models.CharField(max_length=7)),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('destination_location', models.CharField(max_length=100)),
                ('departure_time', models.TimeField(max_length=100)),
                ('available_seats', models.IntegerField()),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='commute_share.drivermodel')),
            ],
        ),
    ]
