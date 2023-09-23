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
from Api.helper_functions.main import get_school_from_user, get_unarranged_transaction_seven_days_ago, process_and_sort_transactions, calculate_cash_and_transfer_transaction_total
from Api.Api_pages.operations.serializers import OperationsAccountSerializer, TransactionSerializer, CashandTransactionTotalSerializer



# Api to get amount available in cash in the operations account
# API to get amount available to transfer in the operations account
# API to get the tootal amount available in the operations account
#tested✅😊
class GetAmountAvailableOperationsAccount(APIView):
    def get(self, request):
        user_school = get_object_or_404(School, id=get_school_from_user(request.user.id))
        operations_account = get_object_or_404(Operations_account, school=user_school)

        serializer = OperationsAccountSerializer(operations_account)

        return Response(serializer.data, status=HTTP_200_OK)




# API to get the total transcations that has happened in the past the past 7 days both transfer abd cash transactions in the operations account
#get the transaction list and filter it by active
# functionality to get the sum of money spent in the past 7 days both in cash and transfer 
#tested✅😊
class GetTransactionSevenDaysAgo (APIView):
    
    def get(self, request):
        user_school = get_object_or_404(School, id=get_school_from_user(request.user.id))
        unarranged_transaction_list = get_unarranged_transaction_seven_days_ago(user_school)

        if unarranged_transaction_list is None:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": "No transactions have been made for the past seven days."})

        processed_data = process_and_sort_transactions(unarranged_transaction_list) 
        cash_total, transfer_total = calculate_cash_and_transfer_transaction_total(unarranged_transaction_list)

        cash_and_transaction_data = {
            "cash_total": cash_total,
            "transfer_total": transfer_total
        }

        transaction_serializer = TransactionSerializer(processed_data, many=True)
        cash_and_transfer_total_serializer = CashandTransactionTotalSerializer(cash_and_transaction_data)

        data = {
            "summary" : cash_and_transfer_total_serializer.data,
            "transfer_list" : transaction_serializer.data
        }

        return Response(data, status=HTTP_200_OK)







#  API to get the summary of amount spent in the operatins account for a particular
#  API to get all approved cash transactions in the operations acount 
# API to get all pending cash transactions
# API to edit a particular cash transaction   
# API to create a cash transaction 