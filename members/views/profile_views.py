from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired
from members.models import Member
from members.views.area_setter import PanelAreaSetter


class ProfileView(DetailView):
    template_name = "members/profile.html"
    model = Member
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        member_id = self.kwargs.get('member_id', '')
        member = get_object_or_404(Member, id=member_id)
        self.request.profile = member
        return member

    def get_template_names(self):
        if self.request.user.is_authenticated and self.request.user == self.request.profile:
            self.template_name = "members/self_profile.html"
        return super(ProfileView, self).get_template_names()


class SelfProfileView(PanelAreaSetter, PermissionCheckerMixin, DetailView):
    permission_classes = [LoginRequired]
    template_name = "members/self_profile.html"
    model = Member
    context_object_name = 'profile'
    admin_area = "my_profile"

    def get_object(self, queryset=None):
        return self.request.user


class EditProfileView(PanelAreaSetter, PermissionCheckerMixin, UpdateView):
    model = Member
    fields = ['first_name', 'last_name', 'username', 'birth_date', 'phone',
              'age', 'profession',
              'education', 'city', 'province', 'address', 'email']

    permission_classes = [LoginRequired]
    template_name = "members/edit_profile.html"
    admin_area = "my_profile"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('members:self:profile')
