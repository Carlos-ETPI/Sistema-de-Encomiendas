from django.contrib import admin
from .models import CustomUser
from .models import ClienteForm

admin.site.register(CustomUser)
admin.site.register(ClienteForm)