from rest_framework import serializers
from .models import Drinks
from .models import Foods
from .models import Orders
from .models import Member


class DrinksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drinks
        # fields = '__all__'
        fields = ('id', 'name', 'price', 'qt', 'image')

class FoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        # fields = '__all__'
        fields = ('id', 'name', 'price', 'qt', 'image')

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        # fields = '__all__'
        fields = ('id', 'order_number', 'user_name', 'product_name', 'price', 'qt', 'image','datetime')

class MemberSerializer(serializers.ModelSerializer):
 
   class Meta:
       model = Member
       fields = '__all__'