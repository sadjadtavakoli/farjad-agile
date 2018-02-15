import json

from django.test import Client
from django.urls.base import reverse
from django_webtest import WebTest
from rest_framework.status import HTTP_200_OK, HTTP_302_FOUND

from members.models import generate_unique_login_code, PhoneCodeMapper, Member


class UserTest(WebTest):
    def setUp(self):
        self.phone = '09639874533'
        self.phone2 = '09999999999'
        self.mapper = PhoneCodeMapper.objects.create(code=generate_unique_login_code(),
                                                     phone=self.phone)
        self.mapper2 = PhoneCodeMapper.objects.create(code=generate_unique_login_code(),
                                                      phone=self.phone2)
        self.client = Client()
        self.data = {
            'first_name': 'test_name',
            'last_name': 'test_family',
            'email': 'test@farjad.co',
            'phone': self.phone,
            'city': 'tehran',
            'province': 'tehran',
            'address': 'khiaboon unja',
            'birth_date': '1995-10-10',
            'profession': 'kaseb',
            'education': 'under_diploma',
        }


class UserJoinTest(UserTest):
    def test_authentication_view(self):
        response = self.client.get(
            reverse('members:authentication:phone'))
        self.assertEqual(response.status_code, HTTP_200_OK)

        response = self.client.post(reverse('members:authentication:phone'),
                                    data={'phone': self.phone,
                                          'code': 'ZZZZZ' if self.mapper.code == '13245' else '12345'})
        self.assertContains(response, "Invalid Code")

        response = self.client.post(reverse('members:authentication:phone'),
                                    data={'phone': self.phone,
                                          'code': self.mapper.code})

        self.assertRedirects(response, reverse('members:authentication:join',
                                               kwargs={'code_pk': self.mapper.pk}),
                             HTTP_302_FOUND)

    def test_join_view(self):
        self.assertFalse(Member.objects.filter(phone=self.data['phone']).exists())
        response = self.client.get(reverse('members:authentication:join',
                                           kwargs={'code_pk': self.mapper.pk}))
        self.assertEqual(response.status_code, HTTP_200_OK)

        response = self.client.post(reverse('members:authentication:join',
                                            kwargs={'code_pk': self.mapper.pk}), data=self.data,
                                    follow=True)
        self.assertRedirects(response, reverse('members:self:books:all'))
        self.assertTrue(Member.objects.filter(phone=self.data['phone']).exists())

    def test_join_required_fields(self):
        data = {}
        response = self.client.post(
            reverse("members:authentication:join", kwargs={'code_pk': self.mapper.pk}), data)
        self.assertContains(response, "This field is required.", count=6)

    def test_invitation_code_gift(self):
        self.client2 = Client()
        self.client.post(reverse('members:authentication:join',
                                 kwargs={'code_pk': self.mapper.pk}), data=self.data)
        self.client.get(reverse('members:self:invitation'))
        member1 = Member.objects.get(phone=self.phone)
        self.assertEqual(member1.balance, 0)
        self.data.update(
            {'phone': self.phone2, 'email': self.data['email'] + 's',
             'invited_with': member1.invitation_code})
        self.client2.post(reverse('members:authentication:join',
                                  kwargs={'code_pk': self.mapper2.pk}), data=self.data)
        member1.refresh_from_db()
        member2 = Member.objects.get(phone=self.phone2)
        self.assertEqual(member1.balance, 10000)
        self.assertEqual(member2.balance, 5000)

    def test_invitation_code_checking(self):
        self.client2 = Client()
        self.client.post(reverse('members:authentication:join',
                                 kwargs={'code_pk': self.mapper.pk}), data=self.data)
        self.client.get(reverse('members:self:invitation'))
        member = Member.objects.get(phone=self.phone)
        response = self.client2.get(reverse('members:self:invitation-check'),
                                    {'code': 'chertopert'})
        self.assertEqual(json.loads(response.content.decode('UTF-8')), {'is_valid': False})
        response = self.client2.get(reverse('members:self:invitation-check'),
                                    {'code': member.invitation_code})
        self.assertEqual(json.loads(response.content.decode('UTF-8')), {'is_valid': True})


class UserLoginTest(UserTest):
    def test_login_valid_data(self):
        self.client.post(reverse('members:authentication:join',
                                 kwargs={'code_pk': self.mapper.pk}), data=self.data)
        self.client.logout()
        self.assertNotIn('_auth_user_id', self.client.session)
        response = self.client.get(
            reverse('members:authentication:phone'))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('members:authentication:phone'),
                                    data={'phone': self.phone,
                                          'code': self.mapper.code}, follow=True)
        self.assertEqual(response.status_code, HTTP_200_OK)


class UserProfile(UserTest):
    def get_profile(self):
        self.client.post(reverse('members:authentication:join',
                                 kwargs={'code_pk': self.mapper.pk}), data=self.data)

        response = self.client.get(reverse('members:self:profile'))
        self.assertEqual(response.status_code, HTTP_200_OK)
