import datetime

from django.test.client import Client
from django.urls.base import reverse
from django_webtest import WebTest

from books.models import Books
from members.models import Member, PhoneCodeMapper, generate_unique_login_code


class AddBookTest(WebTest):
    def setUp(self):
        self.client = Client()
        self.member = Member.objects.first()
        self.mapper = PhoneCodeMapper.objects.create(code=generate_unique_login_code(),
                                                     phone=self.member.phone)

        self.data = {
            'title': 'test_book',
            'author': 'authorauthor',
            'pub_date': datetime.date.today(),
            'price': 2500,
            'period': 'monthly',
            'genre': 'Psychology',
            'reader_age': 'C',
            'page_num': 20,
            'length': 320,
            'jeld_num': 320,
            'width': 12,
            'owner': Member.objects.first().id,
            'description': 'description',
            'summary': 'summary',
        }

    def test_add_book_valid_data(self):
        response = self.client.get(reverse('members:self:books:new'))
        self.assertEqual(response.status_code, 302)
        self.client.post(reverse('members:authentication:phone'),
                         data={'phone': self.member.phone,
                               'code': self.mapper.code}, follow=True)
        response = self.client.get(reverse('members:self:books:new'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Books.objects.count(), 0)
        response = self.client.post(reverse('members:self:books:new'), self.data, follow=True)
        self.assertRedirects(response, reverse("members:self:books:all"))
        self.assertEqual(Books.objects.count(), 1)
        book = Books.objects.last()
        self.assertEqual(book.loan_state(self.member), "")
        self.assertTrue(book.has_not_valid_state(self.member))

    def test_add_book_invalid_data(self):
        self.client.post(reverse('members:authentication:phone'),
                         data={'phone': self.member.phone,
                               'code': self.mapper.code}, follow=True)
        self.assertEqual(Books.objects.count(), 0)
        response = self.client.post(reverse('members:self:books:new'), {})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.', count=14)
        self.assertEqual(Books.objects.count(), 0)
