from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from cars.models import Car
from users.models import User
from service.models import Service, SubService
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from .serializers import *
import random
from django.core.mail import send_mail
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from utils.compress import compress_image, base64img
from rest_framework import filters


class OrderApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        orders=Order.objects.filter(is_finished=False, in_work=False)
        s = OrderSer(orders, many=True)
        return Response(s.data)

    def post(self, request):
        s = OrderCreateSer(data=request.data)
        if s.is_valid():
            Order.objects.create(
                car = Car.objects.get(id=s.validated_data['car_id']),
                about = s.validated_data['about'],
                service = Service.objects.get(id=s.validated_data['service_id']),
                subservice = SubService.objects.get(id=s.validated_data['subservice_id']),
                owner = request.user
            )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class CreateOrderRequestApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = OrderRequestSer(data=request.data)
        if s.is_valid():
            OrderRequest.objects.create(
                order = s.validated_data['order'],
                price = s.validated_data['price'],
                time = s.validated_data['time']
            )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class OrderRequestApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, id):
        orq = OrderRequest.objects.filter(order=id)
        s = OrderRequestSer(orq, many=True)
        return Response(s.data)