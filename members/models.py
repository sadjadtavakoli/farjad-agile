import re

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import ImageField
from django.db.models.manager import Manager
from django.utils.translation import gettext_lazy as _

from farjad.settings import EDUCATION_CHOICES
from farjad.utils.utils_view import get_url
from loan.models import Loan, LoanState


class MemberManager(Manager):

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


class Member(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[ASCIIUsernameValidator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    profile_picture = ImageField(upload_to='profile_pictures/', null=True, blank=True)
    phone = models.CharField(max_length=11, blank=False, null=False, unique=True)
    age = models.IntegerField(null=True, blank=True)
    profession = models.CharField(max_length=32)
    education = models.CharField(max_length=30, choices=EDUCATION_CHOICES)
    city = models.CharField(max_length=60)
    province = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    objects = MemberManager()

    @property
    def image_url(self):
        if self.profile_picture is not None and self.profile_picture != "":
            return self.profile_picture
        else:
            return get_url(None, 'members/icons/default_profile.png')

    @property
    def full_name(self):
        full_name = self.first_name + " " + self.last_name
        full_name = full_name.strip()
        if full_name == "":
            full_name = self.username
        return full_name

    @property
    def new_loan_requests(self):
        return Loan.objects.all().filter(book__owner=self, state__state=LoanState.STATE_NEW)


mobile_regex = RegexValidator(regex=r'^(09|(\+989))\d{9}$',
                              message=_('Mobile number should have 11 digits.'))
