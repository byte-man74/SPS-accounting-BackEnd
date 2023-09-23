from Main.models import School
from Authentication.models import CustomUser


def Get_school_for_user (user_id):
    user_school_id = CustomUser.objects.get(id=user_id)
