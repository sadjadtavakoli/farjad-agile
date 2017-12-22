from django.urls.base import reverse
from django.views.generic.edit import CreateView

from books.models import Books
from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired


class AddBookView(PermissionCheckerMixin, CreateView):
    permission_classes = [LoginRequired]
    template_name = "books/create_book.html"
    model = Books
    fields = "__all__"

    def get_success_url(self):
        return reverse("home")

    def form_valid(self, form):
        res = super(AddBookView, self).form_valid(form)
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return res
