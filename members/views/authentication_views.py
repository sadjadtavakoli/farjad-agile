import re

from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views.generic.base import View
from django.views.generic.edit import FormView, CreateView
from rest_framework.response import Response
from rest_framework.views import APIView

from members.forms.authentication_forms import AuthenticateForm
from members.models import Member, PhoneCodeMapper, mobile_regex, generate_unique_login_code


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("home"))


class JoinView(CreateView):
    template_name = "members/join.html"
    model = Member
    fields = ['first_name', 'last_name', 'phone', 'profession',
              'education', 'city', 'province', 'address', 'email', 'invited_with']

    def get_success_url(self):
        return reverse("home")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(JoinView, self).get_context_data(**kwargs)
        code_pk = self.kwargs.get('code_pk', '')
        phone = PhoneCodeMapper.objects.get(pk=code_pk).phone
        context['phone'] = phone
        return context

    def get_initial(self):
        code_pk = self.kwargs.get('code_pk', '')
        phone = PhoneCodeMapper.objects.get(pk=code_pk).phone
        initial = super(JoinView, self).get_initial()
        initial['phone'] = phone
        return initial

    def form_valid(self, form):
        ret = super().form_valid(form)
        data = form.cleaned_data
        member = Member.objects.get(phone=data['phone'])
        invited_code = data.get('invited_code', None)
        if invited_code is not None:
            inviter_member = Member.objects.get(invitation_code=invited_code)
            inviter_member.increase_balance(10000)
            member.increase_balance(5000)
        custom_login(self.request, member)
        return ret


class CheckInvitationCode(APIView):
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code', '').upper()
        is_valid = True
        if not Member.objects.filter(invitation_code=code).exists():
            is_valid = False
        return Response(data={'is_valid': is_valid})


class AuthenticationCodeCheckingApiView(APIView):
    def post(self, request, *args, **kwargs):
        phone = self.request.data.get('phone', '')
        if not re.match(mobile_regex.regex, phone):
            return Response(data={'is_valid': False, 'error': 'enter valid phone number'})
        code = generate_unique_login_code()
        PhoneCodeMapper.objects.filter(phone=phone).delete()
        PhoneCodeMapper.objects.create(phone=phone, code=code)
        # sms_sending(phone, code)
        print(code)
        return Response(data={'is_valid': True})


class NewAuthenticationView(FormView):
    template_name = 'members/new_authentication.html'
    form_class = AuthenticateForm

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        data = form.cleaned_data
        phone = data['phone']
        if Member.objects.filter(phone=phone).exists():
            member = Member.objects.get(phone=phone)
            custom_login(request=self.request, user=member)
            return super(NewAuthenticationView, self).form_valid(form)
        else:
            return redirect(reverse(
                'members:authentication:join',
                kwargs={'code_pk': PhoneCodeMapper.objects.get(phone=phone).pk}))


def custom_login(request, user):
    login(request=request, user=user)
    PhoneCodeMapper.objects.get(phone=user.phone).delete()
