from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from Api.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
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



# Api to get amount available in cash in the operations account
# API to get amount available to transfer in the operations account
# API to get the tootal amount available in the operations account
# tested✅😊
class GetAmountAvailableOperationsAccount(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        user_school = get_user_school(request.user)
        operations_account = get_object_or_404(
            Operations_account, school=user_school)

        serializer = OperationsAccountSerializer(operations_account)

        return Response(serializer.data, status=HTTP_200_OK)


# API to get the total transcations that has happened in the past the past 7 days both transfer abd cash transactions in the operations account
# get the transaction list and filter it by active
# functionality to get the sum of money spent in the past 7 days both in cash and transfer
# tested✅😊
class GetTransactionSevenDaysAgo (APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_school = get_user_school(request.user)
        unarranged_transaction_list = get_unarranged_transaction_seven_days_ago(
            user_school)

        if unarranged_transaction_list is None:
            return Response(status=HTTP_404_NOT_FOUND, data={"message": "No transactions have been made for the past seven days."})

        processed_data = process_and_sort_transactions(
            unarranged_transaction_list)
        cash_total, transfer_total = calculate_cash_and_transfer_transaction_total(
            unarranged_transaction_list)

        cash_and_transaction_data = {
            "cash_total": cash_total,
            "transfer_total": transfer_total
        }

        transaction_serializer = SummaryTransactionSerializer(
            processed_data, many=True)
        cash_and_transfer_total_serializer = CashandTransactionTotalSerializer(
            cash_and_transaction_data)

        data = {
            "summary": cash_and_transfer_total_serializer.data,
            "transfer_list": transaction_serializer.data
        }

        return Response(data, status=HTTP_200_OK)


#  API to get all approved cash transactions in the operations acount
# API to get all pending cash transactions
# tested✅😊
class GetAllCashTransactions (APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_school = get_user_school(request.user)
        operations_account_cash_transaction = Operations_account_transaction_record.get_transaction(
            school=user_school, transaction_type="Cash")
        print(operations_account_cash_transaction)
        serializer = OperationsAccountCashTransactionRecordSerializer(
            operations_account_cash_transaction, many=True)

        return Response(serializer.data, status=HTTP_200_OK)


# API to edit a particular cash transaction
# API to create a cash transaction
# tested✅😊
class ViewAndModifyCashTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, id):
        try:
            return Operations_account_transaction_record.objects.get(id=id)
        except Operations_account_transaction_record.DoesNotExist:
            raise Http404

    # tested✅😊
    def get(self, request, id, format=None):
        transaction_record = self.get_object(id)
        serializer = CashTransactionReadSerializer(transaction_record)
        return Response(serializer.data, status=HTTP_200_OK)

    # tested✅😊
    def put(self, request, id, format=None):
        transaction_record = self.get_object(id)
        serializer = CashTransactionWriteSerializer(
            transaction_record, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save(is_approved=False)
            # initiate a notification here later to head teacher
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    # tested✅😊
class CreateCashTransaction (APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = CashTransactionWriteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(is_approved=False, school=get_user_school(
                request.user), transaction_type="Cash", transaction_category="Debit")
            # initiate a notification here later to the head teacher
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



#  API to get the summary of amount spent in the operatins account for a particular
# class GetPercentageSummary (APIView):

#     def get(self, request):
#         user_school = get_user_school(request.user)
#         operations_account_tansaction_list = Operations_account_transaction_record.get_transaction().filter(school=user_school)

#         summary = get_transaction_summary_by_header(operations_account_tansaction_list)
#         serializer = PercentageSummarySerializer(summary, many=True)
#         return Response(serializer.data, status=HTTP_200_OK)
