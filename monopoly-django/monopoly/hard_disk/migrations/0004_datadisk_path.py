# Generated by Django 4.1.5 on 2023-01-22 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hard_disk', '0003_remove_datadisk_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='datadisk',
            name='path',
            field=models.CharField(default='c:\\', max_length=50, verbose_name='Текущий путь'),
            preserve_default=False,
        ),
    ]
