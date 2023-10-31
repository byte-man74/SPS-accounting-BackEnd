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
from Main.models import Operations_account, Operations_account_transaction_record
from Api.helper_functions.main import *
from Api.Api_pages.operations.serializers import *
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
account_type = "OPERATIONS"



class GetAllStaffs (APIView):
    # this api is responsible for getting all the staff (active)
    pass


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