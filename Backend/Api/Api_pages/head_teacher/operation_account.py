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
account_type = "PRINCIPAL"


class GetAllPendingTransaction (APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        try:
            check_account_type(request.user, account_type)
            # continue to get pending transactions
            pass
        except PermissionDenied:
            return Response({"message": "Permission denied"}, status=HTTP_401_UNAUTHORIZED)



class ModifyTransaction (APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, id):
        transaction_instance = get_object_or_404(Operations_account_transaction_record, id=id)

        data = request.data
        data.status
        data['status'] 

        transaction_instance.status = data['status']
        transaction_instance.save()
        


class BulkModifyTransaction (APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, status):
        data = request.data

        modified_status = str(status.to_upper())



        for data_instance in data:
            id = data_instance.get('id')

            transaction_instance = get_transaction(id)
            #function to check if transaction 404 to 200
            
            transaction_instance.status = modified_status
            tr



        re