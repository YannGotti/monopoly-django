# Generated by Django 4.1.5 on 2023-01-21 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pc', '0002_alter_disk_full_name_alter_disk_range_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disk',
            name='full_name',
        ),
        migrations.AddField(
            model_name='disk',
            name='free_range',
            field=models.IntegerField(null=True, verbose_name='Свободный объем диска'),
        ),
    ]
