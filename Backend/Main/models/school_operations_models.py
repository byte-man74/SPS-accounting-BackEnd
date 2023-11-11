import uuid
from django.db import models
import json
from Main.model_function.helper import generate_taxroll_staff_table_out_of_payroll
from datetime import datetime
from Main.model_function.helper import *
from Paystack.service import *
from django.core.exceptions import ValidationError


class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email_address = models.EmailField(max_length=50)
    # django media settings
    logo = models.ImageField()

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
    bank = models.ForeignKey("Paystack.Bank", on_delete=models.CASCADE)
    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)
    staff_type = models.ForeignKey(
        Staff_type, on_delete=models.SET_NULL, null=True)
    salary_deduction = models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    tin_number = models.CharField(max_length=50)
    paystack_id = models.CharField(max_length=50, blank=True)

    @staticmethod
    def reset_salary_deduction_for_staffs_in_a_school(school_id):
        staffs = Staff.objects.filter(school=school_id)

        for staff in staffs:
            staff.salary_deduction = 0
            staff.save()

    def get_staf_total_payment(self):
        basic_salary = self.staff_type.basic_salary
        tax = self.staff_type.tax
        salary_deduction = self.salary_deduction
        salary_to_be_paid = basic_salary - (tax + salary_deduction)

        return salary_to_be_paid

    def __str__(self):
        return f'{self.first_name} {self.last_name}'



    def save(self, *args, **kwargs):
        # If paystack_id is not already assigned, generate it.
        if not self.paystack_id:
            paystack_id_generated = generate_paystack_id_for_staff(instance=self)
            
            # Check if the generated paystack_id is 400 (or any other condition you want).
            if paystack_id_generated['status'] == 400:
                raise ValidationError(paystack_id_generated['data'])  # Use ValidationError instead of ValueError
            
            
            self.paystack_id = paystack_id_generated['data']
        
        super().save(*args, **kwargs)
