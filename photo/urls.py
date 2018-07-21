from django.urls import path
from . import views

app_name = 'photo'

urlpatterns = [
    #http://localhost:8000
    path('',views.index,name='index'),
    path('getphoto',views.getphoto,name='getphoto'),
]