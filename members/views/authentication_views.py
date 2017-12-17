from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views.generic.base import View
from django.views.generic.edit import FormView

from members.forms.authentication_forms import LoginForm
from members.models import Member


class LoginView(FormView):
    template_name = 'members/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        data = form.cleaned_data
        member = Member.get_member(data['username_or_phone'])
        user = authenticate(
            username=member.username, password=data['password'])
        login(self.request, user)
        return redirect(reverse("home"))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("members:login"))
