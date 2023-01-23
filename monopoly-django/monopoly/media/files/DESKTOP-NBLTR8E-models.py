from django.db import models
from pc.models import Disk, UserPc

class DataDisk(models.Model):
    path = models.CharField("Текущий путь", max_length=350)
    data = models.JSONField('Содержимое диска', null=True)
    file_path = models.CharField("Текущий путь файла", max_length=350, null=True)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)

class RequestPc(models.Model):
    state = models.BooleanField("Ответил ли", default=False)
    is_file = models.BooleanField("Файл ли", default=False)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)
