# Generated by Django 3.2.15 on 2023-01-31 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_indicator'),
    ]

    operations = [
        migrations.CreateModel(
            name='ErrorNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error_code', models.CharField(max_length=255)),
                ('error_message', models.CharField(max_length=255)),
                ('tag_member', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.indicator')),
            ],
        ),
    ]
