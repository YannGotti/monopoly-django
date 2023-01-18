from django.shortcuts import render, redirect
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
        return redirect('/')

class SelectPc(View):
    def get(self, request, pk):
        pc = UserPc.objects.get(id=pk)
        disks = Disk.objects.filter(user_pc = pk)
        context = {
            'pc': pc,
            'disks' : disks
        }
        return render(request, 'pc/pc.html', context = context)


class DeletePc(View):
    def get(self, request, pk):
        pc = UserPc.objects.get(id=pk)
        pc.delete()
        UserPc.save
        return redirect('/')

class ShowDataDisk(View):
    def get(self, request, pk):
        disk = Disk.objects.get(id=pk)
        context = {
            'disk' : disk
        }
        return redirect('/')
        #return render(request, 'pc/pc.html', context = context)
