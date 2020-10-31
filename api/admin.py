from django.contrib import admin

# Register your models here.

from .models import Node,Device
admin.site.register(Node)
admin.site.register(Device)

