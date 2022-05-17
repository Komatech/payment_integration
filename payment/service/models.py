from itertools import product
from unicodedata import name
from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    telNo = models.CharField(max_length=20)

class Product(models.Model):
    name = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.IntegerField()

class Sales(models.Model):
    customer_id = models.CharField()
    product_id = models.CharField()
    quantity = models.IntegerField()
    Amount = models.IntegerField()
    pay_id = models.CharField()