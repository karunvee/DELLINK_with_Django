# Generated by Django 3.2.15 on 2023-03-20 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_rename_errorcounting_errorhistory'),
    ]

    operations = [
        migrations.RenameField(
            model_name='errorhistory',
            old_name='error_des',
            new_name='error_message',
        ),
        migrations.RemoveField(
            model_name='errorhistory',
            name='error_count',
        ),
    ]