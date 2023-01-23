from django.db import models
from pc.models import Disk, UserPc

class DataDisk(models.Model):
    path = models.CharField("������� ����", max_length=350)
    data = models.JSONField('���������� �����', null=True)
    file_path = models.CharField("������� ���� �����", max_length=350, null=True)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)

class RequestPc(models.Model):
    state = models.BooleanField("������� ��", default=False)
    is_file = models.BooleanField("���� ��", default=False)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)
