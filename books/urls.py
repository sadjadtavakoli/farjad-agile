from django.urls.conf import path

from books.views import BookDetailView

app_name = "book"

urlpatterns = [
    path('<int:book_pk>', BookDetailView.as_view(), name='detail'),
]
