# Generated by Django 3.2.15 on 2023-01-25 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_linerow_plant_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linerow',
            name='plant_name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]