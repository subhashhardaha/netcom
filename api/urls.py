
from django.urls import path
from .views import process,devices,connections,info_routes

urlpatterns = [
    path('process', process,name='process'),
    path('devices', devices,name='devices'),
    path('connections', connections,name='connections'),
    path('info-routes?from=<str:frm>&to=<str:to>', info_routes,name='info_routes'),
    path('devices/<str:name>/strength', devices,name='strength'),



]