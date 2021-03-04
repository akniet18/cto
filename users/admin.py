from django.contrib import admin
from .models import *

admin.site.register(PhoneOTP)
admin.site.register(User)
admin.site.register(CTORequest)
admin.site.register(Message)

