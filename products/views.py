from django.shortcuts import render, redirect

# Create your views here.
from .models import Drinks
from .models import Foods
from .models import Orders
from .models import Member
from .serializers import DrinksSerializer
from .serializers import FoodsSerializer
from .serializers import OrdersSerializer
from .serializers import MemberSerializer
from rest_framework import viewsets
# from .object_detection import Object_detection_webcam as od
from object_detection import Object_detection_webcam as od
from object_detection import Object_detection_webcam_1 as od1
import random
import datetime
import cv2
import os
import lineTool
import time


# Create your views here.
class DrinksViewSet(viewsets.ModelViewSet):
    queryset = Drinks.objects.all()
    serializer_class = DrinksSerializer

class FoodsViewSet(viewsets.ModelViewSet):
    queryset = Foods.objects.all()
    serializer_class = FoodsSerializer

class OrdersViewSet(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

def index(request):
    orders = list(Orders.objects.filter(user_name=str(request.COOKIES['name'])).order_by('-datetime').values())
    print(orders)
    print(type(orders))
    
    
    return render(request, 'products/index.html', locals())
def products(request):
    foods = Foods.objects.all()
    drinks = Drinks.objects.all()
    print(foods,drinks)
    return render(request, 'products/products.html', locals())
def check(request):
    result = od.main()
    prices4,prices5,prices6 = 0,0,0
    # print(result)
    texts = {text:result.count(text) for text in result}
    for i in result:
        if i == "pringles":
            food = list(Foods.objects.filter(name=i).values())
            price1 = food[0]["price"]
            name1 = food[0]["name"]
            image1 = food[0]["image"]
        elif i == "cafe":
            drink = list(Drinks.objects.filter(name=i).values())
            price2 = drink[0]["price"]
            name2 = drink[0]["name"]
            image2 = drink[0]["image"]
        elif i =="doritos":
            food = list(Foods.objects.filter(name=i).values())
            price3 = food[0]["price"]
            name3 = food[0]["name"]
            image3 = food[0]["image"]
    order_number = random.randint(1000000,9999999)
    for j in result:            
        if j == "pringles":
            user_name1 = str(request.COOKIES['name'])
            products_name1 = "pringles"
            price4 = food[0]["price"]
            prices4 = food[0]["price"] * texts["pringles"]
            image4 = food[0]["image"]
            qt1 = 1
            day = datetime.datetime.now()
            nowtime1 = str(day.year) +'/'+str(day.month) +'/'+ str(day.day) + ' '+str(day.hour)+':'+ str(day.minute)
            name4= str(request.COOKIES['name'])
            Orders.objects.create(order_number=order_number,user_name=user_name1,product_name=products_name1,price=price4,qt=qt1,image=image4,datetime=nowtime1,name=name4)
        elif j == "cafe":
            user_name2 = str(request.COOKIES['name'])
            products_name2 = "cafe"
            price5 = drink[0]["price"]
            prices5 = drink[0]["price"] * texts["cafe"]
            image5 = drink[0]["image"]
            qt2 = 1
            day = datetime.datetime.now()
            nowtime2 = str(day.year) +'/'+str(day.month) +'/'+ str(day.day) + ' '+str(day.hour)+':'+ str(day.minute)
            name5 = str(request.COOKIES['name'])
            Orders.objects.create(order_number=order_number,user_name=user_name2,product_name=products_name2,price=price5,qt=qt2,image=image5,datetime=nowtime2,name=name5)
        elif j =="doritos":
            user_name3 = str(request.COOKIES['name'])
            products_name3 = "doritos"
            price6 = food[0]["price"]
            prices6 = food[0]["price"] * texts["doritos"]
            image6 = food[0]["image"]
            qt3 = 1
            day = datetime.datetime.now()
            nowtime3 = str(day.year) +'/'+str(day.month) +'/'+ str(day.day) + ' '+str(day.hour)+':'+ str(day.minute)
            name6 = str(request.COOKIES['name'])
            Orders.objects.create(order_number=order_number,user_name=user_name3,product_name=products_name3,price=price6,qt=qt3,image=image6,datetime=nowtime3,name=name6)
        total = prices4 + prices5 + prices6
    return render(request,'products/check.html',locals())


def detection(request):    
    while 1:
        result = od1.main()
        print(result)
        if result.count("quit") < 1 :
            pringles = result.count("pringles") 
            cafe = result.count("cafe")
            doritos = result.count("doritos")
            # if temp>1:
            # if pringles<1 or cafe<1 or doritos<1:
            Token = "P9SHXtrlr0eEeSVx4M04ZRPab7Vbcry42Avk7Luaeva"
            TurnOn_message = "\n" + " 目前架上的商品數量如下:\n" + "Pringles:" + str(pringles) + "\n" + "cafe:" + str(cafe) + "\n" + "doritos:" + str(doritos) +"\n請確認是否需要補貨,謝謝\n"
            Time_message = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            MESSAGE = ''
            time.sleep(10)
            MESSAGE = TurnOn_message+ Time_message
            print("Send message to Line \n%s\n" % MESSAGE)
            lineTool.lineNotify(Token, MESSAGE)
            time.sleep(10)
        else:
            break
    return redirect('http://localhost:8000/member/memberarea/')


            