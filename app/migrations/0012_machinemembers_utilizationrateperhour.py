# Generated by Django 3.2.15 on 2023-04-17 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_utilizationrateperday_datetime'),
    ]

    operations = [
        migrations.CreateModel(
            name='MachineMembers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plant_name', models.CharField(max_length=255)),
                ('line_name', models.CharField(max_length=255)),
                ('machine_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UtilizationRatePerHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField()),
                ('rate', models.IntegerField()),
                ('machineInfo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.machinemembers')),
            ],
        ),
    ]
