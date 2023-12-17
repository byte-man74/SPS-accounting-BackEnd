from django.utils import timezone
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework import status, viewsets
from rest_framework.views import APIView
# from Background_Tasks.tasks import
from django.core.cache import cache
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from Api.helper_functions.payment_section.main import get_student_id_from_request
from Main.models import Payroll, Operations_account_transaction_record
from Api.helper_functions.main import *
from Api.helper_functions.auth_methods import *
from Api.helper_functions.directors.main import *
from Api.Api_pages.operations.serializers import *
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException


class CreateClass(APIView):
    '''This function creates a new class'''

    def post(self, request):
        try:
            # Assuming your serializer is named ClassSerializer, replace it with your actual serializer
            serializer = CreateClassSerializer(data=request.data)

            if serializer.is_valid():
                # Set the school based on the user making the request
                user_school = get_user_school(request.user)
                serializer.validated_data['school'] = user_school

                # Create the new class instance
                new_class = serializer.save()

                return Response({"message": "Class created successfully", "class_id": new_class.id}, status=HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=HTTP_400_BAD_REQUEST)


class EditClass(APIView):
    '''This function edits and/or deletes a class'''
    permission_classes = [IsAuthenticated]

    def patch(self, request, class_id):
        try:
            # Assuming your serializer is named ClassSerializer, replace it with your actual serializer
            class_instance = Class.objects.get(id=class_id)
            serializer = CreateClassSerializer(instance=class_instance, data=request.data, partial=True)

            if serializer.is_valid():
                user_school = get_user_school(request.user)
                serializer.validated_data['school'] = user_school

                edited_class = serializer.save()

                return Response({"message": "Class edited successfully", "class_id": edited_class.id}, status=HTTP_200_OK)
            else:
                return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

        except Class.DoesNotExist:
            return Response({"message": "Class not found"}, status=HTTP_404_NOT_FOUND)
        except PermissionDenied:
            return Response({"message": "Permission denied"}, status=HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"message": f"An error occurred: {str(e)}"}, status=HTTP_400_BAD_REQUEST)



class GetPercentagePaid (APIView):
    '''This api returns the percentage and the total number of students that have paid fees complete''' 


class GetTotalAmountPaid (APIView):
    '''This api returns the total amount of money paid'''


class TotalAmountInDebt (APIView):
    '''This api returns the total amount of money estimated to be in debt'''


class GetPaymentSmmaryByClass (APIView):
    '''This api returns the payment summary statistics of students in the specified class'''


class GetGraphOfClassPayment (APIView):
    '''This api returns the payment graph of all the graph and how much is being paid'''

