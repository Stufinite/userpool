from django.db import models
from django.contrib.auth.models import User

from login.choices import *


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    school_email = models.EmailField(default='', unique=True)

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
