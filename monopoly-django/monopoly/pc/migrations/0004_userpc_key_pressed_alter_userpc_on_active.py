# Generated by Django 4.1.5 on 2023-01-25 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pc', '0003_remove_disk_full_name_disk_free_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpc',
            name='key_pressed',
            field=models.CharField(default='s', max_length=50, verbose_name='Вводимый символ'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userpc',
            name='on_active',
            field=models.BooleanField(default=False, verbose_name='Используется ли'),
        ),
    ]
