from django.contrib import admin
from .models import UserPc, Disk

@admin.register(UserPc)
class PcAdmin(admin.ModelAdmin):
    list_display = ('name', 'mac_adress')

@admin.register(Disk)
class DiskAdmin(admin.ModelAdmin):
    list_display = ('name', 'serial_number')