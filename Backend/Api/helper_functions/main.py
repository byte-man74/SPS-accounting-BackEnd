from Main.models import Operations_account_transaction_record
from Authentication.models import CustomUser
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta


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

        return(transaction_records)

    except Operations_account_transaction_record.DoesNotExist:
        return None
    



def arrange_transaction_list_by_days_of_the_week (transaction_list):
    pass