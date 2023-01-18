from django.contrib import admin
from .models import UserPc

@admin.register(UserPc)
class PcAdmin(admin.ModelAdmin):
    list_display = ('name', 'mac_adress')