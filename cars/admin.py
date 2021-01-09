from django.contrib import admin
from .models import *

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "brand")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "year", "size", 'milage')


admin.site.register(Image)

