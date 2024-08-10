from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from rest_framework.pagination import PageNumberPagination

from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model where the email address is the unique identifier
    and has an is_admin field to allow access to the admin app 
    """
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        if extra_fields.get('role') != 1:
            raise ValueError('Superuser must have role of Global Admin')
        return self.create_user(email, password, **extra_fields)
    

class TutorManager(models.Manager):
    
    def get_tutor_by_id(self,pk):
        return super().get_queryset().filter(role='2').get(pk=pk)
    def get_all_tutor(self,search):
        return super().get_queryset().filter(role='2').filter(first_name__icontains=search).all().order_by('-id')
    
    def get_approve_tutor(self,order_by='-id'):
        return super().get_queryset().filter(tutor_approve=True).filter(user_blocked=False).filter(role='2').all().order_by(order_by)
        # return super().get_queryset().filter(tutor_approve=True).filter(user_blocked=False).filter(role='2').all()

    def get_not_approve_tutor(self):
        return super().get_queryset().filter(tutor_approve=False).filter(user_blocked=False).filter(role='2').all().order_by('-id')
    
    def get_tutor_subject(self,search=None,order=None):
        
        return super().get_queryset().filter(tutor_approve=True).filter(role='2').filter(Q(subjects__icontains=search)|Q(first_name__icontains=search))

    def get_tutor_order_by(self,order):
        return super().get_queryset().filter(tutor_approve=True).filter(role='2').all().order_by() 

    # get all blocked tutor data 
    def get_all_blocked_tutor(self):
        return super().get_queryset().filter(user_blocked=True).filter(role='2').all().order_by('-id')
 
    
class UserManager(models.Manager):
    def get_all_user(self):
        return super().get_queryset().filter(role=3).filter(isDeleted=False).all().order_by('-id')
    
    def get_user_name(self,search=None,order=None):
        queryset = super().get_queryset().filter(role=3).filter(isDeleted=False).filter(
            Q(last_name__icontains=search) | Q(first_name__icontains=search) | Q(email__icontaine=search) | Q(address__icontained=search)
        ).all().order_by(order)
        return queryset

