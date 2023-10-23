
from django.db import models



class Operations_account (models.Model):
    name = models.CharField(max_length=100, verbose_name="Bank Account Name")
    account_number = models.CharField(
        max_length=100, verbose_name="Account Number")
    school = models.OneToOneField("Main.School", on_delete=models.CASCADE)
    amount_available_cash = models.BigIntegerField()
    amount_available_transfer = models.BigIntegerField()

    def get_total_amount_available(self):
        calculated_amount = self.amount_available_cash + self.amount_available_transfer
        return calculated_amount

    def __str__(self):
        return f'{self.school.name} Operation account'
    


class Capital_Account (models.Model):
    name = models.CharField(max_length=100, verbose_name="Bank Account Name")
    account_number = models.CharField(
        max_length=100, verbose_name="Account Number")
    school = models.OneToOneField("Main.School", on_delete=models.CASCADE)
    amount_availabe = models.BigIntegerField()

    def __str__(self):
        return f'{self.school.name} Capital account'
