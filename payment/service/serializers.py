from rest_framework import serializers
from .models import *

class Customer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'email',
            'telNo'
        ]

class Product(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'quantity',
            'price'
        ]

class Sales(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = [
            'customer_id',
            'product_id',
            'quantity',
            'Amount',
            'pay_id'
        ]