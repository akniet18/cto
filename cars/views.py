from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from .serializers import *


class CarApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        car = Car.objects.filter(user=request.user)
        s = CarSer(car, many=True)
        return Response(s.data)

    def post(self, request):
        s = CreateCarSer(data=request.data)
        if s.is_valid():
            c = Car.objects.create(
                name = s.validated_data['name'],
                year = s.validated_data['year'],
                size = s.validated_data['size'],
                milage = s.validated_data['milage'],
                user = request.user
            )
            imgs = request.FILES.getlist('images')
            # print(imgs)
            # print(type(s.validated_data['images']), s.validated_data['images'])
            for i in imgs:
                # print(type(i))
                Image.objects.create(
                    image = i, car = c
                )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)

    
    def delete(self, request):
        s = CarIdSer(data=request.data)
        if s.is_valid():
            Car.objects.get(id=s.validated_data['id']).delete()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)



