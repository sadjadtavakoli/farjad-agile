from django.urls.base import reverse
from django.views.generic.edit import CreateView

from books.models import Books
from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired


class AddBookView(PermissionCheckerMixin, CreateView):
    permission_classes = [LoginRequired]
    template_name = "books/add_book.html"
    model = Books
    fields = "__all__"

    def get_success_url(self):
        return reverse("home")

    def post(self, request, *args, **kwargs):
        book = super(AddBookView, self).post(request, *args, **kwargs)
        book.owner = self.request.user
        book.save()
        return book
