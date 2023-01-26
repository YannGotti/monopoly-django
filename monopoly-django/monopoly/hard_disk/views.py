from django.shortcuts import render, redirect, HttpResponse
from django.utils.safestring import SafeString
from django.http import JsonResponse
from django.core import serializers
from django.views.generic.base import View
from pc.models import Disk, UserPc
from .models import DataDisk, RequestPc
import os
from pathlib import Path
import time

BASE_DIR = Path(__file__).resolve().parent.parent

class SelectDisk(View):
    def get(self, request, pk):
        try:
            disk = Disk.objects.get(id=pk)
        except Disk.DoesNotExist:
            return render(request, '404.html')

        disk.user_pc.on_active = True
        disk.user_pc.save()
        data = DataDisk.objects.get(disk = disk)
        statePc = RequestPc.objects.filter(disk = disk)

        if (not data): return render(request, '404.html')
        if (not statePc): return render(request, '404.html')


        last_path = ""
        if (data.path == disk.name):
            last_path = disk.name
        else:
            last_path = SelectLastPath(data.path)

        filename = ''
        if (data.path):
            array_path = data.path.split('\\')
            filename = array_path[len(array_path)-2]

        context = {
            'state': statePc[0].state,
            'is_file': statePc[0].is_file,
            'disk' : disk,
            'data' : SafeString(data.data),
            'path' : data.path,
            'last_path' : last_path,
            'pc': disk.user_pc,
            'file_path' : data.file_path,
            'filename': filename
        }

        return render(request, 'disk/disk.html', context = context)


def SelectLastPath(path):
    new_path = ""
    array_path = path.split('\\')
    array_path.pop()
    array_path.pop()

    for p in array_path:
        new_path += f"{p}\\"
    
    return new_path

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

            pc = UserPc.objects.get(name = data.get('pc_name'))

            if (not pc): return HttpResponse('Not Disk')

            disk = Disk.objects.filter(name = data.get('name_disk'), user_pc = pc)

            if (not disk): return HttpResponse('Not Disk')

            data = DataDisk.objects.filter(disk = disk[0])

            if (not data): return HttpResponse('Not Data')

            path = data[0].path

            return HttpResponse(path)

class ClientGetStateRequest(View):
    def get(self, request):
        data = request.GET

        state = bool(int(data.get('state')))
        file_state = bool(int(data.get('file_state')))

        pc = UserPc.objects.get(name = data.get('pc_name'))

        if (not pc): return HttpResponse('Not Disk')

        disk = Disk.objects.filter(name = data.get('name_disk'), user_pc = pc)

        if (not disk): return HttpResponse('Not pc')

        if (RequestPc.objects.filter(disk = disk[0])):
            request_pc = RequestPc.objects.get(disk = disk[0])

            request_pc.state = state
            request_pc.is_file = file_state
            request_pc.save()

            return HttpResponse('RequestState already created')
        
        request_state = RequestPc(state = state, is_file = file_state, disk = disk[0])
        request_state.save()
        return HttpResponse('Ok')

class ClientGetIsFileRequest(View):
    def get(self, request):
        data = request.GET
        is_file = bool(int(data.get('is_file')))

        pc = UserPc.objects.get(name = data.get('pc_name'))

        if (not pc): return HttpResponse('Not Disk')

        disk = Disk.objects.filter(name = data.get('name_disk'), user_pc = pc)

        if (not disk): return HttpResponse('Not pc')

        request_state = RequestPc.objects.get(disk = disk[0])
        request_state.is_file = is_file
        request_state.save()
        return HttpResponse('Ok')

class ClientGetFileData(View):
    def get(self, request):
        data = request.GET

        pc = UserPc.objects.get(name = data.get('pc_name'))

        if (not pc): return HttpResponse('Not Disk')

        disk = Disk.objects.filter(name = data.get('name_disk'), user_pc = pc)

        disk = disk[0]

        if (not disk): return HttpResponse('Not pc')

        requestpc = RequestPc.objects.get(disk = disk)

        if (not requestpc): return HttpResponse('Not pc')

        computer_path = data.get('path')
        data_file = data.get('data_file')

        array_path = computer_path.split('\\')

        filename = array_path[len(array_path)-1]


        path_create_file = os.path.join(BASE_DIR, f'media/files/{disk.user_pc.name}-{filename}')
        site_path = f'media\\files\\{disk.user_pc.name}-{filename}'

        if (not os.path.exists(path_create_file)):
            

            file = open(path_create_file, "w+")
            file.write(data_file)
            file.close()

        requestpc.state = True
        requestpc.save()


        data_disk = DataDisk.objects.get(disk = disk)
        if (not data_disk): return HttpResponse('Not pc')
        data_disk.file_path = site_path
        data_disk.save()


        return HttpResponse(path_create_file)

class GetPathFolder(View):
    def get(self, request, pk):
        data = request.GET

        disk = Disk.objects.filter(id = pk)

        if (not disk): return HttpResponse('Not Disk')

        data_disk = DataDisk.objects.filter(disk = disk[0])

        if (not data_disk): return HttpResponse('Not Data')

        state = RequestPc.objects.filter(disk = disk[0])

        if (not state): return HttpResponse('Not Data')

        state[0].state = False
        state[0].save()

        filename = data.get('filename')


        if (filename == '..' or filename == '..\\'): 
            new_path = ""

            array_path = data_disk[0].path.split('\\')
            array_path.pop()
            array_path.pop()

            for p in array_path:
                new_path += f"{p}\\"

            data_disk[0].path = new_path
            data_disk[0].save()

            return redirect(f"/disk/{pk}")

        if (filename == '.'): 
            return redirect(f"/disk/{pk}")


        data_disk[0].path += filename + '\\'
        data_disk[0].save()

        return redirect(f"/disk/{pk}")

class MainFolderSelect(View):
    def get(self, request, pk):
        data = request.GET
        path = data.get('path')

        disk = Disk.objects.get(id = pk)
        if (not disk): return HttpResponse('Not Disk')

        data_disk = DataDisk.objects.get(disk = disk)
        if (not data_disk): return HttpResponse('Not Data')

        state = RequestPc.objects.get(disk = disk)
        if (not data_disk): return HttpResponse('Not state')

        if (path == "" or path == disk.name[0] or path == f"{disk.name[0]}:" or len(path) < 3):
            data_disk.path = disk.name
            data_disk.save()
            state.state = False
            state.save()
            return redirect(f"/disk/{pk}")
        
        if (path[len(path)-1] != "\\"):
            path += "\\"

        data_disk.path = path

        default_path = ""

        i = 0
        while(i < 3):
            default_path += path[i]
            i += 1

        if (default_path != disk.name):
            data_disk.path = disk.name

        state.state = False
        state.save()
        data_disk.save()
        return redirect(f"/disk/{pk}")