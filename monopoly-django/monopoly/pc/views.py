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

class ShowDataDisk(View):
    def get(self, request, pk, pc):
        try:
            disk = Disk.objects.get(id=pk)
        except Disk.DoesNotExist:
            return render(request, '404.html')

        context = {
            'disk': disk
        }

        return redirect(f'/pc/{pc}/')