from django.apps import AppConfig
from django.db.models.signals import post_migrate

USERNAME = 'farjad'
PASSWORD = 'farjad'
PHONE = '09000000000'
AGE = 24


def create_admin(**kwargs):
    from members.models import Member
    try:
        Member.objects.get(username=USERNAME)
    except Member.DoesNotExist:
        member = Member.objects.create(
            username=USERNAME, email='farjad@gmail.com', password=PASSWORD, phone=PHONE, age=AGE)
        member.is_admin = True
        member.save()


class MembersConfig(AppConfig):
    name = 'members'

    def ready(self):
        post_migrate.connect(create_admin)
