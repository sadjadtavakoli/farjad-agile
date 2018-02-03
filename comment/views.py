from django.urls.base import reverse
from django.views.generic.edit import CreateView
from rest_framework.generics import CreateAPIView

from books.models import Books
from comment.forms import AddCommentForm
from comment.models import Comment
from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired


class AddCommentView(PermissionCheckerMixin, CreateView):
    permission_classes = [LoginRequired]
    template_name = "books/book_detail.html"
    model = Comment
    form_class = AddCommentForm

    def get_success_url(self):
        return reverse("home")

    def get_initial(self):
        initial = super(AddCommentView, self).get_initial()
        book = Books.objects.get(pk=self.request.kwargs['book_pk'])
        initial['writer'] = self.request.user
        initial['book'] = book
        return initial
