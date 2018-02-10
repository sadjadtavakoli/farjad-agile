from django import forms
from django.forms import Form
from django.forms.models import ModelForm
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


class AuthenticateForm(ModelForm):
    class Meta:
        model = Member
        fields = ['phone', 'invitation_code']

    # class Meta:
    #     model = Member
    #     fields = ['phone']

    # def clean_phone(self):
    #     data = self.cleaned_data
    #     username_or_phone = data.get('username_or_phone', None)
    #     member = Member.objects.get_member(username_or_phone)
    #     if member is None:
    #         raise forms.ValidationError(_('Username or Password is incorrect'))
    #     password = data.get('password', None)
    #     if not member.check_password(password):
    #         raise forms.ValidationError(_('Username or Password is incorrect'))
    #     return password

    #
    # class JoinForm(ModelForm):
    #     class Meta:
    #         model = Member
    #         fields = ['first_name', 'last_name', 'password', 'username', 'phone', 'profession',
    #                   'education', 'city', 'province', 'address', 'email', 'invited_with']
    #
    #     def clean_invitation_code(self):
    #         data = self.cleaned_data
    #         invitation_code = data.get('invitation_code', None)
    #         try:
    #             Member.objects.get(code=invitation_code)
    #         except ObjectDoesNotExist:
    #             raise forms.ValidationError('این کد دعوت معتبر نمی‌باشد.')
    #         return invitation_code
