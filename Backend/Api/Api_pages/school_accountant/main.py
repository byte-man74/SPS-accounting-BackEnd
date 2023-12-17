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



class GetPercentagePaid (APIView):
    '''This api returns the percentage and the total number of students that have paid fees complete''' 


class GetTotalAmountPaid (APIView):
    '''This api returns the total amount of money paid'''


class TotalAmountInDebt (APIView):
    '''This api returns the total amount of money estimated to be in debt'''


class GetPaymentSmmaryByClass (APIView):
    '''This api returns the payment summary statistics of students in the specified class'''


class GetGraphOfClassPayment (APIView):
    '''This api returns the payment graph of all the graph and how much is being paid'''

