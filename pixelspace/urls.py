from django.urls import path
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('colors', views.colors, name='colors'),
    path('image', views.image, name='image'),
    path('login', views.login, name='login'),
    path('logo', views.logo, name='logo'),
    path('pixelmap', views.pixelmap, name='pixelmap'),
    path('settings', views.settings, name='settings'),
    path('create-account', views.create_account, name='create-account'),
]
