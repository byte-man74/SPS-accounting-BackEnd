import uuid
from django.db import models
import json
from Main.model_function.helper import generate_taxroll_staff_table_out_of_payroll
from datetime import datetime


class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=50)
    #django media settings
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

    Transaction_type = (
        ("Transfer", "Transfer"),
        ("Cash", "Cash"),
    )
    Transaction_category = (
        ("Credit", "Credit"),
        ("Debit", "Debit"),
    )
    Status_choice = (
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
        ("Cancelled", "Cancelled"),
        ("Retrying", "Retrying"),
    )

    time = models.DateTimeField(default=datetime.now)
    amount = models.BigIntegerField()

    transaction_type = models.CharField(
        max_length=100, choices=Transaction_type)
    status = models.CharField(choices=Status_choice, max_length=50)
    transaction_category = models.CharField(
        max_length=50, choices=Transaction_category)
    particulars = models.ForeignKey(
        "Main.Particulars", on_delete=models.CASCADE)

    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)

    name_of_reciever = models.CharField(max_length=100, blank=False, null=False)
    account_number_of_reciever = models.CharField(max_length=20, null=False, blank=True)
    reciever_bank = models.CharField(max_length=50, null=True, blank=True)

    # the transaction will only start working after approval
    is_approved = models.BooleanField(default=False)

    # ? Methods

    @staticmethod
    def get_transaction(transaction_type=None, transaction_category=None, start_date=None, end_date=None, status=None, school= None):
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

        if school:
            query = query.filter(school=school)


        return query


    def save(self, *args, **kwargs):
        # Check if it's a "Transfer" transaction type
        if self.transaction_type == "Transfer":

            # Check if account number and receiver name are provided
            if not self.account_number_of_reciever and not self.name_of_reciever:
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
    Transaction_category = (
        ("Credit", "Credit"),
        ("Debit", "Debit"),
    )
    time = models.DateTimeField(auto_now_add=True)
    amount = models.BigIntegerField()
    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)


class Particulars (models.Model):
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
    staff_type = models.ForeignKey(Staff_type, on_delete=models.SET_NULL, null=True)
    salary_deduction = models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    tin_number = models.CharField(max_length=50)

    @staticmethod
    def reset_salary_deduction_for_staffs_in_a_school (school_id):
        staffs = Staff.objects.filter(school=school_id)

        for staff in staffs:
            staff.salary_deduction = 0
            staff.save()

    def get_staf_total_payment (self):
        basic_salary = self.staff_type.basic_salary
        tax = self.staff_type.tax
        salary_deduction = self.salary_deduction
        salary_to_be_paid = basic_salary - (tax + salary_deduction)

        return salary_to_be_paid

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    

'''payroll'''
class Payroll(models.Model):
    Status = (
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
        ("Reconciliation", "Reconciliation"),
    )

    name = models.CharField(max_length=100)
    date_initiated = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=Status, default="Pending")
    # Change staffs field to a JSONField
    staffs = models.JSONField()

    #financials
    total_amount_for_tax = models.BigIntegerField()
    total_amount_for_salary = models.BigIntegerField()

    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)


    #!
    def add_staff(self, staff_data_list):
        if "staffs" not in self.staffs:
            self.staffs = []

        self.staffs.extend(staff_data_list)  # Use extend to add all elements in the list


    #! method to calculate the total amount paid for tax
    def total_tax_paid(self):
        total_tax = [ total_tax + staff.Staff.get_staff_total_payment.tax for staff in self.staffs ]
        return total_tax
    
    #! method to calculate the total amount paid for salary
    def total_salary_paid(self):
        total_salary = [ total_salary + staff.Staff.get_staff_total_payment.salary_to_be_paid for staff in self.staffs ]
        return total_salary
    
    

    def remove_staff_by_id(self, staff_id):
        if "staffs" not in self.staffs:
            return  # If staffs is not a list, nothing to remove

        updated_staffs = [staff for staff in self.staffs if staff.get("staff_id") != staff_id]
        self.staffs = updated_staffs


    def get_all_failed_staff_payment(self):
        failed_staffs = []
        for staff in self.staffs:
            if staff.get("status") == "Failed":
                failed_staffs.append(staff)

        return failed_staffs
    
    def get_payment_summary(self):
        total_amount_for_tax = self.total_amount_for_tax
        total_amount_for_salary = self.total_amount_for_salary
        total_staffs = len(self.staffs)
        successful_staffs = sum(1 for staff in self.staffs if staff.get("status") == "SUCCESS")
        failed_staffs = sum(1 for staff in self.staffs if staff.get("status") == "FAILED")

        return {
            "total_amount_for_tax": total_amount_for_tax,
            "total_amount_for_salary": total_amount_for_salary,
            "total_staffs": total_staffs,
            "successful_staffs": successful_staffs,
            "failed_staffs": failed_staffs,
        }

    def save(self, *args, **kwargs):
        # Convert staffs list to JSON before saving
        if isinstance(self.staffs, list):
            self.staffs = json.dumps(self.staffs)
        super().save(*args, **kwargs)



    def __str__(self):
        return self.name



class Taxroll(models.Model):
    Status = (
        ("Pending", "Pending"),
        ("Success", "Success"),
        ("Failed", "Failed"),
        ("Reconciliation", "Reconciliation"),
    )
    
    name = models.CharField(max_length=100)
    amount_paid_for_tax = models.BigIntegerField()
    date_initiated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=Status)
    staffs = models.JSONField()

    # Create a one-to-one relationship with the Payroll model
    payroll = models.OneToOneField("Main.Payroll", on_delete=models.CASCADE)


    def add_staff(self, staff_data_list):
        if "staffs" not in self.staffs:
            self.staffs = []

        self.staffs.extend(staff_data_list)  # Use extend to add all elements in the list


    def save(self, *args, **kwargs):
        # Convert staffs list to JSON before saving
        if isinstance(self.staffs, list):
            self.staffs = json.dumps(self.staffs)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    

    @staticmethod
    def generate_taxroll_out_of_payroll(payroll_id):
        try:
            payroll = Payroll.objects.select_related('school').get(id=payroll_id)
            staffs_on_payroll = json.loads(payroll.staffs)
            
            # Generate taxroll staffs from payroll staffs
            taxroll_staffs = generate_taxroll_staff_table_out_of_payroll(staffs_on_payroll)

            # Create a Taxroll instance
            taxroll_name = f'Taxroll for {payroll.name}'
            taxroll = Taxroll.objects.create(
                name=taxroll_name,
                amount_paid_for_tax=payroll.total_amount_for_tax,
                status=Payroll.Status['Success'],
                staffs=taxroll_staffs,
                payroll=payroll
            )
            taxroll.save()
            return ("SUCCESS")  # Successful generation
        except Payroll.DoesNotExist:
            return ("ERROR_404")
        except Exception as e:
            print(f"Error generating Taxroll: {str(e)}")
            return ("ERROR_502")  # Error occurred during generation




