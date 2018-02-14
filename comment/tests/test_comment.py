from django.test.client import Client
from django_webtest import WebTest

from members.models import Member, PhoneCodeMapper, generate_unique_login_code


class AddCommentTest(WebTest):
    def setUp(self):
        self.client = Client()
        self.member = Member.objects.first()
        self.mapper = PhoneCodeMapper.objects.create(code=generate_unique_login_code(),
                                                     phone=self.member.phone)
