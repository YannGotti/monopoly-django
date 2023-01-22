from django.shortcuts import render, redirect, HttpResponse
from django.utils.safestring import SafeString
from django.http import JsonResponse
from django.core import serializers
from django.views.generic.base import View
from pc.models import Disk, UserPc
from .models import DataDisk, RequestPc



class SelectDisk(View):
    def get(self, request, pk):

        try:
            disk = Disk.objects.get(id=pk)
        except Disk.DoesNotExist:
            return render(request, '404.html')

        data = DataDisk.objects.filter(disk = disk)
        statePc = RequestPc.objects.filter(disk = disk)

        if (not data): return render(request, '404.html')
        if (not statePc): return render(request, '404.html')

        context = {
            'state': statePc[0].request,
            'disk' : disk,
            'data' : SafeString(data[0].data),
            'path' : data[0].path,
            'pc': disk.user_pc
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
            disk_data = DataDisk(data=data.get('data'), path=data.get('path'))
            disk_data.disk = disk[0]
            disk_data.save()
            return HttpResponse('Ok')

        if (current_data[0].data != data.get('data')):
            current_data[0].data = data.get('data')
            current_data[0].save()
            return HttpResponse('Ok')
  
class ClientGetRequest(View):
        def get(self, request):
            data = request.GET

            disk = Disk.objects.filter(name = data.get('name_disk'))

            if (not disk): return HttpResponse('Not Disk')

            data = DataDisk.objects.filter(disk = disk[0])

            if (not data): return HttpResponse('Not Data')

            path = data[0].path

            return HttpResponse(path)

class ClientGetStateRequest(View):
    def get(self, request):
        data = request.GET

        state = bool(int(data.get('state')))

        disk = Disk.objects.filter(name = data.get('name_disk'))

        if (not disk): return HttpResponse('Not pc')

        if (RequestPc.objects.filter(disk = disk[0])):
            request_pc = RequestPc.objects.get(disk = disk[0])

            request_pc.request = state
            request_pc.save()

            return HttpResponse('RequestState already created')
        
        state = RequestPc(request = state, disk = disk[0])
        state.save()
        return HttpResponse('Ok')


class GetPathFolder(View):
    def get(self, request, pk):
        data = request.GET

        disk = Disk.objects.filter(id = pk)

        if (not disk): return HttpResponse('Not Disk')

        data_disk = DataDisk.objects.filter(disk = disk[0])

        if (not data_disk): return HttpResponse('Not Data')

        state = RequestPc.objects.filter(disk = disk[0])

        if (not state): return HttpResponse('Not Data')

        state[0].request = False
        state[0].save()

        data_disk[0].path += data.get('filename') + '\\'
        data_disk[0].save()

        return redirect(f"/disk/{pk}")

class MainFolderSelect(View):
    def get(self, request, pk):
        disk = Disk.objects.get(id = pk)
        if (not disk): return HttpResponse('Not Disk')

        data_disk = DataDisk.objects.get(disk = disk)
        if (not data_disk): return HttpResponse('Not Data')

        state = RequestPc.objects.get(disk = disk)
        if (not data_disk): return HttpResponse('Not state')

        data_disk.path = disk.name
        state.request = False
        state.save()
        data_disk.save()
        return redirect(f"/disk/{pk}")
