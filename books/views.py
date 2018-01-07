from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView

from books.forms import AddBookForm, UpdateBookForm
from books.models import Books
from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired
from members.views.area_setter import PanelAreaSetter


class AddBookView(PanelAreaSetter, PermissionCheckerMixin, CreateView):
    permission_classes = [LoginRequired]
    template_name = "books/create_book.html"
    model = Books
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
        print(form.cleaned_data)
        instance = form.save(commit=False)
        instance.owner = self.request.user
        instance.save()
        return res


class BookDetailView(PanelAreaSetter, DetailView):
    model = Books
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    admin_area = 'my_books'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('book_pk', None)
        book = get_object_or_404(Books, id=pk)
        return book


class BookUpdateView(PanelAreaSetter, PermissionCheckerMixin, UpdateView):
    model = Books
    permission_classes = [LoginRequired]
    template_name = 'books/edit_book.html'
    admin_area = 'my_books'
    form_class = UpdateBookForm

    def get_object(self, queryset=None):
        pk = self.kwargs.get('book_pk', None)
        book = get_object_or_404(Books, id=pk)
        if book.owner != self.request.user:
            raise PermissionDenied
        return book

    def get_success_url(self):
        return reverse('books:detail', args=[self.get_object().id])
