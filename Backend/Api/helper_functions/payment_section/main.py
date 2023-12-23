from django.shortcuts import get_object_or_404
from Backend.Main.models.fees_structure_models import PaymentStatus
from Main.models.school_operations_models import Student
from django.db.models import Sum

def get_student_id_from_request (payload):
    student = get_object_or_404(Student, student_id=payload)
    return student


def get_total_amount_in_debt(students):
    '''This function iterates through all the students and calculates the total amount of debt. It caches the result.'''
    
    total_amount_query = PaymentStatus.objects.filter(student__in=students).aggregate(
        total_amount=Sum('amount_in_debt') + Sum('amount_outstanding')
    )

    # Extract the total amount from the aggregation result
    total_amount = total_amount_query['total_amount'] or 0

    return total_amount


def get_payment_summary (students):
    student_in_debt = 0
    student_outstanding = 0
    student_paid = 0

    for student in students:
        payment_status = PaymentStatus.objects.get(student=student.id)
        
        
        if payment_status.status == "COMPLETED":
            student_paid = student_paid + 1
        elif payment_status.status == "IN DEBT":
            student_in_debt = student_in_debt + 1
        else: 
            student_outstanding = student_outstanding + 1

