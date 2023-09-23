from Main.models import School
from Authentication.models import CustomUser
from django.shortcuts import get_object_or_404

def get_school_from_user(user_id):
    try:
        custom_user = get_object_or_404(CustomUser, id=user_id)
        user_school = custom_user.school
        return user_school.id
    except CustomUser.DoesNotExist:
        # Handle the case where the user does not exist
        return None
