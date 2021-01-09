from django.urls import path, include
from .views import *

urlpatterns = [
    path("phone/", PhoneCode.as_view()),
    path("code/", Register.as_view()),

    path("detail/<id>", UserApi.as_view()),
    path('change/avatar/', ChangeAvatar.as_view())
]