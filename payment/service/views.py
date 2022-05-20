from urllib import response
from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
import requests,math,random
from django.views.decorators.csrf import csrf_exempt
SECRETKEY='FLWSECK_TEST-423128379aba3f3d7f5e24ecab9273a5-X'
# Create your views here.


# An endpoint to create a customer.
@api_view(['POST'])
@csrf_exempt
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
        },status=status.HTTP_201_CREATED)
    except:
        return Response({
            'messages': 'An error occured',
            'status': False,
            'data' : [],
        },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# An endpoint to fetch all the customers.
@api_view(['GET'])
def get_customers(request):
    try:
        customers = Customer.objects.all()
        serializer = customer_serializer(customers,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    except:
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

# An endpoint to fetch a single customer and all the payments made by the customer.
@api_view(['GET'])
def customer_detail(request,pk):
    # try:
    try:
        customers = Customer.objects.get(id=pk)
        customer_data = customer_serializer(customers,many=False)
        
        payments = Sales.objects.filter(customer_id=customers)
        
        if len(payments) == 0:
            customer_payment = {"data":"Customer has no payments"}
            
        else:
            customer_payment = sales_serializer(payments,many=True).data
            
        data = {
            "Customer Info":customer_data.data,
            "Customer Payments":customer_payment
        }
        
        return Response(data,status=status.HTTP_200_OK)
    except:
        return Response({"message":"Customer doesn't exist"},status=status.HTTP_400_BAD_REQUEST) 
        

# payment function
def process_payment(name,email,amount,phone):
    auth_token= SECRETKEY
    hed = {'Authorization': 'Bearer ' + auth_token}
    data = {
            "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
            "amount":amount,
            "currency":"NGN",
            "redirect_url":"http://localhost:8000/callback",
            "payment_options":"card",

            "customer":{
                "email":email,
                "phonenumber":phone,
                "name":name
            },
            
            }
    url = ' https://api.flutterwave.com/v3/payments'
    response = requests.post(url, json=data, headers=hed)
    response=response.json()
    link=response['data']['link']
    data = {"link":link,"tx_ref":data['tx_ref']}
    # print(data)
    return data

# verification function
def verify(transac):
    auth_token= SECRETKEY
    hed = {'Authorization': 'Bearer ' + auth_token}
    
    url = ' https://api.flutterwave.com/v3/transactions/'+transac+'/verify'
    response = requests.get(url,headers=hed)
    response=response.json()
    return response


# An endpoint to charge a customer’s card and pass the card details to Flutterwave for processing
@api_view(['POST'])
@csrf_exempt
def pay(request):
    customer_email = request.data['email']
    amount = request.data['amount']
    customer = Customer.objects.get(email=customer_email)

    customer_name = str(customer.first_name)+ ' '+ str(customer.last_name)
    customer_no = str(customer.telNo)
    amount = amount

    process_payment(customer_name,customer_email,amount,customer_no)
    data = process_payment(customer_name,customer_email,amount,customer_no)
    link = data['link']
    pay_id = data['tx_ref']

    Sales.objects.create(
        customer_id = customer,
        amount = amount,
        pay_id = pay_id
    )
    return Response({'message':'Payment processing',"link":link},status=status.HTTP_200_OK)


# Confirmation endpoint
@api_view(['GET'])
def callback(request):

    try:
        payload = request.GET
        status = payload['status']
        ref_id = payload['tx_ref']
        transac_id = payload['transaction_id']

        transaction = Sales.objects.filter(pay_id=ref_id)
        verification = verify(transac_id)

        if verification['status'] == 'success':
            transaction.update(
                status = 'approved',
                transaction_id = transac_id
            )

        return Response({"message":"Successful","status":status,"pay_id":ref_id,"payload":payload})

    except:
        return Response({"message":"Transaction failes"},status=status.HTTP_400_BAD_REQUEST)


