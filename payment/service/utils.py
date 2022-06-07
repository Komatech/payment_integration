import math
import requests

from django.urls import reverse
from random import SystemRandom
from typing import Dict


def get_header() -> Dict[str, str]:
    auth_token = "FLWSECK_TEST-423128379aba3f3d7f5e24ecab9273a5-X"
    header = {"Authorization": f"Bearer {auth_token}"}
    return header


def process_payment(*, name: str, email: str, amount: int, phone: str) -> dict:
    cryptic = SystemRandom()
    ref = str(math.floor(cryptic.random() * 9000000))
    payload = {
        "tx_ref": ref,
        "amount": amount,
        "currency": "NGN",
        "redirect_url": reverse("service:callback"),
        "payment_option": "card",
        "customer": {
            "email": email,
            "phonenumber": phone,
            "name": name,
        },
    }
    url = "https://api.flutterwave.com/v3/payments"
    header = get_header()
    response = requests.post(url, json=payload, headers=header)
    data = response.json().get("data")
    data.update({"tx_ref": ref})
    return data


def verify_transaction(*, transaction: str):
    header = get_header()
    url = f"https://api.flutterwave.com/v3/transactions/{transaction}/verify"
    response = requests.get(url, headers=header)
    data = response.json()
    return data
