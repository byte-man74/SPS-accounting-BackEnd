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



class OperationsAccountIncomeLastSevenMonths(APIView):
    # this API is responsible for getting and calculating all the income coming in the operations account through transfers
    # return the income for the past seven months 
    pass



class CurrentMonthTransferBudgetSummary(APIView):
    # this API is responsible for getting and calculating all the transfer amount spent in the current month
    # this api is also responsible for getting the total amount available to transfer
    pass



class GetAllTransferTransaction (APIView):
    # this API is responsible for getting all the transfer transactions that has been made
    pass


class InititeTransferTransaction (APIView):
    # this API is responsible for initializing the transfer transaction
    pass


class EditTransferTransaction(APIView):
    # this API is responsible for editing the transfer transaction
    pass


