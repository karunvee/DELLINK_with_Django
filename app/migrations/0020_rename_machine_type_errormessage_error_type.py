# Generated by Django 3.2.15 on 2023-04-18 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20230418_0837'),
    ]

    operations = [
        migrations.RenameField(
            model_name='errormessage',
            old_name='machine_type',
            new_name='error_type',
        ),
    ]