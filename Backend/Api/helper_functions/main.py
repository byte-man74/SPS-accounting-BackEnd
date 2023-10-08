from Main.models import *
from Authentication.models import CustomUser
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from Authentication.models import CustomUser
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.status import *
from rest_framework.exceptions import PermissionDenied
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from django.db.models import Sum


def check_account_type(user, account_type):
    def get_user_type(user, account_type):
        user_model = get_user_model()
        user = user_model.objects.get(id=user.id)

        if user.account_type != account_type:
            raise PermissionDenied()  # Raise an exception if unauthorized

    get_user_type(user, account_type)  # Call the inner function


def get_school_from_user(user_id):
    try:
        custom_user = get_object_or_404(CustomUser, id=user_id)
        user_school = custom_user.school
        return user_school.id
    except CustomUser.DoesNotExist:
        # Handle the case where the user does not exist
        return None


def get_unarranged_transaction_six_months_ago(school_id):
    try:
        current_date = datetime.now()
        print(current_date)
        six_months_ago = current_date - relativedelta(months=6)
        print(six_months_ago)

        # Use the model class directly to filter records
        transaction_records = Operations_account_transaction_record.get_transaction(
            start_date=six_months_ago,
            end_date=current_date,
            school=school_id
        ).filter(status="SUCCESS", transaction_category="DEBIT")

        transaction_records_list = [
            {
                "time": record.time,
                "amount": record.amount,
                "transaction_type": record.transaction_type
            }

            for record in transaction_records
        ]

        return transaction_records_list

    except Operations_account_transaction_record.DoesNotExist:
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
        ).filter(status="SUCCESS")

        # Convert the queryset to a list of dictionaries
        transaction_records_list = [
            {
                "time": record.time,
                "amount": record.amount,
                "transaction_type": record.transaction_type,
                "status": record.status,
                "reason": record.reason,
                "name_of_reciever": record.name_of_reciever,
                "particulars": record.particulars
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


def process_and_sort_transactions_by_months(transactions):
    import calendar

    monthly_totals = {}

    for transaction in transactions:
        transaction_date = transaction['time']
        month_name = calendar.month_name[transaction_date.month]

        # Check if the month already exists in the dictionary, and if not, initialize it
        if month_name not in monthly_totals:
            monthly_totals[month_name] = {
                'month': month_name,
                'total_amount': 0,
            }

        # Update the total amount for the corresponding month
        monthly_totals[month_name]['total_amount'] += transaction['amount']

    # Sort the monthly totals by month name
    sorted_monthly_totals = sorted(
        monthly_totals.values(),
        key=lambda x: list(calendar.month_name).index(x['month'])
    )

    return sorted_monthly_totals


def process_and_sort_transactions_by_days(transactions):
    daily_totals = defaultdict(lambda: {"date": None, "transaction_data": []})

    for transaction in transactions:
        transaction_date = transaction['time'].date()
        data = {
            "particulars": transaction['particulars'].name,
            "amount": transaction['amount'],
            "reason": transaction['reason']
        }

        daily_totals[transaction_date]["date"] = format_date(transaction_date)
        daily_totals[transaction_date]["transaction_data"].append(data)

    return list(daily_totals.values())


def calculate_cash_and_transfer_transaction_total(transactions):
    cash_total = 0
    transfer_total = 0

    for transaction in transactions:
        # Check if the transaction has a 'transaction_type' field and it is "Cash"
        if 'transaction_type' in transaction and transaction['transaction_type'] == "CASH":
            cash_total += transaction['amount']

        if 'transaction_type' in transaction and transaction['transaction_type'] == "TRANSFER":
            transfer_total += transaction['amount']

    return cash_total, transfer_total


def get_user_school(user):
    return get_object_or_404(School, id=get_school_from_user(user.id))


def get_transaction_summary_by_header(transactions):
    transaction_summary = {}

    for transaction in transactions:
        # Get the particulars object associated with the transaction
        particulars = transaction.particulars

        # Get the name of the particulars
        particulars_name = particulars.name

        # Check if a summary for this particulars already exists
        if particulars_name in transaction_summary:
            summary = transaction_summary[particulars_name]
        else:
            # If not, initialize a new summary dictionary
            summary = {
                'total_amount': 0,
                'percentage': 0,
            }

        # Update the summary for this particulars
        summary['total_amount'] += transaction.amount

        # Update or add the summary to the transaction_summary dictionary
        transaction_summary[particulars_name] = summary

    all_amount = sum(summary['total_amount']
                     for summary in transaction_summary.values())

    # Calculate the percentage for each particulars
    for particulars_name, summary in transaction_summary.items():
        percentage = (summary['total_amount'] / all_amount) * 100
        summary['percentage'] = percentage

    return transaction_summary


def get_cash_left_and_month_summary(school_id):
    operation_account = get_object_or_404(Operations_account, school=school_id)
    cash_amount_left = operation_account.amount_available_cash

    # Get the current date and time in the appropriate time zone
    current_date = timezone.now()

    # Calculate the beginning of the current month
    beginning_of_month = timezone.make_aware(
        timezone.datetime(current_date.year, current_date.month, 1)
    )

    total_amount = Operations_account_transaction_record.objects.filter(
        time__range=(beginning_of_month, current_date)
    ).aggregate(Sum('amount'))['amount__sum']

    # Create a dictionary with the result data
    data = {
        "cash_amount": cash_amount_left,
        "total_amount": total_amount or 0
    }

    return data



def get_all_school_header (school_id):
    particulars = Particulars.objects.filter(school=school_id)
    print(particulars)

    return particulars