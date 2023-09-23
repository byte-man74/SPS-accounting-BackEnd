from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND
from Api.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework.views import APIView
#from Background_Tasks.tasks import 
from django.core.cache import cache
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from Main.models import Operations_account, Operations_account_transaction_record, School
from Api.helper_functions.main import get_school_from_user
from Api.Api_pages.operations.serializers import OperationsAccountSerializer

# Api to get amount available in cash in the operations account
# API to get amount available to transfer in the operations account
#Untested⚠️
class GetAmountAvailableOperationsAccount(APIView):
    def get(self, request):
        user_school = get_object_or_404(School, id=get_school_from_user(request.user.id))
        operations_account = get_object_or_404(Operations_account, school=user_school)

        serializer = OperationsAccountSerializer(operations_account)

        return Response(serializer.data, status=HTTP_200_OK)










# API to get the tootal amount available in the operations account
# API to get the total transcations that has happened in the past the past 7 days both transfer abd cash transactions in the operations account
# functionality to get the sum of money spent in the past 7 days both in cash and transfer 
# API to calculate monthly income summary in the operations account / API to calculate monthly debit in the operations account
#  API to get the summary of amount spent in the operatins account for a particular
#  API to get all approved cash transactions in the operations acount 
# API to get all pending cash transactions
# API to edit a particular cash transaction   
# API to create a cash transaction 