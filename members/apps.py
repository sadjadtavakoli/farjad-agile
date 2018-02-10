from django.apps import AppConfig
from django.db.models.signals import post_migrate

USERNAME = 'farjad'
PASSWORD = 'farjad'
PHONE = '09000000000'
AGE = 24


def create_admin(**kwargs):
    from members.models import Member
    try:
        Member.objects.get(phone=PHONE)
    except Member.DoesNotExist:
        Member.objects.create_superuser(
            password=PASSWORD,
            phone=PHONE)


class MembersConfig(AppConfig):
    name = 'members'

    def ready(self):
        post_migrate.connect(create_admin)
