from django.urls import path, include
from .views import *

urlpatterns = [
    path('', CarApi.as_view()),
    path('json', JsonLoad.as_view())
]