from django.db import models
from pc.models import Disk, UserPc

class DataDisk(models.Model):
    path = models.CharField("Текущий путь", max_length=350)
    data = models.JSONField('Содержимое диска', null=True)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)

class RequestPc(models.Model):
    request = models.BooleanField("Ответил ли", default=False)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)