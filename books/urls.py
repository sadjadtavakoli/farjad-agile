from django.urls.conf import path, include

from books.views import BookDetailView, BookUpdateView, BooksListView, BooksListAPIView

app_name = "book"

api_urlpatterns = ([
                       path(r'', BooksListAPIView.as_view(), name="all"),

                   ], 'api')

urlpatterns = [
    path('', BooksListView.as_view(), name='all'),
    path(r'api/', include(api_urlpatterns)),
    path('<int:book_pk>/', BookDetailView.as_view(), name='detail'),
    path('<int:book_pk>/edit/', BookUpdateView.as_view(), name='edit'),
]
