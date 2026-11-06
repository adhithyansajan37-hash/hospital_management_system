from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class dept(models.Model):
    dept_name=models.CharField(max_length=100)
    dept_description=models.TextField()
    def __str__(self):
        return self.dept_name
class doctors(models.Model):
    doctor_name=models.CharField(max_length=100)
    doctor_specialization=models.CharField(max_length=100)
    dept_name=models.ForeignKey(dept,on_delete=models.CASCADE)
    doctor_image=models.ImageField(upload_to='doctor_images/',null=True,blank=True)
    def __str__(self):
        return self.doctor_name
class booking(models.Model):
    patient_name=models.CharField(max_length=100)
    patient_phone=models.CharField(max_length=20)
    patient_email=models.EmailField()
    doctor_name=models.ForeignKey(doctors,on_delete=models.CASCADE)
    booked_on=models.DateField()
    def __str__(self):
        return f"{self.patient_name}  {self.doctor_name} "
class contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=20, blank=True)
    address=models.CharField(max_length=100, blank=True)
    subject=models.CharField(max_length=150)
    message=models.TextField()
    def __str__(self):
        return self.name

class UserProfile(models.Model):

    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='patient'
    )

    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    blood_group = models.CharField(max_length=5, blank=True)
    emergency_contact = models.CharField(max_length=15, blank=True)

    profile_image = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.user.username


