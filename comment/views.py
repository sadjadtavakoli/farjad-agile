import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Books
from comment.models import Comment
from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired


class AddCommentAPIView(PermissionCheckerMixin, APIView):
    permission_classes = [LoginRequired]

    def post(self, request, *args, **kwargs):
        text = request.data.get('text', '')
        book = Books.objects.get(pk=self.kwargs['book_pk'])
        Comment.objects.create(date=datetime.datetime.now(), writer=self.request.user, text=text,
                               book=book)
        return Response(data={})
