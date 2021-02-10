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
from rest_framework import filters


class CtoView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = CTO.objects.filter()