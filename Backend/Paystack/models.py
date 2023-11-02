from django.db import models

# Create your models here.
class Bank (models.Model):
    name = models.CharField(max_length=50)
    bank_code = models.CharField(max_length=10)
    slug = models.CharField(max_length=50)
    bank_type = models.CharField(max_length=40)
    currency = models.CharField(max_length=10)


    def __str__(self):
        return self.name
    