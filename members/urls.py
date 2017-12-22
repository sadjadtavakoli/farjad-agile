from django.urls.conf import include, path

from books.views import AddBookView
from members.views.authentication_views import LoginView, LogoutView, JoinView
from members.views.profile_views import ProfileView, EditProfileView, SelfProfileView
from members.views.user_books_views import UserBooksListView

app_name = "members"
user_books_urlpatterns = ([
                              path(r'', UserBooksListView.as_view(), name="all"),
                              path(r'new/', AddBookView.as_view(), name="new"),

                          ], 'books')
self_urlpatterns = ([
                        path(r'edit_profile/', EditProfileView.as_view(), name="edit-profile"),
                        path(r'books/', include(user_books_urlpatterns)),
                    ], 'self')
urlpatterns = [
    path(r'login/', LoginView.as_view(), name="login"),
    path(r'join/', JoinView.as_view(), name="join"),
    path(r'logout/', LogoutView.as_view(), name="logout"),
    path(r'profile/<int:member_id>/', ProfileView.as_view(), name="profile"),
    path(r'profile/', SelfProfileView.as_view(), name="self"),
    path(r'self/', include(self_urlpatterns)),
]
