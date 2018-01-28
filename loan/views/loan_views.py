import datetime

from django_fsm import TransitionNotAllowed
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from books.models import Books
from farjad.utils.permission_checker import PermissionCheckerMixin, LoginRequired
from loan.models import Loan
from loan.serializers import LoanSerializer


class ChangeLoanStateView(PermissionCheckerMixin, APIView):
    response = {}
    action_map = {}

    def get_buttons(self):
        raise NotImplementedError

    def post(self, request, *args, **kwargs):
        action = self.request.data.get('action')
        try:
            action_method = self.action_map[action]
            action_method(request.order.state)

        except (TransitionNotAllowed, KeyError):
            raise ValidationError("این کار شما مجاز نیست . ")
        return self.get_response()

    def get_response(self):
        buttons = self.get_buttons()
        self.response['buttons'] = buttons
        self.response['state'] = self.request.loan.state.state
        return Response(self.response)


class CreateLoanRequestAPIView(CreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = (LoginRequired,)

    def create(self, request, *args, **kwargs):
        book_id = self.request.data['book']
        book = get_object_or_404(Books, id=book_id)
        Loan.objects.create(book=book, borrower=self.request.user, date=datetime.date.today())
        return Response("object created")
