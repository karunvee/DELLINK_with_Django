# Generated by Django 3.2.15 on 2023-01-20 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_linerow_picturepath'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linerow',
            name='picturePath',
            field=models.ImageField(default='app/static/img/default.png', upload_to='images/'),
        ),
    ]
