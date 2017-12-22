from django.views.generic.list import ListView

from books.models import Books
from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired


class UserBooksListView(PermissionCheckerMixin, ListView):
    model = Books
    permission_classes = [LoginRequired]
    template_name = 'members/user_books.html'
    context_object_name = 'books'

    def dispatch(self, request, *args, **kwargs):
        self.request.admin_area = 'my_books'
        return super(UserBooksListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.books.all()
