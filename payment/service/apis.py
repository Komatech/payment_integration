from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import (
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Customer, Sales
from .serializers import (
    CallbackOutputSerializer,
    CallbackSerializer,
    CustomerSerializer,
    CustomerDetailSerializer,
    PaymentSerializer,
    SalesPaymentSerializer,
)
from .services import payment_create, sales_verify


class CustomerApi(ListCreateAPIView):
    """
    Read all customers with get request
    Create new Customer with post request
    """

    permission_classes = (AllowAny,)
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetailApi(RetrieveUpdateDestroyAPIView):
    """
    Get specifed customer else throw 404 with get request
    Update a specified customer with put request
    """

    permission_classes = (AllowAny,)
    queryset = Customer.objects.all()
    serializer_class = CustomerDetailSerializer


class PaymentApi(GenericAPIView):
    """
    Initiate payment process with a post request
    """

    permission_classes = (AllowAny,)
    serializer_class = PaymentSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sale = payment_create(**serializer.validated_data)
        response = SalesPaymentSerializer(sale)
        return Response(response.data, status=status.HTTP_200_OK)


class CallbackApi(GenericAPIView):
    """
    Verify that payment went through
    """
    permission_classes = (AllowAny,)
    serializer_class = CallbackSerializer

    def get(self, request):
        serializer = self.get_serializer(data=request.GET)
        serializer.is_valid(raise_exception=True)
        data = sales_verify(**serializer.validated_data)
        response = CallbackOutputSerializer(data)
        return Response(response.data, status=status.HTTP_200_OK)
