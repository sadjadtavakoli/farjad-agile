from django import forms
from django.forms import Form
from django.utils.translation import gettext_lazy as _

from members.models import Member


class LoginForm(Form):
    username_or_phone = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_password(self):
        data = self.cleaned_data
        username_or_phone = data.get('username_or_phone', None)
        member = Member.objects.get_member(username_or_phone)
        if member is None:
            raise forms.ValidationError(_('Username or Password is incorrect'))
        password = data.get('password', None)
        if not member.check_password(password):
            raise forms.ValidationError(_('Username or Password is incorrect'))
        return password
