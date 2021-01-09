from .models import *
from rest_framework import serializers


class CarSer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"
        read_only_fields = ("owner",)