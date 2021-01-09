from .models import *
from rest_framework import serializers

class ServiceSer(serializers.Serializer):
    name = serializers.CharField()