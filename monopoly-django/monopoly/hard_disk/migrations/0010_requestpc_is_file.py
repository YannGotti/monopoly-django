# Generated by Django 4.1.5 on 2023-01-23 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hard_disk', '0009_remove_requestpc_pc_requestpc_disk'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestpc',
            name='is_file',
            field=models.BooleanField(default=False, verbose_name='Файл ли'),
        ),
    ]
