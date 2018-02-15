import copy
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from members.models import Member


class InvitationCodeGenerate(APIView):

    def post(self, request, *args, **kwargs):
        phone_number = self.request.data['phone_number']
        response = None
        data = {'invitation_code': response}
        if Member.objects.filter(phone=phone_number).exists():
            member = Member.objects.get(phone=phone_number)
            response = member.get_invitation_code()
            data = {'invitation_code': response}
        return Response(data=data)
