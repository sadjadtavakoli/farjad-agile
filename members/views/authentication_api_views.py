from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import Member


class PhoneValidator(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = self.request.data['phone_number']
        response = False
        data = {'existence': response}
        print(phone_number)
        if Member.objects.filter(phone=phone_number).exists():
            print("inja")
            member = Member.objects.get(phone=phone_number)
            response = True
            member_name = member.full_name
            token, created = Token.objects.get_or_create(user=member)
            data = {'existence': response, "name": member_name, 'token': token.key}
        return Response(data=data)
