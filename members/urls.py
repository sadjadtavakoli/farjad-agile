from django.conf.urls import url

from members.views.authentication_views import LoginView, LogoutView
from members.views.profile_views import ProfileView

app_name = "members"

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
    url(r'^profile/(?P<member_id>\d+)/$', ProfileView.as_view(), name="profile"),
]
