from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from django.conf.urls import url, include
from django.contrib import admin

app_name='products'
urlpatterns = [
    path('', views.index,name='index'),
    path('products', views.products,name='list')
]