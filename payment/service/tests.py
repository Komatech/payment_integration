from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from service.models import Customer,Sales

# Create your tests here.
class createCustomer(APITestCase):
    # complete process test
    def test_account_create(self):
        # Account creation test
        url = reverse('create_customer')
        data = {'first_name': 'Dev','last_name': 'Apps','email': 'devapps@gmail.com','telNo': '09055667712'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().email, 'devapps@gmail.com')

        # Payment test
        url = reverse('payment')
        data = {'email': 'devapps@gmail.com','amount': '100'}
        response = self.client.post(url, data, format='json')     
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sales.objects.get().amount,100)
        self.assertEqual(Sales.objects.get().customer_id.email,'devapps@gmail.com')
        self.assertEqual(response.data["message"], "Payment processing")
        
        url = response.data["link"]
        print(url)


    # def payment(self):
    #     self.test_account_create
    #     url = reverse('payment')
    #     data = {'email': 'devapps@gmail.com','amount': '100'}
    #     response = self.client.post(url, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(Sales.objects.get().amount,100)
    #     self.assertEqual(Sales.objects.get().customer_id.email,'devapps@gmail.com')
    #     self.assertEqual(response['message'], "Payment processing")