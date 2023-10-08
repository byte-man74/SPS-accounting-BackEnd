from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from Api.helper_functions.main import *
from Api.Api_pages.operations.serializers import *

account_type = "OPERATIONS"


class FetchHeader(APIView):
    permission_classes = [IsAuthenticated]
    def get (self, request):
        try:
            check_account_type(request.user, account_type)
            user_school = get_user_school(request.user)

            school_header = get_all_school_header(user_school)

            serializer = ParticularSerializer(
                school_header, many=True)
            
            return Response (serializer.data)
            
        except PermissionDenied:
            return Response({"message": "Permission denied"}, status=HTTP_401_UNAUTHORIZED)


