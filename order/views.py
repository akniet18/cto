from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from cars.models import Car
from users.models import User, Message
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
import requests
from utils.push import send_push

class OrderApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        orders=Order.objects.filter(is_finished=False, in_work=False).exclude(owner=request.user)
        s = OrderSer(orders, many=True, context={'request': request})
        return Response(s.data)

    def post(self, request):
        s = OrderCreateSer(data=request.data)
        if s.is_valid():
            sub_id = s.validated_data.get('subservice_id', None)
            if sub_id:
                sub = SubService.objects.get(id=sub_id)
            else:
                sub = None
            order = Order.objects.create(
                car = Car.objects.get(id=s.validated_data['car_id']),
                about = s.validated_data.get('about', None),
                service = Service.objects.get(id=s.validated_data['service_id']),
                subservice = sub,
                owner = request.user
            )
            imgs = request.FILES.getlist('images')
            for i in imgs:
                Image.objects.create(
                    image=i, order=order
                )
            text = "Ваше объявление опубликовано! Ждите заявок."
            send_push(request.user, text)
            Message.objects.create(
                user = request.user, text = text
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
            text = "На ваше объявление откликнулись"
            send_push(s.validated_data['order'].owner, text)
            Message.objects.create(
                user = s.validated_data['order'].owner, text = text
            )
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


from math import radians, cos, sin, asin, sqrt
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

class OrderRequestApi(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, lat, lng):
        orq = OrderRequest.objects.filter(order__owner=request.user)
        serializer = OrderRequestSer(orq, many=True, context={'request': request})
        # lat = s.validated_data['lat']
        # lng = s.validated_data['lng']
        print(lat, lng)
        dest = ""
        distance = []
        for i in orq:
            # dest += i.cto.cto_lat+","+i.cto.cto_lng+"|"
            a = haversine(lng, lat, i.cto.cto_lng, i.cto.cto_lat)
            distance.append(a)
        # print(orig)
        # origins = f'{lat},{lng}'
        # url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={origins}&destinations={dest}&key=AIzaSyDSQJSfSkaBOGnW94XlDQgn3TzySzfM1W4'
        # print(dest)
        # r = requests.post(url)
        # print(r.json())
        for i in range(len(serializer.data)):
            # serializer.data[i]['distance_text']  = r.json()['rows'][0]['elements'][i]['distance']['text']
            # serializer.data[i]['distance']  = r.json()['rows'][0]['elements'][i]['distance']['value']
            serializer.data[i]['distance_text']  = str(distance[i])
            # serializer.data[i]['duration_text']  = r.json()['rows'][0]['elements'][i]['duration']['text']
            # serializer.data[i]['duration']  = r.json()['rows'][0]['elements'][i]['duration']['value']
        return Response(serializer.data)


class RequestDecline(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        queryset = OrderRequest.objects.get(id=id)
        queryset.delete()

        text = f"Пользователь {queryset.order.owner.nickname} отклонил вашу заявку."
        send_push(queryset.order.owner, text)
        Message.objects.create(
            user = queryset.order.owner, text = text
        )
        return Response({'status': 'ok'})


class RequestAccept(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        queryset = OrderRequest.objects.get(id=id)
        queryset.order.in_work = True
        queryset.order.price = queryset.price
        queryset.order.cto = queryset.cto
        queryset.order.time = queryset.time
        queryset.order.save()
        OrderRequest.objects.filter(order=queryset.order).delete()

        text = f"Пользователь {queryset.order.owner.nickname} принял вашу заявку. Смотрите в активных заказах."
        send_push(queryset.order.owner, text)
        Message.objects.create(
            user = queryset.order.owner, text = text
        )
        return Response({'status': 'ok'})


class History(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, role):
        if role == "0":
            order = Order.objects.filter(is_finished=True, owner=request.user)
            s = OrderSer(order, many=True, context={'request': request})
            return Response(s.data)
        else:
            order = Order.objects.filter(is_finished=True, cto=request.user)
            s = OrderSer(order, many=True, context={'request': request})
            return Response(s.data)


class ActiveOrder(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, role):
        if role == "0":
            order = Order.objects.filter(in_work=True, owner=request.user, is_finished=False)
            s = OrderSer(order, many=True, context={'request': request})
            return Response(s.data)
        else:
            order = Order.objects.filter(in_work=True, cto=request.user, is_finished=False)
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


class FinishOrder(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, id):
        o = Order.objects.get(id=id)
        o.is_finished = True
        o.save()

        text = f"Исполнитель {o.cto.cto_name} завершил ваш заказ. Смотрите в истории заказов."
        send_push(o.owner, text)
        Message.objects.create(
            user = o.owner, text = text
        )
        return Response({'status': 'ok'})


class Push(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        send_push(User.objects.get(id=3), "hello alem")
        return Response({'status': 'ok'})