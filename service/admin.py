from django.contrib import admin
from .models import *

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "service")