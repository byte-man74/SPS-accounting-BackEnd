from django.db import models
from Main.models.payment_models import *
from Main.models.transaction_records_models import *
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
# from django.dispatch import Signal

# transaction_status = [('pending', 'Pending'), 
#                       ('approved', 'Approved'), 
#                       ('declined', 'Declined')]

# class Transaction_status(models.Model):
#     message = models.CharField(max_length=250, choices=transaction_status)

#     def __str__(self):
#         return str(self.message)


Transaction = Operations_account_transaction_record.objects.all()
Payroll = Payroll.objects.all()

@receiver(pre_save, sender=Transaction)
def transaction_pending_handler(sender, instance, **kwargs):
    if instance.status == "PENDING":
        message = "Transaction Pending"
        print(f'{message}')


@receiver(pre_save, sender=Transaction)
def transaction_approved_handler(sender, instance, **kwargs):
    if instance.status == "SUCCESS":
        message = "Transaction Approved"
        print(f'{message}')


@receiver(pre_save, sender=Transaction)
def transaction_declined_handler(sender, instance, **kwargs):
    if instance.status == "CANCELLED":
        message = "Transaction Declined"
        print(f'{message}')


@receiver(pre_save, sender=Transaction)
def transaction_initiated_handler(sender, instance, **kwargs):
    if instance.status == "INITIALIZED" and instance.transaction_type=="CASH":
        message = "Cash Transaction has been initiated"
        print(f'{message}')


@receiver(pre_save, sender=Payroll)
def salary_pending_handler(sender, instance, **kwargs):
    if instance.status == "PENDING":
        message = "Salary Payment is Pending"
        print(f'{message}')

@receiver(pre_save, sender=Payroll)
def salary_initiated_handler(sender, instance, **kwargs):
    if instance.status == "INITIALIZED":
        message = "Salary Payment was Initiated"
        print(f'{message}')

@receiver(pre_save, sender=Payroll)
def salary_success_handler(sender, instance, **kwargs):
    if instance.status == "SUCCESS":
        message = "Salary Payment was successful"
        print(f'{message}')

@receiver(pre_save, sender=Payroll)
def salary_failed_handler(sender, instance, **kwargs):
    if instance.status == "FAILED":
        message = "Salary Payment Failed"
        print(f'{message}')


