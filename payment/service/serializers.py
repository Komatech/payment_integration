from rest_framework import serializers
from .models import *

class customer_serializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class sales_serializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'