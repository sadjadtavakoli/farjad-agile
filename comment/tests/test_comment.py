import datetime

from django.test.client import Client
from django.urls.base import reverse
from django_webtest import WebTest

from books.models import Books
from members.apps import USERNAME, PASSWORD
from members.models import Member


class AddCommentTest(WebTest):
    def setUp(self):
        self.client = Client()
        self.data = {
            'date': datetime.date.today(),
            'likes': 20,
            'text': 'خلاصه نظر',
            "writer":Member.objects.first().id,
            "book":Books.objects.first()

        }
