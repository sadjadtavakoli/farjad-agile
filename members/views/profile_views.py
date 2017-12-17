from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView

from members.models import Member


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
