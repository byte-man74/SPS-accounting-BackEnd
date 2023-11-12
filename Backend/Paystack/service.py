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


def generate_paystack_id(instance, full_name_present=None):
    '''
    Generate paystack_id_for_staff after verifying the account name and bank.
    '''

    url = "https://api.paystack.co/transferrecipient"
    headers = {
        "Authorization": f"Bearer {SECRET_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "type": instance.bank.bank_type,
        "name": f"{instance.name_of_reciever}" if full_name_present else f"{instance.first_name} {instance.last_name}",
        "account_number": instance.reciever_account_number if full_name_present else instance.account_number,
        "bank_code": instance.bank.bank_code,
        "currency": instance.bank.currency
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response_json = response.json()

        if response_json["status"]:
            payload = {'status': 200, 'data': response_json['data']["recipient_code"]}
        else:
            print(response_json)
            payload = {'status': 200, 'data': response_json["message"]}

        return payload

    except requests.exceptions.RequestException as req_err:
        print(f"Error occurred: {req_err}")

    # Return None or an appropriate message if an exception occurs
    return None