from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import UserPc
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
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
        return redirect('/')

class SelectPc(View):
    def get(self, request, pk):
        pc = UserPc.objects.get(id=pk)
        context = {
            'title': 'Пиздес',
            'pc': pc
        }
        return render(request, 'pc/pc.html', context = context)


class DeletePc(View):
    def get(self, request, pk):
        pc = UserPc.objects.get(id=pk)
        pc.delete()
        UserPc.save
        return redirect('/')
