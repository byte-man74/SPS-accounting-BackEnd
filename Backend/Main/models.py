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

    time = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField()

    transaction_type = models.CharField(
        max_length=100, choices=Transaction_type)
    status = models.CharField(choices=Status_choice, max_length=50)
    transaction_category = models.CharField(
        max_length=50, choices=Transaction_category)
    particulars = models.ForeignKey(
        "Main.Particulars", on_delete=models.CASCADE)

    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)

    name_of_reciever = models.CharField(max_length=100)
    account_number_of_reciever = models.CharField(max_length=20)
    reciever_bank = models.CharField(max_length=50, null=True, blank=True)

    # the transaction will only start working after approval
    is_approved = models.BooleanField(default=False)

    # ? Methods

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


    def save(self, *args, **kwargs):
        # Check if it's a "Transfer" transaction type
        if self.transaction_type == "Transfer":

            # Check if account number and receiver name are provided
            if not self.account_number_of_reciever or not self.name_of_reciever:
                raise ValueError(
                    "Both account number and receiver name must be provided for a Transfer transaction.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.transaction_type} transaction {self.school.name}'


class Capital_Account (models.Model):
    name = models.CharField(max_length=100, verbose_name="Bank Account Name")
    account_number = models.CharField(
        max_length=100, verbose_name="Account Number")
    school = models.OneToOneField("Main.School", on_delete=models.CASCADE)
    amount_availabe = models.BigIntegerField()

    def __str__(self):
        return f'{self.school.name} Capital account'


class Capital_account_transaction_history (models.Model):
    Transaction_category = {
        "Credit": "Credit",
        "Debit": "Debit",
    }

    time = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField()
    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)


class Paticulars (models.Model):
    name = models.CharField(max_length=100)
    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)

    def __str__(self):
        return self.name





'''Staff section'''
class Staff_type (models.Model):
    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)
    basic_salary = models.BigIntegerField()
    tax = models.BigIntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Staff (models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    account_number = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=40)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    staff_type = models.ForeignKey(Staff_type, on_delete=models.SET_NULL)
    salary_deduction = models.BigIntegerField()
    is_active = models.BooleanField(default=True)


    @staticmethod
    def reset_salary_deduction_for_staffs_in_a_school (school_id):
        staffs = Staff.objects.filter(school=school_id)

        for staff in staffs:
            staff.salary_deduction = 0
            staff.save()



    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    



'''payroll'''
class Payroll_type (models.Model):
    name = models.CharField(max_length=100)
    date_initiated = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    #financials
    total_amount_for_tax = models.BigIntegerField()
    total_amount_for_salary = models.BigIntegerField()



    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)

    def __str__(self):
        return self.name