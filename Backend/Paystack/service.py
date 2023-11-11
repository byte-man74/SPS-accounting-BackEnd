'''
    This file exist to give the paystack api support for other complex API
'''
import requests
from django.conf import settings


PUBLIC_KEY = settings.PAYSTACK_PUBLIC_KEY
SECRET_KEY = settings.PAYSTACK_SECRET_KEY


def get_banks_from_paystack():
    '''
        this function fetches the list of all the banks from Paystack database
    '''
    url = "https://api.paystack.co/bank"
    headers = {
        "Authorization": f"Bearer {SECRET_KEY}"
    }

    response = requests.get(url, headers=headers)
    return response.json()["data"]


def generate_paystack_id_for_staff(instance):
    '''
        this function generates paystack_id_for_staff after verifying the account name and bank
    '''

    url = "https://api.paystack.co/transferrecipient"
    headers = {
        "Authorization": f"Bearer {SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "type": instance.bank.bank_type,
        "name": f"{instance.first_name} {instance.last_name}",
        "account_number": instance.account_number,
        "bank_code": instance.bank.bank_code,
        "currency": instance.bank.currency
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        print(response.json())

        if response.json()["status"]:
            payload = {
                'status': 200,
                'data': response.json()['data']["recipient_code"]
            }
        else:
            print(response.json())
            payload = {
                'status': 200,
                'data': response.json()["message"]
            }

        return payload

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"General error occurred: {req_err}")

    # Return None or an appropriate message if an exception occurs
    return None
