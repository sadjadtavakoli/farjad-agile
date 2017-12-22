from django.views.generic.list import ListView

from books.models import Books
from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired
from members.views.area_setter import PanelAreaSetter


class UserBooksListView(PanelAreaSetter, PermissionCheckerMixin, ListView):
    model = Books
    permission_classes = [LoginRequired]
    template_name = 'members/user_books.html'
    context_object_name = 'books'
    admin_area = 'my_books'

    def get_queryset(self):
        return self.request.user.books.all()
