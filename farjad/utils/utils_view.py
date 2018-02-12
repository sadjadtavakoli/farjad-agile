import random
import string

from django.conf import settings

from members.models import Member, PhoneCodeMapper


def get_url(image, location):
    if image and hasattr(image, 'url'):
        return image.url
    else:
        return '{}{}'.format(settings.STATIC_URL, location)


def auto_save(func):
    def autosave(self, *args, **kwargs):
        res = func(self, *args, **kwargs)
        self.save()
        return res

    return autosave


def generate_invitation_unique_code():
    code = get_random(10)
    while Member.objects.filter(invitation_code=code).exists():
        code = get_random(10)
    return code


def get_random(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))


def generate_unique_login_code():
    code = get_random(5)
    while PhoneCodeMapper.objects.filter(code=code).exists():
        code = get_random(5)
    return code
