from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='index'),
    path('service', views.service, name='service'),
    path('daegu', views.search_daegu, name='daegu'),
    path('gwangju', views.search_gwangju, name='gwangju'),
    path('daejeon', views.search_daejeon, name='daejeon'),
    path('busan', views.search_busan, name='busan'),
    path('ulsan', views.search_ulsan, name='ulsan'),
    path('incheon', views.search_incheon, name='incheon'),
    path('seoul', views.search_seoul, name='seoul'),

]