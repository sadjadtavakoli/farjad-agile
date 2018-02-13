from django import forms
from django.forms import Form

from members.models import PhoneCodeMapper


class AuthenticateForm(Form):
    code = forms.CharField(max_length=5)
    phone = forms.CharField(max_length=11)

    def clean(self):
        data = self.cleaned_data
        phone = data.get('phone', '')
        code = data.get('code', '')
        if not PhoneCodeMapper.objects.filter(phone=phone, code=code).exists():
            self.add_error('code', 'Invalid Code')
        return data
