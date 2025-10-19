from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings

# -----------------------------
# 1️⃣ Manager personnalisé
# -----------------------------
class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'adresse email doit être définie")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'ADMIN')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('role') != 'ADMIN':
            raise ValueError("Le superuser doit être un admin")
        return self.create_user(email, password, **extra_fields)

# -----------------------------
# 2️⃣ Modèle User personnalisé
# -----------------------------
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
    role = models.CharField(max_length=10, choices=Role.choices)

    username = None
    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['inst_name', 'phone']

    objects = CustomUserManager()  # <-- manager associé

    def __str__(self):
        return self.email

# -----------------------------
# 3️⃣ Autres modèles
# -----------------------------
class Case(models.Model):
    case_of = models.CharField(max_length=100)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='student_cases')
    teachers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='teacher_cases')

class Question(models.Model):
    question_type = models.CharField(max_length=100)
    instance_id = models.CharField(max_length=100)
    status = models.CharField(max_length=12, choices=Status.choices)
    assigned_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Subject(models.Model):
    name = models.CharField(max_length=100)

class SchoolClass(models.Model):
    name = models.CharField(max_length=100)

class Schedule(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    class_obj = models.ForeignKey(SchoolClass, on_delete=models.CASCADE)
