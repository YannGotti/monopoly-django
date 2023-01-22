from django.shortcuts import render, redirect, HttpResponse
from django.utils.safestring import SafeString
from django.http import JsonResponse
from django.core import serializers
from django.views.generic.base import View
from pc.models import Disk
from .models import DataDisk



class SelectDisk(View):
    def get(self, request, pk):

        try:
            disk = Disk.objects.get(id=pk)
        except Disk.DoesNotExist:
            return render(request, '404.html')

        data = DataDisk.objects.filter(disk = disk)

        context = {
            'data' : SafeString(data[0].data)
        }

        return render(request, 'disk/disk.html', context = context)

class ClientDataDisk(View):
    def get(self, request):
        data = request.GET

        if (DataDisk.objects.filter(data = data.get('data'))):
            return HttpResponse('Data already created')

        disk = Disk.objects.filter(serial_number = data.get('serial_number'))

        if (not disk):
            return HttpResponse('Disk not found')

        current_data = DataDisk.objects.filter(disk = disk[0])

        if (not current_data):
            disk_data = DataDisk(data=data.get('data'))
            disk_data.disk = disk[0]
            disk_data.save()
            return HttpResponse('Ok')

        if (current_data[0].data != data.get('data')):
            current_data[0].data = data.get('data')
            current_data[0].save()
            return HttpResponse('Ok')
  

        

