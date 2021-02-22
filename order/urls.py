from django.urls import path, include
from .views import *

urlpatterns = [
    path('', OrderApi.as_view()),
    path('request/create', CreateOrderRequestApi.as_view()),
    path('request/', OrderRequestApi.as_view()),
    path('history/<role>', History.as_view()),
    path('active/<role>', ActiveOrder.as_view()),

    path('request/decline/<id>', RequestDecline.as_view()),
    path('request/accept/<id>', RequestAccept.as_view()),
    path('list/', OrderList.as_view()),
    path('img/delete/', OrderImgDelete.as_view()),

    path('finish/', FinishOrder.as_view())
]
