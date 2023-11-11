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
    permission_classes = [IsAuthenticated]
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
        try:
            # Check if the authenticated user has the required account type.
            check_account_type(request.user, account_type)

            approval_data = request.data['status']
            payroll_instance = Payroll.objects.get(id=payroll_id)
            payroll_instance.status = (approval_data)
            payroll_instance.save()
    
            if approval_data == "INITIALIZED":
                #send a notification to the operations
                process_salary_payment(payroll_id)

            elif approval_data == "CANCELLED":
                #send a notification to the operations accountant 
                pass 

            return Response({"message": "An error occurred"}, status=HTTP_200_OK)


        except PermissionDenied:
            # If the user doesn't have the required permissions, return an HTTP 403 Forbidden response.
            return Response({"message": "Permission denied"}, status=HTTP_403_FORBIDDEN)

        except APIException as e:
            # Handle specific API-related errors and return their details.
            return Response({"message": str(e.detail)}, status=e.status_code)

        except Exception as e:
            # For all other exceptions, return a generic error message.
            return Response({"message": "An error occurred"}, status=HTTP_403_FORBIDDEN)
