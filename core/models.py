from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    STUDENT = 'STUDENT', 'Student'
    TEACHER = 'TEACHER', 'Teacher'

class Status(models.TextChoices):
    STOPPED = 'STOPPED', 'Stopped'
    RUNNING = 'RUNNING', 'Running'
    TERMINATED = 'TERMINATED', 'Terminated'

class User(AbstractUser):
    inst_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    cnr = models.CharField(max_length=100)
    birth_date = models.DateField()
    role = models.CharField(max_length=10, choices=Role.choices)
    
    # Remove original fields from AbstractUser
    username = None
    first_name = None
    last_name = None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['inst_name', 'phone']

class Case(models.Model):
    case_of = models.CharField(max_length=100)
    students = models.ManyToManyField(User, related_name='student_cases')
    teachers = models.ManyToManyField(User, related_name='teacher_cases')

class Question(models.Model):
    type = models.CharField(max_length=100)
    instance_id = models.CharField(max_length=100)
    status = models.CharField(max_length=12, choices=Status.choices)
    assigned_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Subject(models.Model):
    name = models.CharField(max_length=100)

class Class(models.Model):
    name = models.CharField(max_length=100)

class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)