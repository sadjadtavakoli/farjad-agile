from django.conf.urls import url

from members.views import LoginView, LogoutView
app_name = "members"

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
]
