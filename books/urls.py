from django.urls.conf import path

from books.views import BookDetailView, BookUpdateView, BooksListView
from comment.views import AddCommentView

app_name = "book"

urlpatterns = [
    path('', BooksListView.as_view(), name='all'),
    path('<int:book_pk>/', BookDetailView.as_view(), name='detail'),
    path('<int:book_pk>/edit/', BookUpdateView.as_view(), name='edit'),
    path('<int:book_pk>/comment/', AddCommentView.as_view(), name='comment'),
]
