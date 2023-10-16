from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from Api.Api_pages.operations.serializers import CashTransactionReadSerializer
from rest_framework import status, viewsets
from rest_framework.views import APIView
# from Background_Tasks.tasks import
from django.core.cache import cache
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from Main.models import Operations_account_transaction_record
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from Api.Api_pages.head_teacher.main import *
account_type = "PRINCIPAL"


class HeadTeacherGetAllPendingTransaction(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            check_account_type(request.user, account_type)
            user_school = get_user_school(request.user)
            pending_transaction_list = Operations_account_transaction_record.objects.filter(
                school=user_school, status="PENDING", transaction_type="CASH")

            if pending_transaction_list is None:
                return Response(status=HTTP_404_NOT_FOUND, data={"message": "No pending transaction."})

            serializer = CashTransactionReadSerializer(
                pending_transaction_list, many=True)
            return Response(serializer.data, status=HTTP_200_OK)

        except PermissionDenied:
            return Response({"message": "Permission denied"}, status=HTTP_401_UNAUTHORIZED)


class HeadTeacherModifyTransaction (APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        data = request.data
        if not data:
            return Response({"message": "Status must be set"}, status=HTTP_400_BAD_REQUEST)

        try:
            check_account_type(request.user, account_type)
            transaction_instance = get_object_or_404(
                Operations_account_transaction_record, id=id)

            transaction_instance.status = str(data['status'].upper())

            transaction_instance.save()
            return Response(status=HTTP_200_OK)

        except PermissionDenied:
            return Response({"message": "Permission denied"}, status=HTTP_401_UNAUTHORIZED)


class BulkModifyTransaction (APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, status):
        data = request.data.staffs
        if not data:
            return Response({"message": "Status must be set"}, status=HTTP_400_BAD_REQUEST)

        try:
            check_account_type(request.user, account_type)
            modified_status = str(status.upper())

            for data_instance in data:
                id = data_instance.get('id')
                transaction_instance = Operations_account_transaction_record.objects.get(
                    id=id)

                if transaction_instance is None:
                    continue

                transaction_instance.status = modified_status
                transaction_instance.save()
                return Response(status=HTTP_200_OK)

        except PermissionDenied:
            return Response({"message": "Permission denied"}, status=HTTP_401_UNAUTHORIZED)
