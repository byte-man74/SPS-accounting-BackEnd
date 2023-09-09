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



class ResetPasswordView(APIView):
    pass
#post request
# capture the email address from the request and process it   
# we wan search if the email address exists for the database
# if the email doesnt exist return 400
# if the email exist now then we go process the email      

