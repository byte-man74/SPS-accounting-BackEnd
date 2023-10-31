from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from Api.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, viewsets
from rest_framework.views import APIView
# from Background_Tasks.tasks import
from django.core.cache import cache
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from Main.models import Operations_account, Operations_account_transaction_record, Staff
from Api.helper_functions.main import *
from Api.helper_functions.auth_methods import *
from Api.Api_pages.operations.serializers import *
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException



account_type = "OPERATIONS"



class GetAllStaffs (APIView):
    """
    API endpoint to get all the active staff.
    """
    permission_classes = [HasRequiredAccountType, IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            # Fetch the school associated with the requesting user.
            user_school = get_user_school(request.user)

            # Filter out the active staff members associated with the user's school.
            staffs_active_in_school = Staff.objects.filter(school=user_school, is_active=True)

            # Use pagination for the results.
            page = self.pagination_class().paginate_queryset(staffs_active_in_school, request)
            serialized_data = StaffSerializer(page, many=True).data

            return self.pagination_class().get_paginated_response(serialized_data)

        except APIException as e:
            # If there's an API-related error, return its detail.
            return Response({"message": str(e.detail)}, status=e.status_code)
        except Exception as e:
            # General exception handling, consider logging the error for debugging.
            return Response({"message": "An error occurred"}, status=HTTP_403_FORBIDDEN)
        




class AddStaff (APIView):
    # this api is responsible for adding a new staff
    pass 

class EditStaff (APIView):
    # this api is responsible for editing a staff (active)
    pass 


def ModifyStaffSalaryRelief(): 
   # this api is responsible for altering the staff deduction of salary
   pass  



class InitiatePayroll (APIView):
    # this api is responsible for creating a payroll instance
    pass


class InitiateTaxroll (APIView):
    # this api is responsible for creating a Taxroll instance from an existing payroll
    pass 


class GenerateTransactionSummary (APIView):
    # this api is responsible for returning a TransactionSummary from an existing payroll transactio
    pass


class InitiateSalaryPayment (APIView):
    # this api is responsible for initializing a salary payment
    pass 


class GetAllPayroll (APIView):
    # this api is responsible for getting all SalaryPayments
    pass


class RequeryFailedPayrollTransaction (APIView):
    # this api is responsible for requerying failed payments
    pass









########framework
'''class TestClass (APIView):
    # this api is responsible for getting all the staff (active)
    def get(self):
        try:
            check_account_type(self.request.user, account_type)
            user_school = get_user_school(self.request.user)
        except PermissionDenied:
            return Response({"message": "Permission denied"}, status=HTTP_401_UNAUTHORIZED)'''