from django.forms.models import ModelForm

from farjadAgile.members.models import Member


class LoginForm(ModelForm):
    class Meta:
        model = Member
        fields = ('username', 'password')

