import uuid
from django.db import models

class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=50)
    logo = models.ImageField()

    def __str__(self):
        return self.name
    


class Operations_Account (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Bank Account Name")
    account_number = models.CharField(max_length=100, verbose_name="Account Number")
    school = models.OneToOneField("Main.School", on_delete=models.CASCADE)
    amount_available_cash = models.BigIntegerField()
    amount_available_transfer = models.BigIntegerField()


    def get_total_amount_available (self):
        calculated_amount = self.amount_available_cash + self.amount_available_transfer 
        return calculated_amount



class Operations_account_transaction_record (models.Model):

    Transaction_type = {
        "Transfer": "Transfer",
        "Cash": "Cash",
    }
    Transaction_category = {
        "Credit": "Credit",
        "Debit": "Debit",
    }
    Status_choice = {
        "Pending": "Pending",
        "Success": "Success",
        "Failed": "Failed",
        "Cancelled": "Cancelled",
        "Retrying": "Retrying",
    }

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    time = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField()
    transaction_type = models.CharField(max_length=100, choices=Transaction_type )
    status = models.CharField(choices=Status_choice, max_length=50)
    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)
    name_of_reciever = models.CharField(max_length=100)
    transaction_category = models.CharField(max_length=50, choices=Transaction_category)
    particulars = models.ForeignKey("Main.Particulars", on_delete=models.CASCADE)

    # the transaction will only start working after approval 
    is_approved = models.BooleanField(default=False)


    @staticmethod
    def get_transaction(transaction_type=None, transaction_category=None, start_date=None, end_date=None, status=None):
        query = Operations_account_transaction_record.objects.all()

        if transaction_type:
            query = query.filter(transaction_type=transaction_type)

        if transaction_category:
            query = query.filter(transaction_category=transaction_category)

        if start_date:
            query = query.filter(time__date__gte=start_date)

        if end_date:
            query = query.filter(time__date__lte=end_date)

        if status:
            query = query.filter(status=status)

        return query





class Capital_Account (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name="Bank Account Name")
    account_number = models.CharField(max_length=100, verbose_name="Account Number")
    school = models.OneToOneField("Main.School", on_delete=models.CASCADE)
    amount_availabe = models.BigIntegerField()




class Paticulars (models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)

    def __str__(self):
        return self.name