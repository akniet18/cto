from .models import *
from rest_framework import serializers

class PhoneS(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    nickname = serializers.CharField(required=False)

class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar_url', read_only=True)
    class Meta:
        model = User
        fields = ('id', 'phone', 'avatar', 'email', 'nickname', 'second_phone', 'third_phone')
        read_only_fields = ('id', 'phone')

    def get_avatar_url(self, obj):
        return self.context['request'].build_absolute_uri(obj.avatar.url)


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