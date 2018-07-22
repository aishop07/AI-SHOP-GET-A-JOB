from django.shortcuts import render

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