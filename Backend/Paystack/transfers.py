'''
    This file exist to give accept transfer transactions
'''
import requests
from django.conf import settings


PUBLIC_KEY = settings.PAYSTACK_PUBLIC_KEY
SECRET_KEY = settings.PAYSTACK_SECRET_KEY


def process_bulk_transaction (bulk_data):
    '''
        this function processes bulk transactions for salary payment and random payments
        in bulk
    '''
    url = "https://api.paystack.co/transfer/bulk"
    header = {
        "Authorization": f"Bearer {SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "currency": "NGN",
        "source": "balance",
        "transfers": bulk_data
    }

    response = requests.post(url, headers=header, json=data)
    print(response.json())

