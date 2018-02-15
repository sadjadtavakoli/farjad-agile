import re

from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from farjad.utils.utils_view import sms_sending
from members.models import Member, mobile_regex, generate_unique_login_code, PhoneCodeMapper


class PhoneValidator(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = self.request.data['phone_number']
        response = False
        data = {'existence': response}
        if Member.objects.filter(phone=phone_number).exists():
            member = Member.objects.get(phone=phone_number)
            response = True
            member_name = member.full_name
            token, created = Token.objects.get_or_create(user=member)
            data = {'existence': response, "name": member_name, 'token': token.key}
        return Response(data=data)


class AuthenticationCodeValidator(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = self.request.data['phone_number']
        authentication_code = self.request.data['authentication_code']
        if not re.match(mobile_regex.regex, phone_number):
            return Response(data={'is_valid': False, 'error': 'enter valid phone number'})

        if PhoneCodeMapper.objects.filter(phone=phone_number, code=authentication_code).exists():
            response = True
        else:
            return Response(data={'is_valid': False, 'error': 'wrong authentication'})

        return Response(data={'is_valid': response})


class AuthenticationCodeGenerateApiView(APIView):
    def post(self, request, *args, **kwargs):
        phone = self.request.data.get('phone', '')
        if not re.match(mobile_regex.regex, phone):
            return Response(data={'is_valid': False, 'error': 'enter valid phone number'})
        code = generate_unique_login_code()
        PhoneCodeMapper.objects.filter(phone=phone).delete()
        PhoneCodeMapper.objects.create(phone=phone, code=code)
        sms_sending(phone, code)
        return Response(data={'is_valid': True})
