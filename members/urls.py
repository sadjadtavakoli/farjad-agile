from django.urls.conf import include, path

from members.views.authentication_views import LoginView, LogoutView, JoinView
from members.views.profile_views import ProfileView, EditProfileView, SelfProfileView
from members.views.user_books_views import UserBooksListView

app_name = "members"

self_urlpatterns = ([
                        path(r'edit_profile/', EditProfileView.as_view(), name="edit-profile"),
                        path(r'books/', UserBooksListView.as_view(), name="books"),
                    ], 'self')
urlpatterns = [
    path(r'login/', LoginView.as_view(), name="login"),
    path(r'join/', JoinView.as_view(), name="join"),
    path(r'logout/', LogoutView.as_view(), name="logout"),
    path(r'profile/<int:member_id>/', ProfileView.as_view(), name="profile"),
    path(r'profile/', SelfProfileView.as_view(), name="self"),
    path(r'self/', include(self_urlpatterns)),
]
