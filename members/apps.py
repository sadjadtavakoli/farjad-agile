from django.apps import AppConfig
from django.db.models.signals import post_migrate

USERNAME = 'farjad'
PASSWORD = 'farjad'


def create_admin(**kwargs):
    from members.models import Member
    try:
        Member.objects.get(username=USERNAME)
    except Member.DoesNotExist:
        Member.objects.create_superuser(
            USERNAME, 'farjad@gmail.com', PASSWORD)


class MembersConfig(AppConfig):
    name = 'members'

    def ready(self):
        post_migrate.connect(create_admin)
