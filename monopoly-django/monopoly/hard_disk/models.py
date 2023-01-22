from django.db import models
from pc.models import Disk

class DataDisk(models.Model):
    data = models.JSONField('Содержимое диска', null=True)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)