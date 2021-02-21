from .models import *
from rest_framework import serializers
from cars.serializers import CarSer
from service.serializers import ServiceSer


class OrderImg(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_avatar_url')
    class Meta:
        model = Image
        fields = ('id', 'image',)
    def get_avatar_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)

        
class OrderSer(serializers.ModelSerializer):
    car = CarSer(required=False)
    service = ServiceSer(required=False)
    subservice = ServiceSer(required=False)
    order_img = OrderImg(many=True, required=False)
    class Meta:
        model = Order
        fields = ('id', 'car', 'about', "service", "subservice", 'owner', 'order_img', "in_work", 'is_finished')
        read_only_fields = ('id', "in_work", 'is_finished', 'order_img', 'owner')


class OrderCreateSer(serializers.Serializer):
    car_id = serializers.IntegerField()
    service_id = serializers.IntegerField()
    subservice_id = serializers.IntegerField(required=False)
    # owner_id = serializers.IntegerField()
    about = serializers.CharField(required=False)

class CTOSer(serializers.Serializer):
    phone = serializers.CharField()
    cto_name = serializers.CharField()
    cto_logo = serializers.SerializerMethodField('get_avatar_url', read_only=True)

    def get_avatar_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.cto_logo.url)

class OrderRequestSer(serializers.ModelSerializer):
    cto = CTOSer(read_only=True)
    order = OrderSer(read_only=True)
    class Meta:
        model = OrderRequest
        fields = "__all__"


class CreateOrderRequestSer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = ("order", "price", "time")
    


class OrderListSer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Order
        fields = ('id', 'about', 'service', 'subservice')