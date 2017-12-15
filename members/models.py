from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models import ImageField
from django.utils.translation import gettext_lazy as _


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
