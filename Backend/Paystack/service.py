'''
    This file exist to give the paystack api support for other complex API
'''
import requests
from django.conf import settings


PUBLIC_KEY = settings.PAYSTACK_PUBLIC_KEY
SECRET_KEY = settings.PAYSTACK_SECRET_KEY


def get_banks_from_paystack ():
    url = "https://api.paystack.co/bank"
    headers = {
        "Authorization": f"Bearer {SECRET_KEY}"
    }


    response = requests.get(url, headers=headers)
    return response.json().data