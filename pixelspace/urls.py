from django.urls import path
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('colors', views.colors, name='colors'),
    #path('image', views.image, name='image'),
    path('gallery', views.gallery, name='gallery'),
    path('login', views.login, name='login'),
    path('logo', views.logo, name='logo'),
    path('pixelmap', views.pixelmap, name='pixelmap'),
    path('settings', views.settings, name='settings'),
    path('create-account', views.create_account, name='create-account'),
    path('logout', views.logout, name='logout'),
    path('delete-confirm', views.deleteConfirm, name='delete-confirm'),
    path('delete-map-confirm', views.deleteMapConfirm, name='delete-map-confirm'),
    path('results', views.results, name='results'),
    path('detail/<int:map_id>/', views.detail, name='detail'),
    path('comment-delete/<int:map_id>/<int:pk>', views.comment_delete, name='comment_delete'),
    path('reset-password', views.reset_password, name='reset_password'),
]
