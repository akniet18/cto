from .models import *
from rest_framework import serializers
from cars.serializers import CarSer
from service.serializers import ServiceSer


class OrderImg(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('get_avatar_url')
    class Meta:
        model = Image
        fields = ('image',)
    def get_avatar_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)

        
class OrderSer(serializers.ModelSerializer):
    car = CarSer()
    service = ServiceSer()
    subservice = ServiceSer()
    order_img = OrderImg(many=True)
    class Meta:
        model = Order
        fields = ('id', 'car', 'about', "service", "subservice", 'owner', 'order_img')


class OrderCreateSer(serializers.Serializer):
    car_id = serializers.IntegerField()
    service_id = serializers.IntegerField()
    subservice_id = serializers.IntegerField()
    # owner_id = serializers.IntegerField()
    about = serializers.CharField()

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
