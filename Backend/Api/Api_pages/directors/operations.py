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
from Main.models import Operations_account, Operations_account_transaction_record, Staff, Payroll
from Api.helper_functions.main import *
from Api.helper_functions.auth_methods import *
from Api.helper_functions.directors.main import *
from Api.Api_pages.operations.serializers import *
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException
from rest_framework.decorators import api_view
from Main.model_function.helper import generate_staffroll

account_type = "DIRECTOR"



class GetAllPayroll (APIView):
    '''
        this would get the list of all the payroll created
    '''
    pass

class ViewPayrollDetails (APIView):
    '''
        This would get the details of a particular payroll instance
    '''
    pass 


class ApprovePayroll (APIView):
    '''
        This API is responsible for the approval of salary payment after the operation accountant
        has processed it
    '''
    def post (self, request, payroll_id, *args, **kwargs):
        approval_data = request.data['STATUS']
        payroll_instance = Payroll.objects.get(id=payroll_id)
        payroll_instance.status = (approval_data)
        payroll_instance.save()
  
        if approval_data == "SUCCESS":
            #send a notification to the operations
            process_salary_payment(payroll_id)

        elif approval_data == "CANCELLED":
            #send a notification to the operations accountant 
            pass 
