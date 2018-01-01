from django.urls.conf import path

from books.views import BookDetailView, BookUpdateView

app_name = "book"

urlpatterns = [
    path('<int:book_pk>/', BookDetailView.as_view(), name='detail'),
    path('<int:book_pk>/edit/', BookUpdateView.as_view(), name='edit'),
]
