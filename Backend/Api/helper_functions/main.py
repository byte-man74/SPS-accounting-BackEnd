from Main.models import *
from Authentication.models import CustomUser
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from Authentication.models import CustomUser


def get_school_from_user(user_id):
    try:
        custom_user = get_object_or_404(CustomUser, id=user_id)
        user_school = custom_user.school
        return user_school.id
    except CustomUser.DoesNotExist:
        # Handle the case where the user does not exist
        return None


def get_unarranged_transaction_seven_days_ago(school_id):
    try:
        current_date = datetime.now()
        seven_days_ago = current_date - timedelta(days=7)

        # Use the model class directly to filter records
        transaction_records = Operations_account_transaction_record.get_transaction(
            start_date=seven_days_ago,
            end_date=current_date,
            school=school_id
        ).filter(is_approved=True)

        # Convert the queryset to a list of dictionaries
        transaction_records_list = [
            {
                "time": record.time,
                "amount": record.amount,
                "transaction_type": record.transaction_type,
                "status": record.status,
                "name_of_reciever": record.name_of_reciever,
                "particulars": record.particulars

                # Add more fields as needed
            }
            for record in transaction_records
        ]

        return transaction_records_list

    except Operations_account_transaction_record.DoesNotExist:
        return None




def format_date(date):
    # Create a dictionary for mapping month numbers to month names
    month_names = {
        1: "January", 2: "February", 3: "March", 4: "April", 5: "May",
        6: "June", 7: "July", 8: "August", 9: "September", 10: "October",
        11: "November", 12: "December"
    }

    day_of_week = date.strftime("%A")


    day_of_month = date.strftime("%d")
    if day_of_month.endswith("1") and day_of_month != "11":
        day_of_month += "st"
    elif day_of_month.endswith("2") and day_of_month != "12":
        day_of_month += "nd"
    elif day_of_month.endswith("3") and day_of_month != "13":
        day_of_month += "rd"
    else:
        day_of_month += "th"


    month = month_names[date.month]


    year = date.strftime("%Y")

    formatted_date = f"{day_of_week}, {day_of_month} {month} {year}"

    return formatted_date



def process_and_sort_transactions(transactions):

    daily_totals = {}
    for transaction in transactions:
        transaction_date = transaction['time'].date()
        total_amount = daily_totals.get(transaction_date, 0)
        total_amount += transaction['amount']

        daily_totals[transaction_date] = total_amount
    

    sorted_daily_totals = sorted(daily_totals.items(), key=lambda x: x[0])
    
    result = [{'date': format_date(date), 'total_amount': total} for date, total in sorted_daily_totals]
    
    return result


def calculate_cash_and_transfer_transaction_total(transactions):
    cash_total = 0
    transfer_total = 0

    for transaction in transactions:
        # Check if the transaction has a 'transaction_type' field and it is "Cash"
        if 'transaction_type' in transaction and transaction['transaction_type'] == "Cash":
            cash_total += transaction['amount']

        if 'transaction_type' in transaction and transaction['transaction_type'] == "Transfer":
            transfer_total += transaction['amount']

    return cash_total, transfer_total



def get_user_school(user):
    return get_object_or_404(School, id=get_school_from_user(user.id))




def get_transaction_summary_by_header(transactions):
    transaction_summary = {}

    for transaction in transactions:
        # Get the particulars name from the transaction
        particulars_name = transaction['particulars_name']

        # Check if a summary for this particulars already exists
        if particulars_name in transaction_summary:
            summary = transaction_summary[particulars_name]
        else:
            # If not, initialize a new summary dictionary
            summary = {
                'total_amount': 0,
                'transaction_count': 0,
                'transactions': []
            }

        # Update the summary for this particulars
        summary['total_amount'] += transaction['amount']
        summary['transaction_count'] += 1
        summary['transactions'].append(transaction)

        # Update or add the summary to the transaction_summary dictionary
        transaction_summary[particulars_name] = summary

    return transaction_summary
