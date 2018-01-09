from django.urls.conf import include, path

from books.views import AddBookView
from loan.views import LenderLoansRequestList, BorrowerLoansRequestList, BorrowedBooksList, \
    LoanedBooksList, LenderChangeLoanStateView, BorrowerChangeLoanStateView
from members.views.authentication_views import LoginView, LogoutView, JoinView
from members.views.profile_views import ProfileView, EditProfileView, SelfProfileView
from members.views.user_books_views import UserBooksListView

app_name = "members"
self_books_urlpatterns = ([
                              path(r'', UserBooksListView.as_view(), name="all"),
                              path(r'new/', AddBookView.as_view(), name="new"),
                              path(r'borrowed/', BorrowedBooksList.as_view(), name="borrowed"),
                              path(r'loaned/', LoanedBooksList.as_view(), name="loaned"),

                          ], 'books')
self_loans_urlpatterns = ([

                              path(r'lender', LenderLoansRequestList.as_view(), name="as-lender"),
                              path(r'borrower', BorrowerLoansRequestList.as_view(),
                                   name="as-borrower"),
                              path(r'<int:loan_pk>/lender_change_state/',
                                   LenderChangeLoanStateView.as_view(),
                                   name="lender-change-state"),
                              path(r'<int:loan_pk>/borrower_change_state/',
                                   BorrowerChangeLoanStateView.as_view(),
                                   name="borrower-change-state"),

                          ], 'loans')
self_urlpatterns = ([
                        path(r'profile/', SelfProfileView.as_view(), name="profile"),
                        path(r'profile/edit/', EditProfileView.as_view(), name="edit-profile"),
                        path(r'books/', include(self_books_urlpatterns)),
                        path(r'loans/', include(self_loans_urlpatterns)),
                    ], 'self')
urlpatterns = [
    path(r'login/', LoginView.as_view(), name="login"),
    path(r'join/', JoinView.as_view(), name="join"),
    path(r'logout/', LogoutView.as_view(), name="logout"),
    path(r'profile/<int:member_id>/', ProfileView.as_view(), name="profile"),
    path(r'self/', include(self_urlpatterns)),
]


