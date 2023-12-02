from django.db import models
from Main.configuration import *


class PaymentStatus (models.Model):
    student = models.OneToOneField("Main.Student", on_delete=models.CASCADE)
    status = models.CharField(choices=fee_status, max_length=50)
    amount_in_debt = models.BigIntegerField(default=0)
    amount_outstanding = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.student} payment status'
    


class PaymentHistory (models.Model):
    student = models.ForeignKey("Main.Student",  on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date_time_initiated = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    merchant_email = models.EmailField()

    amount_debited = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20)


    receipt_id = models.CharField(max_length=20)
    paystack_reference = models.CharField(max_length=50)


    breakdowns = models.JSONField()

    def __str__(self):
        return f'{self.student} payment reciept'
    


'''
- the breakdown structure
- add the grade section model method 
- test the models in admin
'''