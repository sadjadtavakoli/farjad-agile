from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic.edit import FormView

from farjadAgile.members.forms.authentication_forms import LoginForm
from farjadAgile.members.models import Member


class LoginView(FormView):
    template_name = 'templates/login.html'
    form_class = LoginForm

    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated():
    #         return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    #     return super().get(self, request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        member = Member.get_member(data['username'])
        user = authenticate(
            username=member.username, password=data['password'])

        login(self.request, user)
        return redirect(self.request.path)
