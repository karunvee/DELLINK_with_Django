# Generated by Django 3.2.15 on 2023-04-11 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_errortype_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='UtilizationRatePerDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_name', models.CharField(max_length=255)),
                ('line_name', models.CharField(max_length=255)),
                ('machine_name', models.CharField(max_length=255)),
                ('datetime', models.CharField(max_length=255)),
                ('rate', models.IntegerField()),
            ],
        ),
    ]
