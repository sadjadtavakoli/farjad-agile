import datetime

from django.test.client import Client
from django.urls.base import reverse
from django_webtest import WebTest
from rest_framework.status import HTTP_200_OK

from books.models import Books
from members.apps import PASSWORD
from members.models import Member


class CreateLoanTest(WebTest):
    def setUp(self):
        self.client = Client()
        self.member = Member.objects.create(
            username='sadjad', email='farjad@gmail.com', balance=0, password=PASSWORD, phone='09876543234', age=21)

    def add_books(self, nums):
        self.client.login(username='sadjad', password=PASSWORD)
        for i in range(nums):
            data = {
                'title': 'test_book' + str(i),
                'author': 'authorauthor',
                'pub_date': datetime.date.today(),
                'price': 2500 * i,
                'period': 'monthly',
                'genre': 'Psychology',
                'reader_age': 'C',
                'page_num': 20,
                'length': 320,
                'jeld_num': 320,
                'width': 12,
                'owner': Member.objects.get(username='sadjad').id,
                'description': 'description',
                'summary': 'summary',
            }
            self.client.post(reverse('members:self:books:new'), data, follow=True)

    def test_create_loan(self):
        self.add_books(1)
        self.client.login(username='sadjad', password=PASSWORD)
        book = Books.objects.first()
        response = self.client.post(reverse('api:create-loan'), data={'book': book.id})
        self.assertEqual(response.status_code, HTTP_200_OK)
