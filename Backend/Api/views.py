from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from .serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
#from Background_Tasks.tasks import 
from django.core.cache import cache
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404


#? This api is responsible for Login in an returning a token when the user credentials are valid
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer


# class ResetPasswordView(APIView):

#     #inside here email as parameter
#     def post(self, request):
#         email = request.data['email']
#         CustomUser = get_user_model()

#         try:
#             email = CustomUser.objects.get(email=email)
#             email_status = process_email(email)
#             if email_status:
#                 return Response(status=status.HTTP_200_OK)
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         except CustomUser.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
