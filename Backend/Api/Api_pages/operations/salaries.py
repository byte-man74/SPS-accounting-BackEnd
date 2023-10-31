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
from rest_framework.decorators import api_view

account_type = "OPERATIONS"


class GetAllStaffs(APIView):
    """
    API endpoint to get all the active staff.
    """

    def get(self, request, *args, **kwargs):
        try:
            # Check if the authenticated user has the required account type.
            check_account_type(request.user, account_type)

            # Fetch the school associated with the requesting user.
            user_school = get_user_school(request.user)

            # Filter out the active staff members associated with the user's school.
            staffs_active_in_school = Staff.objects.filter(
                school=user_school, is_active=True)

            # Serialize the staff data for the response.
            serialized_data = StaffReadSerializer(
                staffs_active_in_school, many=True).data

            # Return the serialized staff data with a 200 OK status.
            return Response(serialized_data, status=HTTP_200_OK)

        except PermissionDenied:
            # If the user doesn't have the required permissions, return an HTTP 403 Forbidden response.
            return Response({"message": "Permission denied"}, status=HTTP_403_FORBIDDEN)

        except APIException as e:
            # Handle specific API-related errors and return their details.
            return Response({"message": str(e.detail)}, status=e.status_code)

        except Exception as e:
            # For all other exceptions, return a generic error message.
            return Response({"message": "An error occurred"}, status=HTTP_403_FORBIDDEN)


class AddStaff (APIView):
    """
        this api is responsible for adding a new staff 
        this api is responsible for editing the details of the staff
    """

    def post(self, request):
        try:
            # Check if the authenticated user has the required account type.
            check_account_type(request.user, account_type)
            user_school = get_user_school(request.user)

            data = request.data
            serialized_data = StaffWriteSerializer(data)

            if serialized_data.is_valid():
                serialized_data.save(school=user_school)

                # todo: add notification

                return Response({"message": "Staff edited successfully"}, status=HTTP_201_CREATED)
            return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)

        except PermissionDenied:
            # If the user doesn't have the required permissions, return an HTTP 403 Forbidden response.
            return Response({"message": "Permission denied"}, status=HTTP_403_FORBIDDEN)

        except APIException as e:
            # Handle specific API-related errors and return their details.
            return Response({"message": str(e.detail)}, status=e.status_code)

        except Exception as e:
            # For all other exceptions, return a generic error message.
            return Response({"message": "An error occurred"}, status=HTTP_403_FORBIDDEN)

    def patch(self, request):
        try:
            # Check if the authenticated user has the required account type.
            check_account_type(request.user, account_type)
            user_school = get_user_school(request.user)

            data = request.data
            serialized_data = StaffWriteSerializer(data)

            if serialized_data.is_valid():
                serialized_data.save(school=user_school)

                # todo: add notification
                # todo: process a notification if salary deduction

                return Response({"message": "Staff edited successfully"}, status=HTTP_200_OK)
            return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)

        except PermissionDenied:
            # If the user doesn't have the required permissions, return an HTTP 403 Forbidden response.
            return Response({"message": "Permission denied"}, status=HTTP_403_FORBIDDEN)

        except APIException as e:
            # Handle specific API-related errors and return their details.
            return Response({"message": str(e.detail)}, status=e.status_code)

        except Exception as e:
            # For all other exceptions, return a generic error message.
            return Response({"message": "An error occurred"}, status=HTTP_403_FORBIDDEN)


@api_view(['GET'])
def ShowStaffType(request):
    '''
        this API is responsible for getting the staff type
    '''
    try:
        check_account_type(request.user, account_type)
        user_school = get_user_school(request.user)

        staff_type = Staff_type.objects.filter(school=user_school)

        serialized_data = StaffTypeSerializer(staff_type).data

        return Response(serialized_data, status=HTTP_200_OK)

    except PermissionDenied:
        # If the user doesn't have the required permissions, return an HTTP 403 Forbidden response.
        return Response({"message": "Permission denied"}, status=HTTP_403_FORBIDDEN)

    except APIException as e:
        # Handle specific API-related errors and return their details.
        return Response({"message": str(e.detail)}, status=e.status_code)

    except Exception as e:
        # For all other exceptions, return a generic error message.
        return Response({"message": "An error occurred"}, status=HTTP_403_FORBIDDEN)


class InitiatePayroll (APIView):
    '''
        -The Api is responsible for initiating payroll instance
        -Also the would be a patch request to modify the staffs too
    '''

    def post(self, request, *args, **kwargs):
        try:
            pass 

        except PermissionDenied:
            # If the user doesn't have the required permissions, return an HTTP 403 Forbidden response.
            return Response({"message": "Permission denied"}, status=HTTP_403_FORBIDDEN)

        except APIException as e:
            # Handle specific API-related errors and return their details.
            return Response({"message": str(e.detail)}, status=e.status_code)

        except Exception as e:
            # For all other exceptions, return a generic error message.
            return Response({"message": "An error occurred"}, status=HTTP_403_FORBIDDEN)


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


# framework
'''class TestClass (APIView):
    # this api is responsible for getting all the staff (active)
    def get(self):
        try:
            check_account_type(self.request.user, account_type)
            user_school = get_user_school(self.request.user)
        except PermissionDenied:
            return Response({"message": "Permission denied"}, status=HTTP_401_UNAUTHORIZED)'''
