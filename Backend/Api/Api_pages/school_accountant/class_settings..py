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


class GetFinanacialInfoForAClass (APIView):
    "This function returns information about the payment summary for the given class"

class EditFinancialInformationForAClass (APIView):
    '''This function edits the financial information for the given class'''


class CreateClass (APIView):
    '''This function creates a new class'''

class EditClass (APIView):
    '''This function edits a class'''

class DeleteClass (APIView):
    '''This function deletes a class'''

