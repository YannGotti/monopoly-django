# Generated by Django 4.1.5 on 2023-01-18 12:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pc', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userpc',
            options={'verbose_name': 'Компьютер', 'verbose_name_plural': 'Компьютеров'},
        ),
    ]
