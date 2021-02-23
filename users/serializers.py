from .models import *
from rest_framework import serializers

class PhoneS(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    nickname = serializers.CharField(required=False)

class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField()


class LoginAdminSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=15)


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar_url', read_only=True)
    phone = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ('id', 'phone', 'avatar', 'email', 'nickname', 'second_phone', 'third_phone', "cto_name", "cto_logo", "cto_address")
        read_only_fields = ('id', "cto_name", "cto_logo", "cto_address")

    def get_avatar_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.avatar.url)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.second_phone = validated_data.get('second_phone', instance.second_phone)
        instance.third_phone = validated_data.get('third_phone', instance.third_phone)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance


class ChangeAvaSer(serializers.Serializer):
    avatar = serializers.FileField(required=False)
    nickname = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    second_phone = serializers.CharField(required=False)
    third_phone = serializers.CharField(required=False)

class CreateCtoSer(serializers.Serializer):
    logo = serializers.FileField(required=False)
    name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    lat = serializers.CharField(required=False)
    lng = serializers.CharField(required=False)


class Idser(serializers.Serializer):
    id = serializers.CharField()


class CTOListSer(serializers.ModelSerializer):
    cto_logo = serializers.SerializerMethodField('get_avatar_url')
    class Meta:
        model = User
        fields = ("id", "cto_id", "cto_name", "cto_logo", "cto_address")

    def get_avatar_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.cto_logo.url)

    def update(self, instance, validated_data):
        instance.cto_name = validated_data.get('cto_name', instance.cto_name)
        instance.cto_logo = validated_data.get('cto_logo', instance.cto_logo)
        instance.cto_address = validated_data.get('cto_address', instance.cto_address)
        instance.save()
        return instance
    

class CTORequestSer(serializers.ModelSerializer):
    class Meta:
        model = CTORequest
        fields = "__all__"