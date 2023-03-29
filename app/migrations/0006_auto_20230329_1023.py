# Generated by Django 3.2.15 on 2023-03-29 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_errormessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_type', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='errornotification',
            name='error_code',
        ),
        migrations.RemoveField(
            model_name='errornotification',
            name='error_message',
        ),
        migrations.AddField(
            model_name='errormessage',
            name='error_code',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='errornotification',
            name='error_msg',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='error_msg', to='app.errormessage'),
        ),
        migrations.AlterField(
            model_name='errormessage',
            name='machine_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.errortype'),
        ),
    ]
