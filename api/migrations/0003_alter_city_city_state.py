# Generated by Django 5.0.4 on 2024-04-15 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_subjects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='city_state',
            field=models.CharField(max_length=20),
        ),
    ]
