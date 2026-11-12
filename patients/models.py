from django.db import models

# Create your models here. 
# For any databases needed to be designed or setup for a django project; use the models.py
class Patient(models.Model):
    patient_id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    
    def __str__(self):
        return self.name