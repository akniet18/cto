from django.shortcuts import render
from django.http import JsonResponse
from .models import *
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
import uuid
from push_notifications.models import APNSDevice, GCMDevice

# smsc = SMSC()


class PhoneCode(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = PhoneS(data=request.data)
        # rand = random.randint(1000, 9999)
        rand = "1111"
        if s.is_valid():
            nickname = s.validated_data['nickname']
            phone = s.validated_data['phone']
            if phone[0] != "+":
                phone = "+" + phone
            if PhoneOTP.objects.filter(phone = phone).exists():
                a = PhoneOTP.objects.get(phone = phone)
                a.nickname = nickname
                if phone == "+77783579279":
                    a.otp = "1111"
                else:
                    a.otp = rand
                a.save()
            else:
                if phone == "+77783579279":
                    PhoneOTP.objects.create(phone=phone, otp="1111", nickname=nickname)
                else:
                    PhoneOTP.objects.create(phone=phone, otp=str(rand), nickname=nickname)
            # if phone != "+77783579279":
                # smsc.send_sms(phone, "Код подтверждения для ALU.KZ: "+str(rand), sender="sms")
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class Register(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = RegisterSerializer(data=request.data)
        if s.is_valid():
            print('register: ', s.validated_data['phone'], s.validated_data['code'])
            phone = s.validated_data['phone']
            if phone[0] != "+":
                phone = "+" + phone
            u = PhoneOTP.objects.get(phone=phone)
            if u.otp == str(s.validated_data['code']):
                # u.validated = True
                nickname = u.nickname
                # u.save()
                if User.objects.filter(phone=phone).exists():
                    us = User.objects.get(phone=phone)
                    uid = us.pk
                    us.nickname = nickname
                    us.save()
                else:
                    us = User.objects.create(phone=phone, nickname=nickname)
                    uid = us.pk
                if Token.objects.filter(user=us).exists():
                    token = Token.objects.get(user=us)
                else:
                    token = Token.objects.create(user=us)
                # user = authenticate(phone=phone)
                # django_login(request, us)
                return Response({'key': token.key, 'uid': uid, 'status': 'ok', 'nickname': us.nickname})
            else:
                return Response({'status': 'otp error'})
        else:
            return Response(s.errors)



class LoginAdmin(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = LoginAdminSerializer(data=request.data)
        if s.is_valid():
            phone = s.validated_data['phone']
            password = s.validated_data['password']
            us = User.objects.filter(phone=phone, is_staff=True)
            if us.exists():
                us = us[0]
                if us.check_password(password):
                    if Token.objects.filter(user=us).exists():
                        token = Token.objects.get(user=us)
                    else:
                        token = Token.objects.create(user=us)
                    return Response({'key': token.key, 'uid': us.pk})
                else:
                    return Response({'status': 'error'})
            else:
                return Response({'status': 'error'})
        else:
            return Response(s.errors)


        
class UserApi(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, id):
        user = User.objects.get(id=id)
        s = UserSerializer(user, context={'request': request})
        return Response(s.data)

    def post(self, request, id):
        s = ChangeAvaSer(data=request.data)
        if s.is_valid():
            user = User.objects.get(id=id)
            user.nickname = s.validated_data.get('nickname', user.nickname)
            user.second_phone = s.validated_data.get('second_phone', user.second_phone)
            user.third_phone = s.validated_data.get('third_phone', user.third_phone)
            user.email = s.validated_data.get('email', user.email)
            user.save()
            return Response({'status': 'ok'})
        else:
            return Response(s.errors)


class ChangeAvatar(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = ChangeAvaSer(data=request.data)
        if s.is_valid():
            avatar = s.validated_data['avatar']
            # avatar = base64img(avatar, "ava")
            # avatar = compress_image(avatar, (400,400))
            request.user.avatar = avatar
            request.user.save()
            return Response({'status': "ok"})
        else:
            return Response(s.errors)


class CreateCto(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        s = CreateCtoSer(data=request.data)
        if s.is_valid():
            CTORequest.objects.get(id=s.validated_data['id']).delete()
            cto_id = uuid.uuid4().hex[:10]
            phone = s.validated_data['phone']
            if phone[0] != "+":
                phone = "+" + phone
            check = True
            while check:
                if User.objects.filter(cto_id=cto_id).exists():
                    cto_id = uuid.uuid4().hex[:10]
                else:
                    check = False
            cto = User.objects.filter(phone = phone)
            if cto.exists():
                cto = cto[0]
                if cto.cto_name == None:
                    cto.cto_name = s.validated_data['name']
                    l = s.validated_data.get('logo', None)
                    if l:
                        cto.cto_logo = l
                    cto.cto_id = cto_id
                    cto.cto_address = s.validated_data['address']
                    cto.cto_lat = s.validated_data['lat']
                    cto.cto_lng = s.validated_data['lng']
                    cto.save()
                else:
                    return Response({'status': 'autoservice already exists'})
            else:
                cto = User.objects.create(
                    phone = phone,
                    cto_name=s.validated_data['name'],
                    cto_id=cto_id,
                    cto_address = s.validated_data['address'],
                    cto_lat = s.validated_data['lat'],
                    cto_lng = s.validated_data['lng']
                )
                l = s.validated_data.get('logo', None)
                if l:
                    cto.cto_logo = l
                    cto.save()
            s = CTOListSer(cto, context={'request': request})
            print(cto)    
            return Response(s.data)
        else:
            return Response(s.errors)
        

class UserList(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer
    queryset = User.objects.filter(is_superuser=False, is_staff=False)


class LoginCTO(APIView):
    permission_classes = [permissions.AllowAny,]

    def post(self, request):
        s = Idser(data=request.data)
        if s.is_valid():
            cto_id = s.validated_data['id'].lower()
            cto = User.objects.filter(cto_id = cto_id)
            if cto.exists():
                cto = cto[0]
                if Token.objects.filter(user=cto).exists():
                    token = Token.objects.get(user=cto)
                else:
                    token = Token.objects.create(user=cto)
                return Response({
                    'cto_name': cto.cto_name,
                    'key': token.key,
                    # 'uid': us.pk
                    'cto_logo': request.scheme+'://'+request.META['HTTP_HOST']+cto.cto_logo.url,
                    'cto_address': cto.cto_address
                })
            else:
                return Response({'status': "not found"})
        else:
            return Response(s.errors)


class CTOList(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CTOListSer
    queryset = User.objects.filter(cto_name__isnull=False)

    

class CTODelete(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, id):
        cto = User.objects.get(id=id)
        cto.cto_name = None
        cto.cto_logo = None
        cto.cto_id = None
        cto.cto_address = None
        cto.save()
        return Response({'status': 'ok'})


class SendRequestToAdmin(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        q = CTORequest.objects.all()
        s = CTORequestSer(q, many=True)
        return Response(s.data)


    def post(self, request):
        q = CTORequest.objects.filter(phone = request.user.phone)
        if q.exists():
            q = q[0]
        else:
            CTORequest.objects.create(phone = request.user.phone, nickname = request.user.nickname)
        return Response({'status': 'ok'})


class pushRegister(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    
    def post(self, request):
        s = pushSerializer(data=request.data)
        if s.is_valid():
            cmt = s.validated_data['cmt']
            if cmt == "apn":
                ios = APNSDevice.objects.filter(user = request.user)
                if ios.exists():
                    ios = APNSDevice.objects.get(user = request.user)
                    ios.registration_id = s.validated_data['reg_id']
                    ios.save()
                else:
                    APNSDevice.objects.create(user=request.user, registration_id=s.validated_data['reg_id'])
            else:
                android = GCMDevice.objects.filter(user=request.user)
                if android.exists():
                    android = GCMDevice.objects.get(user=request.user)
                    android.registration_id = s.validated_data['reg_id']
                    android.save()
                else:
                    GCMDevice.objects.create(user=request.user, active=True,
                                        registration_id=s.validated_data['reg_id'],
                                        cloud_message_type="FCM")
            return Response({'status': "ok"})
        else:
            return Response(s.errors)


class getMessages(APIView):
    permission_classes = [permissions.IsAuthenticated,]

    def get(self, request):
        m = Message.objects.filter(user = request.user).order_by('-id')
        s = MessageSer(m, many=True)
        return Response(s.data)


def privatepolicy(request):
    context = {'context': ""}
    return render(request, 'index.html', context)

def Terms_of_use(request):
    context = {'context': ""}
    return render(request, 'index.html', context)