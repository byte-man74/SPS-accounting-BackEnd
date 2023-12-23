from django.shortcuts import get_object_or_404
from Backend.Main.models.fees_structure_models import PaymentStatus
from Main.models.school_operations_models import Student
from django.db.models import Sum
from collections import Counter

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

def get_payment_summary(students):
    '''This function summarizes the payment status of students.'''
    
    # Use Counter to initialize counts for different payment statuses
    status_counts = Counter()

    for student in students:
        payment_status = PaymentStatus.objects.get(student=student.id)
        
        # Increment the corresponding count based on payment status
        status_counts[payment_status.status] += 1

    # Extract counts for each status
    student_paid = status_counts["COMPLETED"]
    student_in_debt = status_counts["IN DEBT"]
    student_outstanding = status_counts["OUTSTANDING"]

    return {
        'student_paid': student_paid,
        'student_in_debt': student_in_debt,
        'student_outstanding': student_outstanding,
    }
