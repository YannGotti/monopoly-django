from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.core import serializers
from django.views.generic.base import View
from .models import UserPc, Disk
from .form import PCForms

class ShowAllPc(View):
    '''вывод'''
    def get(self, request):
        data = UserPc.objects.all
        return render(request, 'pc/index.html', {'data': data})

class AddPc(View):
    '''добавить комп'''
    def post(self, request):
        form = PCForms(request.POST)
        
        if not form.is_valid():
            return redirect('/')

        form = form.save(commit=False)
        pc = UserPc.objects.filter(name = form.name)

        if len(pc) != 0:
            form.name = form.name + " (copy)"

        form.save()
        return HttpResponse('Ok')

class ClietAddPc(View):
    def get(self, request):
        
        data = request.GET

        pc = UserPc(
                name=data.get("name"),
                ip=data.get("ip"),
                mac_adress=data.get("mac_adress"),
                description=data.get("description")
            )

        if (UserPc.objects.filter(name = data.get("name"))):
            return HttpResponse('PC already created')

        pc.save()
        return HttpResponse('Ok')

class ClientAddHardDrive(View):
    def get(self, request):
        
        data = request.GET

        pc = UserPc.objects.filter(name = data.get("pc_name"))

        disk = Disk(
                name=data.get("name")
            )

        disk.user_pc = pc[0]

        if (Disk.objects.filter(name = data.get("name"))):
            return HttpResponse('Disk already have')

        disk.save()
        return HttpResponse('Disk created')

class ClientAddInfoDrive(View):
    def get(self, request):
        data = request.GET

        disk = Disk.objects.filter(name = data.get("name"))

        if (not disk): 
            return HttpResponse('Not disk')

        disk[0].serial_number = data.get("serial_number")
        disk[0].range = data.get("range")
        disk[0].free_range = data.get("free_range")

        disk[0].save()

        return HttpResponse('Ok')

class SelectLastPc(View):
    '''последний комп json'''
    def get(self, request):
        pc = UserPc.objects.all().order_by('-id')[:1]

        return JsonResponse(serializers.serialize('json', pc), safe=False)

class SelectPc(View):
    def get(self, request, pk):

        try:
            pc = UserPc.objects.get(id=pk)
            disks = Disk.objects.filter(user_pc = pk)
        except UserPc.DoesNotExist:
            return render(request, '404.html')

        pc.on_active = False
        pc.save()

        context = {
            'pc': pc,
            'disks' : disks
        }
        return render(request, 'pc/pc.html', context = context)


class DeletePc(View):
    def get(self, request, pk):
        pc = UserPc.objects.get(id=pk)
        pc.delete()
        return JsonResponse({'code': '200'})


class GetKeyPc(View):
    def get(self, request):
        data = request.GET
        return HttpResponse(data.get('key'))