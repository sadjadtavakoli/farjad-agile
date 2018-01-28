from django.test import Client
from django.urls.base import reverse
from django_webtest import WebTest

from members.models import Member


class UserTest(WebTest):
    def setUp(self):
        self.client = Client()
        self.data = {
            'first_name': 'test_name',
            'last_name': 'test_family',
            'username': 'test_username',
            'password': '123456',
            'email': 'test@farjad.co',
            'phone': '09639874533',
            'city': 'tehran',
            'province': 'tehran',
            'address': 'khiaboon unja',
            'birth_date': '1995-10-10',
            'profession': 'kaseb',
            'education': 'under_diploma',
        }


class UserLoginTest(UserTest):
    def test_join_valid_data(self):
        response = self.client.get(reverse('members:join'))
        self.assertEqual(response.status_code, 200)

        self.assertFalse(Member.objects.filter(username=self.data['username']).exists())
        response = self.client.post(reverse("members:join"), self.data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Member.objects.filter(username=self.data['username']).exists())

    def test_join_invalid_data(self):
        data = self.data
        data['username'] = "farjad"
        member_count = Member.objects.count()

        response = self.client.post(reverse("members:join"), data)
        self.assertContains(response, "A user with that username already exists")
        self.assertEqual(member_count, Member.objects.count())

        data = {}
        response = self.client.post(reverse("members:join"), data)
        self.assertContains(response, "This field is required.", count=8)


class UserJoinTest(UserTest):
    def test_login_valid_data(self):
        self.assertNotIn('_auth_user_id', self.client.session)
        response = self.client.get(reverse('members:login'))
        self.assertEqual(response.status_code, 200)
        self.client.post(reverse("members:join"), self.data)

        response = self.client.post(reverse("members:login"),
                                    {'username_or_phone': self.data['username'],
                                     'password': self.data['password']})
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

        self.client.logout()
        self.assertNotIn('_auth_user_id', self.client.session)
        response = self.client.post(reverse("members:login"),
                                    {'username_or_phone': self.data['phone'],
                                     'password': self.data['password']})
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

        self.client.logout()
        self.assertNotIn('_auth_user_id', self.client.session)
        response = self.client.post(reverse("members:login"),
                                    {'username_or_phone': self.data['email'],
                                     'password': self.data['password']})
        self.assertEqual(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_invalid_data(self):
        self.client.post(reverse("members:join"), self.data)
        response = self.client.post(reverse("members:login"),
                                    {'username_or_phone': "chert ",
                                     'password': self.data['password']})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username or Password is incorrect")

        response = self.client.post(reverse("members:login"),
                                    {'username_or_phone': self.data['username'],
                                     'password': "chertTar"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Username or Password is incorrect")
