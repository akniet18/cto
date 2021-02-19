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
        s = OrderSer(orders, many=True, context={'request': request})
        return Response(s.data)

    def post(self, request):
        s = OrderCreateSer(data=request.data)
        if s.is_valid():
            order = Order.objects.create(
                car = Car.objects.get(id=s.validated_data['car_id']),
                about = s.validated_data['about'],
                service = Service.objects.get(id=s.validated_data['service_id']),
                subservice = SubService.objects.get(id=s.validated_data['subservice_id']),
                owner = request.user
            )
            imgs = request.FILES.getlist('images')
            for i in imgs:
                Image.objects.create(
                    image=i, order=order
                )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class CreateOrderRequestApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = CreateOrderRequestSer(data=request.data)
        if s.is_valid():
            OrderRequest.objects.create(
                cto = request.user,
                order = s.validated_data['order'],
                price = s.validated_data['price'],
                time = s.validated_data['time']
            )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class OrderRequestApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        orq = OrderRequest.objects.filter(order__owner=request.user)
        s = OrderRequestSer(orq, many=True, context={'request': request})
        return Response(s.data)


class RequestDecline(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        queryset = OrderRequest.objects.get(id=id)
        queryset.delete()
        return Response({'status': 'ok'})


class RequestAccept(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        queryset = OrderRequest.objects.get(id=id)
        queryset.order.in_work = True
        queryset.order.price = queryset.price
        queryset.order.cto = queryset.cto
        queryset.order.save()
        return Response({'status': 'ok'})

class History(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        order = Order.objects.filter(is_finished=True, owner=request.user)
        s = OrderSer(order, many=True, context={'request': request})
        return Response(s.data)

class OrderList(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        queryset = Order.objects.filter(is_finished=False)
        s = OrderSer(queryset, many=True, context={'request': request})
        return Response(s.data)
    
    def put(self, request):
        s = OrderListSer(data=request.data)
        if s.is_valid():
            order = Order.objects.get(id=s.validated_data['id'])
            order.about = s.validated_data['about']
            order.service = s.validated_data.get('service', order.service)
            order.subservice = s.validated_data.get('subservice', order.subservice)
            order.save()
            ser = OrderSer(order, context={'request': request})
            return Response(ser.data)
        else:
            return Response(s.errors)

    def delete(self, request):
        s = OrderListSer(data=request.data)
        if s.is_valid():
            Order.objects.get(id=s.validated_data['id']).delete()
            return Response({'status':'ok'})
        else:
            return Response(s.errors)


class OrderImgDelete(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        OrderImg.objects.get(id=id).delete()
        return Response({'status': 'ok'})
