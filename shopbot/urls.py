from django.urls import path
from . import views
app_name = 'shopbot'
urlpatterns = [
    path('',views.index,name='index'),
]