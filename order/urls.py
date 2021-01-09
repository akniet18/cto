from django.urls import path, include
from .views import *

urlpatterns = [
    path('', OrderApi.as_view()),
    path('request/create', CreateOrderRequestApi.as_view()),
    path('request/<id>', OrderRequestApi.as_view())
]