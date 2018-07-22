from django.db import models

# Create your models here.
class Drinks(models.Model):
    name = models.CharField(max_length=50,null=False)
    price = models.IntegerField(null=False)
    qt = models.IntegerField(null=False)
    image = models.CharField(max_length=200,null=False)

    class Meta:
        db_table = "Drinks"

class Foods(models.Model):
    name = models.CharField(max_length=50,null=False)
    price = models.IntegerField(null=False)
    qt = models.IntegerField(null=False)
    image = models.CharField(max_length=200,null=False)

    class Meta:
        db_table = "Foods"

class Orders(models.Model):
    order_number = models.IntegerField(null=False)
    user_name = models.CharField(max_length=50,null=False)
    product_name = models.CharField(max_length=50,null=False)
    price = models.IntegerField(null=False)
    qt = models.IntegerField(null=False)
    image = models.CharField(max_length=200,null=False)
    datetime = models.TextField(max_length=200,null=False)

    class Meta:
        db_table = "Orders"
        
class Member(models.Model):
    username = models.CharField(max_length=20,null=False)
    password = models.CharField(max_length=10,null=False)
    useremail = models.EmailField(max_length=100,blank=True)
    userbirth = models.DateField(null=False)
    
    class Meta:
        db_table = "members"

