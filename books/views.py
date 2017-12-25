from django.urls.base import reverse
from django.views.generic.edit import CreateView

from books.forms import AddBookForm
from books.models import Books
from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired
from members.views.area_setter import PanelAreaSetter


class AddBookView(PanelAreaSetter, PermissionCheckerMixin, CreateView):
    permission_classes = [LoginRequired]
    template_name = "books/create_book.html"
    model = Books
    # fields = "__all__"
    admin_area = "my_books"
    form_class = AddBookForm

    def get_success_url(self):
        return reverse("home")

    def get_initial(self):
        data = super(AddBookView, self).get_initial()
        data['owner'] = self.request.user
        return data

    def form_valid(self, form):
        res = super(AddBookView, self).form_valid(form)
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return res
