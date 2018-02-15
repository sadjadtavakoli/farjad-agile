import copy
from tokenize import Token
import re

from django.core import validators
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from members.models import Member, mobile_regex
from members.serializers import MemberSerializer

class MemberListAPIView(ListAPIView):
    model = Member
    serializer_class = MemberSerializer
    queryset = Member.objects.all()


class CreateMemberAPIView(CreateAPIView):
    serializer_class = MemberSerializer

    def create(self, request, *args, **kwargs):
        response = False
        data = copy.deepcopy(self.request.data)
        if Member.objects.filter(phone=data["phone"]).exists():
            return Response(data={'is_create': response, 'error': "user with this phone already exists."})
        if not re.match(mobile_regex.regex, data["phone"]):
            return Response(data={'is_create': response, 'error': "wrong phone"})

        if data.get('invited_with', "") != "":
            if not Member.objects.filter(invitation_code=data['invited_with']).exists():
                return Response(data={'is_create': response, 'error': "wrong invitation code"})

        member = Member.objects.create(first_name=data['first_name'],
                                       last_name=data['last_name'],
                                       phone=data['phone'],
                                       profession=data['profession'],
                                       education=data['education'],
                                       city=data['city'],
                                       province=data['province'],
                                       address=data['address'],
                                       email=data['email'],
                                       invited_with=data['invited_with'])
        invited_code = data.get("invited_with", "")
        if invited_code != "":
            inviter_member = Member.objects.get(invitation_code=invited_code)
            inviter_member.increase_balance(10000)
            member.increase_balance(5000)

        response = True
        return Response(data={'is_create': response})
