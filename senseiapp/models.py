from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    imageURL = models.CharField(max_length=255, blank=True)
    bio = models.TextField()
    whatsapp_number = models.CharField(max_length=20)
    location = models.CharField(max_length=255)




    REQUIRED_FIELDS = []
class Teacher(models.Model):
    student_list = models.ManyToManyField('Student', blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    qualifications = models.TextField()
    areas_of_expertise = ArrayField(models.CharField(max_length=100), blank=True, null=True)



class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    which_class = models.IntegerField()


class Review(models.Model):
    content = models.TextField()
    rating = models.IntegerField()
    student = models.OneToOneField('Student', on_delete=models.SET_NULL, null=True)
    teacher = models.OneToOneField('Teacher', on_delete=models.SET_NULL, null=True)



