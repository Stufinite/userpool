from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    school_email = models.EmailField(default='')
    grade = models.IntegerField(default=1)
    major = models.CharField(max_length=100, default='')
    verified = models.BooleanField(default=False)

    def get_full_name(self):
        full_name = '%s %s' % (
            self.user.last_name.upper(), self.user.first_name)
        return full_name.strip()
