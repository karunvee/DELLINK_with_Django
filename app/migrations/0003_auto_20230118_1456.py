# Generated by Django 3.2.15 on 2023-01-18 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_linerow'),
    ]

    operations = [
        migrations.AddField(
            model_name='linerow',
            name='line_name',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='linerow',
            name='plant_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
