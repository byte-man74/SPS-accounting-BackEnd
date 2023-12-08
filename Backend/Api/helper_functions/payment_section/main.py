

from django.shortcuts import get_object_or_404
from Main.models.school_operations_models import Student


def get_student_id_from_request (payload):
    student = get_object_or_404(Student, student_id=payload)
    return student
    