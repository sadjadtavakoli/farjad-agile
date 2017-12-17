from django.urls.conf import include, path

from members.views.authentication_views import LoginView, LogoutView
from members.views.profile_views import ProfileView, EditProfileView, SelfProfileView

app_name = "members"

self_urlpatterns = ([
                        path(r'edit_profile/', EditProfileView.as_view(), name="edit-profile"),
                    ], 'self')
urlpatterns = [
    path(r'login/', LoginView.as_view(), name="login"),
    path(r'logout/', LogoutView.as_view(), name="logout"),
    path(r'profile/<int:member_id>/', ProfileView.as_view(), name="profile"),
    path(r'profile/', SelfProfileView.as_view(), name="self-profile"),
    path(r'self/', include(self_urlpatterns)),
]
