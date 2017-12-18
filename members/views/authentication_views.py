from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls.base import reverse
from django.views.generic.base import View
from django.views.generic.edit import FormView, CreateView

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


class JoinView(CreateView):
    template_name = "members/join.html"
    model = Member
    fields = ['first_name', 'last_name', 'username', 'birth_date', 'phone',
              'age', 'profession',
              'education', 'city', 'province', 'address', 'email']

    def get_success_url(self):
        return reverse("home")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get(request, *args, **kwargs)
