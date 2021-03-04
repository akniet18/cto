from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)
# from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import RegexValidator
from datetime import datetime



class UserManager(BaseUserManager):
    def create_user(self, phone):
        if not phone:
            raise ValueError(_("Users must have an phone address"))
        # email = self.normalize_email(email)
        user = self.model(phone=phone)
        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password,**extra_fields):
        user = self.create_user(phone)
        # user.is_active = True
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        # user.role = User.ROLE_ADMINISTRATOR
        user.save(using=self._db)
        return user

    def create_staffuser(self, phone, password=None):
        user = self.create_user(phone, password=password, is_staff=True, is_active=True)
        return user


def user_photos_dir(instanse, filename):
    usrnme = f'{instanse.phone}'
    folder_name = f"{usrnme}/{filename}"
    return folder_name


class User(AbstractBaseUser, PermissionsMixin):
    # phone_regex = RegexValidator( regex = r'^\+?1?\d{7,12}$',
    # message = "Phone number in the format '+77777777'. Up to 12 digits")
    # phone = models.CharField(max_length=12,validators = [phone_regex], unique=True)
    phone = models.CharField(max_length=15, unique=True)
    password1 = models.CharField(max_length=20, blank=True, null=True)
    password2 = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    nickname = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True,
                                auto_now=False,
                                auto_now_add=False)
    second_phone = models.CharField(max_length=15, blank=True, null=True)
    third_phone = models.CharField(max_length=15, blank=True, null=True)

    user_lat = models.CharField(max_length=150, null=True, blank=True)
    user_lng = models.CharField(max_length=150, null=True, blank=True)


    # ------------------------------------------------------
    # country = models.ForeignKey("locations.Country", on_delete=models.CASCADE, blank=True, null=True)
    # region = models.ForeignKey("locations.Region", on_delete=models.CASCADE, blank=True, null=True)
    # city = models.ForeignKey("locations.City", on_delete=models.CASCADE, blank=True, null=True)

    #--------------------------------------------------------
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_autoservice = models.BooleanField(default=False)

    #--------------------------------------------------------
    cto_name = models.CharField(max_length=50, null=True, blank=True)
    cto_logo = models.ImageField(upload_to=user_photos_dir, default="default/default.png")
    cto_id = models.CharField(max_length=50, null=True, blank=True)
    cto_lat = models.CharField(max_length=150, null=True, blank=True)
    cto_lng = models.CharField(max_length=150, null=True, blank=True)
    cto_address = models.CharField(max_length=150, null=True, blank=True)
 
    #--------------------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    last_online = models.DateTimeField(null=True, blank=True)
     
    #--------------------------------------------------------
    avatar = models.ImageField(upload_to=user_photos_dir, default="default/default.png")

    # -------------------------------------------------------
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return str(self.id) + ", " + self.phone



class PhoneOTP(models.Model):
    # phone_regex = RegexValidator( regex = r'^\+?1?\d{7,12}$',
    # message = "Phone number in the format '+77777777'. Up to 12 digits")
    # phone = models.CharField(max_length=12,validators = [phone_regex], unique=True)
    phone = models.CharField(max_length = 12, unique = True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    otp = models.CharField(max_length=9, blank=True, null=True)
    validated = models.BooleanField(default=False, help_text = 'True means user has a validated otp correctly in second API')

    def __str__(self):
        return str(self.phone) + ' is sent ' + str(self.otp)



class CTORequest(models.Model):
    phone = models.CharField(max_length = 12, unique = True)
    nickname = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.phone



class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    is_readed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.phone