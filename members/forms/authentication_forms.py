from django import forms
from django.forms import Form
from django.utils.translation import gettext_lazy as _

from members.models import Member


class LoginForm(Form):
    username = forms.CharField()
    password = forms.CharField()

    def clean_password(self):
        data = self.cleaned_data
        username = data.get('username', None)
        member = Member.objects.get(username=username)
        if member is None:
            raise forms.ValidationError(_('Username or Password is incorrect'))
        password = data.get('password', None)
        if not member.check_password(password):
            raise forms.ValidationError(_('Username or Password is incorrect'))
        return password
