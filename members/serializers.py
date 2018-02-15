from django.core import validators
from rest_framework.fields import EmailField
from rest_framework.serializers import ModelSerializer

from members.models import Member


class MemberSerializer(ModelSerializer):

    class Meta:
        model = Member
        fields = ('pk', 'first_name', 'last_name', 'phone', 'profession',
                  'education', 'city', 'province', 'address', 'email', 'invited_with')
