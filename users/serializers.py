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
    phone = serializers.CharField(required=False)
    class Meta:
        model = User
        fields = ('id', 'phone', 'avatar', 'email', 'nickname', 'second_phone', 'third_phone')
        read_only_fields = ('id', )

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


class Idser(serializers.Serializer):
    id = serializers.IntegerField()




    