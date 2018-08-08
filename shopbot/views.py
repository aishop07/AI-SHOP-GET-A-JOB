from django.shortcuts import render,redirect
from django.http import HttpResponse

# from . import chtatterbotchinese as cb
# Create your views here.
def index(request):
    return render(request,'shopbot/index.html',locals()) 

