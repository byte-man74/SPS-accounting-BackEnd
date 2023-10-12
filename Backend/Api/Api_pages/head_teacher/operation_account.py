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
from Api.Api_pages.head_teacher.serializers import *
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from Api.Api_pages.head_teacher.main import *
account_type = "PRINCIPAL"


class GetAllPendingTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            check_account_type(request.user, account_type)
            user_school = get_user_school(request.user)
            pending_transaction_list = get_all_pending_transaction(
                user_school)

            if pending_transaction_list is None:
                return Response(status=HTTP_404_NOT_FOUND, data={"message": "No pending transaction."})

            else:

                processed_data = process_and_sort_transactions_by_months(
                pending_transaction_list)
                transaction_serializer = MonthlyTransactionSerializer(
                processed_data, many=True)

                return Response(pending_transaction_list, status=HTTP_200_OK)

        except PermissionDenied:
            return Response({"message": "Permission denied"}, status=HTTP_401_UNAUTHORIZED)


    

class ModifyTransaction (APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, id):
        transaction_instance = get_object_or_404(Operations_account_transaction_record, id=id)

        data = request.data.get(id=id)
        transaction_instance.status = data['status']
        transaction_instance.save()

        
class BulkModifyTransaction (APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, status):
        data = request.data
        modified_status = str(status.upper())

        for data_instance in data:
            id = data_instance.get('id')

            transaction_instance = get_transaction(id)
            if transaction_instance is None:
                return Response(status=HTTP_404_NOT_FOUND, data={"message": "No transaction available."})

            else:
                transaction_instance.status = modified_status
                return Response(status=HTTP_200_OK)