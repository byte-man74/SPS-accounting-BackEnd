from unicodedata import category
from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import status, viewsets
from rest_framework.views import APIView
# from Background_Tasks.tasks import
from django.core.cache import cache
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from Api.helper_functions.payment_section.main import get_student_id_from_request
from Main.models import Payroll, Operations_account_transaction_record
from Api.helper_functions.main import *
from Api.helper_functions.auth_methods import *
from Api.helper_functions.directors.main import *
from Api.Api_pages.operations.serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException
account_type = "SCHOOL_ACCOUNTANT"

class GetFinancialInfoForAClass(APIView):
    '''This function returns information about the payment summary for the given class'''
    permission_classes = [IsAuthenticated]

    def get(self, request, grade_id, term):
        try:
            # Make sure to replace 'account_type' with the actual account type you are checking
            check_account_type(request.user, 'account_type')

            user_school = get_user_school(request.user)

            # Retrieve fees category for the given grade
            fees_category = FeesCategory.objects.get(school=user_school, grade=grade_id)

            # Retrieve financial information related to school fees
            school_fees_category = SchoolFeesCategory.objects.filter(term=term, category=fees_category)

            # Retrieve financial information related to bus fees
            bus_fee_category = BusFeeCategory.objects.filter(category=fees_category).first()

            # Retrieve financial information related to uniform and books fees
            uniform_and_books = UniformAndBooksFeeCategory.objects.filter(grades=grade_id, school=user_school)

            # Retrieve financial information related to other fees
            other_fees = OtherFeeCategory.objects.filter(grades=grade_id, school=user_school)

            # Serialize the data for the API response
            serialized_data = {
                "school_fees": SchoolFeesCategorySerializer(school_fees_category, many=True).data,
                "bus_fee": BusFeeCategorySerializer(bus_fee_category).data if bus_fee_category else None,
                "uniform_and_books": UniformAndBooksFeeCategorySerializer(uniform_and_books, many=True).data,
                "other_fees": OtherFeeCategorySerializer(other_fees, many=True).data,
            }

            return Response(serialized_data, status=HTTP_200_OK)

        except FeesCategory.DoesNotExist:
            return Response({"message": "Fees category not found for the given grade"}, status=HTTP_401_UNAUTHORIZED)
        except PermissionDenied:
            return Response({"message": "Permission denied"}, status=HTTP_401_UNAUTHORIZED)




class EditFinancialInformationForAClass (APIView):
    '''This function edits the financial information for the given class'''


class CreateClass (APIView):
    '''This function creates a new class'''

class EditClass (APIView):
    '''This function edits a class'''

class DeleteClass (APIView):
    '''This function deletes a class'''

