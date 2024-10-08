# Generated by Django 5.0.4 on 2024-05-11 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0002_alter_booking_subject_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='isDeleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='booking',
            name='booking_time',
            field=models.CharField(max_length=50),
        ),
    ]
