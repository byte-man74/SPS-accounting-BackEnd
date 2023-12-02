from django.db import models
from Main.configuration import *


  
"""
Django models for handling various fee categories in a school management system.

1. FeesCategory:
   Represents a general fee category associated with a school grade.
   Fields:
   - school: One-to-One relationship with the School model.
   - grade: ForeignKey relationship with the Class model.
   - name: CharField for the name of the category.
   - category_type: CharField with choices from category_types.

2. SchoolFeesCategory:
   Represents a specific fee category associated with a school, grade, and term.
   Fields:
   - name: CharField for the name of the category.
   - category: ForeignKey relationship with the FeesCategory model.
   - term: CharField with choices from school_terms.
   - minimum_percentage: BigIntegerField for the minimum percentage.
   - amount: BigIntegerField for the amount.
   - is_compoulslry: BooleanField indicating whether the fee is compulsory.

3. BusFeeCategory:
   Represents a fee category specifically for bus fees associated with a school, grade, and term.
   Fields:
   - name: CharField for the name of the category.
   - category: ForeignKey relationship with the FeesCategory model.
   - morning_bus_fee: BigIntegerField for the morning bus fee.
   - evening_bus_fee: BigIntegerField for the evening bus fee.

4. UniformAndBooksFeeCategory:
   Represents a fee category for uniform and books associated with a school, grade, and category.
   Fields:
   - name: CharField for the name of the category.
   - image: ImageField for an image associated with the category.
   - category: ForeignKey relationship with the FeesCategory model.
   - grades: Many-to-Many relationship with the Class model.
   - school: ForeignKey relationship with the School model.
   - is_recommended: BooleanField indicating whether it is recommended.
   - amount: BigIntegerField for the amount.

5. OtherFeeCategory:
   Represents other fee categories associated with a school, grade, and category.
   Fields:
   - name: CharField for the name of the category.
   - image: ImageField for an image associated with the category.
   - category: ForeignKey relationship with the FeesCategory model.
   - grades: Many-to-Many relationship with the Class model.
   - school: ForeignKey relationship with the School model.
   - is_recommended: BooleanField indicating whether it is recommended.
   - amount: BigIntegerField for the amount.
"""

class FeesCategory (models.Model):

    school = models.OneToOneField("Main.School", on_delete=models.CASCADE)
    grade = models.ForeignKey("Main.Class", on_delete=models.CASCADE)
    name =  models.CharField(max_length=50)
    category_type = models.CharField(max_length=60, choices=category_types)

    def __str__(self):
        return self.name
    



class SchoolFeesCategory (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey("Main.FeesCategory", on_delete=models.CASCADE)
    term = models.CharField(max_length=50, choices=school_terms)


    '''financials'''
    minimum_percentage = models.BigIntegerField(default=0)
    amount = models.BigIntegerField(default=0)
    is_compoulslry = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} school fee category for {self.category} in {self.category.grade} for {self.term}'



class BusFeeCategory (models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey("Main.FeesCategory", on_delete=models.CASCADE)

    '''financials'''
    morning_bus_fee = models.BigIntegerField(default=0)
    evening_bus_fee = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.name} bus fee category for {self.category} in {self.category.grade} for {self.term}'



class UniformAndBooksFeeCategory (models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField()
    category = models.ForeignKey("Main.FeesCategory", on_delete=models.CASCADE) 
    grades = models.ManyToManyField("Main.Class")
    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)
    is_recommended = models.BooleanField(default=False)

    '''financials'''
    amount = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.name} uniform  fee category for {self.school}'
    


class OtherFeeCategory (models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField()
    category = models.ForeignKey("Main.FeesCategory", on_delete=models.CASCADE) 
    grades = models.ManyToManyField("Main.Class")
    school = models.ForeignKey("Main.School", on_delete=models.CASCADE)
    is_compoulslry = models.BooleanField(default=False)

    '''financials'''
    amount = models.BigIntegerField(default=0)

    def __str__(self):
        return f'{self.name} bus fee category for {self.school}'