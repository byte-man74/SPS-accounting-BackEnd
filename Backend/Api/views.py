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


#post request
# capture the email address from the request and process it   
# we wan search if the email address exists for the database
# if the email doesnt exist return 400
# if the email exist now then we go process the email     
# 
class ResetPasswordView(APIView):
    def post(self, request, email):
        try:
            email = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            new_password = '123456'
            request.data.password = new_password
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


