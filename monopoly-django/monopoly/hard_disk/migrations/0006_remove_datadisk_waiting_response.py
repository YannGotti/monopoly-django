# Generated by Django 4.1.5 on 2023-01-22 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hard_disk', '0005_datadisk_waiting_response'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datadisk',
            name='waiting_response',
        ),
    ]
