import random
import re
import string

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.fields.files import ImageField
from django.utils.translation import gettext_lazy as _

from farjad.settings import EDUCATION_CHOICES
from farjad.utils.utils_view import get_url
from loan.models import Loan, LoanState

mobile_regex = RegexValidator(
    regex=r'^(09|(\+989))\d{9}$',
    message=_('Mobile number should start with 09 and should have 11 digits.'))


def generate_code():
    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    while Member.objects.filter(invitation_code=code).exists():
        code = ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    return code


class MemberManager(BaseUserManager):
    def get_member(self, phone_email_username):
        try:
            if '@' in phone_email_username:
                kwargs = {'email': phone_email_username}
            elif re.match(mobile_regex.regex, phone_email_username):
                kwargs = {'phone': phone_email_username}
            else:
                kwargs = {'username': phone_email_username}
            member = super().get(**kwargs)
            return member

        except(TypeError, Member.MultipleObjectsReturned, Member.DoesNotExist):
            return None

    use_in_migrations = True

    def _create_user(self, phone, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not phone:
            raise ValueError('The given phone must be set')
        # email = self.normalize_email(email)
        user = self.model(phone=phone, **extra_fields)

        if password is not None:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_user(self, phone, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class Member(AbstractUser):
    username = None
    phone = models.CharField(max_length=11, blank=False, null=False, unique=True,
                             validators=[mobile_regex],
                             error_messages={
                                 'unique': _("A user with that phone already exists."),
                             })
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = ImageField(upload_to='profile_pictures/', null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    profession = models.CharField(max_length=32)
    education = models.CharField(max_length=30, choices=EDUCATION_CHOICES)
    city = models.CharField(max_length=60)
    province = models.CharField(max_length=60)
    address = models.CharField(max_length=60)
    balance = models.IntegerField(default=0)
    invitation_code = models.CharField(max_length=10, blank=True, null=True, unique=True)
    objects = MemberManager()
    invited_with = models.CharField(max_length=10, blank=True, null=True)
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    @property
    def image_url(self):
        if self.profile_picture is not None and self.profile_picture != "":
            return self.profile_picture
        else:
            return get_url(None, 'members/icons/default_profile.png')

    def increase_balance(self, amount):
        self.balance += amount
        self.save()

    @property
    def full_name(self):
        full_name = self.first_name + " " + self.last_name
        full_name = full_name.strip()
        if full_name == "":
            full_name = self.phone
        return full_name

    def get_invitation_code(self):
        if self.invitation_code is None:
            self.invitation_code = generate_code()
            self.save()

        return self.invitation_code

    @property
    def new_loan_requests(self):
        return Loan.objects.all().filter(book__owner=self, state__state=LoanState.STATE_NEW)
