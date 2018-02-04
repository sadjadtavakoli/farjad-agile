from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls.base import reverse
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.mixins import UpdateModelMixin

from books.forms import AddBookForm, UpdateBookForm
from books.models import Books
from books.serializsers import BookSerializer
from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired
from members.models import Member
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


def query_on_title(query):
    queryset = Books.objects.all()
    return queryset.filter(title__icontains=query)


def query_on_genre(query):
    queryset = Books.objects.all()
    return queryset.filter(genre__icontains=query)


def query_on_author(query):
    queryset = Books.objects.all()
    return queryset.filter(author__icontains=query)


class BooksListView(ListView):
    model = Books
    context_object_name = 'books'
    template_name = 'books/all_books.html'

    def get_queryset(self):
        field = self.request.GET.get('field', '')
        query = self.request.GET.get('query', '')
        function = self.action_map.get(field, None)
        if function is not None:
            return function(query)
        return Books.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['field'] = self.request.GET.get('field', '')
        context['query'] = self.request.GET.get('query', '')
        context['books'] = [{'book_info': book, 'loan_state': book.loan_state(self.request.user)}
                            for book in
                            self.get_queryset()]
        return context

    action_map = {
        'title': query_on_title,
        'author': query_on_author,
        'genre': query_on_genre,

    }


class BooksListAPIView(ListAPIView):
    model = Books
    serializer_class = BookSerializer
    queryset = Books.objects.all()


class CreateBookAPIView(CreateAPIView):
    serializer_class = BookSerializer

    def post(self, request, *args, **kwargs):
        data = self.request.data
        token = data.get('token', None)
        try:
            Token.objects.get(key=token)
        except Token.DoesNotExist:
            raise ValidationError(detail='token is not valid')
        else:
            request.data['owner'] = Member.objects.get(username=Token.objects.get(key=token).user.username)
        return super(CreateBookAPIView, self).post(request, *args, **kwargs)
    # def create(self, request, *args, **kwargs):
    #     data = self.request.data
    #     token = data.get('token', None)
    #     try:
    #         Token.objects.get(key=token)
    #     except Token.DoesNotExist:
    #         raise ValidationError(detail='token is not valid')
    #     else:
    #         request.data['owner'] = Member.objects.get(username=Token.objects.get(key=token).user.username)
    #         return super(CreateBookAPIView, self).create(request, *args, **kwargs)
