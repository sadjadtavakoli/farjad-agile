from django.contrib.auth.models import AbstractUser

from django.db import models


class Member(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
