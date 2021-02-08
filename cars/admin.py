from django.contrib import admin
from .models import *
from django import forms

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', "brand")

class CarImage(admin.TabularInline):
    model = Image

# @admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [CarImage]
    list_display = ('id', 'name', "year", "size", 'milage')


admin.site.register(Car, CarAdmin)
admin.site.register(Image)

