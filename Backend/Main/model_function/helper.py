from django.core.exceptions import ObjectDoesNotExist
from Main.models import Staff, School

def generate_taxroll_staff_table_out_of_payroll(staffs_on_payroll):
    taxroll_staffs = []
    
    for staff_data in staffs_on_payroll:
        try:
            staff_object = Staff.objects.get(id=staff_data['staff_id'])
            annual_income = staff_data['basic_salary'] * 12

            taxroll_staff = {
                "staff_name": staff_data.get('staff_name'),
                "staff_id": staff_data.get('staff_id'),
                "rank": staff_data.get('rank'),
                "tax_payable": staff_data.get('tax'),
                "basic_salary": staff_data.get('basic_salary'),
                "Annual_Income": annual_income,
                "TIN": staff_object.tin_number,
                "account_number": staff_data.get('account_number'),  # Use provided account_number or None
                "bank": staff_data.get('bank'),  # Use provided bank or None
                "account_name": staff_data.get('account_name'),
            }

            taxroll_staffs.append(taxroll_staff)
        except ObjectDoesNotExist:
            # Handle the case where the staff with the specified staff_id does not exist
            pass

    return taxroll_staffs


def generate_staffroll (school_name):
    staff_payroll = []
    # staffs inside the schol with active acount
    # create empty list
    # loop through all the staffs
    staffs = Staff.objects.select_related("staff_type").filter(school=school_name)
    for staff in staffs:
        try:
            if staff.is_active == "True": 
                staff_payroll = {
                    "staff_firstname": staff.first_name,
                    "staff_lastname": staff.last_name,
                    "staff_phonenumber": staff.phone_number,
                    "staff_id": staff.get('staff_id'),
                    "rank": staff.get('rank'),
                    "tax_payable": staff.Staff_type.tax,
                    "basic_salary": staff.Staff_type.basic_salary,
                    "Annual_Income": staff['basic_salary'] * 12,
                    "school": staff.school,
                    "TIN": staff.tin_number,
                    "account_number": staff.account_number, 
                    "bank": staff.bank_name,     
                }

            staff_payroll.append(staff_payroll)
        except ObjectDoesNotExist:
            # Handle the case where the staff with the specified staff_id does not exist
            pass
    return staff_payroll