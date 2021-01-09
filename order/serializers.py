from .models import *
from rest_framework import serializers
from cars.serializers import CarSer
from service.serializers import ServiceSer

class OrderSer(serializers.ModelSerializer):
    car = CarSer()
    service = ServiceSer()
    subservice = ServiceSer()
    class Meta:
        model = Order
        fields = ('id', 'car', 'about', "service", "subservice", 'owner')


class OrderCreateSer(serializers.Serializer):
    car_id = serializers.IntegerField()
    service_id = serializers.IntegerField()
    subservice_id = serializers.IntegerField()
    # owner_id = serializers.IntegerField()
    about = serializers.CharField()


class OrderRequestSer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = "__all__"
