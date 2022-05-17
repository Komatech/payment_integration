from rest_framework import serializers
from .models import *

class customer_serializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'email',
            'telNo'
        ]

class product_serializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'quantity',
            'price'
        ]

class sales_serializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = [
            'customer_id',
            'product_id',
            'quantity',
            'Amount',
            'pay_id'
        ]