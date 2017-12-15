from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.edit import FormView

from members.forms.authentication_forms import LoginForm
from members.models import Member


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        data = form.cleaned_data
        member = Member.objects.get(username=data['username'])
        user = authenticate(
            username=member.username, password=data['password'])
        login(self.request, user)
        return redirect("")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("")
