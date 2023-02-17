from django.urls import path
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('colors', views.colors, name='colors'),
]