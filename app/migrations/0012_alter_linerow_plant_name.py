# Generated by Django 3.2.15 on 2023-01-25 07:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20230125_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linerow',
            name='plant_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.plantinfo'),
        ),
    ]
