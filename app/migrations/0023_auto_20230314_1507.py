# Generated by Django 3.2.15 on 2023-03-14 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_auto_20230302_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorCounting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_time', models.DateTimeField()),
                ('error_code', models.CharField(max_length=255)),
                ('error_des', models.CharField(max_length=255)),
                ('error_count', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='linerow',
            name='remote_host',
            field=models.CharField(default='hostname', max_length=255),
        ),
        migrations.AlterField(
            model_name='linerow',
            name='remote_password',
            field=models.CharField(default='12345678', max_length=255),
        ),
    ]
