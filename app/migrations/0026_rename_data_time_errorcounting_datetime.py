# Generated by Django 3.2.15 on 2023-03-20 06:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0025_timelinestatus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='errorcounting',
            old_name='data_time',
            new_name='datetime',
        ),
    ]
