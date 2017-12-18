import re

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import ImageField
from django.utils.translation import gettext_lazy as _

from farjad.settings import EDUCATION_CHOICES


class Member(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[UnicodeUsernameValidator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    profile_picture = ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone = models.CharField(max_length=11, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    profession = models.CharField(max_length=32)
    education = models.CharField(max_length=1, choices=EDUCATION_CHOICES)
    city = models.CharField(max_length=60)
    province = models.CharField(max_length=60)
    address = models.CharField(max_length=60)

    @staticmethod
    def get_member(phone_email_username):
        try:
            if '@' in phone_email_username:
                kwargs = {'email': phone_email_username}
            elif re.match(mobile_regex.regex, phone_email_username):
                kwargs = {'phone': phone_email_username}
            else:
                kwargs = {'username': phone_email_username}
            member = Member.objects.get(**kwargs)
            return member

        except(TypeError, Member.MultipleObjectsReturned, Member.DoesNotExist):
            return None


mobile_regex = RegexValidator(regex=r'^(09|(\+989))\d{9}$',
                              message=_('Mobile number should have 11 digits.'))
