from django.urls import path
from . import views

app_name = 'photo'

urlpatterns = [
    #http://localhost:8000
    path('',views.index,name='index'),
    path('takephoto',views.takephoto,name='takephoto'),
    path('getphoto',views.getphoto,name='getphoto'),
    path('image',views.image,name='image'),
]