"""
Custom user model schema
"""
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
