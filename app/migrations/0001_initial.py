# Generated by Django 3.2.15 on 2023-01-10 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlantInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('detail', models.CharField(max_length=255)),
                ('ip1', models.CharField(max_length=255)),
                ('port1', models.CharField(max_length=255)),
                ('ip2', models.CharField(blank=True, max_length=255)),
                ('port2', models.CharField(blank=True, max_length=255)),
                ('ip3', models.CharField(blank=True, max_length=255)),
                ('port3', models.CharField(blank=True, max_length=255)),
                ('ip4', models.CharField(blank=True, max_length=255)),
                ('port4', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
