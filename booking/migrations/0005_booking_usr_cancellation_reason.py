# Generated by Django 5.0.4 on 2024-05-24 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_alter_booking_booking_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='usr_cancellation_reason',
            field=models.TextField(blank=True),
        ),
    ]
