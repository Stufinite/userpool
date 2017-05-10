from django.db import models
from django.contrib.auth.models import User

from login.choices import *


class OAuthUserProfile(models.Model):
    school = models.CharField(
        max_length=64, choices=SCHOOL_CHOICES, default='')
    career = models.CharField(
        max_length=8, choices=CAREER_CHOICES, default='')
    major = models.CharField(
        max_length=128, choices=MAJOR_CHOICES, default='')
    grade = models.IntegerField(default=1)


class FacebookUser(models.Model):
    user_id = models.CharField(max_length=128, unique=True)
    profile = models.OneToOneField(
        OAuthUserProfile, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{}'.format(self.user_id)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    school_email = models.EmailField(default='')

    school = models.CharField(
        max_length=100, choices=SCHOOL_CHOICES, default='NCHU')
    career = models.CharField(
        max_length=100, choices=CAREER_CHOICES, default='U')
    major = models.CharField(
        max_length=100, choices=MAJOR_CHOICES, default='U56')
    second_major = models.CharField(
        max_length=100, choices=SECOND_MAJOR_CHOICES, default='None')
    grade = models.IntegerField(default=1)

    verified = models.BooleanField(default=False)

    def get_full_name(self):
        full_name = '%s %s' % (
            self.user.last_name.upper(), self.user.first_name)
        return full_name.strip()
