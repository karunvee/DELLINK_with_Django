# Generated by Django 3.2.15 on 2023-03-28 01:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_timelinestartend'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelinestartend',
            name='end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='timelinestartend',
            name='start',
            field=models.DateTimeField(),
        ),
    ]