from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'list', UserList, basename='users')
router.register(r'autoservices', CTOList, basename='users')

urlpatterns = [
    path("phone/", PhoneCode.as_view()),
    path("code/", Register.as_view()),
    path('login/admin/', LoginAdmin.as_view()),
    path('login/cto/', LoginCTO.as_view()),

    path("detail/<id>", UserApi.as_view()),
    path('change/avatar/', ChangeAvatar.as_view()),

    path('create/autoservice/', CreateCto.as_view()),
    path('autoservices/delete/<id>/', CTODelete.as_view()),
    path('autoservice/request/', SendRequestToAdmin.as_view()),

    path('push/register/', pushRegister.as_view()),
    path('my/message/', getMessages.as_view())
]
urlpatterns += router.urls
