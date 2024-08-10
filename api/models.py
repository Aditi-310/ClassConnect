from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
# from rating.models import Feedback

from .managers import CustomUserManager,TutorManager,UserManager

# Create your models here.
# class abc(models.Model):
#     name
# role based user

class City(models.Model):
    city_name = models.CharField(unique=True, max_length=20)
    city_state = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.city_name
    

class Subject(models.Model):
    subject_name = models.CharField(unique=True, max_length=20)
    isDisabled = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return self.subject_name

class User(AbstractUser):
 
    # These fields tie to the roles!
    ADMIN = 1
    TUTOR = 2
    USER = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (TUTOR, 'Tutor'),
        (USER, 'User')
    )

    username = None

    email = models.EmailField(max_length=100,unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
    profile_image = models.ImageField(upload_to="my_pictures", blank=True) 
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    tutor_approve = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True)
    dob=models.CharField(max_length=10,blank=True)
    contact=models.CharField(max_length=10,blank=True)
    experience = models.CharField(max_length=10,blank=True)
    gender = models.CharField(max_length=10,blank=True)
    short_bio = models.CharField(max_length=200,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, blank=True)
    subjects = models.ForeignKey(Subject, blank=True, on_delete=models.PROTECT, null=True)
    user_blocked = models.BooleanField(default=False)
    isDeleted = models.BooleanField(default=False)

    objects = CustomUserManager()
    tutorObject = TutorManager()
    userObject=UserManager()

    def __str__(self):
        return self.email
        
    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def get_subject_name(self):
        return self.subjects.subject_name
    
    @property
    def get_city_name(self):
        return self.city.city_name
    