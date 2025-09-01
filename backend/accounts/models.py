from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

import string
from datetime import timedelta
from django.utils import timezone
import secrets
# Create your models here.


class UserManager(BaseUserManager):


        # helper to dave the user validate m normalize and create 
    def _create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Please set the email")
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields)


        user.set_password(password)

        user.save(using=self._db)
        return user

    # for ordinary user
    def create_user(self,email,password=None , **extra_fields):
        extra_fields.setdefault('is_staff',False)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_active',False) 
        return self._create_user(email,password,**extra_fields)

    # for super user 
    def create_superuser(self,email,password=None , **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True) 

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email,password,**extra_fields)

class User(AbstractUser):
    """extends the abstract user class"""

    username = None
    email = models.EmailField(_('email address') , unique=True)
    is_email_verified = models.BooleanField(default=False)



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] #email and password required by default 

    objects = UserManager()
    def _str_(self):
        return self.email

    # dynamically checks if user is seller or not 
    @property
    def is_seller(self):
        return hasattr(self,'seller')

class Seller(models.Model):


    SELLER_TYPES = [
        ('individual', 'Individual'),
        ('wholesaler', 'Wholesaler'),
        ('enterprise', 'Enterprise'),
    ]


    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seller',
        primary_key=True
    )
    shop_name = models.CharField(max_length=200)
    gst_number = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    seller_type = models.CharField(max_length=20, choices=SELLER_TYPES, default='individual')
    is_verified = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        indexes= [
            models.Index(fields=['shop_name']),
            models.Index(fields=['gst_number'])

        ]
    def _str_(self):
        return self.shop_name


