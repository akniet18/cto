from .models import *
from rest_framework import serializers

class CarImg(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image',)

class CarSer(serializers.ModelSerializer):
    car_img = CarImg(many=True)
    class Meta:
        model = Car
        fields = "__all__"
        read_only_fields = ("owner",)

class CreateCarSer(serializers.Serializer):
    name = serializers.CharField()
    year = serializers.IntegerField()
    size = serializers.FloatField()
    milage = serializers.FloatField()
    # images = CarImg(many=True)
