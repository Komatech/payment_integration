from django.urls import path

from .apis import CallbackApi, CustomerApi, CustomerDetailApi, PaymentApi

app_name = "service"

urlpatterns = [
    path("customer/", CustomerApi.as_view(), name="customers"),
    path("customer/pay/", PaymentApi.as_view(), name="payment"),
    path("customer/<str:pk>/", CustomerDetailApi.as_view(), name="customer"),
    path("callback/", CallbackApi.as_view(), name="callback"),
]
