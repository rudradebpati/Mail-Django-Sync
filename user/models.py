from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserDetails(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    """
    is_email_verified = models.BooleanField(default=False)
    # is_phone_verified = models.BooleanField(default=False)
    # Add any additional fields you need for your user model here
    # For example, you can add a profile picture field, bio, etc.
    

    class Meta:
        db_table = 'user_details'
        verbose_name = 'User Details'
        verbose_name_plural = 'User Details'
    def __str__(self):
        return self.username
    # def __repr__(self):
    #     return self.username