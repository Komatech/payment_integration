from itertools import product
from tkinter import CASCADE
from unicodedata import name
from django.db import models

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250,unique=True)
    telNo = models.CharField(max_length=20)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Sales(models.Model):
    customer_id = models.ForeignKey('Customer',on_delete=models.CASCADE,blank=False,null=False)
    amount = models.IntegerField()
    pay_id = models.CharField(max_length=250)
    transaction_id = models.CharField(max_length=250)
    status = models.CharField(max_length=20,default='pending')

    def __str__(self):
        return str(self.customer_id) + " " + self.transaction_id