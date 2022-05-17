from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
# Create your views here.

#                   Create/Post views
@api_view(['POST'])
def create_customer(request):
    serializer = customer_serializer(data=request.data)

    try:
        if serializer.is_valid():
            serializer.save()

        data = serializer.data
        return Response({
            'message': 'Customer created successfully',
            'status': True,
            'data' : data,
        },status=status.HTTP_200_OK)
    except:
        return Response({
            'messages': 'An error occured',
            'status': False,
            'data' : [],
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def create_product(request):
    serializer = product_serializer(data=request.data)

    try:
        if serializer.is_valid():
            serializer.save()

        data = serializer.data
        return Response({
            'message': 'Product created successfully',
            'status': True,
            'data' : data,
        },status=status.HTTP_200_OK)
    except:
        return Response({
            'messages': 'An error occured',
            'status': False,
            'data' : [],
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    