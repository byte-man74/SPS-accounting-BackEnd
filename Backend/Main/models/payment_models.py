import uuid
from django.db import models
import json
from Main.model_function.helper import generate_taxroll_staff_table_out_of_payroll
from datetime import datetime



class Payroll(models.Model):
    Status = (
        ("PENDING", "PENDING"),
        ("INITIALIZED", "INITIALIZED"),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
        ("RECONCILIATION", "RECONCILIATION"),
    )

    name = models.CharField(max_length=100)
    date_initiated = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=100, choices=Status, default="PENDING")
    # Change staffs field to a JSONField
    staffs = models.JSONField()

    # financials
    total_amount_for_tax = models.BigIntegerField()
    total_amount_for_salary = models.BigIntegerField()

    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)

    #!

    def add_staff(self, staff_data_list):
        if "staffs" not in self.staffs:
            self.staffs = []

        # Use extend to add all elements in the list
        self.staffs.extend(staff_data_list)

    #! method to calculate the total amount paid for tax

    def total_tax_paid(self):
        total_tax = [
            total_tax + staff.Staff.get_staff_total_payment.tax for staff in self.staffs]
        return total_tax

    #! method to calculate the total amount paid for salary
    def total_salary_paid(self):
        total_salary = [
            total_salary + staff.Staff.get_staff_total_payment.salary_to_be_paid for staff in self.staffs]
        return total_salary

    def remove_staff_by_id(self, staff_id):
        if "staffs" not in self.staffs:
            return  # If staffs is not a list, nothing to remove

        updated_staffs = [
            staff for staff in self.staffs if staff.get("staff_id") != staff_id]
        self.staffs = updated_staffs

    def get_all_failed_staff_payment(self):
        failed_staffs = []
        for staff in self.staffs:
            if staff.get("status") == "FAILED":
                failed_staffs.append(staff)

        return failed_staffs

    def get_payment_summary(self):
        total_amount_for_tax = self.total_amount_for_tax
        total_amount_for_salary = self.total_amount_for_salary
        total_staffs = len(self.staffs)
        successful_staffs = sum(
            1 for staff in self.staffs if staff.get("status") == "SUCCESS")
        failed_staffs = sum(
            1 for staff in self.staffs if staff.get("status") == "FAILED")

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
        ("PENDING", "PENDING"),
        ("INITIALIZED", "INITIALIZED"),
        ("SUCCESS", "SUCCESS"),
        ("FAILED", "FAILED"),
        ("RECONCILIATION", "RECONCILIATION"),
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

        # Use extend to add all elements in the list
        self.staffs.extend(staff_data_list)

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
            payroll = Payroll.objects.select_related(
                'school').get(id=payroll_id)
            staffs_on_payroll = json.loads(payroll.staffs)

            # Generate taxroll staffs from payroll staffs
            taxroll_staffs = generate_taxroll_staff_table_out_of_payroll(
                staffs_on_payroll)

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
            return ("ERROR_502")  # Error occurred during generation3
